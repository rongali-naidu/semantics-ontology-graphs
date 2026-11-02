-- ===========================================================================
-- Retail semantic layer - Snowflake Semantic View
-- CREATE SEMANTIC VIEW defines tables, relationships, facts (row-level),
-- dimensions and metrics inside Snowflake; Cortex Analyst and BI tools query
-- it. Snowflake started the Open Semantic Interchange (now Apache Ossie).
-- Written from the documented syntax; check the current Snowflake docs.
-- ===========================================================================
CREATE OR REPLACE SEMANTIC VIEW analytics.retail.retail_sv

  TABLES (
    order_lines AS analytics.retail.order_lines PRIMARY KEY (order_line_id)
      WITH SYNONYMS = ('line items', 'order items')
      COMMENT = 'One row per product line within an order',
    orders      AS analytics.retail.orders      PRIMARY KEY (order_id),
    customers   AS analytics.retail.customers   PRIMARY KEY (customer_id)
      WITH SYNONYMS = ('buyers', 'shoppers'),
    products    AS analytics.retail.products    PRIMARY KEY (product_id),
    categories  AS analytics.retail.categories  PRIMARY KEY (category_id)
  )

  RELATIONSHIPS (
    order_lines_to_orders   AS order_lines (order_id)    REFERENCES orders,
    order_lines_to_products AS order_lines (product_id)  REFERENCES products,
    orders_to_customers     AS orders (customer_id)      REFERENCES customers,
    products_to_categories  AS products (category_id)    REFERENCES categories
  )

  FACTS (
    order_lines.line_amount     AS quantity * unit_price,
    order_lines.quantity        AS quantity,
    order_lines.discount_amount AS order_lines.quantity * (products.list_price - order_lines.unit_price)
  )

  DIMENSIONS (
    orders.order_date          AS order_date,
    orders.status              AS status,
    customers.customer_name    AS name   WITH SYNONYMS = ('customer', 'buyer name'),
    customers.is_premium       AS is_premium,
    products.product_name      AS name,
    categories.category_level_1 AS category_level_1
      WITH SYNONYMS = ('department', 'top category')
  )

  METRICS (
    order_lines.revenue      AS SUM(order_lines.line_amount)
      WITH SYNONYMS = ('sales', 'GMV') COMMENT = 'Sum of quantity * unit price paid',
    order_lines.units_sold   AS SUM(order_lines.quantity),
    order_lines.order_count  AS COUNT(DISTINCT order_lines.order_id),
    order_lines.discount_amount_total AS SUM(order_lines.discount_amount),
    order_lines.average_order_value   AS order_lines.revenue / order_lines.order_count,
    orders.buyer_count       AS COUNT(DISTINCT orders.customer_id)
  )

  COMMENT = 'Retail orders semantic view (same metrics as warehouse/metrics.sql)';

-- Query: pick dimensions and metrics; Snowflake generates the joins
SELECT * FROM SEMANTIC_VIEW(
  analytics.retail.retail_sv
  DIMENSIONS customers.customer_name
  METRICS order_lines.revenue, order_lines.order_count
)
ORDER BY revenue DESC;
