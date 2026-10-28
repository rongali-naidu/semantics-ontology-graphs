#!/usr/bin/env python3
"""Run every SPARQL query in ../sparql against an in-memory store (no server).

    pip install rdflib pyshacl owlrl
    python scripts/run_sparql_local.py            # run all queries
    python scripts/run_sparql_local.py --reason   # materialise OWL RL first
    python scripts/run_sparql_local.py --shacl    # also validate with SHACL

Ontology + data are loaded into one graph (like loading both into Neptune).
Q11 (named graphs) is run against the TriG file.
"""
import argparse
from pathlib import Path

from rdflib import Dataset, Graph

ROOT = Path(__file__).resolve().parent.parent


def show(title: str, result) -> None:
    print(f"\n=== {title} " + "=" * max(0, 70 - len(title)))
    if result.type == "ASK":
        print(result.askAnswer)
    elif result.type == "CONSTRUCT":
        for s, p, o in sorted(result.graph):
            print(f"{s.n3()} {p.n3()} {o.n3()} .")
    else:
        names = [str(v) for v in result.vars]
        print(" | ".join(names))
        for row in result:
            print(" | ".join("" if v is None else str(v) for v in row))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reason", action="store_true", help="apply OWL 2 RL inference (owlrl)")
    ap.add_argument("--shacl", action="store_true", help="validate data with SHACL (pyshacl)")
    args = ap.parse_args()

    g = Graph()
    g.parse(ROOT / "ontology/retail-ontology.ttl")
    g.parse(ROOT / "rdf/retail-data.ttl")
    print(f"loaded {len(g)} triples")

    if args.reason:
        import owlrl
        owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
        print(f"after OWL RL reasoning: {len(g)} triples")

    for q in sorted((ROOT / "sparql").glob("*.rq")):
        text = q.read_text()
        if "GRAPH ?g" in text:
            ds = Dataset()
            ds.parse(ROOT / "rdf/retail-data.trig", format="trig")
            show(q.name, ds.query(text))
        else:
            show(q.name, g.query(text))

    # Updates run on a copy so the queries above stay deterministic
    for u in sorted((ROOT / "sparql").glob("*.ru")):
        copy = Graph()
        for t in g:
            copy.add(t)
        before = len(copy)
        copy.update(u.read_text())
        print(f"\n=== {u.name}: {before} -> {len(copy)} triples")

    if args.shacl:
        from pyshacl import validate
        conforms, _, report = validate(
            data_graph=Graph().parse(ROOT / "rdf/retail-data.ttl"),
            shacl_graph=Graph().parse(ROOT / "ontology/retail-shapes.ttl"),
            ont_graph=Graph().parse(ROOT / "ontology/retail-ontology.ttl"),
            inference="rdfs",
        )
        print("\n=== SHACL validation:", "CONFORMS" if conforms else "VIOLATIONS")
        if not conforms:
            print(report)


if __name__ == "__main__":
    main()
