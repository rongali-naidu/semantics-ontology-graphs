# 1. What is a semantic model (semantic layer)?

A **semantic model** sits between raw tables and the people (or AI agents)
asking questions. It gives business names to data and defines, **once**,
how every metric is calculated and how tables join.

```
   "What was revenue by department last quarter?"        ← business question
                         │
   ┌─────────────────────▼──────────────────────────┐
   │ Semantic model                                  │
   │  metric   revenue = SUM(quantity * unit_price)  │
   │  dimension department = category_level_1        │
   │  join     order_lines → products → categories   │
   └─────────────────────┬──────────────────────────┘
                         │ generates SQL
   ┌─────────────────────▼──────────────────────────┐
   │ Warehouse tables: order_lines, orders, products │
   └─────────────────────────────────────────────────┘
```

Without it, every dashboard, notebook and analyst re-implements "revenue"
slightly differently. That's how two reports end up with two numbers for the
same thing. The semantic model is the **single source of truth for
business logic**, the way an ontology is the single source of truth for
**meaning**.

## 1.1 Building blocks

| Block | Also called | Retail example ([Ossie model](../../examples/retail/semantic-model/ossie/retail.semantic_model.yaml)) |
|---|---|---|
| **Dataset / entity** | table, view, cube, logical table | `order_lines`, `customers`, `products` |
| **Grain** | level of detail | one row per order line |
| **Dimension** | attribute, field, column | `customer_name`, `status`, `category_level_1` |
| **Time dimension** | date dimension | `order_date` (day → month → year) |
| **Hierarchy** | drill path, levels | Department → Level 2 → Level 3 → Product |
| **Measure** | aggregation of a column | `SUM(quantity)` |
| **Metric** | KPI, calculated measure | `revenue`, `average_order_value = revenue / order_count` |
| **Relationship / join** | foreign key, entity link | `order_lines.product_id → products.product_id` (many-to-one) |
| **Filter / segment** | named condition | premium customers only |
| **Synonyms / AI context** | descriptions, instructions | "GMV", "sales" → revenue |
| **Security** | row-level security, perspectives | sellers see only their products |

### Facts and dimensions (the star schema)

Semantic models usually sit on a **dimensional model** (Kimball): narrow,
tall **fact** tables of events (order lines, reviews) surrounded by
**dimension** tables of context (customer, product, date).

```
                 customers ─┐
                            │
     categories ─ products ─┼─ order_lines (fact) ─ orders ─ addresses
                  sellers ──┘                       (header)
                 reviews (second fact, its own grain) ─ products, customers
```

See [`warehouse/schema.sql`](../../examples/retail/warehouse/schema.sql).

## 1.2 The hard problems a semantic model solves

| Problem | What goes wrong | How the semantic model fixes it |
|---|---|---|
| **Inconsistent definitions** | Finance's revenue ≠ Marketing's revenue | One governed `revenue` metric |
| **Fan-out (join explosion)** | Joining orders (1) to lines (many) and summing an order-level column double-counts | Knows each table's grain and primary key; aggregates before joining, or uses symmetric aggregates (Looker) |
| **Chasm trap** | Two facts (order lines, reviews) joined through a shared dimension multiply each other | Treats each fact separately and stitches the results ("multi-fact" queries) |
| **Non-additive metrics** | Summing averages or ratios per group gives wrong totals | `average_order_value` is defined as `SUM/COUNT DISTINCT` and re-computed at every grain |
| **Semi-additive metrics** | Inventory or balances can't be summed over time | `semi_additive` / last-value rules (AtScale, Power BI `LASTDATE`) |
| **Time intelligence** | YoY, MTD, rolling 30 days implemented 20 different ways | Built-in time grains and offsets (MetricFlow `offset_window`, DAX time functions) |
| **Hierarchies** | Drill-down needs fixed levels | Level-based hierarchies (the graph's recursive tree must be flattened, see [`rdf_to_tables.py`](../../examples/retail/scripts/rdf_to_tables.py)) |
| **Security** | Every tool re-implements access rules | Row/column security defined once |
| **AI hallucination** | Text-to-SQL guesses joins and formulas | LLM picks *metrics and dimensions*, the layer writes the SQL |

## 1.3 A short history

| Era | Milestone |
|---|---|
| 1990s | **BusinessObjects "universe"** (patented 1990s), Cognos catalogs/Framework Manager, MicroStrategy schema objects: the first semantic layers, inside BI suites |
| 1990s–2000s | **OLAP cubes** (Essbase, Microsoft SSAS Multidimensional, MDX query language): pre-aggregated dimensional models |
| 2010 | **SSAS Tabular / Power Pivot** and the **DAX** language → today's Power BI semantic models |
| 2012 | **Looker** and **LookML**: semantic model as code, in git, generating SQL on the cloud warehouse |
| 2019–2022 | **"Headless BI" / metrics layer**: Cube (2019), Transform's MetricFlow, dbt Semantic Layer (2022, built on MetricFlow after dbt Labs acquired Transform in 2023), AtScale's open SML |
| 2023–2025 | **Warehouse-native** semantic layers: Snowflake semantic views, Databricks metric views, Microsoft Fabric semantic models, Google Looker modeler as a standalone layer |
| 2025 | **Open Semantic Interchange (OSI)** launched by Snowflake with Salesforce, dbt Labs, BlackRock, RelationalAI and others to stop format lock-in; dbt Labs open-sources MetricFlow |
| 2026 | OSI enters the Apache Incubator as **Apache Ossie**, with an ontology layer and converters for 20+ tools |

Why the renewed interest: **AI agents**. An LLM answering "revenue by
department" is far more accurate when it chooses from governed metrics
instead of writing SQL from scratch, which is why every vendor now ships
synonyms, descriptions and "AI context" in its semantic model.

## 1.4 Semantic model vs ontology — the short version

| | Ontology | Semantic model |
|---|---|---|
| Question it answers | What *is* a customer? How do things relate? | How do I *calculate* revenue by customer? |
| Unit | concept, relationship, axiom | dataset, dimension, metric, join |
| Strength | meaning, integration, inference, identity | aggregation, consistency of numbers, performance |
| World | open (unknown ≠ false) | closed (tables are complete) |
| Standard | W3C RDF / OWL / SHACL | Apache Ossie (emerging); many vendor formats |
| Lives on | graphs (RDF or property graph) | tables (warehouse / lakehouse) |

They're complementary, and converging; Apache Ossie even has both layers
plus a mapping between them. Full comparison in
[chapter 4](04-semantic-models-and-ontologies.md).

Next: [2. Semantic models in reporting tools](02-semantic-models-in-reporting-tools.md)
