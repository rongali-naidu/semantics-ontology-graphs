# Databricks

| Concept | Databricks product | Retail example |
|---|---|---|
| Semantic model | **Unity Catalog metric views** (YAML 1.1; `MEASURE()` in SQL), part of Unity Catalog business semantics | [`retail_metric_view.sql`](retail_metric_view.sql) |
| Graph processing | **GraphFrames** on Spark (motif finding, PageRank, connected components) | [`retail_graphframes.py`](retail_graphframes.py) |
| Graph database | none native; partner graph DBs (e.g. Neo4j, TigerGraph) via connectors | — |
| Ontology / catalog semantics | Unity Catalog tags, descriptions, metric views; Apache Ossie support | [Ossie model](../../examples/retail/semantic-model/ossie/) |
| AI on semantics | Genie (AI/BI) uses metric views and their synonyms | — |

## How the generic concepts map

* A **metric view** = one Ossie fact dataset plus its joins: `source` is the
  fact (`order_lines`), `joins` (nested for snowflake schemas) are the Ossie
  relationships, `dimensions` are fields, `measures` are metrics.
* Measures can build on measures: `MEASURE(revenue) / MEASURE(order_count)`.
* Graph questions (Q5 "also bought", PageRank) run as Spark jobs with
  GraphFrames over the same Delta tables.

Not executed on Databricks in this repo. The metric-view YAML follows the
v1.1 structure used in the Apache Ossie Databricks converter fixtures; check
the current docs for nested-join support on your runtime.

Docs: [Metric views](https://docs.databricks.com/aws/en/metric-views/) ·
[GraphFrames](https://graphframes.io/)
