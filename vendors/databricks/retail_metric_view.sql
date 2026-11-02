-- ===========================================================================
-- Retail semantic layer - Databricks Unity Catalog metric view (YAML 1.1)
-- Same metrics as warehouse/metrics.sql. Syntax follows the Databricks
-- metric-view spec as used by the Apache Ossie converter test fixtures.
-- ===========================================================================
CREATE OR REPLACE VIEW main.retail.retail_metrics
WITH METRICS
LANGUAGE YAML
AS $$
version: "1.1"
source: main.retail.order_lines
comment: One row per product line within an order
joins:
  - name: orders
    source: main.retail.orders
    on: source.order_id = orders.order_id
    rely:
      at_most_one_match: true
    joins:
      - name: customers
        source: main.retail.customers
        on: orders.customer_id = customers.customer_id
  - name: products
    source: main.retail.products
    on: source.product_id = products.product_id
    joins:
      - name: categories
        source: main.retail.categories
        on: products.category_id = categories.category_id
dimensions:
  - name: order_date
    expr: orders.order_date
  - name: order_month
    expr: DATE_TRUNC('MONTH', orders.order_date)
  - name: status
    expr: orders.status
  - name: customer_name
    expr: orders.customers.name
    synonyms: [customer, buyer]
  - name: is_premium
    expr: orders.customers.is_premium
  - name: product_name
    expr: products.name
  - name: department
    expr: products.categories.category_level_1
    synonyms: [category, top category]
measures:
  - name: revenue
    expr: SUM(quantity * unit_price)
    comment: Sum of quantity * unit price paid
    synonyms: [sales, GMV]
  - name: units_sold
    expr: SUM(quantity)
  - name: order_count
    expr: COUNT(DISTINCT order_id)
  - name: buyer_count
    expr: COUNT(DISTINCT orders.customer_id)
  - name: discount_amount
    expr: SUM(quantity * (products.list_price - unit_price))
  - name: average_order_value
    expr: MEASURE(revenue) / MEASURE(order_count)
$$;

-- Query: MEASURE() aggregates correctly at whatever grain you GROUP BY
SELECT customer_name,
       MEASURE(revenue)             AS revenue,
       MEASURE(order_count)         AS orders,
       MEASURE(average_order_value) AS aov
FROM main.retail.retail_metrics
GROUP BY customer_name
ORDER BY revenue DESC;
