# SAP: graphs

> **Verification:** ⚪ documented from SAP learning material; nothing run on SAP.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for graphs | Retail example |
|---|---|---|
| **SAP HANA Cloud knowledge graph engine** | RDF triple store with SPARQL inside HANA Cloud (needs the triple-store feature enabled); SPARQL from SQL and SQL from SPARQL | the [RDF files](../../../../examples/retail/rdf/) + [SPARQL queries](../../../../examples/retail/sparql/) |
| **SAP HANA graph engine** | property graphs over HANA tables (graph workspaces) | — |
| LangChain integration | `SAP HANA RDF graph` connector for SPARQL-backed LLM apps | — |

SAP also appears in
[ontologies (SAP Knowledge Graph)](../../../../ontologies/implementations/providers/sap/README.md) and
[semantic models (Datasphere / Business Data Cloud)](../../../../semantic-models/implementations/providers/sap/README.md).

## How the concepts map

Because the knowledge graph engine speaks RDF and SPARQL, it plays the same
role as Neptune's RDF side or Oracle RDF Graph: load
[`retail-data.ttl`](../../../../examples/retail/rdf/retail-data.ttl) and
the ontology, then run the repo's `.rq` files. Check SAP's docs for reasoning
and SPARQL 1.1 coverage.

Docs: [HANA Cloud knowledge graph engine (SAP Learning)](https://learning.sap.com/courses/prd-hc-introduction/k-graph) ·
[LangChain: SAP HANA RDF graph](https://docs.langchain.com/oss/python/integrations/graphs/sap_hana_rdf_graph)
