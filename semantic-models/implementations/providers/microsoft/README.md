# Microsoft: semantic models

> **Verification:** ⚪ written to documented syntax (TMDL layout follows the Apache Ossie converter fixtures; PBIP JSON files parse); not run in Power BI or Fabric.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for semantic models | Retail example |
|---|---|---|
| **Power BI / Fabric semantic model** | tabular model: tables, relationships, DAX measures, hierarchies; Import, DirectQuery or Direct Lake | [`power-bi/Retail.SemanticModel/`](power-bi/Retail.SemanticModel/) |
| **Fabric Git integration** + PBIP | the model as TMDL text files in your Azure DevOps or GitHub repo | same folder (PBIP layout) |
| Fabric IQ | binds an ontology to semantic models for agents | see [ontologies](../../../../ontologies/implementations/providers/microsoft/README.md) |
| Apache Ossie | Microsoft joined; TMDL converter in ossie-converters | [Ossie model](../../../../examples/retail/semantic-model/ossie/) |

Microsoft also appears in
[ontologies (Fabric IQ, DTDL)](../../../../ontologies/implementations/providers/microsoft/README.md) and
[graphs (Fabric Graph, Cosmos DB)](../../../../graphs/implementations/providers/microsoft/README.md).

## How the concepts map

* Tables = datasets, columns = fields, relationships = joins,
  **DAX measures** = metrics (`Revenue = SUMX('Order Lines', [Quantity] * [Unit Price])`,
  `Average Order Value = DIVIDE([Revenue], [Order Count])`).
* The category tree is a `Level 1 → 2 → 3` hierarchy on `Categories`.
* Measures evaluate in the visual's filter context, so ratios stay correct at every grain.
* Where the model lives (workspace runtime, PBIP/TMDL in git, deployment
  pipelines, XMLA endpoint):
  [semantic models concepts 3](../../../concepts/03-semantic-model-repositories.md#32-microsoft-power-bi--fabric).

## Files

```
power-bi/
  .gitignore                                  excludes .pbi/localSettings.json, .pbi/cache.abf
  Retail.SemanticModel/
    definition.pbism  .platform               PBIP / Fabric Git metadata
    definition/
      database.tmdl  model.tmdl  expressions.tmdl  relationships.tmdl
      tables/OrderLines.tmdl                  Revenue, Units Sold, Order Count, Average Order Value, Buyer Count, Discount Amount
      tables/Orders|Customers|Products|Categories|Reviews.tmdl
```

Docs: [TMDL](https://learn.microsoft.com/analysis-services/tmdl/tmdl-overview) ·
[Power BI projects (PBIP)](https://learn.microsoft.com/power-bi/developer/projects/projects-overview)
