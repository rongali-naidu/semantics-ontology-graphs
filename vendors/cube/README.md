# Cube: headless semantic layer

> **Verification:** 🟡 syntax-checked: YAML parses and follows the Cube data-model reference; not run in Cube.
> Last reviewed 2026-11-02. Legend: [vendors/README.md](../README.md#verification-levels).

| Concept | Cube | Retail example |
|---|---|---|
| Semantic model | **cubes** (dimensions, measures, joins, hierarchies) + **views** (curated, consumer-facing) | [`model/`](model/) |
| Query interfaces | SQL API (Postgres wire protocol), REST, GraphQL, MDX (Excel), AI API / MCP | — |
| Performance | pre-aggregations, caching | — |
| Open format | Cube ↔ Apache Ossie converter | [Ossie model](../../examples/retail/semantic-model/ossie/) |

## How the generic concepts map

| Ossie / generic | Cube |
|---|---|
| dataset | cube (`sql_table` or `sql`) |
| relationship | `joins` with `relationship: many_to_one` |
| field | `dimensions` (`string`, `number`, `time`, `boolean`) |
| metric | `measures` (`sum`, `count_distinct`, `avg`, `number` for calculated) |
| hierarchy | `hierarchies` with `levels` |
| curated subject area | `views` with `join_path` + `includes` |

Run locally with `npx cubejs-cli create` (or the Cube Docker image), copy
`model/` into the project, and point it at a database loaded with
[`warehouse/`](../../examples/retail/warehouse/). Not executed in this repo;
the YAML parses and follows the Cube data-model reference.

Docs: [Data modeling](https://cube.dev/docs/product/data-modeling/overview)
