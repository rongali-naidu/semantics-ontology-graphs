# Databricks: semantic models

> **Verification:** ⚪ written to documented syntax (metric-view structure follows the Apache Ossie converter fixtures); not run on Databricks.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for semantic models | Retail example |
|---|---|---|
| **Unity Catalog metric views** | YAML-defined source, joins, dimensions and measures; queried with `MEASURE()` in SQL | [`retail_metric_view.sql`](retail_metric_view.sql) |
| Genie (AI/BI) | natural-language questions using metric views and their synonyms | — |
| Genie Ontology | learned context layer that uses metric views as its governed core | see [ontologies](../../../../ontologies/implementations/providers/databricks/README.md) |
| Apache Ossie | Databricks ↔ Ossie converter | [Ossie model](../../../../examples/retail/semantic-model/ossie/) |

Databricks also appears in [graphs (GraphFrames)](../../../../graphs/implementations/providers/databricks/README.md).

## How the concepts map

* A metric view = one Ossie fact dataset plus its joins: `source` is the
  fact (`order_lines`), `joins` (nested for snowflake schemas) are the Ossie
  relationships, `dimensions` are fields, `measures` are metrics.
* Measures can build on measures: `MEASURE(revenue) / MEASURE(order_count)`.
* Where the model lives: an object in Unity Catalog; keep the YAML in git
  and deploy with Databricks Asset Bundles.

Check the current docs for nested-join support on your runtime.

Docs: [Metric views](https://docs.databricks.com/aws/en/metric-views/)
