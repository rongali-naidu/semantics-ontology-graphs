// ===========================================================================
// Retail graph - openCypher queries
// The SAME questions as ../../sparql/*.rq, asked of the property-graph model:
//
//   (Customer)-[:PLACED]->(Order)-[:CONTAINS {quantity, unitPrice}]->(Product)
//   (Product)-[:IN_CATEGORY]->(Category)-[:SUBCATEGORY_OF]->(Category)
//   (Product)-[:SOLD_BY]->(Seller)
//   (Customer)-[:WROTE]->(Review)-[:REVIEWS]->(Product)
//   (Customer)-[:HAS_ADDRESS]->(Address)<-[:SHIPS_TO]-(Order)
//
// Written to run on both Neo4j and Amazon Neptune (openCypher). Where the two
// differ, the alternative is shown in a comment.
// Spec / docs: https://opencypher.org  |  https://neo4j.com/docs/cypher-manual/
// ===========================================================================


// Q2. Products under "Electronics" at any depth (variable-length path *0..)
// Expected: Laptop Pro 14, Mechanical Keyboard, USB-C Charger 65W, Wireless Earbuds X
MATCH (root:Category {name: 'Electronics'})<-[:SUBCATEGORY_OF*0..]-(c:Category)<-[:IN_CATEGORY]-(p:Product)
RETURN p.name AS product, c.name AS category
ORDER BY product;


// Q3. Spend per customer. Line attributes live ON THE EDGE (l.quantity),
// no OrderLine node needed.
// Expected: Naidu 1498.97 (2 orders), Bob 199.98, Carol 179.48
MATCH (c:Customer)-[:PLACED]->(o:Order)-[l:CONTAINS]->(:Product)
RETURN c.name AS customer,
       count(DISTINCT o) AS orders,
       sum(l.quantity * l.unitPrice) AS totalSpent
ORDER BY totalSpent DESC;


// Q4. Details of order O1. `~id` matches the element id on Neptune and the
// plain `~id` property created by 01-create-retail-graph.cypher on Neo4j.
// Neptune-only alternative:  MATCH (o:Order) WHERE id(o) = 'O1'
MATCH (c:Customer)-[:PLACED]->(o:Order {`~id`: 'O1'})-[l:CONTAINS]->(p:Product),
      (o)-[:SHIPS_TO]->(a:Address)
RETURN c.name AS customer, o.orderDate AS orderDate, o.status AS status, a.city AS city,
       p.name AS product, l.quantity AS qty, l.unitPrice AS unitPrice,
       l.quantity * l.unitPrice AS lineTotal
ORDER BY product;


// Q5. Customers who bought "Wireless Earbuds X" also bought ...
// Expected: Knowledge Graphs 101, Laptop Pro 14, USB-C Charger 65W (1 buyer each)
MATCH (target:Product {name: 'Wireless Earbuds X'})<-[:CONTAINS]-(:Order)<-[:PLACED]-(c:Customer),
      (c)-[:PLACED]->(:Order)-[:CONTAINS]->(other:Product)
WHERE other <> target
RETURN other.name AS product, count(DISTINCT c) AS buyers
ORDER BY buyers DESC, product;


// Q6. Average rating per product. Note: avg() over no rows is null in Cypher
// (SPARQL AVG over no rows returns 0).
MATCH (p:Product)
OPTIONAL MATCH (p)<-[:REVIEWS]-(r:Review)
RETURN p.name AS product, count(r) AS reviews, avg(r.rating) AS avgRating
ORDER BY avgRating DESC, product;


// Q7. Products never ordered. Expected: Mechanical Keyboard
// Neo4j 5 also allows:  WHERE NOT EXISTS { (p)<-[:CONTAINS]-(:Order) }
MATCH (p:Product)
OPTIONAL MATCH (p)<-[l:CONTAINS]-(:Order)
WITH p, count(l) AS timesOrdered
WHERE timesOrdered = 0
RETURN p.name AS product;


// Q8. How is Naidu connected to Carol through purchases?
// Naidu -PLACED-> O3 -CONTAINS-> Earbuds <- O2 <- Bob -> O2 -> Book <- O4 <- Carol
// Neo4j has shortestPath(); this bounded variable-length form also runs on Neptune.
MATCH path = (a:Customer {name: 'Naidu Rongali'})-[:PLACED|CONTAINS*1..8]-(b:Customer {name: 'Carol Diaz'})
RETURN [n IN nodes(path) | coalesce(n.name, n.status)] AS hops, length(path) AS len
ORDER BY len
LIMIT 1;


// Q9. Category tree with depth
MATCH path = (c:Category)-[:SUBCATEGORY_OF*0..]->(root:Category)
OPTIONAL MATCH (root)-[up:SUBCATEGORY_OF]->()
WITH root, c, path, up
WHERE up IS NULL                       // root = has no parent
RETURN root.name AS root, c.name AS category, length(path) AS depth
ORDER BY root, depth, category;


// W1. Write: Bob orders a Mechanical Keyboard (compare 12-insert-new-order.ru)
MATCH (c:Customer {name: 'Bob Smith'}), (p:Product {sku: 'KBD-MECH'}), (a:Address {city: 'Austin'})
CREATE (o:Order {`~id`: 'O5', orderDate: datetime('2026-10-20T00:00:00Z'),
                 status: 'PLACED', paymentMethod: 'CARD'}),
       (c)-[:PLACED]->(o),
       (o)-[:SHIPS_TO]->(a),
       (o)-[:CONTAINS {quantity: 1, unitPrice: 89.00}]->(p);


// W2. Update: mark shipped orders delivered (compare 13-update-status.ru)
MATCH (o:Order {status: 'SHIPPED'})
SET o.status = 'DELIVERED'
RETURN count(o) AS updated;


// W3. Upsert a seller (idempotent)
MERGE (s:Seller {name: 'Gadget World'})
ON CREATE SET s.createdAt = datetime('2026-10-28T00:00:00Z')
RETURN s;


// Housekeeping: inspect / reset
MATCH (n) RETURN labels(n) AS label, count(*) AS n ORDER BY n DESC;
MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS n ORDER BY n DESC;
// MATCH (n) DETACH DELETE n;    // wipe the graph (careful!)
