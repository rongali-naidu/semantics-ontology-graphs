-- ===========================================================================
-- Retail property graph on Google Cloud Spanner Graph (ISO GQL)
-- https://cloud.google.com/spanner/docs/graph/overview
-- Spanner Graph maps a property graph onto ordinary Spanner tables, the same
-- idea as SQL/PGQ. Tables = examples/retail/warehouse/schema.sql (Spanner
-- types: STRING(n), INT64, NUMERIC, DATE, BOOL).
-- ===========================================================================

CREATE PROPERTY GRAPH RetailGraph
  NODE TABLES (
    customers  KEY (customer_id) LABEL Customer,
    orders     KEY (order_id)    LABEL `Order`,
    products   KEY (product_id)  LABEL Product,
    categories KEY (category_id) LABEL Category,
    sellers    KEY (seller_id)   LABEL Seller
  )
  EDGE TABLES (
    orders AS Placed
      KEY (order_id)
      SOURCE KEY (customer_id) REFERENCES customers (customer_id)
      DESTINATION KEY (order_id) REFERENCES orders (order_id)
      LABEL PLACED,
    order_lines AS Contains
      KEY (order_line_id)
      SOURCE KEY (order_id) REFERENCES orders (order_id)
      DESTINATION KEY (product_id) REFERENCES products (product_id)
      LABEL CONTAINS PROPERTIES (quantity, unit_price),
    products AS InCategory
      KEY (product_id)
      SOURCE KEY (product_id) REFERENCES products (product_id)
      DESTINATION KEY (category_id) REFERENCES categories (category_id)
      LABEL IN_CATEGORY,
    categories AS SubcategoryOf
      KEY (category_id)
      SOURCE KEY (category_id) REFERENCES categories (category_id)
      DESTINATION KEY (parent_category_id) REFERENCES categories (category_id)
      LABEL SUBCATEGORY_OF
  );

-- Q2. Products under Electronics, any depth (quantified path {0,3})
GRAPH RetailGraph
MATCH (root:Category {name: 'Electronics'})<-[:SUBCATEGORY_OF]-{0,3}(c:Category)<-[:IN_CATEGORY]-(p:Product)
RETURN p.name AS product, c.name AS category
ORDER BY product;

-- Q5. Customers who bought "Wireless Earbuds X" also bought ...
GRAPH RetailGraph
MATCH (t:Product {name: 'Wireless Earbuds X'})<-[:CONTAINS]-(:`Order`)<-[:PLACED]-(c:Customer)
      -[:PLACED]->(:`Order`)-[:CONTAINS]->(other:Product)
WHERE other.product_id <> t.product_id
RETURN other.name AS product, COUNT(DISTINCT c.customer_id) AS buyers
GROUP BY product
ORDER BY buyers DESC, product;
