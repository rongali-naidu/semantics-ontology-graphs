# Google Cloud: ontologies

> **Verification:** ⚪ documented from Google's announcements; nothing run on Google Cloud.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for ontologies | Retail example |
|---|---|---|
| **Knowledge Catalog** (formerly Dataplex Universal Catalog) | a **context graph** of the business: tables, semantic models, glossary terms and data products as nodes; lineage, joins and associations as edges; grounds Gemini and custom agents | the retail tables + the [Looker model](../../../../semantic-models/implementations/providers/gcp/looker/) would become nodes |
| **Knowledge Engine** (announced at Next '26) | Gemini-driven enrichment: tagging, definitions, relationship mapping | — |
| Enterprise Knowledge Graph API | entity reconciliation against Google's Knowledge Graph | — |

Google Cloud also appears in
[graphs (Spanner Graph, BigQuery Graph)](../../../../graphs/implementations/providers/gcp/README.md) and
[semantic models (Looker, Knowledge Catalog ingestion)](../../../../semantic-models/implementations/providers/gcp/README.md).

## Overview

* **There is no standalone ontology product.** **Knowledge Catalog** (formerly Dataplex Universal Catalog) builds a *context graph* from metadata you already have.
* **How it works:** the catalog harvests data assets (BigQuery tables and others) and ingests semantic models: LookML, dbt MetricFlow, Snowflake semantic views, Databricks metric views, SAP CSN and BigQuery Graph. It links business-glossary terms to tables and columns. **Knowledge Engine** uses Gemini to add tags, definitions and relationships.
* **Where the model lives:** as managed catalog entries in your Google Cloud project, with no OWL file to export.
* **How agents use it:** Gemini and custom agents ground their answers on the context graph.
* **Status (Nov 2026):** semantic-model ingestion GA (Oct 2026); Knowledge Studio in preview.

## How the concepts map

Google's ontology story is a **context graph assembled from existing
semantic models**, not a standalone OWL ontology:

| Ontology concept ([concepts 1](../../../concepts/01-what-is-an-ontology.md)) | In Knowledge Catalog |
|---|---|
| shared vocabulary | business glossary terms linked to tables and columns |
| classes / relationships | entities and join paths taken from LookML, MetricFlow, Snowflake semantic views, Databricks metric views, SAP CSN, BigQuery Graph |
| competing definitions | kept side by side, labelled by source, for stewards to reconcile |
| formal axioms, reasoning | none: no OWL, no reasoner |
| global identifiers | catalog entries (not IRIs) |

For a formal ontology on Google Cloud, keep the OWL file (e.g.
[`retail-ontology.ttl`](../../../../examples/retail/ontology/retail-ontology.ttl))
and run an RDF store yourself (Jena, GraphDB, Oxigraph on GKE), or map it
onto Spanner Graph / BigQuery Graph as a property graph.

## Product documentation

* [Expanded semantic model support in Knowledge Catalog (29 Oct 2026)](https://cloud.google.com/blog/products/data-analytics/expanded-semantic-model-support-in-knowledge-catalog): which semantic models are ingested, and how
* [Catalog overview](https://cloud.google.com/dataplex/docs/catalog-overview): entries, aspects, search, lineage
* [Business glossary](https://cloud.google.com/dataplex/docs/business-glossary-overview): terms linked to tables and columns
* [Enterprise Knowledge Graph](https://cloud.google.com/enterprise-knowledge-graph/docs/overview): entity reconciliation
