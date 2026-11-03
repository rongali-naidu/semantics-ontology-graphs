#!/usr/bin/env python3
"""Run the R2RML mapping on the warehouse tables and compare with retail-data.ttl.

    pip install morph-kgc rdflib
    python scripts/check_r2rml.py

1. Loads warehouse/data/*.csv into a temporary SQLite database (schema.sql).
2. Runs mapping/retail-r2rml.ttl with Morph-KGC (an open-source R2RML/RML engine).
3. Checks the generated graph equals rdf/retail-data.ttl. Literals are
   compared by value, because SQLite returns 1299.00 as 1299.0 and RDF
   treats "1299.0"^^xsd:decimal and "1299.00"^^xsd:decimal as the same number.

This closes the loop: RDF → tables (rdf_to_tables.py) → RDF (R2RML) gives
back the original knowledge graph.
"""
import csv
import sqlite3
import sys
import tempfile
from decimal import Decimal
from pathlib import Path

import morph_kgc
from rdflib import Graph, Literal
from rdflib.compare import isomorphic

ROOT = Path(__file__).resolve().parent.parent


def build_sqlite(path: Path) -> None:
    db = sqlite3.connect(path)
    db.executescript((ROOT / "warehouse/schema.sql").read_text())
    for f in sorted((ROOT / "warehouse/data").glob("*.csv")):
        with f.open(encoding="utf-8") as fh:
            rows = list(csv.reader(fh))
        cols = rows[0]
        db.executemany(f"INSERT INTO {f.stem} ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                       [[None if v == "" else v for v in r] for r in rows[1:]])
    db.commit()
    db.close()


def by_value(g: Graph) -> Graph:
    out = Graph()
    for s, p, o in g:
        if isinstance(o, Literal) and o.datatype is not None:
            v = o.toPython()
            if isinstance(v, (Decimal, float)):
                o = Literal(Decimal(str(v)).normalize(), datatype=o.datatype)
            elif isinstance(v, int):
                o = Literal(str(v), datatype=o.datatype)
        out.add((s, p, o))
    return out


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "retail.db"
        build_sqlite(db)
        config = f"""
[CONFIGURATION]
output_format = N-TRIPLES

[RetailWarehouse]
mappings = {ROOT / 'mapping/retail-r2rml.ttl'}
db_url = sqlite:///{db}
"""
        generated = morph_kgc.materialize(config)
    expected = Graph().parse(ROOT / "rdf/retail-data.ttl")
    if isomorphic(by_value(generated), by_value(expected)):
        print(f"ok  R2RML mapping              {len(generated)} triples from the warehouse tables "
              f"= retail-data.ttl ({len(expected)} triples)")
        return 0
    g, e = by_value(generated), by_value(expected)
    print("R2RML output differs from retail-data.ttl")
    for t in sorted(e - g)[:10]:
        print("  missing", t)
    for t in sorted(g - e)[:10]:
        print("  extra  ", t)
    return 1


if __name__ == "__main__":
    sys.exit(main())
