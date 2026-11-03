# SAP: semantic models

> **Verification:** ⚪ documented; nothing run on SAP.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for semantic models | Retail example |
|---|---|---|
| **SAP Business Data Cloud / Datasphere** | analytic models (facts, dimensions, measures, associations) over SAP and non-SAP data | mapping below |
| **CSN** (Core Schema Notation, JSON) | SAP's machine-readable format for entity and model definitions; ingested by e.g. Google Knowledge Catalog | — |
| SAP BusinessObjects universes | the classic semantic layer (`.unx`, CMS repository) | see [semantic models concepts 3](../../../concepts/03-semantic-model-repositories.md#35-sap-businessobjects-and-sap-datasphere) |
| SAP Knowledge Graph | business semantics for Joule agents | see [ontologies](../../../../ontologies/implementations/providers/sap/README.md) |

## How the concepts map

| Ossie / generic | SAP Datasphere / BDC |
|---|---|
| dataset | fact / dimension (views with semantic usage) |
| relationship | association |
| field | attribute |
| metric | measure (with aggregation), calculated measure |
| model | analytic model |
| text format | CSN (JSON) |

SAP's big advantage is that standard business content (sales orders,
customers, materials) arrives **pre-modelled**; the retail model would map
onto standard sales entities rather than be built from scratch.

Docs: [SAP BDC and the autonomous enterprise](https://news.sap.com/2026/05/sap-bdc-accelerate-autonomous-enterprise/)
