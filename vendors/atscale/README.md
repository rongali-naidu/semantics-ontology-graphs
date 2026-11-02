# AtScale: universal semantic layer + SML

| Concept | AtScale | Retail example |
|---|---|---|
| Semantic model | AtScale semantic model, defined in **SML** (Semantic Modeling Language, Apache 2.0) | [`sml/`](sml/) |
| Query interfaces | SQL, MDX/DAX (Excel, Power BI live connection), Python, REST; LLM / MCP access | — |
| Performance | autonomous aggregates on the warehouse | — |
| Open format | SML is open; AtScale supports Apache Ossie | [Ossie model](../../examples/retail/semantic-model/ossie/) |

## How the generic concepts map

| Ossie / generic | SML object |
|---|---|
| warehouse connection | `object_type: connection` |
| dataset (table or SQL) | `object_type: dataset` with `columns` |
| dimension + hierarchy | `object_type: dimension` with `hierarchies` / `level_attributes` |
| metric | `object_type: metric` (`calculation_method: sum`, `count distinct`, ...) |
| ratio metric | `object_type: metric_calc` (MDX-style expression) |
| relationship | `relationships` in the model (dataset → dimension level) |
| model / subject area | `object_type: model` |

SML is OLAP-shaped: relationships go from a fact dataset to a dimension
**level**, and hierarchies are first-class. The fact dataset here is a SQL
query that pre-joins `order_lines` with `orders` so it carries `customer_id`.

Not deployed to AtScale in this repo; the YAML parses and follows the
[SML reference](https://github.com/semanticdatalayer/sml/tree/main/sml-reference).
