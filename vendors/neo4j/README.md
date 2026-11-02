# Neo4j

| Concept | Neo4j | Retail example |
|---|---|---|
| Property graph DB | **Neo4j** (AuraDB managed or self-hosted); Cypher, converging with ISO GQL | [`02-queries.cypher`](../../examples/retail/property-graph/cypher/02-queries.cypher), [`01-create-retail-graph.cypher`](../../examples/retail/property-graph/cypher/01-create-retail-graph.cypher) |
| RDF / OWL / SHACL | **neosemantics (n10s)**: import/export RDF, import OWL, SHACL validation, simple inference | [`ontology-import.cypher`](ontology-import.cypher) |
| Graph algorithms | Graph Data Science library | — |
| GraphRAG | Neo4j GraphRAG packages, vector indexes | — |

## How the generic concepts map

* The generated `01-create-retail-graph.cypher` builds the property graph
  (`~id` is just a property in Neo4j).
* With **n10s** you can load the *same* OWL ontology and RDF data used by the
  SPARQL examples, run subclass inference
  (`n10s.inference.nodesLabelled`), and validate with the SHACL shapes. That's
  the bridge between the RDF and property-graph halves of this repo.

Not executed in this repo (no Neo4j server here).

Docs: [Cypher manual](https://neo4j.com/docs/cypher-manual/current/) ·
[neosemantics](https://neo4j.com/labs/neosemantics/)
