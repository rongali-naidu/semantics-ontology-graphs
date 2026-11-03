# Microsoft: graphs

> **Verification:** ⚪ written to documented syntax; not run in Fabric or Azure.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for graphs | Retail example |
|---|---|---|
| **Graph in Microsoft Fabric** | property graph (ISO GQL) modelled over OneLake tables | [`fabric-graph/retail-queries.gql`](fabric-graph/retail-queries.gql) |
| **Azure Cosmos DB for Apache Gremlin** | managed Gremlin graph database | reuse [`02-queries.groovy`](../../../../examples/retail/property-graph/gremlin/02-queries.groovy) |
| **SQL Server / Azure SQL graph tables** | `NODE` / `EDGE` tables with `MATCH` in T-SQL | — |

Microsoft also appears in
[ontologies (Fabric IQ, DTDL)](../../../../ontologies/implementations/providers/microsoft/README.md) and
[semantic models (Power BI)](../../../../semantic-models/implementations/providers/microsoft/README.md).

## How the concepts map

* **Fabric Graph** builds its graph model over lakehouse tables, the same
  table-to-graph mapping as [Spanner Graph](../gcp/spanner-graph/retail-graph.sql):
  map `customers`/`orders`/`products`/`categories` to node types and
  `orders`/`order_lines`/`products`/`categories` to PLACED / CONTAINS /
  IN_CATEGORY / SUBCATEGORY_OF edge types, then query with GQL. In Fabric IQ,
  the ontology routes graph questions to this engine.
* **Cosmos DB for Gremlin** takes the generated
  [`01-create-retail-graph.groovy`](../../../../examples/retail/property-graph/gremlin/01-create-retail-graph.groovy)
  traversal (Cosmos DB supports a subset of Gremlin steps; check the docs).

Docs: [Microsoft Fabric docs (Graph)](https://learn.microsoft.com/fabric/) ·
[Cosmos DB for Gremlin](https://learn.microsoft.com/azure/cosmos-db/gremlin/)
