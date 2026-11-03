#!/usr/bin/env python3
"""Prove the RDF files and the property-graph CSVs describe the same data.

    pip install rdflib
    python scripts/check_consistency.py

1. Every RDF serialization (ttl, nt, rdf, jsonld, trig, nq) parses to a graph
   isomorphic to retail-data.ttl.
2. The Neptune openCypher CSV and Gremlin CSV files, loaded into plain Python
   dicts, give the same answers as the SPARQL queries for Q2, Q3, Q5 and Q7.
"""
import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from rdflib import Dataset, Graph
from rdflib.compare import isomorphic

ROOT = Path(__file__).resolve().parent.parent
AWS = ROOT.parent.parent / "graphs/implementations/providers/aws"      # Neptune-specific load files


def check_rdf_formats() -> None:
    base = Graph().parse(ROOT / "rdf/retail-data.ttl")
    for name, fmt in [("retail-data.nt", "nt"), ("retail-data.rdf", "xml"),
                      ("retail-data.jsonld", "json-ld")]:
        g = Graph().parse(ROOT / "rdf" / name, format=fmt)
        assert isomorphic(base, g), name
        print(f"ok  {name:22} {len(g)} triples, isomorphic to retail-data.ttl")
    for name, fmt in [("retail-data.trig", "trig"), ("retail-data.nq", "nquads")]:
        ds = Dataset()
        ds.parse(ROOT / "rdf" / name, format=fmt)
        merged = Graph()
        for s, p, o, _ in ds.quads():
            merged.add((s, p, o))
        assert isomorphic(base, merged), name
        print(f"ok  {name:22} {len(merged)} triples in named graphs, isomorphic")


def load_pg(folder: Path, id_col: str, label_col: str, type_col: str, from_col: str, to_col: str):
    nodes, edges = {}, []
    for f in sorted(Path(folder).glob("*.csv")):
        with f.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        for r in rows:
            props = {k.split(":")[0]: v for k, v in r.items()
                     if not k.startswith(("~", ":")) and v != ""}
            if from_col in r:
                edges.append((r[from_col], r[to_col], r[type_col], props))
            else:
                nodes[r[id_col]] = (r[label_col], props)
    return nodes, edges


def pg_answers(nodes, edges):
    out_ = defaultdict(list)
    in_ = defaultdict(list)
    for a, b, label, props in edges:
        out_[(a, label)].append((b, props))
        in_[(b, label)].append((a, props))
    name = lambda n: nodes[n][1].get("name")

    # Q2 products under Electronics at any depth
    root = next(n for n, (l, p) in nodes.items() if l == "Category" and p["name"] == "Electronics")
    cats, frontier = {root}, [root]
    while frontier:
        c = frontier.pop()
        for child, _ in in_[(c, "SUBCATEGORY_OF")]:
            cats.add(child)
            frontier.append(child)
    q2 = sorted({name(p) for c in cats for p, _ in in_[(c, "IN_CATEGORY")]})

    # Q3 spend per customer
    q3 = {}
    for c, (label, props) in nodes.items():
        if label == "Customer":
            q3[props["name"]] = sum(Decimal(l["quantity"]) * Decimal(l["unitPrice"])
                                    for o, _ in out_[(c, "PLACED")]
                                    for _, l in out_[(o, "CONTAINS")])

    # Q5 also bought
    target = next(n for n, (l, p) in nodes.items() if p.get("name") == "Wireless Earbuds X")
    buyers = {c for o, _ in in_[(target, "CONTAINS")] for c, _ in in_[(o, "PLACED")]}
    q5 = defaultdict(set)
    for c in buyers:
        for o, _ in out_[(c, "PLACED")]:
            for p, _ in out_[(o, "CONTAINS")]:
                if p != target:
                    q5[name(p)].add(c)
    q5 = {k: len(v) for k, v in q5.items()}

    # Q7 never ordered
    q7 = sorted(name(p) for p, (l, _) in nodes.items() if l == "Product" and not in_[(p, "CONTAINS")])
    return q2, q3, q5, q7


def sparql_answers():
    g = Graph()
    g.parse(ROOT / "rdf/retail-data.ttl")
    q = lambda f: list(g.query((ROOT / "sparql" / f).read_text()))
    q2 = sorted(str(r.productName) for r in q("02-electronics-products-incl-subcategories.rq"))
    q3 = {str(r.customerName): r.totalSpent.toPython() for r in q("03-order-totals-per-customer.rq")}
    q5 = {str(r.otherName): int(r.buyers) for r in q("05-customers-who-bought-also-bought.rq")}
    q7 = sorted(str(r.productName) for r in q("07-products-never-ordered.rq"))
    return q2, q3, q5, q7


def main() -> None:
    check_rdf_formats()
    expected = sparql_answers()
    for folder, cols in [(AWS / "opencypher-csv", (":ID", ":LABEL", ":TYPE", ":START_ID", ":END_ID")),
                         (AWS / "gremlin-csv", ("~id", "~label", "~label", "~from", "~to"))]:
        got = pg_answers(*load_pg(folder, *cols))
        for qname, e, a in zip(("Q2", "Q3", "Q5", "Q7"), expected, got):
            assert e == a, f"{folder} {qname}: SPARQL={e} PG={a}"
        print(f"ok  {Path(folder).name:22} Q2/Q3/Q5/Q7 match SPARQL results")
    print("all consistent")


if __name__ == "__main__":
    main()
