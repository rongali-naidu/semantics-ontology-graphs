# Microsoft: ontologies

> **Verification:** ⚪ documented. The DTDL file is valid JSON written to the DTDL v3 spec; nothing was run in Fabric or Azure.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for ontologies | Retail example |
|---|---|---|
| **Fabric IQ ontology** | business entity types, relationships and rules bound to OneLake data and Power BI semantic models; routes questions to semantic models (DAX), Fabric Graph (GQL) or event data (KQL) for agents | conceptually = [`retail-ontology.ttl`](../../../../examples/retail/ontology/retail-ontology.ttl) / [Ossie ontology](../../../../examples/retail/semantic-model/ossie/retail.ontology.yaml) |
| **Azure Digital Twins: DTDL v3** | JSON-LD-based modelling language for twins (interfaces, properties, relationships) | [`digital-twins-dtdl/retail-ontology.json`](digital-twins-dtdl/retail-ontology.json) |

Microsoft also appears in
[graphs (Fabric Graph, Cosmos DB for Gremlin)](../../../../graphs/implementations/providers/microsoft/README.md) and
[semantic models (Power BI / Fabric)](../../../../semantic-models/implementations/providers/microsoft/README.md).

## Overview

* **Fabric IQ** is a workload in Microsoft Fabric. The ontology is an **item in a Fabric workspace**, authored in Fabric rather than exchanged as a file.
* **How you build it:** define entity types, properties and relationships, or generate a draft from a Power BI semantic model. Then bind them to OneLake tables, semantic models and Eventhouse data.
* **How it answers:** the ontology routes each question to the right engine: metrics to the semantic model (DAX), relationships to Fabric Graph (GQL), events to Eventhouse (KQL). Fabric data agents and Copilot use it.
* **DTDL** is a JSON-LD modelling language for **Azure Digital Twins**. You upload model files to a Digital Twins instance, then create twins (instances) and relationships and query them with the Digital Twins query language.
* **Status (Nov 2026):** Fabric IQ GA since June 2026, but the ontology item was still labelled preview in October 2026. DTDL v3 is GA.

## How the concepts map

| OWL ([ontologies concepts 1](../../../concepts/01-what-is-an-ontology.md)) | DTDL v3 | Fabric IQ ontology |
|---|---|---|
| `owl:Class` | `Interface` | entity type |
| `rdfs:subClassOf` | `extends` | — |
| datatype property | `Property` with a `schema` | property bound to a column |
| object property | `Relationship` (with `target`, `maxMultiplicity`) | relationship |
| reified relation (`OrderLine`) | relationship **with properties** (`quantity`, `unitPrice`) | relationship bound to a table |
| enumerated values | `Enum` schema | — |
| global identifier (IRI) | DTMI (`dtmi:example:retail:Order;1`, versioned) | item in the Fabric workspace |

## Fabric IQ ontology in practice

* **Generate from a semantic model:** Fabric IQ can draft an ontology from a
  Power BI semantic model: tables become **entity types**, columns become
  **properties**, model relationships become **relationships**. The draft
  still needs review and business context.
* **Bind, don't replace:** the ontology sits alongside the semantic model.
  Metrics stay as the model's DAX measures, and entity types bind to OneLake
  tables, semantic models and Eventhouse data.
* **Status:** the Fabric IQ workload was announced generally available in
  June 2026, but the **ontology item was still labelled preview** in
  Microsoft's documentation as of October 2026. Reported current
  limitations include Direct Lake models only, data already in OneLake,
  mostly manual modelling, and no native ontology versioning. Check
  Microsoft Learn before relying on these.
* For the retail model, generating from
  [`Retail.SemanticModel`](../../../../semantic-models/implementations/providers/microsoft/power-bi/Retail.SemanticModel/)
  would yield Order Lines, Orders, Customers, Products, Categories and Reviews
  entity types. Compare that with the hand-written OWL ontology: the subclass
  (`PremiumCustomer`), the transitive category tree and the cardinality
  rules would have to be added by hand.

DTDL is aimed at digital twins (IoT, buildings, supply chains), but it's
Microsoft's only *textual* ontology language, so the retail ontology is
expressed in it here. Fabric IQ's ontology is authored in Fabric and bound to
data rather than exchanged as a file.

## Product documentation

* [Microsoft Fabric documentation](https://learn.microsoft.com/fabric/): Fabric IQ, ontology item, data agents
* [DTDL v3 specification](https://github.com/Azure/opendigitaltwins-dtdl/blob/master/DTDL/v3/DTDL.v3.md): the modelling language
* [Azure Digital Twins overview](https://learn.microsoft.com/azure/digital-twins/overview): the service that runs DTDL models
* [Azure Digital Twins models](https://learn.microsoft.com/azure/digital-twins/concepts-models): writing and uploading DTDL models
