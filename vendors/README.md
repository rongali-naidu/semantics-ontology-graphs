# Vendors: how each platform implements the concepts

The [`concepts/`](../concepts/) are vendor-neutral. Each folder here maps
those concepts onto one vendor's products and implements the **same retail
example** in that vendor's formats.

| Group | Folders |
|---|---|
| Cloud & data platforms | [aws](aws/) · [gcp](gcp/) · [microsoft](microsoft/) · [oracle](oracle/) · [databricks](databricks/) · [snowflake](snowflake/) |
| Semantic-layer tools | [dbt-labs](dbt-labs/) · [atscale](atscale/) · [cube](cube/) |
| Graph databases | [neo4j](neo4j/) (Neptune is under [aws](aws/)) |

## Verification levels

Every vendor README opens with one of these, plus the date it was last reviewed:

| Level | Meaning | Folders |
|---|---|---|
| ✅ **executed** | runs end to end and is checked against the SPARQL answers in CI | dbt-labs |
| 🟡 **checked** | files parse and/or generated data is proven consistent; not run on the vendor's engine | aws (data files), atscale, cube |
| ⚪ **documented** | written to the vendor's documented syntax; not run | gcp, microsoft, databricks, snowflake, neo4j, oracle (design only) |

The vendor-neutral Apache Ossie model
([`examples/retail/semantic-model/ossie/`](../examples/retail/semantic-model/ossie/))
is ✅: validated against the official Ossie schemas in CI, with its metrics
compiled and executed.

## Concept → vendor matrix

Status as of November 2026. Vendor offerings change quickly (several are in
preview), so check each vendor's docs. **This matrix is the only place
product status is tracked**; vendor READMEs link here instead of repeating it.

### Graphs and ontologies

| Concept | [AWS](aws/) | [Google Cloud](gcp/) | [Microsoft](microsoft/) | [Oracle](oracle/) | [Databricks](databricks/) | [Snowflake](snowflake/) | [Neo4j](neo4j/) |
|---|---|---|---|---|---|---|---|
| RDF store + SPARQL | **Neptune** Database | — | — | **RDF Graph** in Oracle Database | — | — | via neosemantics (n10s) |
| Property graph DB | **Neptune** (Gremlin, openCypher) | **Spanner Graph** (GQL) | **Fabric Graph** (GQL); Cosmos DB for Gremlin | **Property graphs** (SQL/PGQ, PGQL) | — (GraphFrames on Spark) | — | **Neo4j** (Cypher) |
| Graph over existing tables | — | **BigQuery Graph**, Spanner Graph | Fabric Graph over OneLake; SQL Server graph tables | SQL/PGQ property graph views (23ai) | — | — | — |
| Graph analytics / algorithms | **Neptune Analytics** | BigQuery / Spanner Graph | Fabric Graph | Graph Server (PGX) | GraphFrames | — | Graph Data Science |
| Ontology / conceptual model | load OWL as RDF into Neptune | Enterprise Knowledge Graph API | **Fabric IQ ontology** (preview); Azure Digital Twins **DTDL** | OWL/RDFS in RDF Graph | Unity Catalog metadata | Ossie ontology | n10s OWL import |
| GraphRAG / AI | Bedrock Knowledge Bases + Neptune Analytics | Vertex AI + Spanner/BigQuery Graph | Fabric IQ + Foundry / Copilot | Oracle AI Vector Search + graphs | Mosaic AI (vector + partners) | Cortex | Neo4j GraphRAG |

### Semantic models (metrics layer)

| Concept | [AWS](aws/) | [Google Cloud](gcp/) | [Microsoft](microsoft/) | [Oracle](oracle/) | [Databricks](databricks/) | [Snowflake](snowflake/) | [dbt Labs](dbt-labs/) | [AtScale](atscale/) | [Cube](cube/) |
|---|---|---|---|---|---|---|---|---|---|
| Semantic model | QuickSight datasets + Topics | **Looker** LookML | **Power BI / Fabric** semantic model | **Oracle Analytics** RPD / Semantic Modeler | **Metric views** | **Semantic views** | **Semantic Layer** (MetricFlow) | **SML** | Cube data model |
| Definition format | API / UI | LookML | TMDL + DAX | RPD (MDS XML) / SMML | YAML 1.1 | SQL DDL / YAML | YAML | YAML (SML) | YAML / JS |
| Model stored in your git repo | — | built in | Fabric Git integration (PBIP) | Semantic Modeler Git integration | via Asset Bundles | via CI | native | native | native |
| Apache Ossie support | — | via converters | Microsoft joined; TMDL converter | — | converter | founding member | converter | supporter | converter |
| Retail example | — | [looker/](gcp/looker/) | [power-bi/](microsoft/power-bi/Retail.SemanticModel/) | [layer mapping](oracle/) | [metric view](databricks/retail_metric_view.sql) | [semantic view](snowflake/retail_semantic_view.sql) | [retail_dbt/](dbt-labs/retail_dbt/) ✅ | [sml/](atscale/sml/) | [model/](cube/model/) |

Where each tool stores its semantic model and how it's promoted:
[concepts/semantic-modelling/03](../concepts/semantic-modelling/03-semantic-model-repositories.md).

## Adding a vendor

See [CONTRIBUTING.md](../CONTRIBUTING.md#adding-a-vendor).
