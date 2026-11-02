# Apache Ossie retail model

| File | Spec | What it is |
|---|---|---|
| [`retail.semantic_model.yaml`](retail.semantic_model.yaml) | core spec | datasets, fields, relationships, metrics over [`../../warehouse/`](../../warehouse/) |
| [`retail.ontology.yaml`](retail.ontology.yaml) | ontology spec | concepts and relationships, each linked by `iri` to the OWL ontology |
| [`retail.mapping.yaml`](retail.mapping.yaml) | mapping spec | which semantic-model fields populate which ontology concepts/links |

## Pinned spec version

Apache Ossie is in incubation and its spec is a **draft** that may change
before 0.2.0 is released. These files are validated against:

| | |
|---|---|
| Spec version | `0.2.0.dev0` |
| apache/ossie commit | `10116f936e628944eadaa70ec7578caf23912e96` (2026-11-02) |

CI checks out exactly that commit (`OSSIE_COMMIT` in the
[Makefile](../../../../Makefile)). To move to a newer spec: bump the commit,
run `make check-ossie`, fix what breaks, and update this table.

Explanation: [concepts/semantic-modelling/04](../../../../concepts/semantic-modelling/04-open-semantic-formats.md).
