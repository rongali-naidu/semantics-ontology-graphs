# Google Cloud: semantic models

> **Verification:** ⚪ written to documented syntax; not run in Looker.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for semantic models | Retail example |
|---|---|---|
| **Looker** (LookML) | semantic model as code: views, explores, measures; also served to Looker Studio, Sheets and other BI tools through connectors | [`looker/`](looker/) |
| Looker conversational analytics / Gemini | natural-language questions over LookML | — |
| **Knowledge Catalog** | ingests semantic models from **LookML, BigQuery Graph (with measures), dbt MetricFlow, Snowflake semantic views, Databricks metric views and SAP CSN** into one context graph for agents; overlapping definitions kept side by side, labelled by source | the [Looker](looker/) and [dbt](../../tools/dbt/) retail models would both land here |

Google Cloud also appears in [graphs (Spanner Graph, BigQuery Graph)](../../../../graphs/implementations/providers/gcp/README.md).

## Overview

* **Looker** is a semantic model as code. A **LookML project** is a git repository (views, explores, measures). A Looker instance compiles each question into SQL against your warehouse (BigQuery and others), so no data is copied.
* **How you change it:** in development mode on a git branch, then deploy to production.
* **Who uses it:**
  * Looker itself;
  * Looker Studio, Sheets and other BI tools, through connectors;
  * **conversational analytics** with Gemini.
* **Knowledge Catalog** ingests LookML, plus semantic models from other vendors, into one context graph for agents.

## How the concepts map

* LookML **views** = Ossie datasets, **explores** = join graphs,
  **measures** = metrics, `dimension_group` = time dimensions.
* Every join declares `relationship: many_to_one`. Looker uses it for
  **symmetric aggregates**, which stop fan-out double counting
  ([semantic models concepts 1](../../../concepts/01-what-is-a-semantic-model.md#12-the-hard-problems-a-semantic-model-solves)).
* The ontology's category tree becomes drillable `category_level_1/2/3` dimensions.
* Reviews get their own explore: a separate fact at its own grain.
* Where the model lives: a LookML project is a git repository with
  development branches ([semantic models concepts 3](../../../concepts/03-semantic-model-repositories.md#33-google-looker)).

## Files

```
looker/
  retail.model.lkml          explores: order_lines (+ orders, customers, products, categories), reviews
  views/*.view.lkml          one view per table; revenue, units_sold, order_count, average_order_value, discount_amount, buyer_count, average_rating
```

## Product documentation

* [What is LookML?](https://cloud.google.com/looker/docs/what-is-lookml): views, explores, measures
* [Looker documentation](https://cloud.google.com/looker/docs): development mode, git, deployment, conversational analytics
* [Expanded semantic model support in Knowledge Catalog](https://cloud.google.com/blog/products/data-analytics/expanded-semantic-model-support-in-knowledge-catalog): LookML and others in the context graph
