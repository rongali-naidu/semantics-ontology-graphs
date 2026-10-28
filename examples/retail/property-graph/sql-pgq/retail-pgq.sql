-- ===========================================================================
-- Retail graph with SQL/PGQ (ISO/IEC 9075-16:2023, "Property Graph Queries")
-- Keep the data in ordinary relational tables and DEFINE a property-graph
-- view over them; then use MATCH inside SQL via GRAPH_TABLE.
-- Implemented by e.g. Oracle Database 23ai and DuckDB (duckpgq extension);
-- syntax details vary slightly by engine.
-- Standard: https://www.iso.org/standard/79473.html
-- ===========================================================================

CREATE TABLE customer   (id VARCHAR PRIMARY KEY, name VARCHAR, email VARCHAR, premium BOOLEAN, member_since DATE);
CREATE TABLE category   (id VARCHAR PRIMARY KEY, name VARCHAR, parent_id VARCHAR REFERENCES category(id));
CREATE TABLE seller     (id VARCHAR PRIMARY KEY, name VARCHAR);
CREATE TABLE product    (id VARCHAR PRIMARY KEY, name VARCHAR, sku VARCHAR, price DECIMAL(10,2),
                         category_id VARCHAR REFERENCES category(id), seller_id VARCHAR REFERENCES seller(id));
CREATE TABLE orders     (id VARCHAR PRIMARY KEY, customer_id VARCHAR REFERENCES customer(id),
                         order_date DATE, status VARCHAR, payment_method VARCHAR);
CREATE TABLE order_line (id VARCHAR PRIMARY KEY, order_id VARCHAR REFERENCES orders(id),
                         product_id VARCHAR REFERENCES product(id), quantity INT, unit_price DECIMAL(10,2));

INSERT INTO customer VALUES
  ('C1','Alice Johnson','alice@example.com',TRUE ,DATE '2024-03-15'),
  ('C2','Bob Smith'    ,'bob@example.com'  ,FALSE,NULL),
  ('C3','Carol Diaz'   ,'carol@example.com',TRUE ,DATE '2025-11-01');
INSERT INTO category VALUES
  ('CAT-ELECTRONICS','Electronics',NULL), ('CAT-COMPUTERS','Computers','CAT-ELECTRONICS'),
  ('CAT-LAPTOPS','Laptops','CAT-COMPUTERS'), ('CAT-AUDIO','Audio','CAT-ELECTRONICS'),
  ('CAT-BOOKS','Books',NULL), ('CAT-KITCHEN','Kitchen',NULL);
INSERT INTO seller VALUES ('S1','TechHub Inc'), ('S2','PageTurner Books'), ('S3','HomeGoods Co');
INSERT INTO product VALUES
  ('P1','Laptop Pro 14','LAP-PRO-14',1299.00,'CAT-LAPTOPS','S1'),
  ('P2','Wireless Earbuds X','EAR-X',149.99,'CAT-AUDIO','S1'),
  ('P3','USB-C Charger 65W','CHG-65W',29.99,'CAT-ELECTRONICS','S1'),
  ('P4','Knowledge Graphs 101','BK-KG101',49.99,'CAT-BOOKS','S2'),
  ('P5','Chef Knife 8in','KNF-8',79.50,'CAT-KITCHEN','S3'),
  ('P6','Mechanical Keyboard','KBD-MECH',89.00,'CAT-COMPUTERS','S1');
INSERT INTO orders VALUES
  ('O1','C1',DATE '2026-09-01','DELIVERED','CARD'), ('O2','C2',DATE '2026-09-05','SHIPPED','PAYPAL'),
  ('O3','C1',DATE '2026-09-20','DELIVERED','CARD'), ('O4','C3',DATE '2026-10-02','PLACED','GIFT_CARD');
INSERT INTO order_line VALUES
  ('O1-L1','O1','P1',1,1299.00), ('O1-L2','O1','P3',2,29.99),
  ('O2-L1','O2','P4',1,49.99),   ('O2-L2','O2','P2',1,149.99),
  ('O3-L1','O3','P2',1,139.99),
  ('O4-L1','O4','P5',1,79.50),   ('O4-L2','O4','P4',2,49.99);

-- The property graph is a mapping over the tables (no data is copied)
CREATE PROPERTY GRAPH retail
  VERTEX TABLES (
    customer LABEL Customer,
    orders   LABEL "Order",
    product  LABEL Product,
    category LABEL Category
  )
  EDGE TABLES (
    orders AS placed
      SOURCE KEY (customer_id) REFERENCES customer (id)
      DESTINATION KEY (id)     REFERENCES orders (id)
      LABEL PLACED,
    order_line AS contains
      SOURCE KEY (order_id)        REFERENCES orders (id)
      DESTINATION KEY (product_id) REFERENCES product (id)
      LABEL CONTAINS PROPERTIES (quantity, unit_price),
    product AS in_category
      SOURCE KEY (id)               REFERENCES product (id)
      DESTINATION KEY (category_id) REFERENCES category (id)
      LABEL IN_CATEGORY,
    category AS subcategory_of
      SOURCE KEY (id)             REFERENCES category (id)
      DESTINATION KEY (parent_id) REFERENCES category (id)
      LABEL SUBCATEGORY_OF
  );

-- Q3. Spend per customer: MATCH in the FROM clause, plain SQL around it
SELECT customer, COUNT(DISTINCT order_id) AS orders, SUM(qty * price) AS total_spent
FROM GRAPH_TABLE (retail
  MATCH (c IS Customer)-[IS PLACED]->(o IS "Order")-[l IS CONTAINS]->(p IS Product)
  COLUMNS (c.name AS customer, o.id AS order_id, l.quantity AS qty, l.unit_price AS price)
)
GROUP BY customer
ORDER BY total_spent DESC;

-- Q5. Also bought
SELECT other, COUNT(DISTINCT buyer) AS buyers
FROM GRAPH_TABLE (retail
  MATCH (t IS Product)<-[IS CONTAINS]-(IS "Order")<-[IS PLACED]-(c IS Customer)
        -[IS PLACED]->(IS "Order")-[IS CONTAINS]->(x IS Product)
  WHERE t.name = 'Wireless Earbuds X' AND x.id <> t.id
  COLUMNS (c.id AS buyer, x.name AS other)
)
GROUP BY other
ORDER BY buyers DESC, other;

-- Q2 in plain SQL needs a recursive CTE - compare with the one-line graph path
WITH RECURSIVE tree(id) AS (
  SELECT id FROM category WHERE name = 'Electronics'
  UNION ALL
  SELECT c.id FROM category c JOIN tree t ON c.parent_id = t.id
)
SELECT p.name FROM product p JOIN tree t ON p.category_id = t.id ORDER BY p.name;
