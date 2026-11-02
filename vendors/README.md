# Vendors: how each platform implements the concepts

The [`concepts/`](../concepts/) are vendor-neutral. Each folder here maps
those concepts onto one vendor's products and implements the **same retail
example** in that vendor's formats.

## Concept → vendor matrix

Status as of November 2026. Vendor offerings change quickly (several are in
preview), so check each vendor's docs.

### Graphs and ontologies

| Concept | [AWS](aws/) | [Google Cloud](gcp/) | [Microsoft](microsoft/) | [Databricks](databricks/) | [Snowflake](snowflake/) | [Neo4j](neo4j/) |
|---|---|---|---|---|---|---|
| RDF store + SPARQL | **Neptune** Database | — | — | — | — | via neosemantics (n10s) |
| Property graph DB | **Neptune** (Gremlin, openCypher) | **Spanner Graph** (GQL) | **Fabric Graph** (GQL); Cosmos DB for Gremlin | — (GraphFrames on Spark) | — | **Neo4j** (Cypher) |
| Graph over existing tables (SQL/PGQ-style) | — | **BigQuery Graph**, Spanner Graph | Fabric Graph over OneLake; SQL Server graph tables | metric views (not graph) | — | — |
| Graph analytics / algorithms | **Neptune Analytics** | BigQuery / Spanner Graph | Fabric Graph | GraphFrames | — | Graph Data Science |
| Ontology / conceptual model | load OWL as RDF into Neptune | Enterprise Knowledge Graph API | **Fabric IQ ontology** (preview); Azure Digital Twins **DTDL** | Unity Catalog metadata | Ossie ontology | n10s OWL import |
| GraphRAG / AI | Bedrock Knowledge Bases + Neptune Analytics | Vertex AI + Spanner/BigQuery Graph | Fabric IQ + Foundry / Copilot | Mosaic AI (vector + partners) | Cortex | Neo4j GraphRAG |

### Semantic models (metrics layer)

| Concept | [AWS](aws/) | [Google Cloud](gcp/) | [Microsoft](microsoft/) | [Databricks](databricks/) | [Snowflake](snowflake/) | [dbt Labs](dbt-labs/) | [AtScale](atscale/) | [Cube](cube/) |
|---|---|---|---|---|---|---|---|---|
| Semantic model | QuickSight datasets + Topics | **Looker** LookML | **Power BI / Fabric** semantic model | **Metric views** | **Semantic views** | **Semantic Layer** (MetricFlow) | **SML** | Cube data model |
| Definition format | API / UI | LookML | TMDL + DAX | YAML 1.1 | SQL DDL / YAML | YAML | YAML (SML) | YAML / JS |
| Apache Ossie support | — | via converters | Microsoft joined; TMDL converter | converter | founding member | converter | supporter | converter |
| Retail example | — | [looker/](gcp/looker/) | [power-bi/](microsoft/power-bi/Retail.SemanticModel/definition/) | [metric view](databricks/retail_metric_view.sql) | [semantic view](snowflake/retail_semantic_view.sql) | [retail_dbt/](dbt-labs/retail_dbt/) ✅ | [sml/](atscale/sml/) | [model/](cube/model/) |

✅ = executed end-to-end in this repo. The vendor-neutral Apache Ossie model
([`examples/retail/semantic-model/ossie/`](../examples/retail/semantic-model/ossie/))
is validated against the official Ossie schemas and executed.

## Folder template

Each vendor folder has:

* `README.md`: which products cover which concepts, links to docs, and
  the example files with how they map back to the generic ones.
* The retail example in the vendor's formats, using the shared warehouse
  tables ([`examples/retail/warehouse/`](../examples/retail/warehouse/)) or
  graph files.

To add a vendor, copy the structure of an existing folder and add a column to
the matrix above.
