# Semantic models: implementations

Semantic layers and BI semantic models, each encoding the same retail
metrics ([`metrics.sql`](../../examples/retail/warehouse/metrics.sql)).
Status as of November 2026; product status is tracked only in these tables.
Verification levels: [legend](../../README.md#verification-levels).

## Providers

| Provider | Product | Format | Model in your git repo | Apache Ossie | Verified |
|---|---|---|---|---|---|
| [AWS](providers/aws/README.md) | **COA metric service** · QuickSight datasets + Topics | JSON (API) · UI/API | via API files | — | 🟡 COA metrics run in CI |
| [Google Cloud](providers/gcp/README.md) | **Looker** | LookML | built in | converters | ⚪ |
| [Microsoft](providers/microsoft/README.md) | **Power BI / Fabric semantic model** | TMDL + DAX (PBIP) | Fabric Git integration | Microsoft joined; TMDL converter | ⚪ |
| [Oracle](providers/oracle/README.md) | **Oracle Analytics** RPD / Semantic Modeler | RPD (MDS XML) / SMML | Semantic Modeler Git integration | — | ⚪ design only |
| [Snowflake](providers/snowflake/README.md) | **Semantic views** (+ Cortex Analyst) | SQL DDL / YAML | via CI | founding member | ⚪ |
| [Databricks](providers/databricks/README.md) | **Metric views** (+ Genie) | YAML 1.1 | via Asset Bundles | converter | ⚪ |

## Tools

| Tool | Format | Model in your git repo | Apache Ossie | Verified |
|---|---|---|---|---|
| [dbt Semantic Layer (MetricFlow)](tools/dbt/README.md) | YAML | native | converter | ✅ executed in CI |
| [AtScale](tools/atscale/README.md) | SML (YAML) | native | supporter | 🟡 |
| [Cube](tools/cube/README.md) | YAML / JS | native | converter | 🟡 |
| Apache Ossie (vendor-neutral) | YAML / JSON | native | — | ✅ [retail model](../../examples/retail/semantic-model/ossie/) |

Where each tool stores its model and how it's promoted:
[semantic models concepts 3](../concepts/03-semantic-model-repositories.md).
Planned: Tableau, Qlik, ThoughtSpot, MicroStrategy, Omni, Lightdash.
