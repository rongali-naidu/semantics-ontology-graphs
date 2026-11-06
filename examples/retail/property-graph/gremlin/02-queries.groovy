// ===========================================================================
// Retail graph - Gremlin (Apache TinkerPop) traversals
// Same questions as ../cypher/02-queries.cypher and ../../sparql/*.rq.
//
// Gremlin is imperative: you describe HOW to walk the graph step by step
// (start at vertices -> follow edges -> filter -> aggregate).
//
// Run: Gremlin Console (:remote connect tinkerpop.server conf/neptune.yaml,
// then :remote console), a Neptune notebook (%%gremlin), or any GLV
// (gremlinpython, Java, JS, .NET, Go). Avoid lambdas: Neptune rejects them.
// Docs: https://tinkerpop.apache.org/docs/current/reference/
// ===========================================================================


// Q2. Products under "Electronics" at any depth.
// emit() before repeat() also emits the root category itself (depth 0).
g.V().has('Category', 'name', 'Electronics').
  emit().repeat(__.in('SUBCATEGORY_OF')).
  in('IN_CATEGORY').dedup().
  order().by('name').
  values('name')
// ==> Laptop Pro 14, Mechanical Keyboard, USB-C Charger 65W, Wireless Earbuds X


// Q3. Spend per customer: math() multiplies the two edge properties.
g.V().hasLabel('Customer').
  project('customer', 'orders', 'totalSpent').
    by('name').
    by(out('PLACED').count()).
    by(out('PLACED').outE('CONTAINS').
       project('q', 'p').by('quantity').by('unitPrice').
       math('q * p').sum()).
  order().by(select('totalSpent'), desc)


// Q4. Order O1: header + lines. g.V('O1') looks up by element id.
g.V('O1').
  project('customer', 'orderDate', 'status', 'city', 'lines').
    by(in('PLACED').values('name')).
    by('orderDate').
    by('status').
    by(out('SHIPS_TO').values('city')).
    by(outE('CONTAINS').
       project('product', 'qty', 'unitPrice').
         by(inV().values('name')).
         by('quantity').
         by('unitPrice').
       fold())


// Q5. Customers who bought "Wireless Earbuds X" also bought ...
g.V().has('Product', 'name', 'Wireless Earbuds X').as('target').
  in('CONTAINS').in('PLACED').dedup().as('c').      // the buyers
  out('PLACED').out('CONTAINS').
  where(neq('target')).as('other').
  select('c', 'other').dedup().                     // count each buyer once
  select('other').
  groupCount().by('name').
  order(local).by(values, desc)
// ==> [Knowledge Graphs 101:1, Laptop Pro 14:1, USB-C Charger 65W:1]


// Q6. Average rating per product; coalesce() covers products with no reviews.
g.V().hasLabel('Product').
  project('product', 'reviews', 'avgRating').
    by('name').
    by(in('REVIEWS').count()).
    by(coalesce(in('REVIEWS').values('rating').mean(), constant('n/a')))


// Q7. Products never ordered (no incoming CONTAINS edge).
g.V().hasLabel('Product').not(inE('CONTAINS')).values('name')
// ==> Mechanical Keyboard


// Q8. Path from Naidu to Carol through purchases (simplePath avoids cycles).
g.V().has('Customer', 'name', 'Naidu Rongali').
  repeat(both('PLACED', 'CONTAINS').simplePath()).
    until(has('Customer', 'name', 'Carol Diaz').or().loops().is(8)).
  has('Customer', 'name', 'Carol Diaz').
  limit(1).
  path().by(coalesce(values('name'), id()))


// Q9. Category tree: each category with its path to the root.
g.V().hasLabel('Category').
  repeat(out('SUBCATEGORY_OF')).emit().
  path().by('name')


// W1. Bob orders a Mechanical Keyboard.
g.addV('Order').property(T.id, 'O5').
    property('orderDate', datetime('2026-10-20T00:00:00Z')).
    property('status', 'PLACED').property('paymentMethod', 'CARD').as('o').
  V('C2').addE('PLACED').to('o').
  V('A2').addE('SHIPS_TO').from('o').
  V('P6').addE('CONTAINS').from('o').
    property(T.id, 'O5-L1').property('quantity', 1).property('unitPrice', 89.00).
  iterate()


// W2. Mark shipped orders delivered. single = replace, not add a 2nd value.
g.V().has('Order', 'status', 'SHIPPED').
  property(single, 'status', 'DELIVERED').
  count()


// W3. Idempotent upsert with mergeV (TinkerPop 3.6+; Neptune 1.2.1.0+).
g.mergeV([(T.id): 'S4']).
  option(onCreate, [(T.label): 'Seller', 'name': 'Gadget World'])


// Housekeeping
g.V().groupCount().by(label)
g.E().groupCount().by(label)
// g.V().drop().iterate()        // wipe the graph (careful!)
