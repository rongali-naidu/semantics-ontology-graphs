# Google Cloud: graphs

> **Verification:** ⚪ written to documented syntax; not run on Google Cloud.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for graphs | Retail example |
|---|---|---|
| **Spanner Graph** | property graph (ISO GQL) declared over Spanner tables | [`spanner-graph/retail-graph.sql`](spanner-graph/retail-graph.sql) |
| **BigQuery Graph** | property graph (GQL) over BigQuery warehouse tables, mixed with SQL via `GRAPH_TABLE` | [`bigquery-graph/retail-graph.sql`](bigquery-graph/retail-graph.sql) |
| Vertex AI + Spanner / BigQuery Graph | GraphRAG | — |
| **Knowledge Catalog** | ingests BigQuery Graph definitions into its context graph alongside semantic models | see [ontologies](../../../../ontologies/implementations/providers/gcp/README.md) |
| RDF / SPARQL | none native (run Jena, GraphDB or Oxigraph on GKE / Compute Engine) | — |

Google Cloud also appears in [semantic models (Looker)](../../../../semantic-models/implementations/providers/gcp/README.md).

## How the concepts map

* **No copy into a graph store.** Both products declare `CREATE PROPERTY GRAPH`
  over existing tables, like SQL/PGQ
  ([`retail-pgq.sql`](../../../../examples/retail/property-graph/sql-pgq/retail-pgq.sql)).
  Node tables: `customers`, `orders`, `products`, `categories`. Edge tables: `orders`
  (PLACED), `order_lines` (CONTAINS, with quantity/unit_price), `products`
  (IN_CATEGORY), `categories` (SUBCATEGORY_OF).
* **Querying** ([graphs concepts 3](../../../concepts/03-querying-property-graphs.md)):
  ISO GQL quantified paths such as `-[:SUBCATEGORY_OF]-{0,3}` walk the category tree.
  BigQuery's `GRAPH_TABLE(...)` feeds graph matches into SQL aggregation (= SPARQL Q3).

Docs: [Spanner Graph](https://cloud.google.com/spanner/docs/graph/overview) ·
[GQL reference (Spanner)](https://cloud.google.com/spanner/docs/reference/standard-sql/graph-intro) ·
[BigQuery docs (Graph)](https://cloud.google.com/bigquery/docs)
