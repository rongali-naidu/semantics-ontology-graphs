# Databricks: graphs

> **Verification:** ⚪ written to documented syntax; not run on Databricks.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for graphs | Retail example |
|---|---|---|
| **GraphFrames** on Spark | graph processing over Delta tables: motif finding (pattern matching), PageRank, connected components | [`retail_graphframes.py`](retail_graphframes.py) |
| Graph database | none native; partners (Neo4j, TigerGraph) via connectors | — |

Databricks also appears in [semantic models (metric views)](../../../../semantic-models/implementations/providers/databricks/README.md).

## How the concepts map

Vertices and edges are DataFrames built from the warehouse tables
(`main.retail.*`). Motifs such as `(c)-[]->(o1); (o1)-[]->(t)` express the
"customers who bought X also bought" pattern (Q5), and algorithms run as
Spark jobs. That suits batch analytics, not interactive traversal.

Docs: [GraphFrames](https://graphframes.io/)
