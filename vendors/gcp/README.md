# Google Cloud

> **Verification:** ⚪ written to documented syntax; not run on Google Cloud.
> Last reviewed 2026-11-02. Legend: [vendors/README.md](../README.md#verification-levels).

| Concept | Google Cloud product | Retail example |
|---|---|---|
| Property graph DB (ISO GQL) | **Spanner Graph**: a property graph mapped onto Spanner tables | [`spanner-graph/retail-graph.sql`](spanner-graph/retail-graph.sql) |
| Graph over the warehouse | **BigQuery Graph** (GQL over BigQuery tables) | [`bigquery-graph/retail-graph.sql`](bigquery-graph/retail-graph.sql) |
| Semantic model | **Looker** (LookML); Looker semantic layer also serves Looker Studio, Sheets, Tableau and others via connectors | [`looker/`](looker/) |
| Knowledge graph service | Enterprise Knowledge Graph API (entity reconciliation), Google Knowledge Graph Search API | — |
| GraphRAG / AI | Vertex AI + Spanner Graph / BigQuery Graph; Looker conversational analytics | — |
| RDF / SPARQL | none native (run Jena/GraphDB/Oxigraph on GKE or Compute Engine) | — |

## How the generic concepts map

* **Property graph** ([concepts/ontologies-and-graphs/07](../../concepts/ontologies-and-graphs/07-property-graphs.md)):
  Spanner Graph and BigQuery Graph don't copy data into a graph store; they
  declare `CREATE PROPERTY GRAPH` over tables, much like SQL/PGQ
  ([`retail-pgq.sql`](../../examples/retail/property-graph/sql-pgq/retail-pgq.sql)).
  Node tables = `customers`, `orders`, `products`, `categories`; edge tables =
  `orders` (PLACED), `order_lines` (CONTAINS with quantity/unit_price),
  `products` (IN_CATEGORY), `categories` (SUBCATEGORY_OF).
* **Querying** ([concepts/.../09](../../concepts/ontologies-and-graphs/09-querying-property-graphs.md)):
  ISO GQL, e.g. quantified paths `-[:SUBCATEGORY_OF]-{0,3}` for the category
  tree; `GRAPH_TABLE(...)` mixes graph patterns into SQL.
* **Semantic model** ([concepts/semantic-modelling/02](../../concepts/semantic-modelling/02-semantic-models-in-reporting-tools.md)):
  LookML views = Ossie datasets, explores = join graphs, measures = metrics.
  Note the `relationship: many_to_one` on every join: Looker uses it for
  *symmetric aggregates*, which prevent fan-out double counting.

## Files

```
looker/
  retail.model.lkml          explores: order_lines (+ orders, customers, products, categories), reviews
  views/*.view.lkml          one view per table; measures revenue, order_count, average_order_value...
spanner-graph/retail-graph.sql   CREATE PROPERTY GRAPH + GQL Q2 / Q5
bigquery-graph/retail-graph.sql  CREATE PROPERTY GRAPH + GRAPH_TABLE aggregation (= SPARQL Q3)
```

Not executed against Google Cloud in this repo; written to the documented syntax.

Docs: [Spanner Graph](https://cloud.google.com/spanner/docs/graph/overview) ·
[BigQuery docs (Graph)](https://cloud.google.com/bigquery/docs) ·
[LookML](https://cloud.google.com/looker/docs/what-is-lookml) ·
[GQL reference (Spanner)](https://cloud.google.com/spanner/docs/reference/standard-sql/graph-intro)
