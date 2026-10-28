#!/usr/bin/env python3
"""Generate every RDF serialization from the Turtle source of truth.

    pip install rdflib
    python scripts/build_rdf_formats.py

Reads   rdf/retail-data.ttl          (ABox, hand-written)
Writes  rdf/retail-data.nt           N-Triples   (Neptune bulk loader: ntriples)
        rdf/retail-data.rdf          RDF/XML     (Neptune bulk loader: rdfxml)
        rdf/retail-data.jsonld       JSON-LD     (NOT a Neptune bulk-load format)
        rdf/retail-data.trig         TriG        (Turtle + named graphs)
        rdf/retail-data.nq           N-Quads     (Neptune bulk loader: nquads)
        ontology/retail-ontology.nt  ontology as N-Triples
        neptune/rdf/*                copies ready to upload to S3

Named graphs: each subject is put into a graph based on its rdf:type, so the
quad formats show a realistic split (catalog / customers / orders / reviews).
"""
from pathlib import Path
import shutil

from rdflib import Dataset, Graph, Namespace, URIRef
from rdflib.namespace import RDF

ROOT = Path(__file__).resolve().parent.parent
RETAIL = Namespace("https://example.org/retail/ontology#")
EX = Namespace("https://example.org/retail/data/")
GRAPH = Namespace("https://example.org/retail/graph/")

GRAPH_BY_TYPE = {
    RETAIL.Category: GRAPH.catalog,
    RETAIL.Seller: GRAPH.catalog,
    RETAIL.Product: GRAPH.catalog,
    RETAIL.Customer: GRAPH.customers,
    RETAIL.PremiumCustomer: GRAPH.customers,
    RETAIL.Address: GRAPH.customers,
    RETAIL.Order: GRAPH.orders,
    RETAIL.OrderLine: GRAPH.orders,
    RETAIL.Review: GRAPH.reviews,
}

JSONLD_CONTEXT = {
    "@vocab": str(RETAIL),
    "ex": str(EX),
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "placedBy": {"@type": "@id"},
    "hasLine": {"@type": "@id"},
    "forProduct": {"@type": "@id"},
    "inCategory": {"@type": "@id"},
    "subCategoryOf": {"@type": "@id"},
    "soldBy": {"@type": "@id"},
    "shipsTo": {"@type": "@id"},
    "hasAddress": {"@type": "@id"},
    "reviewOf": {"@type": "@id"},
    "writtenBy": {"@type": "@id"},
    "price": {"@type": "xsd:decimal"},
    "unitPrice": {"@type": "xsd:decimal"},
    "quantity": {"@type": "xsd:positiveInteger"},
    "orderDate": {"@type": "xsd:date"},
    "memberSince": {"@type": "xsd:date"},
}


def main() -> None:
    data = Graph().parse(ROOT / "rdf/retail-data.ttl", format="turtle")
    for prefix, ns in (("retail", RETAIL), ("ex", EX)):
        data.bind(prefix, ns)

    out = ROOT / "rdf"
    data.serialize(out / "retail-data.nt", format="nt", encoding="utf-8")
    data.serialize(out / "retail-data.rdf", format="pretty-xml", encoding="utf-8")
    data.serialize(out / "retail-data.jsonld", format="json-ld",
                   context=JSONLD_CONTEXT, indent=2, encoding="utf-8")

    ds = Dataset()
    ds.bind("retail", RETAIL)
    ds.bind("ex", EX)
    ds.bind("g", GRAPH)
    for s in set(data.subjects()):
        graph_iri = next((GRAPH_BY_TYPE[t] for t in data.objects(s, RDF.type)
                          if t in GRAPH_BY_TYPE), GRAPH.misc)
        g = ds.graph(URIRef(graph_iri))
        for p, o in data.predicate_objects(s):
            g.add((s, p, o))
    ds.serialize(out / "retail-data.trig", format="trig", encoding="utf-8")
    ds.serialize(out / "retail-data.nq", format="nquads", encoding="utf-8")

    onto = Graph().parse(ROOT / "ontology/retail-ontology.ttl", format="turtle")
    onto.serialize(ROOT / "ontology/retail-ontology.nt", format="nt", encoding="utf-8")

    neptune = ROOT / "neptune/rdf"
    neptune.mkdir(parents=True, exist_ok=True)
    for name in ("retail-data.ttl", "retail-data.nt", "retail-data.nq", "retail-data.rdf"):
        shutil.copy(out / name, neptune / name)
    shutil.copy(ROOT / "ontology/retail-ontology.ttl", neptune / "retail-ontology.ttl")

    print(f"data triples: {len(data)}  ontology triples: {len(onto)}  "
          f"named graphs: {len(list(ds.graphs())) - 1}")


if __name__ == "__main__":
    main()
