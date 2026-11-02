#!/usr/bin/env python3
"""Check the warehouse tables and the Apache Ossie model against the graph answers.

    pip install rdflib pyyaml jsonschema
    python scripts/check_semantic_model.py                          # structural + numeric checks
    python scripts/check_semantic_model.py --ossie-repo ../ossie    # + official JSON-schema validation
        (git clone https://github.com/apache/ossie to get the schemas)

1. Loads warehouse/data/*.csv into SQLite (warehouse/schema.sql) and runs
   warehouse/metrics.sql. Revenue by customer must equal SPARQL Q3; revenue by
   top-level category must equal a SPARQL roll-up over subCategoryOf*.
2. Compiles every Ossie metric to SQL (fields -> expressions, joins from the
   declared relationships), runs it on SQLite, and compares with metrics.sql.
3. Checks Ossie references: relationship fields, mapping expressions, and
   that every ontology `iri` names a term defined in the OWL ontology.
"""
import argparse
import csv
import json
import re
import sqlite3
from collections import deque
from decimal import Decimal
from pathlib import Path

import yaml
from rdflib import Graph, URIRef

ROOT = Path(__file__).resolve().parent.parent
OSSIE = ROOT / "semantic-model/ossie"

EXPECTED_TOTALS = {"revenue": Decimal("1878.43"), "units_sold": 9, "order_count": 4,
                   "average_order_value": Decimal("469.61"), "buyer_count": 3,
                   "discount_amount": Decimal("10.00"), "average_rating": Decimal("4.25"),
                   "review_count": 4}


