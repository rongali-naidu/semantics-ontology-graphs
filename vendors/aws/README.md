# AWS

> **Verification:** 🟡 data checked: the Neptune CSVs and RDF files are generated and proven to reproduce the SPARQL answers; the loader script and Python clients were not run against a Neptune cluster.
> Last reviewed 2026-11-02. Legend: [vendors/README.md](../README.md#verification-levels).

| Concept | AWS product | Files here |
|---|---|---|
| RDF store + SPARQL | **Amazon Neptune Database** | [`rdf/`](rdf/), [`loading.md`](loading.md), [`querying.md`](querying.md) |
| Property graph (Gremlin, openCypher) | **Amazon Neptune Database** | [`gremlin-csv/`](gremlin-csv/), [`opencypher-csv/`](opencypher-csv/) |
| Graph analytics, algorithms, vector search | **Amazon Neptune Analytics** | [`loading.md`](loading.md#116-neptune-analytics) |
| Ontology | load OWL as RDF into Neptune (no built-in reasoner) | [below](#104-neptune-and-ontologies) |
| GraphRAG | Amazon Bedrock Knowledge Bases with Neptune Analytics | — |
| Semantic model (BI) | Amazon QuickSight datasets + **Topics** (natural-language layer); no open semantic-layer format, so pair with dbt / Cube / AtScale over Redshift or Athena | [`../dbt-labs/`](../dbt-labs/), [`../cube/`](../cube/) |
| Scripts | bulk loader + Python clients | [`bulk-load.sh`](bulk-load.sh), [`python/`](python/) |

---

## Amazon Neptune

**Amazon Neptune** is AWS's fully managed graph database service (GA May
2018). It's unusual in supporting **both graph models**:

| Model | Query languages | Bulk-load formats |
|---|---|---|
| Property graph | **Gremlin** (Apache TinkerPop), **openCypher** | `csv` (Gremlin CSV), `opencypher` (openCypher CSV) |
| RDF | **SPARQL 1.1** Query + Update | `turtle`, `ntriples`, `nquads`, `rdfxml` |

> In **Neptune Database** the two models are kept apart: data loaded as RDF
> is only visible to SPARQL; data loaded as property graph is visible to
> **both Gremlin and openCypher** (they share the same graph).

## 10.1 The Neptune family

| | Neptune Database | Neptune Analytics |
|---|---|---|
| Purpose | OLTP: app back-end, high-concurrency reads/writes | OLAP: load big graphs in memory, run algorithms, vector similarity |
| Deployment | Cluster in your VPC: 1 writer + up to 15 read replicas; storage auto-grows, 6 copies across 3 AZs; **Serverless** option; **Global Database** | "Graph" resource sized in memory units (m-NCUs); public or private endpoint |
| Languages | Gremlin, openCypher, SPARQL | openCypher (+ algorithm procedures `neptune.algo.*`) |
| Loading | Bulk loader from S3, or queries | Import from S3 / Neptune DB snapshot / cluster; `CALL neptune.load(...)` batch load |
| Extras | Streams (CDC), full-text search via OpenSearch, ML (Neptune ML / GNNs), IAM auth, audit logs | Graph algorithms (PageRank, Louvain, BFS, ...), **vector search** (embeddings on nodes), GraphRAG |

Related: **Neptune Workbench** (managed Jupyter/SageMaker notebooks with
[graph-notebook](https://github.com/aws/graph-notebook) magics),
**[Graph Explorer](https://github.com/aws/graph-explorer)** (visual
browsing), **Neptune ML**, **Neptune Streams**, and integrations such as
Amazon Bedrock Knowledge Bases (GraphRAG backed by Neptune Analytics) and
LangChain / LlamaIndex graph stores.

## 10.2 Architecture in one picture

```
                        Your VPC
 ┌────────────────────────────────────────────────────────────────┐
 │  EC2 / Lambda / ECS / notebook ──────────┐                     │
 │                                           │ HTTPS / WSS / Bolt │
 │                                           ▼ port 8182          │
 │   cluster endpoint ─► [ Writer instance ]                      │
 │   reader endpoint  ─► [ Replica ] [ Replica ] ... (≤15)        │
 │                              │                                 │
 │              shared, distributed, auto-growing storage         │
 │              (6 copies / 3 AZs, quad indexes)                  │
 │                                                                │
 │   S3 gateway VPC endpoint ◄── bulk loader reads s3://bucket    │
 └────────────────────────────────────────────────────────────────┘
```

Endpoints (all on port **8182**, TLS required):

| Path | Purpose |
|---|---|
| `wss://<endpoint>:8182/gremlin` | Gremlin over WebSocket (drivers, console) |
| `https://<endpoint>:8182/gremlin` | Gremlin over HTTP (`{"gremlin": "..."}`) |
| `https://<endpoint>:8182/openCypher` | openCypher over HTTP (`query=...`) |
| `bolt://<endpoint>:8182` | openCypher over Bolt (Neo4j drivers) |
| `https://<endpoint>:8182/sparql` | SPARQL query/update |
| `https://<endpoint>:8182/loader` | Bulk loader |
| `https://<endpoint>:8182/status` | Engine status / version |
| `.../gremlin/explain`, `/gremlin/profile`, `/openCypher/explain`, SPARQL `explain=` | Query plans |

## 10.3 Getting started (minimal)

1. **Create a cluster** — console *Neptune → Create database* (choose
   Serverless or an instance class like `db.r6g.large`), or IaC
   (CloudFormation / CDK / Terraform `aws_neptune_cluster`).
2. **Network**: Neptune Database lives in private subnets. Connect from
   something in the same VPC (EC2, Cloud9, Lambda, a Neptune notebook) or via
   VPN / SSM port-forwarding / a bastion.
3. **Security**: security group allowing TCP 8182 from your client;
   optionally enable **IAM database authentication** (then every request must
   be SigV4-signed with service name `neptune-db`).
4. **For bulk load**: an **S3 gateway VPC endpoint** and an **IAM role** that
   Neptune can assume with `s3:GetObject` + `s3:ListBucket`, added to the
   cluster.
5. **Create a notebook** (*Neptune → Notebooks*) — fastest way to start.

```bash
# health check
curl https://$NEPTUNE_ENDPOINT:8182/status
```

## 10.4 Neptune and ontologies

* Load the **ontology** (TBox) and the **data** (ABox) as RDF — ideally in
  different **named graphs** so the ontology can be replaced independently.
* **Neptune does not run an OWL/RDFS reasoner.** Options:
  * query-time paths (`rdf:type/rdfs:subClassOf*`) — see
    [08-all-customers-via-subclass.rq](../../examples/retail/sparql/08-all-customers-via-subclass.rq);
  * materialise inferences offline (owlrl, Jena, RDFox, ROBOT) and load the result;
  * materialise with SPARQL `INSERT ... WHERE` rules
    (e.g. [09-construct-purchased.rq](../../examples/retail/sparql/09-construct-purchased.rq) → `INSERT`).
* Validate with **SHACL** before loading (pySHACL / TopBraid / Jena SHACL in
  your pipeline).
* For property-graph workloads, keep the OWL file as the documented
  model and implement it as labels/edge types (see
  [chapter 7](../../concepts/ontologies-and-graphs/07-property-graphs.md)).

## 10.5 Neptune-specific gotchas

| Topic | Note |
|---|---|
| Gremlin property cardinality | Default is **set** (adding a value appends). Use `property(single, ...)` or `name:String(single)` in CSV headers. |
| Ids | Gremlin/openCypher ids are strings; if you don't supply them Neptune makes UUIDs. Bulk loading requires ids. |
| Lambdas / Groovy scripts | Not supported in Gremlin; use pure traversal steps. |
| Transactions | Each HTTP/script request is a transaction; sessions available for multi-request transactions. |
| Default RDF graph | Triples with no graph go to `http://aws.amazon.com/neptune/vocab/v01/DefaultNamedGraph`; queries by default see the **union** of all graphs. |
| Datatypes | No decimal in property-graph CSV (use Double). RDF keeps `xsd:decimal`. |
| Mixing models | Gremlin + openCypher share data; SPARQL doesn't. Neptune Analytics can import RDF for openCypher querying. |
| Query timeouts | `neptune_query_timeout` parameter (default 120 s); per-query hints exist. |

Docs: [Neptune user guide](https://docs.aws.amazon.com/neptune/latest/userguide/intro.html) ·
[Neptune Analytics guide](https://docs.aws.amazon.com/neptune-analytics/latest/userguide/what-is-neptune-analytics.html) ·
[Neptune data model](https://docs.aws.amazon.com/neptune/latest/userguide/feature-overview-data-model.html) ·
[Best practices](https://docs.aws.amazon.com/neptune/latest/userguide/best-practices.html) ·
[awslabs/amazon-neptune-tools](https://github.com/awslabs/amazon-neptune-tools) (export, CSV↔RDF utilities)

Next: [Loading the retail example into Neptune](loading.md)
