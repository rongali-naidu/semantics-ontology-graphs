# dbt Semantic Layer (MetricFlow): semantic models

> **Verification:** ✅ executed: `dbt build`, `mf validate-configs` and `mf query` on DuckDB, checked in CI against the SPARQL answers.
> Last reviewed 2026-11-02. Legend: [verification levels](../../../../README.md#verification-levels).

| Concept | dbt | Retail example |
|---|---|---|
| Transformation to a star schema | dbt models (SQL) | [`retail_dbt/models/marts/`](retail_dbt/models/marts/) |
| Semantic model | **semantic_models** (entities, dimensions, measures) | [`retail_semantic_models.yml`](retail_dbt/models/semantic/retail_semantic_models.yml) |
| Metrics | **metrics** (simple, ratio, derived, cumulative, conversion) | same file |
| Query engine | **MetricFlow** (`mf` CLI; Semantic Layer APIs: JDBC / GraphQL in dbt Cloud) | — |
| Open format | MetricFlow is open source; dbt ↔ Ossie converter | [Ossie model](../../../../examples/retail/semantic-model/ossie/) |

## ✅ Executed

This one runs end to end on DuckDB, no cloud account needed. From the repo root:

```bash
pip install -r semantic-models/implementations/tools/dbt/requirements.txt
make dbt        # dbt build + mf validate-configs + check_metricflow.py (compares results with the SPARQL answers)
```

Or by hand:

```bash
cd semantic-models/implementations/tools/dbt/retail_dbt
export DBT_PROFILES_DIR=.
dbt build                     # seeds (= warehouse/data) + marts + time spine
mf validate-configs           # semantic model validated against the warehouse
mf query --metrics revenue,units_sold,order_count,average_order_value,buyer_count,discount_amount
#   revenue 1878.43 · units 9 · orders 4 · AOV 469.61 · buyers 3 · discount 10
mf query --metrics revenue,order_count --group-by customer__customer_name --order -revenue
#   Alice Johnson 1498.97 (2) · Bob Smith 199.98 (1) · Carol Diaz 179.48 (1)   = SPARQL Q3
mf query --metrics revenue --group-by product__category_level_1
#   Electronics 1648.96 · Books 149.97 · Kitchen 79.5
mf query --metrics premium_revenue
#   1678.45   (Alice + Carol: the ontology's PremiumCustomer class as a metric filter)
```

Tested with dbt-core 1.12.6, dbt-duckdb 1.11.1, dbt-metricflow 0.15.0 (pinned in [`requirements.txt`](requirements.txt)); CI runs [`check_metricflow.py`](check_metricflow.py) on every push.

## How the generic concepts map

| Ossie / generic | MetricFlow |
|---|---|
| dataset | `semantic_model` (over a dbt model) |
| relationship (join) | **entities**: semantic models join where entity names match (`customer`, `product`) |
| field | `dimensions` (`categorical` / `time`) |
| dataset metric | `measure` + `type: simple` metric |
| model metric (ratio) | `type: ratio` |
| filtered metric / segment | `filter: {{ Dimension('customer__is_premium') }} = true` |

MetricFlow requires every measure to have a time dimension, which is why
reviews (no review date) are left out. That's a real design difference from
Ossie, Cube and LookML.

Docs: [Semantic models](https://docs.getdbt.com/docs/build/semantic-models) ·
[Metrics](https://docs.getdbt.com/docs/build/metrics-overview) ·
[MetricFlow](https://github.com/dbt-labs/metricflow)
