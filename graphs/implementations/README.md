# Graphs: implementations

Graph databases and graph engines, each loading or querying the retail graph
(29 nodes / 41 edges, or 165 RDF triples). **Status** is as of November 2026
(details on each page). Verification levels: [legend](../../README.md#verification-levels).


## Providers

| Provider | Product | Model / languages | Status | Verified |
|---|---|---|---|---|
| [AWS](providers/aws/README.md) | **Amazon Neptune** Database | RDF (SPARQL) + property graph (Gremlin, openCypher) | GA | 🟡 load files |
| [AWS](providers/aws/README.md#101-the-neptune-family) | **Neptune Analytics** | in-memory, openCypher + algorithms + vector search | GA | ⚪ |
| [AWS](providers/aws/README.md#aws-context-ontology-accelerator-coa-the-knowledge-graph-side) | **Context Ontology Accelerator (COA)** | ontology-backed KG in Neptune + virtual KG (Ontop) over SQL | open source | ⚪ |
| [Google Cloud](providers/gcp/README.md) | **Spanner Graph** · **BigQuery Graph** | property graph over tables, ISO GQL | GA · GA (2026) | ⚪ |
| [Microsoft](providers/microsoft/README.md) | **Fabric Graph** · **Cosmos DB for Gremlin** · SQL graph tables | GQL · Gremlin · T-SQL `MATCH` | GA · GA · GA | ⚪ |
| [Oracle](providers/oracle/README.md) | **Property graphs** (SQL/PGQ, PGQL) · Graph Studio · 80+ algorithms | property graph over tables; RDF graphs too | GA (AI Database 26ai) | ⚪ |
| [Snowflake](providers/snowflake/README.md) | **KG_NODE / KG_EDGE** pattern + SPCS graph analytics | graph in two tables | Labs sample | ⚪ |
| [Databricks](providers/databricks/README.md) | **GraphFrames** · **OntoBricks** triple store | Spark motifs + algorithms · RDF/SPARQL | open source · Labs (as-is) | ⚪ |
| [SAP](providers/sap/README.md) | **HANA Cloud knowledge graph engine** · HANA graph engine | RDF + SPARQL · property graph | see SAP docs | ⚪ |

## Tools

| Tool | Model / languages | Verified |
|---|---|---|
| [Neo4j](tools/neo4j/README.md) | property graph, Cypher (→ GQL), Graph Data Science | ⚪ |
| Cypher / Gremlin / GQL / SQL-PGQ scripts | [`examples/retail/property-graph/`](../../examples/retail/property-graph/) | ⚪ (CI planned) |

Planned (see [ROADMAP](../../ROADMAP.md)): Apache TinkerPop Gremlin Server,
Apache Jena Fuseki, Oxigraph, DuckDB + duckpgq, TigerGraph, Memgraph.
