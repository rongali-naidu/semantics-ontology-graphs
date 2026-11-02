# Querying the retail graph in Neptune — every way

| Language | Transport | Tool / client | Example |
|---|---|---|---|
| SPARQL | HTTPS `POST /sparql` | curl, awscurl, `requests`, SPARQLWrapper, RDF4J, Jena | [`sparql_query.py`](python/sparql_query.py) |
| openCypher | HTTPS `POST /openCypher` | curl, boto3 `neptunedata` | [`opencypher_query.py`](python/opencypher_query.py) `https` / `boto3` |
| openCypher | Bolt `bolt://...:8182` | Neo4j drivers (Python, Java, JS, Go, .NET) | `opencypher_query.py bolt` |
| Gremlin | WebSocket `wss://.../gremlin` | gremlinpython / Java / JS / .NET / Go, Gremlin Console | [`gremlin_query.py`](python/gremlin_query.py) `ws` |
| Gremlin | HTTPS `POST /gremlin` | curl, boto3 `neptunedata` | `gremlin_query.py boto3` |
| all three | notebook magics | `%%sparql`, `%%oc`, `%%gremlin` | below |
| all three | visual | [Graph Explorer](https://github.com/aws/graph-explorer) | |

> If **IAM database authentication** is enabled every request must be
> SigV4-signed (service `neptune-db`). `common.py` does this for you; the
> AWS CLI / boto3 `neptunedata` client signs automatically; for curl use
> [`awscurl`](https://github.com/okigan/awscurl).

## 12.1 Notebook (fastest start)

```
%%sparql
PREFIX retail: <https://example.org/retail/ontology#>
SELECT ?customerName (SUM(?qty * ?price) AS ?totalSpent) WHERE {
  ?o retail:placedBy/retail:name ?customerName ; retail:hasLine ?l .
  ?l retail:quantity ?qty ; retail:unitPrice ?price .
} GROUP BY ?customerName ORDER BY DESC(?totalSpent)
```

```
%%oc
MATCH (c:Customer)-[:PLACED]->(o:Order)-[l:CONTAINS]->(:Product)
RETURN c.name AS customer, sum(l.quantity * l.unitPrice) AS totalSpent
ORDER BY totalSpent DESC
```

```
%%gremlin -p v,oute,inv
g.V().has('Customer','name','Alice Johnson').outE('PLACED').inV().outE('CONTAINS').inV().path()
```

The `-p` option builds an interactive **graph visualisation** of the path
result. `%%oc explain` / `%%gremlin profile` / `%%sparql explain` show plans.

## 12.2 SPARQL over HTTPS

```bash
# SELECT → JSON
curl -s https://$NEPTUNE_ENDPOINT:8182/sparql \
  -H 'Accept: application/sparql-results+json' \
  --data-urlencode query@examples/retail/sparql/02-electronics-products-incl-subcategories.rq

# results as CSV
curl -s https://$NEPTUNE_ENDPOINT:8182/sparql -H 'Accept: text/csv' \
  --data-urlencode query@examples/retail/sparql/03-order-totals-per-customer.rq

# CONSTRUCT → Turtle
curl -s https://$NEPTUNE_ENDPOINT:8182/sparql -H 'Accept: text/turtle' \
  --data-urlencode query@examples/retail/sparql/09-construct-purchased.rq

# UPDATE
curl -s https://$NEPTUNE_ENDPOINT:8182/sparql \
  --data-urlencode update@examples/retail/sparql/12-insert-new-order.ru

# query plan
curl -s https://$NEPTUNE_ENDPOINT:8182/sparql -d explain=dynamic \
  --data-urlencode query@examples/retail/sparql/05-customers-who-bought-also-bought.rq
```

Python: `python sparql_query.py ../../../examples/retail/sparql/05-customers-who-bought-also-bought.rq`.

Neptune SPARQL extras: query hints (`hint:Query hint:joinOrder "Ordered"`),
full-text search via OpenSearch (`neptune-fts:` SERVICE), `explain=static|dynamic|details`,
and SPARQL `SERVICE` federation to other endpoints.

## 12.3 openCypher over HTTPS / boto3 / Bolt

```bash
curl -s https://$NEPTUNE_ENDPOINT:8182/openCypher \
  --data-urlencode "query=MATCH (p:Product) RETURN p.name, p.price ORDER BY p.price DESC"

# parameterised (preferred: plan cache + no injection)
curl -s https://$NEPTUNE_ENDPOINT:8182/openCypher \
  --data-urlencode 'query=MATCH (p:Product {sku: $sku}) RETURN p' \
  --data-urlencode 'parameters={"sku": "EAR-X"}'

aws neptunedata execute-open-cypher-query --endpoint-url https://$NEPTUNE_ENDPOINT:8182 \
  --open-cypher-query "MATCH (c:Customer) RETURN c.name, c.premium"
```

```python
import boto3, json
client = boto3.client("neptunedata", endpoint_url=f"https://{endpoint}:8182")
r = client.execute_open_cypher_query(
    openCypherQuery="MATCH (o:Order)-[l:CONTAINS]->(p:Product) WHERE id(o) = $id "
                    "RETURN p.name AS product, l.quantity AS qty",
    parameters=json.dumps({"id": "O1"}))
print(r["results"])
```

Bolt (Neo4j driver — existing Neo4j app code mostly works):
```python
from neo4j import GraphDatabase
driver = GraphDatabase.driver(f"bolt://{endpoint}:8182", auth=("neptune", "ignored"), encrypted=True)
with driver.session() as s:
    for rec in s.run("MATCH (c:Customer)-[:PLACED]->(o) RETURN c.name, count(o) AS orders"):
        print(rec.data())
```

## 12.4 Gremlin over WebSocket / HTTPS

```python
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import P

conn = DriverRemoteConnection(f"wss://{endpoint}:8182/gremlin", "g")
g = traversal().with_remote(conn)

# Q5 — also bought
print(g.V().has("Product", "name", "Wireless Earbuds X").as_("t")
       .in_("CONTAINS").in_("PLACED").dedup()
       .out("PLACED").out("CONTAINS").where(P.neq("t"))
       .group_count().by("name").next())
conn.close()
```
(Python renames steps that clash with keywords: `in_`, `as_`, `not_`, `sum_`. This short form counts paths; see Q5 in `02-queries.groovy` for the distinct-buyer version.)

```bash
curl -s https://$NEPTUNE_ENDPOINT:8182/gremlin \
  -d '{"gremlin": "g.V().hasLabel(\"Product\").not(inE(\"CONTAINS\")).values(\"name\")"}'

curl -s https://$NEPTUNE_ENDPOINT:8182/gremlin/profile \
  -d '{"gremlin": "g.V().has(\"Customer\",\"name\",\"Alice Johnson\").out(\"PLACED\").count()"}'
```

Gremlin Console: `conf/neptune-remote.yaml` with `hosts: [endpoint]`,
`port: 8182`, `connectionPool: { enableSsl: true }`, serializer
`GraphBinaryMessageSerializerV1`; then `:remote connect tinkerpop.server
conf/neptune-remote.yaml` and `:remote console`.

## 12.5 One graph, two languages

After loading the **property graph** once (CSV, Cypher or Gremlin), *both*
of these work against the same data:

```cypher
MATCH (c:Customer {name:'Bob Smith'})-[:PLACED]->(o) RETURN id(o), o.status
```
```groovy
g.V().has('Customer','name','Bob Smith').out('PLACED').project('id','status').by(id).by('status')
```

## 12.6 Performance checklist

* Start traversals from **selective** points (an id, a unique property)
  rather than `g.V()` / `MATCH (n)`.
* Always put **labels** in patterns; Neptune indexes them.
* Use **parameters**, not string concatenation.
* Use **explain/profile** to find full scans.
* Send reads to the **reader endpoint**; writes to the cluster endpoint.
* Batch writes (e.g. 100–1,000 elements per request) and use the bulk loader
  for anything big.
* Neptune Analytics for whole-graph algorithms instead of huge OLTP traversals.

Back to: [vendors overview](../README.md) · [standards, links & glossary](../../reference/standards-links-glossary.md)
