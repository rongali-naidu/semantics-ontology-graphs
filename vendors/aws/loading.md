# Loading the retail example into Neptune — every format

Same retail graph, six bulk-load formats plus three "load by query" options.

| # | Method | Format / API | Files | Queried by |
|---|---|---|---|---|
| A | Bulk loader | `csv` (Gremlin CSV) | [`gremlin-csv/`](gremlin-csv/) | Gremlin + openCypher |
| B | Bulk loader | `opencypher` (openCypher CSV) | [`opencypher-csv/`](opencypher-csv/) | openCypher + Gremlin |
| C | Bulk loader | `turtle` | [`rdf/retail-data.ttl`](rdf/retail-data.ttl) + ontology | SPARQL |
| D | Bulk loader | `ntriples` | [`rdf/retail-data.nt`](rdf/retail-data.nt) | SPARQL |
| E | Bulk loader | `nquads` | [`rdf/retail-data.nq`](rdf/retail-data.nq) (4 named graphs) | SPARQL |
| F | Bulk loader | `rdfxml` | [`rdf/retail-data.rdf`](rdf/retail-data.rdf) | SPARQL |
| G | Query | openCypher `CREATE` | [`01-create-retail-graph.cypher`](../../examples/retail/property-graph/cypher/01-create-retail-graph.cypher) | openCypher + Gremlin |
| H | Query | Gremlin `addV/addE` | [`01-create-retail-graph.groovy`](../../examples/retail/property-graph/gremlin/01-create-retail-graph.groovy) | Gremlin + openCypher |
| I | Query | SPARQL `INSERT DATA` / `LOAD <url>` | [`12-insert-new-order.ru`](../../examples/retail/sparql/12-insert-new-order.ru) | SPARQL |

Pick **one** of A/B/G/H for the property graph (they create the same 29
nodes and 41 edges) and **one** of C/D/E/F/I for RDF (same 165 data triples +
238 ontology triples). JSON-LD and TriG are not bulk-load formats — convert
them to N-Quads/Turtle first (`build_rdf_formats.py` already does).

## 11.1 Format A — Gremlin CSV (`"format": "csv"`)

One file per vertex label plus edge files. System columns start with `~`;
property columns are `name:Type` with optional `(single)` / `(set)`
cardinality.

`vertices-customer.csv`
```csv
~id,~label,name:String(single),email:String(single),premium:Bool(single),memberSince:Date(single)
C1,Customer,Alice Johnson,alice@example.com,true,2024-03-15
C2,Customer,Bob Smith,bob@example.com,false,
C3,Customer,Carol Diaz,carol@example.com,true,2025-11-01
```

`edges-contains.csv` — edge properties are what replace the RDF `OrderLine`
```csv
~id,~from,~to,~label,quantity:Int,unitPrice:Double
O1-L1,O1,P1,CONTAINS,1,1299.00
O1-L2,O1,P3,CONTAINS,2,29.99
```

`edges.csv`
```csv
~id,~from,~to,~label
C1-PLACED-O1,C1,O1,PLACED
P1-IN_CATEGORY-CAT-LAPTOPS,P1,CAT-LAPTOPS,IN_CATEGORY
```

Types: `Bool Byte Short Int Long Float Double String Date`; arrays by
`String[]`; multiple labels by `Customer;PremiumCustomer`; an empty field
means "no property". Spec:
[Gremlin load data format](https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load-tutorial-format-gremlin.html).

## 11.2 Format B — openCypher CSV (`"format": "opencypher"`)

Same idea, Neo4j-import-like headers.

`nodes-customer.csv`
```csv
:ID,:LABEL,name:String,email:String,premium:Bool,memberSince:DateTime
C1,Customer,Alice Johnson,alice@example.com,true,2024-03-15
```

`relationships-contains.csv`
```csv
:ID,:START_ID,:END_ID,:TYPE,quantity:Int,unitPrice:Double
O1-L1,O1,P1,CONTAINS,1,1299.00
```

Types: `Bool Byte Short Int Long Float Double String DateTime`; arrays with
`[]`; multi-labels with `;`. Properties are single-valued. Spec:
[openCypher load data format](https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load-tutorial-format-opencypher.html).

## 11.3 Formats C–F — RDF

Any of Turtle, N-Triples, N-Quads or RDF/XML. For triple formats you can set
the target graph with `parserConfiguration.namedGraphUri` (otherwise the
Neptune default graph); N-Quads carry their own graph per line.
`parserConfiguration.baseUri` resolves relative IRIs.
Spec: [RDF load data formats](https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load-tutorial-format-rdf.html).

Recommended layout:

| Named graph | Contents |
|---|---|
| `https://example.org/retail/graph/ontology` | `retail-ontology.ttl` (TBox) |
| `https://example.org/retail/graph/data` | `retail-data.ttl` (ABox) — or the 4 graphs in `retail-data.nq` |

## 11.4 Running the bulk loader

### Option 1 — the script in this repo (curl)

```bash
export NEPTUNE_ENDPOINT=my-cluster.cluster-abc123.us-east-1.neptune.amazonaws.com
export BUCKET=my-graph-data-bucket
export LOADER_ROLE_ARN=arn:aws:iam::123456789012:role/NeptuneLoadFromS3
export AWS_REGION=us-east-1
./vendors/aws/bulk-load.sh
```

What it sends ([full file](bulk-load.sh)):

