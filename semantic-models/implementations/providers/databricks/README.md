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

## Overview

* **Metric views are Unity Catalog objects** defined in YAML: source, joins, dimensions and measures. They get Unity Catalog permissions and lineage like any table or view.
* **How you query them:** from SQL with `MEASURE()`, and from dashboards and Genie, so every consumer uses the same definitions.
* **How you deploy them:** keep the YAML in git and deploy with **Databricks Asset Bundles**.
* **For agents:** Genie spaces answer questions over metric views, and Genie Ontology uses them as its governed core.
* **Portability:** an Apache Ossie converter turns metric views to and from Ossie.

## How the concepts map

* A metric view = one Ossie fact dataset plus its joins: `source` is the
  fact (`order_lines`), `joins` (nested for snowflake schemas) are the Ossie
  relationships, `dimensions` are fields, `measures` are metrics.
* Measures can build on measures: `MEASURE(revenue) / MEASURE(order_count)`.
* Where the model lives: an object in Unity Catalog; keep the YAML in git
  and deploy with Databricks Asset Bundles.

Check the current docs for nested-join support on your runtime.

## Product documentation

* [Metric views](https://docs.databricks.com/aws/en/metric-views/): YAML spec, `MEASURE()`, joins
* [Genie (AI/BI)](https://docs.databricks.com/aws/en/genie/): natural-language questions over metric views
* [Databricks Asset Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/): deploying definitions from git
