# Ontologies: implementations

Products for authoring, storing, reasoning over and serving ontologies,
each implementing the retail ontology
([`retail-ontology.ttl`](../../examples/retail/ontology/retail-ontology.ttl)).
Status as of November 2026; product status is tracked only in these tables.
Verification levels: [legend](../../README.md#verification-levels).

## Providers

| Provider | Product | What it does for ontologies | Verified |
|---|---|---|---|
| [AWS](providers/aws/README.md) | **Context Ontology Accelerator (COA)** | LLM-induced OWL ontologies, grounding (FIBO, schema.org), expert approval, HermiT/ELK reasoning, MCP serving to agents; open source | ⚪ |
| [AWS](providers/aws/README.md#amazon-neptune-as-an-ontology-store) | **Amazon Neptune** | RDF/OWL store, SPARQL; no reasoner | 🟡 load files |
| [Microsoft](providers/microsoft/README.md) | **Fabric IQ ontology** · **Azure Digital Twins DTDL** | business ontology bound to Fabric data and semantic models · JSON-LD twin models | ⚪ |
| [Oracle](providers/oracle/README.md) | **Oracle RDF Graph** | RDF/OWL in Oracle Database with in-database entailment | ⚪ |

## Tools

| Tool | What it does for ontologies | Verified |
|---|---|---|
| [Neo4j neosemantics (n10s)](tools/neo4j-neosemantics/README.md) | OWL/RDF import into Neo4j, subclass inference, SHACL validation | ⚪ |
| Apache Ossie ontology spec | vendor-neutral ontology + mapping to semantic models; [retail version](../../examples/retail/semantic-model/ossie/retail.ontology.yaml) | ✅ |
| rdflib · pySHACL · owlrl (Python) | parse, validate and reason over the retail ontology in CI | ✅ |

Planned (see [ROADMAP](../../ROADMAP.md)): Protégé, Ontotext GraphDB, Stardog,
TopBraid, Apache Jena, Palantir Ontology, RelationalAI.
