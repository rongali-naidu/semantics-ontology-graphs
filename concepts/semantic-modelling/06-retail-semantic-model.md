# 6. The retail semantic model, end to end

## 5.1 From graph to tables

[`rdf_to_tables.py`](../../examples/retail/scripts/rdf_to_tables.py)
flattens the RDF data into the warehouse star schema
([`schema.sql`](../../examples/retail/warehouse/schema.sql),
[`data/`](../../examples/retail/warehouse/data/)). Two transformations
matter:

1. **N-ary links become fact rows.** `retail:OrderLine` →
   `order_lines (order_id, product_id, quantity, unit_price)`.
2. **The recursive tree is flattened.** `subCategoryOf*` → fixed columns:

   | category | level 1 | level 2 | level 3 |
   |---|---|---|---|
   | Laptops | Electronics | Computers | Laptops |
   | Computers | Electronics | Computers | |
   | Audio | Electronics | Audio | |
   | Books | Books | | |

## 5.2 The metric catalogue

Defined once in plain SQL in
[`metrics.sql`](../../examples/retail/warehouse/metrics.sql), then in every
semantic format:

| Metric | Definition | Total | Type |
|---|---|---|---|
| `revenue` | `SUM(quantity * unit_price)` | 1878.43 | additive |
| `units_sold` | `SUM(quantity)` | 9 | additive |
| `order_count` | `COUNT(DISTINCT order_id)` | 4 | non-additive (distinct) |
| `average_order_value` | `revenue / order_count` | 469.61 | ratio |
| `buyer_count` | `COUNT(DISTINCT customer_id)` | 3 | non-additive |
| `discount_amount` | `SUM(quantity * (list_price − unit_price))` | 10.00 | additive, cross-table |
| `average_rating` | `AVG(rating)` on reviews | 4.25 | second fact |

Revenue by customer: Alice 1498.97 · Bob 199.98 · Carol 179.48
(= SPARQL Q3). Revenue by department: Electronics 1648.96 · Books 149.97 ·
Kitchen 79.50 (= SPARQL roll-up over `subCategoryOf*`).

## 5.3 One model, every format

| Format | Path | Checked how |
|---|---|---|
| Apache Ossie semantic model + ontology + mapping | [`examples/retail/semantic-model/ossie/`](../../examples/retail/semantic-model/ossie/) | ✅ official JSON schemas; metrics compiled and executed; IRIs resolved in OWL |
| dbt MetricFlow | [`vendors/dbt-labs/retail_dbt/`](../../vendors/dbt-labs/retail_dbt/) | ✅ `dbt build` + `mf validate-configs` + `mf query` on DuckDB give the numbers above |
| Cube | [`vendors/cube/model/`](../../vendors/cube/model/) | YAML parses; written to documented syntax |
| AtScale SML | [`vendors/atscale/sml/`](../../vendors/atscale/sml/) | YAML parses; written to the SML reference |
| Looker LookML | [`vendors/gcp/looker/`](../../vendors/gcp/looker/) | written to documented syntax |
| Power BI TMDL + DAX | [`vendors/microsoft/power-bi/`](../../vendors/microsoft/power-bi/Retail.SemanticModel/definition/) | written to documented syntax |
| Snowflake semantic view | [`vendors/snowflake/`](../../vendors/snowflake/) | written to documented syntax |
| Databricks metric view | [`vendors/databricks/`](../../vendors/databricks/) | written to documented syntax |
| Oracle Analytics (RPD / Semantic Modeler) | [`vendors/oracle/`](../../vendors/oracle/) | layer-by-layer design, no model file yet |

"Written to documented syntax" means not executed against the vendor's
engine here. Please open an issue if one doesn't load.

## 5.4 Run it

```bash
cd examples/retail
pip install rdflib pyyaml jsonschema
python scripts/rdf_to_tables.py                 # graph -> warehouse CSVs
python scripts/check_semantic_model.py          # warehouse + Ossie vs SPARQL
git clone https://github.com/apache/ossie /tmp/ossie
python scripts/check_semantic_model.py --ossie-repo /tmp/ossie   # + official schemas

cd ../../vendors/dbt-labs/retail_dbt
pip install dbt-duckdb "dbt-metricflow[duckdb]"
export DBT_PROFILES_DIR=.
dbt build
mf query --metrics revenue,order_count --group-by customer__customer_name
mf query --metrics revenue --group-by product__category_level_1
```

## 5.5 Exercises

1. Add a `gross_margin` metric (needs a `cost` column) to the Ossie model and
   two vendor formats.
2. Add a review date and bring `average_rating` into the dbt model.
3. Add a row-level security rule: sellers only see their own products (SML
   `row_security`, Power BI roles, Cube `access_policy`).
4. Write an Ossie ontology `derived_by` rule for "repeat customer" (2+ orders)
   and the equivalent dbt metric filter.
5. Round-trip the Ossie model through an
   [ossie-converter](https://github.com/apache/ossie-converters) and diff the
   output with the hand-written vendor file.

Next: the vendor folders, see [`vendors/README.md`](../../vendors/README.md).
