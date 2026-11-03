# SAP: ontologies

> **Verification:** ⚪ documented from SAP announcements and learning material; nothing run on SAP.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for ontologies | Retail example |
|---|---|---|
| **SAP Knowledge Graph** (SAP Business AI Platform) | the semantic layer that maps SAP business entities, processes and relationships for Joule agents; announced at Sapphire 2026 as covering hundreds of thousands of SAP tables | — |
| **SAP HANA Cloud knowledge graph engine** | RDF triple store inside HANA Cloud: SPARQL, SPARQL embedded in SQL, RDF import/export (Turtle, JSON-LD...) | load [`retail-ontology.ttl`](../../../../examples/retail/ontology/retail-ontology.ttl) + [`retail-data.ttl`](../../../../examples/retail/rdf/retail-data.ttl); run the [SPARQL queries](../../../../examples/retail/sparql/) |

SAP also appears in
[graphs (HANA Cloud)](../../../../graphs/implementations/providers/sap/README.md) and
[semantic models (Datasphere / Business Data Cloud, CSN)](../../../../semantic-models/implementations/providers/sap/README.md).

## How the concepts map

* **SAP Knowledge Graph** is SAP's *pre-built* domain ontology for its own
  applications: customers don't model "Sales Order" or "Customer" from scratch.
  Treat it as a large domain ontology, like FIBO for finance.
* **HANA Cloud knowledge graph engine** is a standards-based RDF store, so
  the retail ontology and data load as Turtle and the SPARQL files apply.
  Check SAP's docs for reasoning support and for which SPARQL 1.1 features apply.
* SAP business data also carries semantics in **CSN** (Core Schema
  Notation), which Google's Knowledge Catalog and others ingest.

Docs: [SAP Sapphire 2026 announcement](https://news.sap.com/2026/05/sap-sapphire-sap-unveils-autonomous-enterprise/) ·
[HANA Cloud knowledge graph engine (SAP Learning)](https://learning.sap.com/courses/prd-hc-introduction/k-graph)