```bash
curl -X POST https://$NEPTUNE_ENDPOINT:8182/loader -H 'Content-Type: application/json' -d '{
  "source":      "s3://my-graph-data-bucket/retail/gremlin-csv/",
  "format":      "csv",
  "iamRoleArn":  "arn:aws:iam::123456789012:role/NeptuneLoadFromS3",
  "region":      "us-east-1",
  "failOnError": "FALSE",
  "parallelism": "MEDIUM",
  "updateSingleCardinalityProperties": "FALSE",
  "queueRequest": "TRUE"
}'
# → {"status":"200 OK","payload":{"loadId":"ef478d76-..."}}

curl "https://$NEPTUNE_ENDPOINT:8182/loader/ef478d76-...?details=true&errors=true"
```

RDF example with a named graph:

```json
{
  "source": "s3://my-graph-data-bucket/retail/rdf/retail-ontology.ttl",
  "format": "turtle",
  "iamRoleArn": "...", "region": "us-east-1",
  "parserConfiguration": { "namedGraphUri": "https://example.org/retail/graph/ontology" }
}
```

Useful loader options: `mode` (`NEW` / `RESUME` / `AUTO`), `parallelism`
(`LOW` … `OVERSUBSCRIBE`), `queueRequest` + `dependencies` (chain jobs, e.g.
vertices before edges), `failOnError`, `updateSingleCardinalityProperties`.
[Loader command reference](https://docs.aws.amazon.com/neptune/latest/userguide/load-api-reference-load.html).

### Option 2 — AWS CLI (signs requests, so it works with IAM auth)

```bash
aws neptunedata start-loader-job \
  --endpoint-url https://$NEPTUNE_ENDPOINT:8182 \
  --source s3://$BUCKET/retail/opencypher-csv/ --format opencypher \
  --s3-bucket-region $AWS_REGION --iam-role-arn $LOADER_ROLE_ARN

aws neptunedata get-loader-job-status --endpoint-url https://$NEPTUNE_ENDPOINT:8182 --load-id <id>
```

### Option 3 — Python / boto3

```bash
pip install -r vendors/aws/python/requirements.txt
python vendors/aws/python/bulk_load.py s3://$BUCKET/retail/rdf/retail-data.nq nquads
```
([bulk_load.py](python/bulk_load.py) starts the job and polls until it finishes.)

### Option 4 — Neptune notebook

```
%load                 # opens a form: source, format, role, mode...
%load_status <loadId>
%seed                 # loads built-in sample datasets (air-routes etc.)
```

## 11.5 Loading by query (small data, dev, incremental updates)

**openCypher** — paste the generated single `CREATE` statement:
```
%%oc
CREATE (n_C1:Customer {`~id`: 'C1', name: 'Alice Johnson', ...}), ..., (n_C1)-[:PLACED]->(n_O1), ...
```
Neptune honours `` `~id` `` as the element id.

**Gremlin** — one long traversal:
```
%%gremlin
g.addV('Customer').property(T.id, 'C1').property('name', 'Alice Johnson')...as('C1')
 .addE('PLACED').from('C1').to('O1').property(T.id, 'C1-PLACED-O1') ... .iterate()
```

**SPARQL Update**:
```sparql
INSERT DATA { GRAPH <https://example.org/retail/graph/data> { ... triples ... } }

# or let Neptune fetch a file over HTTP(S) (small files; bulk loader for big ones)
LOAD <https://my-bucket.s3.amazonaws.com/retail/rdf/retail-data.ttl>
  INTO GRAPH <https://example.org/retail/graph/data>
```

## 11.6 Neptune Analytics

```cypher
// batch load from S3 into an existing graph (openCypher procedure)
CALL neptune.load({
  source: "s3://my-graph-data-bucket/retail/opencypher-csv/",
  region: "us-east-1",
  format: "opencypher"          // also: "csv" (Gremlin CSV), "ntriples", "parquet"
})
```
Or create the graph with an **import task** from S3 or from a Neptune
Database snapshot (`aws neptune-graph create-graph-using-import-task ...`).
Check the [Neptune Analytics loading docs](https://docs.aws.amazon.com/neptune-analytics/latest/userguide/loading-data.html)
for the formats and options your version supports.

## 11.7 Verify the load

```cypher
MATCH (n) RETURN labels(n) AS label, count(*) AS n ORDER BY n DESC
// Customer 3, Address 3, Seller 3, Category 6, Product 6, Order 4, Review 4  (29)
MATCH ()-[r]->() RETURN type(r), count(*)      // 41 relationships
```
```groovy
g.V().groupCount().by(label)
g.E().count()                                    // 41
```
```sparql
SELECT ?g (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?s ?p ?o } } GROUP BY ?g
# data: 165 triples, ontology: 238 triples
```

## 11.8 Troubleshooting

| Symptom | Likely cause |
|---|---|
| `403` from `/loader` | IAM auth enabled → sign requests (awscurl / AWS CLI / boto3) |
| `S3_ACCESS_DENIED` / loader can't reach S3 | Missing S3 **gateway VPC endpoint**, role not attached to cluster, or wrong region |
| `LOAD_DATA_DEADLOCK` / slow | lower `parallelism`; split files; load vertices before edges with `dependencies` |
| `FROM_OR_TO_VERTEX_ARE_MISSING` | edge file references ids not (yet) loaded |
| Properties have 2 values after reload | Gremlin set cardinality — use `(single)` and `updateSingleCardinalityProperties` |
| Data loaded but SPARQL sees nothing | You loaded CSV (property graph) — SPARQL only sees RDF |
| Parse error on RDF | check prefixes / encoding (UTF-8), or convert to N-Triples to find the bad line |

Next: [Querying Neptune](querying.md)
