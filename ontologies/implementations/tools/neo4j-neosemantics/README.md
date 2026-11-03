# Neo4j neosemantics (n10s): ontologies

> **Verification:** ⚪ written to documented syntax; not run on Neo4j.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for ontologies | Retail example |
|---|---|---|
| **neosemantics (n10s)**, a Neo4j Labs plugin | import/export RDF; import OWL/RDFS ontologies as `:Class` nodes and `SCO` (subclass) edges; simple inference; SHACL validation of the property graph | [`ontology-import.cypher`](ontology-import.cypher) |

Neo4j also appears in [graphs (Neo4j database, Cypher)](../../../../graphs/implementations/tools/neo4j/README.md).

## What the script does

1. Configures n10s (`handleVocabUris: 'IGNORE'` so instance labels such as
   `Customer` match the imported class names).
2. Imports the OWL ontology [`retail-ontology.ttl`](../../../../examples/retail/ontology/retail-ontology.ttl).
3. Imports the RDF data [`retail-data.ttl`](../../../../examples/retail/rdf/retail-data.ttl),
   which becomes nodes and edges.
4. Runs **subclass inference**: all `Customer`s, including those labelled only
   `PremiumCustomer` (= SPARQL [`08-all-customers-via-subclass.rq`](../../../../examples/retail/sparql/08-all-customers-via-subclass.rq)).
5. Validates the graph with the SHACL shapes [`retail-shapes.ttl`](../../../../examples/retail/ontology/retail-shapes.ttl).

This is the bridge between the topics: the *same* OWL ontology and RDF data
used for SPARQL end up as a Neo4j property graph, with the ontology still
usable for inference and validation.

Docs: [neosemantics](https://neo4j.com/labs/neosemantics/)
