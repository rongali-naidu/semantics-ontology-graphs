# 3. Open semantic formats: Apache Ossie and friends

For thirty years every semantic model was locked inside the tool that
defined it. Moving from Looker to Power BI meant rewriting every metric.
Open formats aim to make the semantic model **portable**.

## 3.1 The landscape

| Format | Owner / license | Scope | Notes |
|---|---|---|---|
| **Apache Ossie** (formerly Open Semantic Interchange, OSI) | Apache Software Foundation (incubating), Apache 2.0 | semantic model **+ ontology + mapping** | Vendor-neutral interchange; converters for 20+ tools |
| **dbt MetricFlow** YAML | dbt Labs, open source | semantic models + metrics | The dbt Semantic Layer engine; also an Ossie converter target |
| **AtScale SML** | AtScale, Apache 2.0 | full OLAP-style model (dimensions, hierarchies, calcs, security) | https://github.com/semanticdatalayer/sml |
| **Cube** data model | Cube, Apache 2.0 (core) | cubes, views, joins, pre-aggregations | YAML / JS |
| **Malloy** | open source (originally Google) | a semantic modelling + query *language* | https://www.malloydata.dev/ |
| **LookML** | Google, proprietary but text | views, explores, measures | De-facto standard for model-as-code |
| **TMDL** | Microsoft, documented text format | Power BI / Analysis Services tabular models | Text serialization of the Tabular Object Model |
| **Snowflake semantic view YAML** | Snowflake | tables, facts, dimensions, metrics | Also the Cortex Analyst semantic-model format |
| **Databricks metric view YAML** | Databricks | source, joins, dimensions, measures | Unity Catalog |

## 3.2 Apache Ossie in depth

**What:** a vendor-neutral, YAML/JSON specification for exchanging semantic
metadata across BI, analytics and AI tools.
**Where:** https://github.com/apache/ossie · site https://ossie.apache.org/ ·
converters https://github.com/apache/ossie-converters
**Status (Nov 2026):** core spec `0.2.0.dev0` (draft; v0.1 released January
2026), Apache Incubator since mid-2026. Supporters include Snowflake,
Databricks, Salesforce/Tableau, dbt Labs, AtScale, Microsoft, RelationalAI,
Hex, Lightdash, Holistics, GoodData, ThoughtSpot, Sigma, Omni and others.

### Three document types

```
 retail.ontology.yaml  ◄──── retail.mapping.yaml ────►  retail.semantic_model.yaml
 (concepts,                  (which fields populate      (datasets, fields,
  relationships, rules)       which concepts/links)       relationships, metrics)
         │                                                        │
   iri: retail:Customer  ──► OWL ontology                source: retail.orders ──► warehouse
```

