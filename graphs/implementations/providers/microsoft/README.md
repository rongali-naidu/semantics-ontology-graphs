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

## Overview

* **Graph in Microsoft Fabric** is a Fabric item. You create a graph model that maps lakehouse tables to node and edge types; the data stays in OneLake. You query it with GQL in Fabric, and Fabric IQ routes relationship questions to it.
* **Azure Cosmos DB for Apache Gremlin** is a managed, globally distributed graph database. You query it with Gremlin. Each graph needs a partition key, and you pay in request units.
* **SQL Server / Azure SQL graph tables** are `NODE` and `EDGE` tables queried with `MATCH` in T-SQL, inside a relational database.

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

## Product documentation

* [Microsoft Fabric documentation](https://learn.microsoft.com/fabric/): Graph in Fabric, Fabric IQ
* [Azure Cosmos DB for Apache Gremlin](https://learn.microsoft.com/azure/cosmos-db/gremlin/): setup, supported Gremlin steps, partitioning
* [SQL Graph overview](https://learn.microsoft.com/sql/relational-databases/graphs/sql-graph-overview): node and edge tables, `MATCH`
