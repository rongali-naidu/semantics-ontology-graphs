# Salesforce: semantic models

> **Verification:** ⚪ documented from Salesforce material; nothing run in Tableau or Data 360.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for semantic models | Retail example |
|---|---|---|
| **Tableau Semantics** (in Data 360) | semantic layer that turns raw tables into governed metrics, dimensions and relationships; powers Tableau Next and Agentforce analytics | mapping below |
| **Data 360** (formerly Data Cloud) | data and metadata layer on Apache Iceberg that hosts the semantic data model | — |
| Tableau Next MCP server | lets MCP clients query the same semantic model Agentforce uses | — |
| Apache Ossie | Salesforce co-founded OSI (now Ossie); a Data 360 workflow converts Ossie YAML into Tableau semantic data model JSON | [retail Ossie model](../../../../examples/retail/semantic-model/ossie/retail.semantic_model.yaml) |

## Overview

* **Tableau Semantics is part of Salesforce Data 360** (formerly Data Cloud). The *semantic data model* is metadata over Data 360 data objects, which sit on an Apache Iceberg lakehouse.
* **How you build it:** in the Data 360 / Tableau Next interface: data objects, relationships, calculated fields and metrics with semantic descriptions.
* **Who uses it:** Tableau Next and **Agentforce** analytics, and any MCP client through the Tableau Next MCP server.
* **Portability:** the model isn't a set of files in your git repo; the Apache Ossie conversion is the portable route.

## How the concepts map

| Ossie / generic | Tableau Semantics |
|---|---|
| dataset | data object in the semantic data model |
| relationship | relationship between data objects |
| field | dimension / measure field |
| metric | **calculated field / metric** with a definition and semantic description |
| `ai_context.synonyms` | descriptions and synonyms used by Agentforce |

Where the model lives: as metadata in Data 360, not as files in your git
repo; Ossie export/import is the portable route
([semantic models concepts 3](../../../concepts/03-semantic-model-repositories.md#34-tableau)).
Classic Tableau published data sources (`.tds`) are a separate, older
semantic model.

## Product documentation

* [Tableau Semantics](https://www.tableau.com/products/tableau-semantics): product overview
* [Semantic layers for AI agents with Data 360](https://www.salesforce.com/blog/semantic-layer-ai-agents-data-360/): how agents use it
* [From Alliance to Apache: open semantics](https://www.salesforce.com/blog/alliance-to-apache-next-chapter-for-open-semantics/): Ossie conversion
