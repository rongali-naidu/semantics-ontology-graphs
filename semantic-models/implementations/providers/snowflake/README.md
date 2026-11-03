# Snowflake: semantic models

> **Verification:** ⚪ written to documented syntax; not run on Snowflake.
> Last reviewed 2026-11-02. Legend: [verification levels](../../../../README.md#verification-levels).

| Concept | Snowflake product | Retail example |
|---|---|---|
| Semantic model | **Semantic views** (`CREATE SEMANTIC VIEW`; query with `SEMANTIC_VIEW(...)` or standard SQL) | [`retail_semantic_view.sql`](retail_semantic_view.sql) |
| AI on semantics | **Cortex Analyst** and Cortex Agents (natural language → SQL using semantic views) | — |
| Model generation | **Semantic View Autopilot**: generates semantic views from existing schemas and query history | — |
| Knowledge graph sync | **RelationalAI** syncs both ways with semantic views (concepts and measures) | see [ontologies](../../../../ontologies/implementations/providers/snowflake/README.md) |
| Open format | Initiated the **Open Semantic Interchange**, now **Apache Ossie**; converters Ossie ↔ Cortex Analyst YAML | [Ossie model](../../../../examples/retail/semantic-model/ossie/) |
| Graph | none native (partners, e.g. RelationalAI knowledge graphs in Snowflake) | — |

## Overview

* **Semantic views are schema-level objects** created with `CREATE SEMANTIC VIEW`, stored in Snowflake and governed by its role-based access control.
* **How you query them:** with the `SEMANTIC_VIEW(...)` clause or standard SQL.
* **Who uses them:** **Cortex Analyst** and **Cortex Agents** generate SQL from them, with synonyms helping match the user's words.
* **How you build them:** by hand, or with **Semantic View Autopilot**, which generates them from existing schemas and query history. The older Cortex Analyst YAML format is what the Ossie converter emits.

## How the generic concepts map

| Ossie | Snowflake semantic view |
|---|---|
| dataset | `TABLES (... PRIMARY KEY ...)` |
| relationship | `RELATIONSHIPS (x AS a (col) REFERENCES b)` |
| field (row-level, numeric) | `FACTS` |
| field (grouping) | `DIMENSIONS` |
| metric | `METRICS` (can reference other metrics) |
| `ai_context.synonyms` | `WITH SYNONYMS = (...)` |

Not executed on Snowflake in this repo; written from the documented DDL
syntax. The equivalent YAML (Cortex Analyst format) is what the Ossie
Snowflake converter emits.

## Product documentation

* [Semantic views overview](https://docs.snowflake.com/en/user-guide/views-semantic/overview): concepts
* [CREATE SEMANTIC VIEW](https://docs.snowflake.com/en/sql-reference/sql/create-semantic-view): DDL syntax
* [Cortex Analyst](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst): natural language → SQL
* [Cortex Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents): agents over semantic views
