# AWS: semantic models

> **Verification:** 🟡 checked. Every metric in [`coa-retail-metrics.json`](coa-retail-metrics.json) is run on the warehouse in CI and matches the SPARQL answers, and its fields follow COA's API model, but it was not loaded into a COA deployment. QuickSight is described only.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for semantic models | Retail example |
|---|---|---|
| **AWS Context Ontology Accelerator (COA)**: metric service | Governed, named **Tier-1 metrics** (SQL per dialect + synonyms + links to ontology concepts) that agents resolve before anything else | [`coa-retail-metrics.json`](coa-retail-metrics.json) |
| **Amazon QuickSight** | BI datasets (joins, calculated fields) and **Topics**, the natural-language layer used by Amazon Q in QuickSight | description below |

AWS has no open semantic-layer format of its own; dbt, Cube or AtScale over
Amazon Redshift or Athena are common choices
([tools](../../tools/)). AWS also appears in the other topics:
[COA and Neptune for ontologies](../../../../ontologies/implementations/providers/aws/README.md),
[Neptune as a graph database](../../../../graphs/implementations/providers/aws/README.md).

---

## COA metrics (Tier 1)

COA ([what it is](../../../../ontologies/implementations/providers/aws/README.md#aws-context-ontology-accelerator-coa))
answers a question in tiers, most precise first:

| Tier | Uses | Answers |
|---|---|---|
| **1. Metric** | a governed metric definition | "What was revenue?": the registered SQL, identical for every caller |
| **2. Ontology** | the ontology + R2RML mappings (VKG: NL → SPARQL → SQL via Ontop), or NL-to-SQL over the catalog | ad-hoc questions: "revenue from premium customers in Electronics" |
| **3. Documents** | vector search + graph traversal + LLM synthesis | "why": policies, rationale, procedures |

COA's guidance on what goes where matches this repo's split: **metric** for
reusable governed calculations, **ontology** for concepts and relationships,
**documents** for prose
([foundations 3](../../../../foundations/03-semantic-models-and-ontologies.md)
makes the same argument).

### A COA metric, field by field

| COA field | Meaning | Ossie / generic equivalent |
|---|---|---|
| `name`, `label`, `description` | identity and display name | metric `name`, description |
| `expression.dialects[]` | complete read-only SQL per engine (`TRINO`, `POSTGRESQL`, `REDSHIFT`, `SNOWFLAKE`, `DATABRICKS`, `MYSQL`) | Ossie `expression.dialects` |
| `dataSourceId`, `sourceTable` | the **one** source table the metric aggregates | dataset |
| `defaultTimeGrain`, `unit`, `returnType` | presentation | datatype, format |
| `aiContext.synonyms / instructions / examples` | for agents to find and apply the metric | Ossie `ai_context` |
| `ontologyConcepts` | **IRIs of ontology concepts** the metric is about | Ossie mapping / `iri` |

`ontologyConcepts` is a direct bridge between the buckets: the retail
metrics point at the OWL terms in
[`retail-ontology.ttl`](../../../../examples/retail/ontology/retail-ontology.ttl)
(e.g. `revenue` → `retail:OrderLine`, `retail:unitPrice`, `retail:quantity`),
and CI checks that every IRI exists.

### Constraints compared with other semantic layers

* A metric binds to a **single source table**, so `discount_amount` (which
  needs `products.list_price`) isn't a Tier-1 metric. COA's answer is to let
  Tier 2 build that query from the ontology.
* A question with qualifiers ("by month", "for premium customers") falls
  through to Tier 2 unless the dimensions are passed explicitly. Tier 2
  still receives the metric's definition.
* There are no joins, dimensions or hierarchies as in LookML or Power BI.
  Those live in the ontology and its mappings instead.

### Registering the retail metrics

Each object in `metrics` is one `CreateMetric` body:

```bash
# after authenticating (COA uses OIDC tokens on behalf of a user)
jq -c '.metrics[]' coa-retail-metrics.json | while read -r m; do
  curl -sS -X POST "$COA_API/namespaces/$NAMESPACE_ID/metrics" \
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' -d "$m"
done
```

Agents then use the MCP tools `list_metrics` and `query`.

---

## Amazon QuickSight

* **Datasets** hold joins, calculated fields and row-level security, so they
  are QuickSight's semantic model, managed in the QuickSight service (API /
  asset bundles for promotion, no text format in git).
* **Topics** add business names, synonyms and semantic types on top of
  datasets so **Amazon Q in QuickSight** can answer natural-language
  questions. This plays the same role as Ossie `ai_context` or COA `aiContext`.
* For the retail model: one dataset joining `order_lines` → `orders` →
  `customers`, `products` → `categories`, with calculated field
  `line_amount = quantity * unit_price` and a Topic declaring `revenue`,
  `order_count`, `average_order_value` with synonyms.

Docs: [COA metrics](https://github.com/aws/context-ontology-accelerator/blob/main/external-docs/content/metrics.md) ·
[COA serving tiers](https://github.com/aws/context-ontology-accelerator/blob/main/external-docs/content/serve.md) ·
[Amazon QuickSight](https://docs.aws.amazon.com/quicksight/)
