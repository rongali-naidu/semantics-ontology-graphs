# Databricks: ontologies

> **Verification:** ⚪ documented; nothing run on Databricks.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for ontologies | Retail example |
|---|---|---|
| **Genie Ontology** | a continuously learned **context layer** for Genie agents, built from Unity Catalog semantics (glossary terms, domains, metric views, certification) plus "snippets" mined from lineage and query history, ranked by OntoRank | — |
| **OntoBricks** (Databricks Labs) | standards-based ontology app: design or import **OWL/RDFS** (FIBO, CDISC, HL7 FHIR...), map to Unity Catalog tables with **R2RML**, materialize triples, reason (**OWL 2 RL, SWRL, SHACL**), query with SPARQL / GraphQL / MCP | import [`retail-ontology.ttl`](../../../../examples/retail/ontology/retail-ontology.ttl), map to [`warehouse/`](../../../../examples/retail/warehouse/) |

Databricks also appears in
[graphs (GraphFrames, OntoBricks triple store)](../../../../graphs/implementations/providers/databricks/README.md) and
[semantic models (metric views)](../../../../semantic-models/implementations/providers/databricks/README.md).

## Overview

* **Genie Ontology** is **built automatically** for Genie from Unity Catalog metadata (glossary terms, domains, metric views, certifications) and from usage (lineage, query history). There is nothing to author. You steer it by certifying metric views and curating terms. Public preview (2026).
* **OntoBricks** (Databricks Labs) is an **app you deploy in your workspace**:
  * design or import OWL;
  * map it to Unity Catalog tables with R2RML;
  * materialize triples (Lakebase/Postgres by default, Delta tables or Neo4j);
  * reason with OWL 2 RL, SWRL and SHACL;
  * query with SPARQL, GraphQL or MCP.
* OntoBricks is v0.9.x, provided as-is.
* **Both rely on Unity Catalog** for permissions and lineage on the underlying tables.

## Two different ideas of "ontology"

| | Genie Ontology | OntoBricks |
|---|---|---|
| Source of meaning | **learned** from metadata and usage, plus governed semantics | **designed** by people (OWL), optionally drafted by an LLM |
| Standards | none exposed (no OWL / RDF) | OWL, RDFS, R2RML, SPARQL, SHACL, SWRL |
| Reasoning | ranking of definitions (OntoRank) | OWL 2 RL inference, SWRL rules, SHACL validation |
| Best for | grounding natural-language analytics | regulated domains, explicit rules, interoperability |
| Status | public preview (2026) | Databricks Labs, v0.9.x, provided as-is without formal support; Databricks License (source-available) |

OntoBricks is the closest Databricks counterpart to the
[AWS Context Ontology Accelerator](../aws/README.md#aws-context-ontology-accelerator-coa):
both pair OWL + R2RML with LLM-assisted modelling and MCP serving.

## Product documentation

* [databrickslabs/ontobricks](https://github.com/databrickslabs/ontobricks): install, modelling, mapping, reasoning
* [Genie (AI/BI)](https://docs.databricks.com/aws/en/genie/): Genie spaces and agents
* [AI/BI and Genie release notes 2026](https://docs.databricks.com/aws/en/ai-bi/release-notes/2026): Genie Ontology preview
* [Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/): governance, metadata, lineage
