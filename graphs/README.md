# Graphs

Storing and querying connected data: property graphs (nodes, edges,
properties) and RDF graphs, graph databases, and the languages that query
them (Cypher, Gremlin, ISO GQL, SQL/PGQ, SPARQL).

## Concepts

| # | Chapter |
|---|---|
| 1 | [Property graphs (and mapping RDF ⇄ property graph)](concepts/01-property-graphs.md) |
| 2 | [Graph databases](concepts/02-graph-databases.md) |
| 3 | [Querying property graphs: Cypher, Gremlin, GQL, SQL/PGQ](concepts/03-querying-property-graphs.md) |
| 4 | [RDBMS vs graph database, and knowledge graph vs property graph](concepts/04-relational-vs-graph.md) |

RDF and SPARQL are covered in the ontologies topic
([SPARQL](../ontologies/concepts/03-querying-rdf-sparql.md)), since RDF is
the knowledge-representation stack.

## Implementations

[All products](implementations/README.md): AWS (Neptune, Neptune Analytics,
COA) · Google Cloud (Spanner Graph, BigQuery Graph) · Microsoft (Fabric Graph,
Cosmos DB) · Oracle (property graphs) · Snowflake (KG tables) · Databricks
(GraphFrames, OntoBricks) · SAP (HANA Cloud) · Neo4j.

## Retail example files

[`property-graph/`](../examples/retail/property-graph/) (Cypher, Gremlin,
GQL, SQL/PGQ) · [Neptune load files](implementations/providers/aws/)

Related: [foundations](../foundations/README.md) · [ontologies](../ontologies/README.md) · [semantic models](../semantic-models/README.md)
