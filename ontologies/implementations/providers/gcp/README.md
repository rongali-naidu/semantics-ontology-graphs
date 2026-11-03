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

Docs: [Expanded semantic model support in Knowledge Catalog (29 Oct 2026)](https://cloud.google.com/blog/products/data-analytics/expanded-semantic-model-support-in-knowledge-catalog)
