# Semantic models

The business layer over tables: datasets, dimensions, joins and governed
metrics defined once for every dashboard, notebook and AI agent (semantic
layers, BI models, Apache Ossie).

## Concepts

| # | Chapter |
|---|---|
| 1 | [What is a semantic model?](concepts/01-what-is-a-semantic-model.md) |
| 2 | [How reporting tools do it: Power BI, Looker, Tableau, Qlik...](concepts/02-semantic-models-in-reporting-tools.md) |
| 3 | [Where semantic models live: BI metadata repositories vs git (Oracle Analytics RPD/SMML, Power BI PBIP/TMDL, Looker...)](concepts/03-semantic-model-repositories.md) |
| 4 | [Open formats: Apache Ossie, MetricFlow, SML, Cube, Malloy](concepts/04-open-semantic-formats.md) |
| 5 | [The retail semantic model, end to end](concepts/05-retail-semantic-model.md) |

How semantic models relate to ontologies:
[foundations 3](../foundations/03-semantic-models-and-ontologies.md).

## Implementations

[All products](implementations/README.md): AWS (COA metrics, QuickSight) ·
Google Cloud (Looker) · Microsoft (Power BI / Fabric) · Oracle (Analytics) ·
Snowflake · Databricks · dbt · AtScale · Cube.

## Retail example files

[`warehouse/`](../examples/retail/warehouse/) (star schema, data,
`metrics.sql`) · [`semantic-model/ossie/`](../examples/retail/semantic-model/ossie/)
(Apache Ossie model, ontology, mapping)

Related: [foundations](../foundations/README.md) · [ontologies](../ontologies/README.md) · [graphs](../graphs/README.md)
