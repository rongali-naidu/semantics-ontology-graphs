# Microsoft (Fabric, Power BI, Azure)

| Concept | Microsoft product | Retail example |
|---|---|---|
| Semantic model | **Power BI / Fabric semantic model** (Tabular: TMDL + DAX; Import, DirectQuery, Direct Lake) | [`power-bi/Retail.SemanticModel/definition/`](power-bi/Retail.SemanticModel/definition/) |
| Property graph (ISO GQL) | **Graph in Microsoft Fabric** (GA): graph model over OneLake tables | [`fabric-graph/retail-queries.gql`](fabric-graph/retail-queries.gql) |
| Ontology | **Fabric IQ ontology** (preview as of Oct 2026): entity types, relationships and rules bound to semantic models / lakehouse tables | conceptually = [`retail-ontology.ttl`](../../examples/retail/ontology/retail-ontology.ttl) / [Ossie ontology](../../examples/retail/semantic-model/ossie/retail.ontology.yaml) |
| Ontology language (IoT / twins) | **Azure Digital Twins – DTDL v3** | [`digital-twins-dtdl/retail-ontology.json`](digital-twins-dtdl/retail-ontology.json) |
| Gremlin graph DB | **Azure Cosmos DB for Apache Gremlin** | reuse [`02-queries.groovy`](../../examples/retail/property-graph/gremlin/02-queries.groovy) |
| Graph in SQL | **SQL Server / Azure SQL graph tables** (`NODE`/`EDGE` tables, `MATCH`) | — |
| Open semantic format | Joined **Apache Ossie**; TMDL ↔ Ossie converter in ossie-converters | — |

## How the generic concepts map

* **Semantic model** → Power BI tables (datasets), columns (fields),
  relationships (joins), **DAX measures** (metrics), hierarchies. The
  category tree is a `Level 1 → 2 → 3` hierarchy on `Categories`.
* **Ontology** → DTDL interfaces are JSON-LD-based: `extends` ≈ `rdfs:subClassOf`,
  `Property` ≈ datatype property, `Relationship` ≈ object property, and
  relationships can have properties (like the `CONTAINS` edge).
  Fabric IQ's ontology plays the same role for analytics: it names business
  entities once and routes questions to semantic models (DAX), graphs (GQL)
  or event data (KQL).

## Files

```
power-bi/Retail.SemanticModel/definition/   TMDL (open in Power BI Desktop as a PBIP project, or deploy with Fabric git integration)
  database.tmdl  model.tmdl  expressions.tmdl  relationships.tmdl
  tables/OrderLines.tmdl (Revenue, Units Sold, Order Count, Average Order Value, Buyer Count, Discount Amount)
  tables/Orders|Customers|Products|Categories|Reviews.tmdl
digital-twins-dtdl/retail-ontology.json     DTDL v3 interfaces: Party, Customer, Order, Product, Category, Seller
fabric-graph/retail-queries.gql             GQL over a Fabric graph model
```

Not executed against Microsoft services in this repo. The TMDL follows the
TMDL format used in the Apache Ossie converter fixtures; the DTDL file is
valid JSON written to the DTDL v3 spec.

Docs: [TMDL](https://learn.microsoft.com/analysis-services/tmdl/tmdl-overview) ·
[Power BI projects (PBIP)](https://learn.microsoft.com/power-bi/developer/projects/projects-overview) ·
[Microsoft Fabric docs (Graph, IQ)](https://learn.microsoft.com/fabric/) ·
[DTDL v3](https://github.com/Azure/opendigitaltwins-dtdl/blob/master/DTDL/v3/DTDL.v3.md) ·
[Cosmos DB for Gremlin](https://learn.microsoft.com/azure/cosmos-db/gremlin/)
