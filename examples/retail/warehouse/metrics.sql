-- ===========================================================================
-- The canonical metric definitions, in plain SQL.
-- Every semantic model in this repo (Apache Ossie, dbt MetricFlow, AtScale
-- SML, Cube, LookML, Power BI TMDL, Snowflake semantic view, Databricks metric
-- view) encodes THESE definitions. scripts/check_semantic_model.py runs this
-- file on SQLite and compares the answers with the SPARQL results.
--
--   metric               definition                                  total
--   -------------------  ------------------------------------------  -------
--   revenue              SUM(quantity * unit_price)                  1878.43
--   units_sold           SUM(quantity)                               9
--   order_count          COUNT(DISTINCT order_id)                    4
--   average_order_value  revenue / order_count                       469.61
--   buyer_count          COUNT(DISTINCT orders.customer_id)          3
--   discount_amount      SUM(quantity * (list_price - unit_price))   10.00
--   average_rating       AVG(reviews.rating)                         4.25
-- ===========================================================================

-- M1. Headline metrics
SELECT ROUND(SUM(ol.quantity * ol.unit_price), 2)                                  AS revenue,
       SUM(ol.quantity)                                                            AS units_sold,
       COUNT(DISTINCT ol.order_id)                                                 AS order_count,
       ROUND(SUM(ol.quantity * ol.unit_price) / COUNT(DISTINCT ol.order_id), 2)    AS average_order_value,
       COUNT(DISTINCT o.customer_id)                                               AS buyer_count,
       ROUND(SUM(ol.quantity * (p.list_price - ol.unit_price)), 2)                 AS discount_amount
FROM order_lines ol
JOIN orders   o ON o.order_id   = ol.order_id
JOIN products p ON p.product_id = ol.product_id;

-- M2. Revenue by customer  (= SPARQL Q3: Alice 1498.97, Bob 199.98, Carol 179.48)
SELECT c.name AS customer, c.is_premium,
       COUNT(DISTINCT o.order_id)                 AS order_count,
       ROUND(SUM(ol.quantity * ol.unit_price), 2) AS revenue
FROM order_lines ol
JOIN orders    o ON o.order_id    = ol.order_id
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.name, c.is_premium
ORDER BY revenue DESC;

-- M3. Revenue by top-level category (Electronics 1648.96, Books 149.97, Kitchen 79.50)
-- The graph answers this with a recursive path; the warehouse uses the
-- flattened category_level_1 column.
SELECT cat.category_level_1 AS category,
       ROUND(SUM(ol.quantity * ol.unit_price), 2) AS revenue,
       SUM(ol.quantity) AS units_sold
FROM order_lines ol
JOIN products   p   ON p.product_id   = ol.product_id
JOIN categories cat ON cat.category_id = p.category_id
GROUP BY cat.category_level_1
ORDER BY revenue DESC;

-- M4. Revenue by order month and status
SELECT SUBSTR(o.order_date, 1, 7) AS order_month, o.status,
       ROUND(SUM(ol.quantity * ol.unit_price), 2) AS revenue
FROM order_lines ol
JOIN orders o ON o.order_id = ol.order_id
GROUP BY order_month, o.status
ORDER BY order_month, o.status;

-- M5. Average rating per product (reviews are a separate fact at a different grain)
SELECT p.name AS product, COUNT(r.review_id) AS reviews, AVG(r.rating) AS average_rating
FROM products p
LEFT JOIN reviews r ON r.product_id = p.product_id
GROUP BY p.name
ORDER BY average_rating DESC, product;
