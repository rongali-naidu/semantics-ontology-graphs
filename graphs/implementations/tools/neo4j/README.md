# Neo4j: graphs

> **Verification:** ⚪ written to documented syntax; not run on Neo4j.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for graphs | Retail example |
|---|---|---|
| **Neo4j** (self-hosted or AuraDB) | property-graph database; Cypher, converging with ISO GQL | [`01-create-retail-graph.cypher`](../../../../examples/retail/property-graph/cypher/01-create-retail-graph.cypher), [`02-queries.cypher`](../../../../examples/retail/property-graph/cypher/02-queries.cypher) |
| **Graph Data Science** | algorithms (PageRank, community detection, similarity, embeddings) | — |
| **Neo4j GraphRAG** | vector indexes + graph retrieval for LLM apps | — |

Neo4j also appears in [ontologies (neosemantics: OWL import, SHACL, inference)](../../../../ontologies/implementations/tools/neo4j-neosemantics/README.md).

## How the concepts map

The generated `01-create-retail-graph.cypher` builds the 29-node, 41-edge
retail graph in one `CREATE` (`` `~id` `` is just a property in Neo4j, so
``MATCH (n {`~id`: 'O1'})`` works on both Neo4j and Neptune). The queries
file answers Q2–Q9 and the write examples; Neo4j-specific alternatives such as
`shortestPath()` and `EXISTS {}` subqueries are noted inline.

Docs: [Cypher manual](https://neo4j.com/docs/cypher-manual/current/) ·
[Graph Data Science](https://neo4j.com/docs/graph-data-science/current/)
