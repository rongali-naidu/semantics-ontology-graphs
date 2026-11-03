# Snowflake: semantic models

> **Verification:** ⚪ written to documented syntax; not run on Snowflake.
> Last reviewed 2026-11-02. Legend: [verification levels](../../../../README.md#verification-levels).

| Concept | Snowflake product | Retail example |
|---|---|---|
| Semantic model | **Semantic views** (`CREATE SEMANTIC VIEW`; query with `SEMANTIC_VIEW(...)` or standard SQL) | [`retail_semantic_view.sql`](retail_semantic_view.sql) |
| AI on semantics | **Cortex Analyst** (natural language → SQL using the semantic view / semantic-model YAML) | — |
| Open format | Initiated the **Open Semantic Interchange**, now **Apache Ossie**; converters Ossie ↔ Cortex Analyst YAML | [Ossie model](../../../../examples/retail/semantic-model/ossie/) |
| Graph | none native (partners, e.g. RelationalAI knowledge graphs in Snowflake) | — |

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

Docs: [Semantic views](https://docs.snowflake.com/en/user-guide/views-semantic/overview) ·
[Cortex Analyst](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst)
