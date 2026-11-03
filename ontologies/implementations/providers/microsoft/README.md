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

DTDL is aimed at digital twins (IoT, buildings, supply chains), but it's
Microsoft's only *textual* ontology language, so the retail ontology is
expressed in it here. Fabric IQ's ontology is authored in Fabric and bound to
data rather than exchanged as a file.

Docs: [DTDL v3](https://github.com/Azure/opendigitaltwins-dtdl/blob/master/DTDL/v3/DTDL.v3.md) ·
[Microsoft Fabric docs (IQ)](https://learn.microsoft.com/fabric/)
