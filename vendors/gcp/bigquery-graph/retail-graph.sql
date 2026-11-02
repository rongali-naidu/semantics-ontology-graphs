-- ===========================================================================
-- Retail property graph on BigQuery Graph (GQL over BigQuery tables)
-- Same mapping as ../spanner-graph/retail-graph.sql; BigQuery uses
-- dataset-qualified names and NOT ENFORCED keys.
-- ===========================================================================
CREATE OR REPLACE PROPERTY GRAPH retail.RetailGraph
  NODE TABLES (
    retail.customers  KEY (customer_id) LABEL Customer,
    retail.orders     KEY (order_id)    LABEL `Order`,
    retail.products   KEY (product_id)  LABEL Product,
    retail.categories KEY (category_id) LABEL Category
  )
  EDGE TABLES (
    retail.orders AS Placed
      KEY (order_id)
      SOURCE KEY (customer_id) REFERENCES customers (customer_id)
      DESTINATION KEY (order_id) REFERENCES orders (order_id)
      LABEL PLACED,
    retail.order_lines AS Contains
      KEY (order_line_id)
      SOURCE KEY (order_id) REFERENCES orders (order_id)
      DESTINATION KEY (product_id) REFERENCES products (product_id)
      LABEL CONTAINS PROPERTIES (quantity, unit_price),
    retail.products AS InCategory
      KEY (product_id)
      SOURCE KEY (product_id) REFERENCES products (product_id)
      DESTINATION KEY (category_id) REFERENCES categories (category_id)
      LABEL IN_CATEGORY
  );

-- Graph pattern + SQL aggregation in one statement (= SPARQL Q3)
SELECT customer, COUNT(DISTINCT order_id) AS orders, SUM(amount) AS revenue
FROM GRAPH_TABLE (
  retail.RetailGraph
  MATCH (c:Customer)-[:PLACED]->(o:`Order`)-[l:CONTAINS]->(p:Product)
  COLUMNS (c.name AS customer, o.order_id AS order_id, l.quantity * l.unit_price AS amount)
)
GROUP BY customer
ORDER BY revenue DESC;
