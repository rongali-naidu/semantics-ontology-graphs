# Snowflake: ontologies

> **Verification:** ⚪ documented; nothing run on Snowflake.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for ontologies | Retail example |
|---|---|---|
| **Ontology on Snowflake** (Snowflake-Labs, Apache 2.0) | reference architecture: ontology metadata in tables (`ONT_CLASS`, `ONT_RELATION_DEF`, `ONT_PROPERTY`, `ONT_RULE`...), instances in `KG_NODE` / `KG_EDGE`, generated views, Cortex Analyst models, and a Cortex Agent | mapping below |
| **RelationalAI** (native app on Snowflake) | knowledge graph and reasoning engine; syncs both ways with Snowflake semantic views | — |
| Apache Ossie ontology | Snowflake started OSI (now Ossie), whose spec includes an ontology layer | [retail Ossie ontology](../../../../examples/retail/semantic-model/ossie/retail.ontology.yaml) |

Snowflake also appears in
[graphs (KG tables + graph analytics)](../../../../graphs/implementations/providers/snowflake/README.md) and
[semantic models (semantic views)](../../../../semantic-models/implementations/providers/snowflake/README.md).

## Overview

* **Snowflake has no native ontology feature.** Ontologies are built from tables, apps and the Ossie spec.
* **Ontology on Snowflake** (Snowflake-Labs, Apache 2.0) is a **reference architecture you deploy with SQL scripts**. It provides:
  * ontology tables (`ONT_*`);
  * a node/edge graph (`KG_NODE`, `KG_EDGE`);
  * generated views;
  * three Cortex Analyst models;
  * a Cortex Agent that chooses between them.
* **RelationalAI** is a **native app** from the Snowflake Marketplace that runs inside your account. You model concepts and rules (in Python), and they sync both ways with semantic views.
* **Apache Ossie**, started by Snowflake as OSI, includes an ontology layer that sits next to semantic models.

## How the concepts map

*Ontology on Snowflake* expresses an ontology **as relational tables**, not
OWL:

| OWL ([retail-ontology.ttl](../../../../examples/retail/ontology/retail-ontology.ttl)) | Ontology on Snowflake |
|---|---|
| `owl:Class` (Customer, Order, Product...) | rows in `ONT_CLASS` |
| object properties (placedBy, inCategory...) | rows in `ONT_RELATION_DEF` |
| datatype properties | rows in `ONT_PROPERTY` |
| rules / inference | `ONT_RULE` |
| individuals (ex:C1, ex:O1...) | rows in `KG_NODE` (VARIANT properties) |
| triples between individuals | rows in `KG_EDGE` |
| class-level queries | generated `VW_ONT_*` views |

An agent then picks between three Cortex Analyst models (concrete data,
ontology-level, governance metadata) and graph-analytics tools. The retail
graph's [property-graph CSVs](../../../../graphs/implementations/providers/aws/opencypher-csv/)
would load almost directly into `KG_NODE` / `KG_EDGE`. Note the project's
own caveat: Cortex Analyst and Cortex Agent were preview features when it
was published.

## Product documentation

* [Snowflake-Labs/ontology-on-snowflake](https://github.com/snowflake-Labs/ontology-on-snowflake): scripts and architecture
* [Native semantic views and RelationalAI sync](https://www.snowflake.com/en/blog/engineering/native-semantic-views-ai-bi/): how ontology and semantic views connect
* [RelationalAI documentation](https://docs.relational.ai/): native app, modelling, reasoning
* [Cortex Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents): the agent layer
