# Oracle: ontologies

> **Verification:** ⚪ documented; no Oracle-specific example file yet.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for ontologies | Retail example |
|---|---|---|
| **Oracle RDF Graph** (in Oracle Database) | RDF/OWL store with SPARQL; RDFS and OWL rule-based inference; graph shares the database's security and SQL access | load [`retail-ontology.ttl`](../../../../examples/retail/ontology/retail-ontology.ttl) + [`retail-data.ttl`](../../../../examples/retail/rdf/retail-data.ttl), run the [SPARQL queries](../../../../examples/retail/sparql/) |

Oracle also appears in
[graphs (property graphs, PGX)](../../../../graphs/implementations/providers/oracle/README.md) and
[semantic models (Oracle Analytics RPD / Semantic Modeler)](../../../../semantic-models/implementations/providers/oracle/README.md).

## How the concepts map

* Ontology and data are loaded as RDF triples (Turtle / N-Triples), so the
  files under [`examples/retail/rdf/`](../../../../examples/retail/rdf/) apply as is.
* Unlike Neptune, Oracle RDF Graph can compute **entailments** (RDFS, OWL
  profiles) inside the database, so `?c a retail:Customer` can return
  PremiumCustomers without the `rdfs:subClassOf*` path trick.
* Relational data can be exposed as RDF through **RDF views** (R2RML-style
  mappings), the same idea as COA's virtual knowledge graph and Ossie mappings.

* **Oracle AI Database 26ai renamed the concepts:** a "semantic model" is
  now an **RDF graph** and an "entailment" is now an **inferred graph**. 26ai
  adds new `SEM_APIS` subprograms, 32K `VARCHAR` RDF values, and a
  `SEM_SQL` SQL macro for querying RDF from SQL.
* RDF graphs support **SPARQL 1.1** with RDF, RDFS and a subset of **OWL**,
  plus GraphRAG and vector search in the same database; samples live in
  [oracle-samples/oracle-graph](https://github.com/oracle-samples/oracle-graph) (`rdf/`, `knowledge-graph/`).

A worked Oracle example is on the [roadmap](../../../../ROADMAP.md).

Docs: [Oracle Database graph (RDF)](https://docs.oracle.com/en/database/oracle/property-graph/)
