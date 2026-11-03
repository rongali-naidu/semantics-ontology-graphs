# Ontologies: implementations

Products for authoring, storing, reasoning over and serving ontologies,
each related to the retail ontology
([`retail-ontology.ttl`](../../examples/retail/ontology/retail-ontology.ttl)).
**Status** is as of November 2026 (details and sources on each page).
Verification levels: [legend](../../README.md#verification-levels).


## Providers

| Provider | Product | Kind | What it does for ontologies | Status | Verified |
|---|---|---|---|---|---|
| [AWS](providers/aws/README.md) | **Context Ontology Accelerator (COA)** | formal (OWL) | LLM-induced OWL ontologies + R2RML, grounding (FIBO, schema.org), expert approval, HermiT/ELK reasoning, MCP serving | open source, v0.3.x | ⚪ |
| [AWS](providers/aws/README.md#amazon-neptune-as-an-ontology-store) | **Amazon Neptune** | RDF store | stores OWL + data, SPARQL; no reasoner | GA | 🟡 load files |
| [Google Cloud](providers/gcp/README.md) | **Knowledge Catalog** context graph · Knowledge Engine | context graph | graph of tables, semantic models, glossary; ingests LookML, MetricFlow, Snowflake, Databricks, SAP CSN | ingestion GA (Oct 2026); Knowledge Studio preview | ⚪ |
| [Microsoft](providers/microsoft/README.md) | **Fabric IQ ontology** · Azure Digital Twins **DTDL** | business ontology · twin models | entity types bound to OneLake and Power BI models; JSON-LD twin models | Fabric IQ GA (Jun 2026), ontology item preview; DTDL v3 GA | ⚪ |
| [Oracle](providers/oracle/README.md) | **Oracle RDF Graph** (AI Database 26ai) | formal (RDF/OWL) | RDF graphs, SPARQL 1.1, RDFS/OWL-subset inferred graphs, `SEM_SQL` | GA | ⚪ |
| [Snowflake](providers/snowflake/README.md) | **Ontology on Snowflake** · RelationalAI | ontology in tables | `ONT_*` metadata + `KG_NODE`/`KG_EDGE`, Cortex Agent; RelationalAI reasoning | Labs sample · partner app | ⚪ |
| [Databricks](providers/databricks/README.md) | **Genie Ontology** · **OntoBricks** | learned context · formal (OWL) | learned context from Unity Catalog + usage · OWL/R2RML/SHACL/SWRL app | public preview · Labs (as-is) | ⚪ |
| [SAP](providers/sap/README.md) | **SAP Knowledge Graph** · HANA Cloud knowledge graph engine | pre-built domain ontology · RDF store | business semantics for Joule · RDF + SPARQL | announced May 2026 · see SAP docs | ⚪ |
| [Palantir](providers/palantir/README.md) | **Foundry Ontology** | operational | object, link and **action** types driving apps and agents | GA | ⚪ |

## Tools

| Tool | What it does for ontologies | Verified |
|---|---|---|
| [Neo4j neosemantics (n10s)](tools/neo4j-neosemantics/README.md) | OWL/RDF import into Neo4j, subclass inference, SHACL validation | ⚪ |
| Apache Ossie ontology spec | vendor-neutral ontology + mapping to semantic models; [retail version](../../examples/retail/semantic-model/ossie/retail.ontology.yaml) | ✅ |
| rdflib · pySHACL · owlrl (Python) | parse, validate and reason over the retail ontology in CI | ✅ |

Planned (see [ROADMAP](../../ROADMAP.md)): Protégé, Ontotext GraphDB, Stardog,
TopBraid, Apache Jena, RelationalAI.