| Document | Spec | Retail file |
|---|---|---|
| **Semantic model** | [core-spec/spec.md](https://github.com/apache/ossie/blob/main/core-spec/spec.md) | [`retail.semantic_model.yaml`](../../examples/retail/semantic-model/ossie/retail.semantic_model.yaml) |
| **Ontology** | [ontology/ontology.md](https://github.com/apache/ossie/blob/main/ontology/ontology.md) | [`retail.ontology.yaml`](../../examples/retail/semantic-model/ossie/retail.ontology.yaml) |
| **Mapping** | same, *Ontology mappings* | [`retail.mapping.yaml`](../../examples/retail/semantic-model/ossie/retail.mapping.yaml) |

### Semantic model essentials

```yaml
version: 0.2.0.dev0
name: retail_semantic_model
datasets:
  - name: order_lines
    source: retail.order_lines          # physical table
    primary_key: [order_line_id]
    fields:                             # source columns -> named fields
      - name: line_amount
        expression: { sql: quantity * unit_price }   # portable OSSIE_SQL_2026
        datatype: Decimal
    metrics:                            # dataset-scoped: bare field names
      - name: revenue
        expression: { sql: SUM(line_amount) }
        ai_context:
          synonyms: [sales, GMV]
relationships:                          # many -> one joins, field to field
  - name: order_lines_to_orders
    from: order_lines
    to: orders
    from_columns: [order_id]
    to_columns: [order_id]
metrics:                                # model-scoped: dataset.field
  - name: average_order_value
    expression: { sql: SUM(order_lines.line_amount) / COUNT(DISTINCT order_lines.order_id) }
```

Rules worth knowing:

* Three name levels: **source columns** → **fields** (the public
  interface) → **metrics**. Metrics and relationships see only fields.
* Expressions have a portable `sql` (dialect `OSSIE_SQL_2026`) plus optional
  per-engine `dialects:` (Snowflake, BigQuery, Databricks...).
* `datatype` (type) and `dimension.is_time` (role) are separate.
* `ai_context` (synonyms, instructions) everywhere, for LLM grounding.
* `custom_extensions` carry vendor-specific extras without breaking portability.
* Current limits: no field-on-field or metric-on-metric references (so
  ratios repeat their parts), one model per document.

### Ontology essentials

Ossie's ontology language is **fact-oriented** (in the ORM / FCO-IM
tradition), not OWL, but carries OWL IRIs for alignment:

```yaml
- concept: PremiumCustomer
  type: EntityType
  extends: [ Customer ]                 # = rdfs:subClassOf
  iri: retail:PremiumCustomer           # = the OWL class
  derived_by: [ 'Customer.is_premium' ]
- concept: Rating
  type: ValueType
  extends: [ Integer ]
  requires: [ 1 <= Rating, Rating <= 5 ]   # = SHACL minInclusive/maxInclusive
```

| Ossie ontology | OWL / RDF / SHACL equivalent |
|---|---|
| `EntityType` concept | `owl:Class` |
| `ValueType` concept + `requires` | datatype + SHACL constraints |
| `extends` | `rdfs:subClassOf` |
| relationship under a concept | `owl:ObjectProperty` / `owl:DatatypeProperty` (with the concept as domain) |
| n-ary relationship (`roles: [...]`) | reified class (our `OrderLine`) |
| `multiplicity: ManyToOne` | `owl:FunctionalProperty` |
| `identify_by` | `owl:hasKey` |
| `derived_by` (recursive) | `owl:TransitiveProperty`, property chains, SPARQL CONSTRUCT |
| `derived_by` with `SUM[...]` | *no OWL equivalent* (aggregate rules) |
| `requires` | SHACL shapes (closed-world checks) |
| `verbalizes` | `rdfs:label` patterns (natural-language readings) |
| `iri` | the term's IRI itself |

### Mapping essentials

The mapping says how semantic-model fields create ontology objects and
links, the same job R2RML/RML does for RDF:

```yaml
- concept: Order
  object_mappings:
  - referent_mappings:
    - relationship: id
      expression: orders.order_id         # each orders row -> an Order object
  link_mappings:
  - object_mapping: { referent_mappings: [ { relationship: id, expression: orders.order_id } ] }
    children:
    - object_mapping:
        concept: Customer
        referent_mappings: [ { relationship: id, expression: orders.customer_id } ]
      relationship: placed_by              # -> Order placed_by Customer links
```

### Validation in this repo

```bash
git clone https://github.com/apache/ossie /tmp/ossie
cd examples/retail
python scripts/check_semantic_model.py --ossie-repo /tmp/ossie
# ok  Ossie JSON schemas          semantic model, ontology and mapping validate
# ok  Ossie references            relationships, mapping fields, 34 IRIs resolve in OWL
# ok  Ossie metrics -> SQL        8 metrics compile and equal metrics.sql (revenue 1878.43, AOV 469.61)
```

The script also compiles each Ossie metric to SQL, runs it, and checks it
against SPARQL over the RDF graph, so the semantic model and the knowledge
graph provably say the same thing.

## 3.3 Converters

The [ossie-converters](https://github.com/apache/ossie-converters) repo has
bidirectional converters for dbt, Snowflake, Databricks metric views, Cube,
Microsoft (TMDL/BIM), Salesforce/Tableau, GoodData, Polaris, ThoughtSpot,
Sigma, Omni, Hex, Lightdash, Holistics, Honeydew, RelationalAI, Palantir,
NVIDIA and more, plus an interop test harness. Maturity varies by converter
(many are alpha), so test round-trips on your own models.

Next: [4. Semantic models and ontologies](04-semantic-models-and-ontologies.md)
