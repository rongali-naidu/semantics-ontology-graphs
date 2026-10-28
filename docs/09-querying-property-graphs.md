# 9. Querying property graphs

| Language | Style | Standard / owner | Runs on |
|---|---|---|---|
| **Cypher / openCypher** | declarative ASCII-art patterns | Neo4j; [openCypher](https://opencypher.org/) (open spec) | Neo4j, Neptune, Memgraph, Kùzu, AGE, FalkorDB, Neptune Analytics, ... |
| **Gremlin** | imperative traversal steps | [Apache TinkerPop](https://tinkerpop.apache.org/) | Neptune, JanusGraph, Cosmos DB, TinkerGraph, ... |
| **GQL** | declarative (Cypher-like) | **ISO/IEC 39075:2024** | Spanner Graph, Neo4j (converging), others emerging |
| **SQL/PGQ** | `MATCH` inside SQL | **ISO/IEC 9075-16:2023** | Oracle 23ai, DuckDB (duckpgq) |
| GSQL | procedural + declarative | TigerGraph | TigerGraph |
| AQL, nGQL, DQL | vendor | vendor | ArangoDB, NebulaGraph, Dgraph |

## 9.1 Same question, four languages

*"Customers who bought Wireless Earbuds X also bought ..."*

**SPARQL (RDF)**
```sparql
SELECT ?otherName (COUNT(DISTINCT ?customer) AS ?buyers) WHERE {
  ?target retail:name "Wireless Earbuds X" .
  ?o1 retail:placedBy ?customer ; retail:hasLine/retail:forProduct ?target .
  ?o2 retail:placedBy ?customer ; retail:hasLine/retail:forProduct ?other .
  FILTER(?other != ?target)
  ?other retail:name ?otherName .
} GROUP BY ?otherName ORDER BY DESC(?buyers)
```

**openCypher / Cypher**
```cypher
MATCH (target:Product {name: 'Wireless Earbuds X'})<-[:CONTAINS]-(:Order)<-[:PLACED]-(c:Customer),
      (c)-[:PLACED]->(:Order)-[:CONTAINS]->(other:Product)
WHERE other <> target
RETURN other.name AS product, count(DISTINCT c) AS buyers
ORDER BY buyers DESC
```

**Gremlin**
```groovy
g.V().has('Product', 'name', 'Wireless Earbuds X').as('target').
  in('CONTAINS').in('PLACED').dedup().as('c').
  out('PLACED').out('CONTAINS').where(neq('target')).as('other').
  select('c', 'other').dedup().select('other').
  groupCount().by('name').order(local).by(values, desc)
```

**GQL**
```gql
MATCH (target:Product {name: 'Wireless Earbuds X'})<-[:CONTAINS]-(:"Order")<-[:PLACED]-(c:Customer),
      (c)-[:PLACED]->(:"Order")-[:CONTAINS]->(other:Product)
FILTER other <> target
RETURN other.name AS product, COUNT(DISTINCT c) AS buyers
ORDER BY buyers DESC
```

Full files: [Cypher](../examples/retail/property-graph/cypher/02-queries.cypher) ·
[Gremlin](../examples/retail/property-graph/gremlin/02-queries.groovy) ·
[GQL](../examples/retail/property-graph/gql/queries.gql) ·
[SQL/PGQ](../examples/retail/property-graph/sql-pgq/retail-pgq.sql) ·
[SPARQL](../examples/retail/sparql/).

## 9.2 Cypher / openCypher cheat sheet

```cypher
// pattern syntax
(n)                         // any node
(c:Customer)                // node with label
(c:Customer {name:'Bob'})   // with property filter
-[:PLACED]->                // directed relationship of a type
-[r:CONTAINS]->             // bind relationship to a variable
-[:SUBCATEGORY_OF*0..]->    // variable length 0..n hops
-[:PLACED|CONTAINS]-        // either type, either direction

// clauses
MATCH / OPTIONAL MATCH      // find patterns
WHERE                       // filter
WITH                        // pipe results to the next part (like a subquery)
RETURN ... ORDER BY ... SKIP ... LIMIT
UNWIND [1,2,3] AS x         // list → rows
CREATE / MERGE / SET / REMOVE / DELETE / DETACH DELETE
CALL proc() YIELD ...       // procedures (algorithms, loaders)

// aggregates & functions
count() sum() avg() min() max() collect()
labels(n) type(r) id(n) properties(n) keys(n)
nodes(path) relationships(path) length(path)
coalesce() toUpper() split() datetime()
```

Neptune-specific notes:
* Element ids are strings you choose at load time (`~id` / `:ID`); match with
  `WHERE id(n) = 'O1'` or `{`~id`: 'O1'}`.
* Supported features are listed under *openCypher standards compliance in
  Amazon Neptune* — e.g. use bounded variable-length paths; Neo4j-specific
  procedures (APOC, GDS) are not available.
* Use **parameters** (`$product`) for plan caching and injection safety.

Spec: [openCypher 9 reference](https://s3.amazonaws.com/artifacts.opencypher.org/openCypher9.pdf) ·
[Neo4j Cypher manual](https://neo4j.com/docs/cypher-manual/current/) ·
[Neptune openCypher](https://docs.aws.amazon.com/neptune/latest/userguide/access-graph-opencypher.html)

## 9.3 Gremlin cheat sheet

```groovy
g.V()                         // all vertices        g.E()  all edges
g.V('O1')                     // by id
.hasLabel('Customer')         .has('Product','name','EAR-X')   .has('price', gt(100))
.out('PLACED')  .in('PLACED')  .both()        // move to adjacent vertices
.outE('CONTAINS').inV()       // go via the edge (to read edge properties)
.values('name')  .valueMap()  .elementMap()  .id()  .label()
.repeat(out('SUBCATEGORY_OF')).times(3) / .until(...) / .emit()
.as('x') ... .select('x')     // label & recall steps
.where(neq('x'))  .not(inE('CONTAINS'))  .dedup()  .limit(10)
.order().by('name', desc)
.count() .sum() .mean() .group().by(...).by(...) .groupCount().by(...)
.project('a','b').by(...).by(...)   // build maps (like SELECT columns)
.math('q * p')                // arithmetic on labelled values
.path().by('name')  .simplePath()
.addV('Order').property(T.id,'O5')  .addE('PLACED').from('c').to('o')
.property(single,'status','DELIVERED')   .drop()
.mergeV([(T.id):'S4']).option(onCreate, [...])   // upsert (3.6+)
.explain() .profile()
```

Two ways to submit Gremlin:
* **Bytecode** from a GLV (gremlinpython, Java, JS, .NET, Go) — preferred; type-safe.
* **String scripts** over WebSocket/HTTP — handy in notebooks, curl.

Docs: [TinkerPop reference](https://tinkerpop.apache.org/docs/current/reference/) ·
[Practical Gremlin (free book)](https://kelvinlawrence.net/book/Gremlin-Graph-Guide.html) ·
[Neptune Gremlin](https://docs.aws.amazon.com/neptune/latest/userguide/access-graph-gremlin.html)

## 9.4 GQL and SQL/PGQ in one paragraph each

**GQL** (ISO/IEC 39075:2024) standardises the Cypher-style pattern language:
`MATCH`, `FILTER`, `RETURN`, `INSERT`, `SET`, `DELETE`, quantified paths
`-[:R]->{1,5}`, path search prefixes (`ANY SHORTEST`, `ALL SHORTEST`), graph
types (schemas), sessions and transactions. Think "SQL for graphs".

**SQL/PGQ** (ISO/IEC 9075-16:2023) lets you `CREATE PROPERTY GRAPH` as a
*view* over existing tables and then write `SELECT ... FROM GRAPH_TABLE
(g MATCH ... COLUMNS (...))`. Great when the data already lives in a
relational DB and you just want path queries.

## 9.5 SPARQL ↔ Cypher ↔ Gremlin phrasebook

| Concept | SPARQL | Cypher | Gremlin |
|---|---|---|---|
| Find by type | `?c a retail:Customer` | `MATCH (c:Customer)` | `g.V().hasLabel('Customer')` |
| Filter on attribute | `?p retail:price ?x FILTER(?x > 100)` | `WHERE p.price > 100` | `.has('price', gt(100))` |
| Follow relation | `?o retail:placedBy ?c` | `(c)-[:PLACED]->(o)` | `.out('PLACED')` |
| Reverse | `^retail:placedBy` | `<-[:PLACED]-` | `.in('PLACED')` |
| Any depth | `retail:subCategoryOf*` | `-[:SUBCATEGORY_OF*0..]->` | `.emit().repeat(out('SUBCATEGORY_OF'))` |
| Optional | `OPTIONAL { }` | `OPTIONAL MATCH` | `coalesce(..., constant(x))` |
| Negation | `FILTER NOT EXISTS { }` | `count(...) = 0` / `NOT EXISTS {}` | `.not(...)` |
| Group & count | `GROUP BY` + `COUNT` | implicit grouping in `RETURN` | `.groupCount()` / `.group()` |
| Insert | `INSERT DATA { }` | `CREATE` | `addV()/addE()` |
| Upsert | `DELETE/INSERT WHERE` | `MERGE` | `mergeV()/mergeE()` |
| Explain | `explain=` (Neptune) | `EXPLAIN` / `/openCypher/explain` | `.explain()` / `/gremlin/explain` |

Next: [10. Amazon Neptune](10-amazon-neptune.md)