def load_warehouse() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.executescript((ROOT / "warehouse/schema.sql").read_text())
    for f in sorted((ROOT / "warehouse/data").glob("*.csv")):
        with f.open(encoding="utf-8") as fh:
            rows = list(csv.reader(fh))
        cols = rows[0]
        db.executemany(f"INSERT INTO {f.stem} ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                       [[None if v == "" else v for v in r] for r in rows[1:]])
    return db


def statements(sql_text: str):
    body = "\n".join(l for l in sql_text.splitlines() if not l.strip().startswith("--"))
    return [s.strip() for s in body.split(";") if s.strip()]


def money(x) -> Decimal:
    return Decimal(str(x)).quantize(Decimal("0.01"))


def sparql_truth():
    g = Graph()
    g.parse(ROOT / "rdf/retail-data.ttl")
    q3 = {str(r.customerName): money(r.totalSpent.toPython())
          for r in g.query((ROOT / "sparql/03-order-totals-per-customer.rq").read_text())}
    by_top = g.query("""
        PREFIX retail: <https://example.org/retail/ontology#>
        SELECT ?top (SUM(?q * ?p) AS ?rev) WHERE {
          ?line retail:forProduct/retail:inCategory ?cat ; retail:quantity ?q ; retail:unitPrice ?p .
          ?cat retail:subCategoryOf* ?t . ?t retail:name ?top .
          FILTER NOT EXISTS { ?t retail:subCategoryOf ?any }
        } GROUP BY ?top""")
    return q3, {str(r.top): money(r.rev.toPython()) for r in by_top}


def check_warehouse(db):
    m1, m2, m3, _, _ = statements((ROOT / "warehouse/metrics.sql").read_text())
    names = ["revenue", "units_sold", "order_count", "average_order_value", "buyer_count", "discount_amount"]
    got = dict(zip(names, db.execute(m1).fetchone()))
    for k in names:
        assert Decimal(str(got[k])) == Decimal(str(EXPECTED_TOTALS[k])), (k, got[k])
    q3, by_top = sparql_truth()
    assert {r[0]: money(r[3]) for r in db.execute(m2)} == q3, "M2 != SPARQL Q3"
    assert {r[0]: money(r[1]) for r in db.execute(m3)} == by_top, "M3 != SPARQL roll-up"
    print("ok  warehouse metrics.sql       totals match; M2 == SPARQL Q3; M3 == SPARQL subCategoryOf* roll-up")


# --- a tiny Ossie -> SQL compiler (enough for this model) -------------------
def compile_metric(model, metric, dataset=None) -> str:
    ds = {d["name"]: d for d in model["datasets"]}
    fexpr = lambda d, f: next(x["expression"]["sql"] for x in ds[d]["fields"] if x["name"] == f)
    sql = metric["expression"]["sql"]
    if dataset:   # dataset-scoped: bare field names
        names = {f["name"] for f in ds[dataset]["fields"]}
        sql = re.sub(r"\b([a-z_]+)\b", lambda m: f"({qualify(dataset, fexpr(dataset, m[1]))})"
                     if m[1] in names else m[1], sql)
        used = [dataset]
    else:         # model-scoped: dataset.field
        used = []
        def rep(m):
            used.append(m[1]) if m[1] not in used else None
            return f"({qualify(m[1], fexpr(m[1], m[2]))})"
        sql = re.sub(r"\b([a-z_]+)\.([a-z_]+)\b", rep, sql)
    return f"SELECT {sql} FROM {join_path(model, used)}"


def qualify(dataset, expr):
    return re.sub(r"\b([a-z_]+)\b", lambda m: m[1] if m[1].upper() in SQL_WORDS else f"{dataset}.{m[1]}", expr)


SQL_WORDS = {"SUM", "AVG", "COUNT", "DISTINCT", "MIN", "MAX", "CASE", "WHEN", "THEN", "ELSE", "END", "AND", "OR"}


def join_path(model, used):
    """Join the used datasets along declared relationships (many -> one)."""
    src = lambda d: next(x["source"] for x in model["datasets"] if x["name"] == d).split(".")[-1]
    start = used[0]
    edges = {}
    for r in model["relationships"]:
        edges.setdefault(r["from"], []).append(r)
    # BFS from the most granular dataset that reaches all others
    for root in [start] + [d["name"] for d in model["datasets"]]:
        parent, seen, q = {}, {root}, deque([root])
        while q:
            cur = q.popleft()
            for r in edges.get(cur, []):
                if r["to"] not in seen:
                    seen.add(r["to"]); parent[r["to"]] = r; q.append(r["to"])
        if set(used) <= seen:
            break
    need, joins = set(used) - {root}, []
    while need:
        d = need.pop()
        r = parent[d]
        if r not in joins:
            joins.append(r)
        if r["from"] != root:
            need.add(r["from"])
    out = f"{src(root)} AS {root}"
    for r in sorted(joins, key=lambda r: r["from"] != root):
        cond = " AND ".join(f"{r['from']}.{a} = {r['to']}.{b}"
                            for a, b in zip(r["from_columns"], r["to_columns"]))
        out += f" JOIN {src(r['to'])} AS {r['to']} ON {cond}"
    return out


def check_ossie(db, ossie_repo):
    model = yaml.safe_load((OSSIE / "retail.semantic_model.yaml").read_text())
    onto = yaml.safe_load((OSSIE / "retail.ontology.yaml").read_text())
    mapping = yaml.safe_load((OSSIE / "retail.mapping.yaml").read_text())

    if ossie_repo:
        import jsonschema
        for doc, schema in [(model, "core-spec/ossie-schema.json"), (onto, "ontology/ontology.json"),
                            (mapping, "ontology/mapping.json")]:
            jsonschema.validate(doc, json.loads((Path(ossie_repo) / schema).read_text()))
        print("ok  Ossie JSON schemas          semantic model, ontology and mapping validate")

    fields = {(d["name"], f["name"]) for d in model["datasets"] for f in d.get("fields", [])}
    for r in model["relationships"]:
        for a, b in zip(r["from_columns"], r["to_columns"]):
            assert (r["from"], a) in fields and (r["to"], b) in fields, r["name"]
    for text in re.findall(r"expression: ([a-z_]+\.[a-z_]+)", (OSSIE / "retail.mapping.yaml").read_text()):
        assert tuple(text.split(".")) in fields, f"mapping references unknown field {text}"

    concepts = {c["concept"]: c for c in onto["ontology"]}
    rels = {(c["concept"], r["name"]) for c in onto["ontology"] for r in c.get("relationships", [])}
    def owns(concept, rel):       # relationship declared on the concept or a supertype
        while concept:
            if (concept, rel) in rels:
                return True
            concept = (concepts.get(concept, {}).get("extends") or [None])[0]
        return False
    def walk(cm_concept, lm):
        om = lm["object_mapping"]
        if "relationship" in lm:
            assert owns(cm_concept, lm["relationship"]), (cm_concept, lm["relationship"])
        for c in lm.get("children", []):
            walk(cm_concept, c)
    for cm in mapping["concept_mappings"]:
        assert cm["concept"] in concepts, cm["concept"]
        for lm in cm.get("link_mappings", []):
            walk(cm["concept"], lm)

    owl = Graph().parse(ROOT / "ontology/retail-ontology.ttl")
    prefixes = onto["prefixes"]
    iris = [x["iri"] for c in onto["ontology"] for x in [c] + c.get("relationships", []) if "iri" in x]
    for q in iris:
        p, local = q.split(":", 1)
        assert (URIRef(prefixes[p] + local), None, None) in owl, f"{q} not defined in OWL ontology"
    print(f"ok  Ossie references           relationships, mapping fields, {len(iris)} IRIs resolve in OWL")

    results = {}
    for d in model["datasets"]:
        for m in d.get("metrics", []):
            results[m["name"]] = db.execute(compile_metric(model, m, d["name"])).fetchone()[0]
    for m in model.get("metrics", []):
        results[m["name"]] = db.execute(compile_metric(model, m)).fetchone()[0]
    for k, v in results.items():
        exp = EXPECTED_TOTALS[k]
        ok = money(v) == money(exp) if isinstance(exp, Decimal) else v == exp
        assert ok, f"Ossie metric {k} = {v}, expected {exp}"
    print(f"ok  Ossie metrics -> SQL       {len(results)} metrics compile and equal metrics.sql "
          f"(revenue {money(results['revenue'])}, AOV {money(results['average_order_value'])})")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ossie-repo", help="path to a clone of github.com/apache/ossie for schema validation")
    args = ap.parse_args()
    db = load_warehouse()
    check_warehouse(db)
    check_ossie(db, args.ossie_repo)
    print("semantic model consistent with the knowledge graph")


if __name__ == "__main__":
    main()
