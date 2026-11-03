# Palantir: ontologies

> **Verification:** ⚪ documented from Palantir's docs; nothing run in Foundry.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for ontologies | Retail example |
|---|---|---|
| **Foundry Ontology** (with AIP) | an **operational** ontology: object types backed by datasets, link types between them, and **action types** that change data, used by apps, workflows and AI agents | mapping below |
| Ontology SDK (OSDK) | typed client libraries generated from the ontology | — |

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
act through governed actions instead of writing SQL. There's no OWL import
or export; the ontology is defined inside Foundry.

Docs: [Ontology core concepts](https://www.palantir.com/docs/foundry/ontology/core-concepts) ·
[Types reference](https://palantir.com/docs/foundry/object-link-types)
