# Graphs: implementations

Graph databases and graph engines, each loading or querying the retail graph
(29 nodes / 41 edges, or 165 RDF triples). Status as of November 2026;
product status is tracked only in these tables.
Verification levels: [legend](../../README.md#verification-levels).

## Providers

| Provider | Product | Model / languages | Verified |
|---|---|---|---|
| [AWS](providers/aws/README.md) | **Amazon Neptune** Database | RDF (SPARQL) + property graph (Gremlin, openCypher) | 🟡 load files |
| [AWS](providers/aws/README.md#101-the-neptune-family) | **Neptune Analytics** | in-memory, openCypher + algorithms + vector search | ⚪ |
| [AWS](providers/aws/README.md#aws-context-ontology-accelerator-coa-the-knowledge-graph-side) | **Context Ontology Accelerator (COA)** | ontology-backed knowledge graph in Neptune + virtual KG (Ontop) over SQL | ⚪ |
| [Google Cloud](providers/gcp/README.md) | **Spanner Graph** · **BigQuery Graph** | property graph over tables, ISO GQL | ⚪ |
| [Microsoft](providers/microsoft/README.md) | **Fabric Graph** · **Cosmos DB for Gremlin** · SQL graph tables | GQL · Gremlin · T-SQL `MATCH` | ⚪ |
| [Oracle](providers/oracle/README.md) | **Property graphs** (SQL/PGQ, PGQL) · Graph Server (PGX) | property graph over tables | ⚪ |
| [Databricks](providers/databricks/README.md) | **GraphFrames** | Spark motifs + algorithms | ⚪ |

## Tools

| Tool | Model / languages | Verified |
|---|---|---|
| [Neo4j](tools/neo4j/README.md) | property graph, Cypher (→ GQL), Graph Data Science | ⚪ |
| Cypher / Gremlin / GQL / SQL-PGQ scripts | [`examples/retail/property-graph/`](../../examples/retail/property-graph/) | ⚪ (CI planned) |

Planned (see [ROADMAP](../../ROADMAP.md)): Apache TinkerPop Gremlin Server,
Apache Jena Fuseki, Oxigraph, DuckDB + duckpgq, TigerGraph, Memgraph.
