# Ontologies

What exists in a domain, what it's called, how things relate, and which
rules always hold: written down formally so machines can share and reason
over it (OWL, RDFS, SKOS, SHACL, RDF, SPARQL).

## Concepts

| # | Chapter |
|---|---|
| 1 | [What is an ontology?](concepts/01-what-is-an-ontology.md) |
| 2 | [Documenting an ontology: RDFS, OWL, SKOS, SHACL; Turtle, JSON-LD, RDF/XML, Manchester...](concepts/02-documenting-ontologies.md) |
| 3 | [Querying ontologies and RDF knowledge graphs with SPARQL](concepts/03-querying-rdf-sparql.md) |
| 4 | [The retail ordering example, end to end](concepts/04-retail-example.md) |
| 5 | [Ontologies for software engineers: from OOP to OWL (primitive vs defined classes)](concepts/05-ontology-for-software-engineers.md) |
| 6 | [Properties, restrictions and axioms (TBox, RBox, ABox; functional; transitive…)](concepts/06-properties-restrictions-axioms.md) |
| 7 | [Mapping an ontology to tables and columns (R2RML, OBDA, ETL, LLM, COA)](concepts/07-mapping-ontology-to-tables.md) |

## Implementations

[All products](implementations/README.md): AWS (Context Ontology Accelerator,
Neptune) · Google Cloud (Knowledge Catalog) · Microsoft (Fabric IQ, DTDL) ·
Oracle (RDF Graph) · Snowflake · Databricks (Genie Ontology, OntoBricks) ·
SAP (Knowledge Graph) · Palantir (Foundry Ontology) · Neo4j neosemantics.

## Retail example files

[`ontology/`](../examples/retail/ontology/) (OWL + SHACL) ·
[`rdf/`](../examples/retail/rdf/) (data in 6 formats) ·
[`sparql/`](../examples/retail/sparql/) (13 queries/updates) ·
[`mapping/`](../examples/retail/mapping/) (R2RML, verified) ·
[Ossie ontology](../examples/retail/semantic-model/ossie/retail.ontology.yaml)

Related: [foundations](../foundations/README.md) · [graphs](../graphs/README.md) · [semantic models](../semantic-models/README.md)
