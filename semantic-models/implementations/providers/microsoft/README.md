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

## Overview

* **A Power BI / Fabric semantic model** is a tabular model hosted in a workspace and run by the Analysis Services engine (VertiPaq).
* **Storage modes:**
  * **Import:** data is copied into the model.
  * **DirectQuery:** queries go to the source.
  * **Direct Lake:** reads Delta tables in OneLake directly.
* **How you build and version it:** author in Power BI Desktop or the web. Save as a **PBIP** project with **TMDL** files. **Fabric Git integration** syncs the workspace with Azure DevOps or GitHub, and deployment pipelines promote it.
* **Who uses it:** Power BI reports, Excel, external tools through the **XMLA endpoint**, and Copilot / Fabric data agents. **Fabric IQ** binds an ontology to it.

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

## Product documentation

* [Semantic models in the Power BI service](https://learn.microsoft.com/power-bi/connect-data/service-datasets-understand): what a semantic model is
* [TMDL](https://learn.microsoft.com/analysis-services/tmdl/tmdl-overview): the text format
* [Power BI projects (PBIP)](https://learn.microsoft.com/power-bi/developer/projects/projects-overview): folder layout
* [Fabric Git integration](https://learn.microsoft.com/fabric/cicd/git-integration/intro-to-git-integration): workspace ↔ git
* [Direct Lake](https://learn.microsoft.com/fabric/fundamentals/direct-lake-overview): storage mode over OneLake
