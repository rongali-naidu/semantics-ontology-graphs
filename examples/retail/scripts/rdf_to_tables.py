#!/usr/bin/env python3
"""Flatten the RDF retail data into warehouse tables (the input of a semantic layer).

    pip install rdflib
    python scripts/rdf_to_tables.py

Writes warehouse/data/*.csv (and copies them to vendors/dbt-labs/retail_dbt/seeds).
The table definitions are in warehouse/schema.sql.

This is the third shape of the same data:
  RDF triples      -> rdf/retail-data.ttl          (meaning, global ids, inference)
  property graph   -> vendors/aws/*-csv/           (nodes + edges, traversal)
  relational tables-> warehouse/data/*.csv         (rows + keys, aggregation)  <- here

Two things happen on the way to tables:
  * the many-to-many / n-ary links become fact rows (order_lines);
  * the recursive category tree is FLATTENED into fixed columns
    (category_level_1/2/3), because BI tools model hierarchies as levels.
"""
import csv
import shutil
from pathlib import Path

from rdflib import Graph, Namespace
from rdflib.namespace import RDF

ROOT = Path(__file__).resolve().parent.parent
DBT_SEEDS = ROOT.parent.parent / "vendors/dbt-labs/retail_dbt/seeds"   # dbt loads the same CSVs
R = Namespace("https://example.org/retail/ontology#")
EX = "https://example.org/retail/data/"


def local(iri) -> str:
    return str(iri).removeprefix(EX)


def val(g, s, p):
    v = g.value(s, p)
    return "" if v is None else (local(v) if str(v).startswith(EX) else str(v))


def write(name, header, rows):
    out = ROOT / "warehouse/data" / f"{name}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(sorted(rows))


def main() -> None:
    g = Graph().parse(ROOT / "rdf/retail-data.ttl")
    of_type = lambda c: sorted(g.subjects(RDF.type, c))

    write("customers", ["customer_id", "name", "email", "is_premium", "member_since", "address_id"],
          [[local(c), val(g, c, R.name), val(g, c, R.email),
            "true" if (c, RDF.type, R.PremiumCustomer) in g else "false",
            val(g, c, R.memberSince), val(g, c, R.hasAddress)]
           for c in of_type(R.Customer) + of_type(R.PremiumCustomer)])

    write("addresses", ["address_id", "city", "state", "postal_code", "country"],
          [[local(a), val(g, a, R.city), val(g, a, R.state), val(g, a, R.postalCode), val(g, a, R.country)]
           for a in of_type(R.Address)])

    write("sellers", ["seller_id", "name"], [[local(s), val(g, s, R.name)] for s in of_type(R.Seller)])

    # Category tree -> one row per category with its full path as fixed levels
    def path(c):
        p = [c]
        while (parent := g.value(p[0], R.subCategoryOf)) is not None:
            p.insert(0, parent)
        return p
    rows = []
    for c in of_type(R.Category):
        names = [val(g, x, R.name) for x in path(c)] + ["", ""]
        rows.append([local(c), val(g, c, R.name), val(g, c, R.subCategoryOf), *names[:3]])
    write("categories", ["category_id", "name", "parent_category_id",
                         "category_level_1", "category_level_2", "category_level_3"], rows)

    write("products", ["product_id", "sku", "name", "list_price", "category_id", "seller_id"],
          [[local(p), val(g, p, R.sku), val(g, p, R.name), val(g, p, R.price),
            val(g, p, R.inCategory), val(g, p, R.soldBy)] for p in of_type(R.Product)])

    write("orders", ["order_id", "customer_id", "order_date", "status", "payment_method", "ship_address_id"],
          [[local(o), val(g, o, R.placedBy), val(g, o, R.orderDate), val(g, o, R.status),
            val(g, o, R.paymentMethod), val(g, o, R.shipsTo)] for o in of_type(R.Order)])

    write("order_lines", ["order_line_id", "order_id", "product_id", "quantity", "unit_price"],
          [[local(line), local(o), val(g, line, R.forProduct), val(g, line, R.quantity), val(g, line, R.unitPrice)]
           for o, line in g.subject_objects(R.hasLine)])

    write("reviews", ["review_id", "customer_id", "product_id", "rating", "review_text"],
          [[local(r), val(g, r, R.writtenBy), val(g, r, R.reviewOf), val(g, r, R.rating), val(g, r, R.reviewText)]
           for r in of_type(R.Review)])
    DBT_SEEDS.mkdir(parents=True, exist_ok=True)
    for f in (ROOT / "warehouse/data").glob("*.csv"):
        shutil.copy(f, DBT_SEEDS / f.name)
    print("wrote", len(list((ROOT / "warehouse/data").glob("*.csv"))), "tables")


if __name__ == "__main__":
    main()
