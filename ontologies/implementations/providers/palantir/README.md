# Palantir: ontologies

> **Verification:** ⚪ documented from Palantir's docs; nothing run in Foundry.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for ontologies | Retail example |
|---|---|---|
| **Foundry Ontology** (with AIP) | an **operational** ontology: object types backed by datasets, link types between them, and **action types** that change data, used by apps, workflows and AI agents | mapping below |
| Ontology SDK (OSDK) | typed client libraries generated from the ontology | — |

## Overview

* **The Foundry Ontology is part of Palantir Foundry** (hosted). Object types are backed by datasets that Foundry pipelines produce. Foundry indexes them so applications can read and change *objects* rather than rows.
* **How you build it:** in **Ontology Manager**. Define object types, link types and **action types**: the permitted edits, with validation and permissions. **Functions** (TypeScript or Python) compute derived values.
* **How it's used:**
  * Workshop apps and workflows.
  * The **Ontology SDK (OSDK)**, which generates typed client libraries.
  * **AIP** agents, which call actions and functions as tools instead of writing SQL.
* **No OWL import or export:** the ontology exists only inside Foundry.

## How the concepts map

| OWL ([retail-ontology.ttl](../../../../examples/retail/ontology/retail-ontology.ttl)) | Foundry Ontology |
|---|---|
| `owl:Class` Customer, Order, Product | **object types** Customer, Order, Product (each backed by a dataset) |
| datatype properties | **properties** |
| object properties `placedBy`, `inCategory` | **link types** |
| individuals | **objects** |
| rules / derived properties | **functions** |
| *(no OWL equivalent)* | **action types**, e.g. "Mark order delivered", "Refund order line" |

The defining difference is **actions**: Palantir's ontology describes what
exists *and* what you're allowed to do to it, with permissions, so agents
act through governed actions instead of writing SQL.

## Product documentation

* [Ontology core concepts](https://www.palantir.com/docs/foundry/ontology/core-concepts): objects, links, actions
* [Object and link types reference](https://palantir.com/docs/foundry/object-link-types): defining types and properties
* [Action types](https://www.palantir.com/docs/foundry/action-types/overview): governed edits
* [Ontology SDK](https://www.palantir.com/docs/foundry/ontology-sdk/overview): generated clients
* [AIP](https://www.palantir.com/docs/foundry/aip/overview): agents over the ontology
