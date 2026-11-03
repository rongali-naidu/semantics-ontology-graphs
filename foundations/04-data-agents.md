# 4. Does a data agent need an ontology, a semantic model and a knowledge graph?

A **data agent** is an LLM that answers questions about your data, or acts
on it, by calling tools (SQL, APIs, MCP servers) instead of answering from
memory. Most of its mistakes don't come from the LLM's reasoning; they come
from **missing context**: it doesn't know what "revenue" means here, which
table holds it, how tables join, or that "client" and "customer" are the same
thing.

The three components each supply a different kind of context.

![A data agent routes questions: how much → semantic model, what does it mean → ontology, who and how connected → knowledge graph; all over the same data](../assets/diagrams/data-agent.svg)

## 4.1 What each component gives the agent

| Component | Answers | Without it, the agent… | Retail example |
|---|---|---|---|
| **Semantic model** (semantic layer) | **how much / how many**: governed metrics, dimensions, joins | writes its own SQL and invents a formula ("revenue = SUM(list_price)") or a join that double counts | `revenue = SUM(quantity × unit_price)`, `average_order_value = revenue / order_count`; Alice's revenue is 1498.97 every time |
| **Ontology** | **what does this mean**: vocabulary, synonyms, class hierarchy, rules, what is allowed | confuses terms ("buyer", "client", "account"), misses subclasses, can't tell which concept a question is about | "premium members" = `PremiumCustomer`; a PremiumCustomer **is** a Customer; every Order has exactly one Customer |
| **Knowledge graph** (ontology + data) | **who / which / how connected**: entities, relationships, paths, provenance | can't resolve "Alice" to one entity, can't answer multi-hop questions without fragile self-joins | "customers who bought the earbuds also bought…"; "how is Alice connected to Carol?" |
| *(Documents)* | **why**: policies, definitions, rationale (RAG) | has numbers but can't explain them | "what counts as a delivered order?" |

## 4.2 Do you need all three?

Not on day one. Choose by the questions the agent must answer:

| Your agent mainly answers… | Minimum you need | Add next |
|---|---|---|
| KPI questions over a warehouse ("revenue by month") | **semantic model** (with synonyms / AI context) | ontology for vocabulary across many models |
| questions across many systems and teams with inconsistent names | **ontology** (shared vocabulary) + semantic models per domain | knowledge graph for identity resolution |
| relationship questions ("who is connected to whom", recommendations, lineage, fraud) | **knowledge graph** | semantic model for any metrics on top |
| a mix, in production, with audit requirements | **all three**, linked: ontology terms ↔ semantic-model fields ↔ KG entities | governance, tests, human approval of mappings |

Rule of thumb: **semantic model first for numbers, ontology when vocabulary
gets inconsistent, knowledge graph when the questions become about
relationships.**

## 4.3 How they work together in one question

*"Why did revenue from premium customers in Electronics drop last month, and
who are those customers?"*

1. **Ontology** maps the words: "premium customers" → `retail:PremiumCustomer`
   (⊑ `Customer`), "Electronics" → `CAT-ELECTRONICS` *including its
   subcategories* (`subCategoryOf` is transitive), "revenue" → the
   governed `revenue` metric (Ossie `iri`, COA `ontologyConcepts`).
2. **Semantic model** computes the number with the approved definition:
   `revenue` by `order_month`, filtered to `is_premium = true` and
   `category_level_1 = 'Electronics'`. The agent picks a metric instead of
   writing SQL.
3. **Knowledge graph** answers "who": the premium customers connected to
   Electronics orders, their other purchases, reviews and addresses, with
   provenance.
4. **Documents** (optional) explain "why": a promotion ended, a policy
   changed.

Each step is **checkable**: the metric is defined once, the vocabulary is
explicit, and the graph path can be shown to a human.

## 4.4 How products package this (November 2026)

| Product | Semantic model | Ontology | Knowledge graph | Agent interface |
|---|---|---|---|---|
| [AWS Context Ontology Accelerator](../ontologies/implementations/providers/aws/README.md) | Tier-1 metrics | OWL (induced + approved) | Neptune + virtual KG | MCP (6 tools), tiered routing |
| [Microsoft Fabric IQ](../ontologies/implementations/providers/microsoft/README.md) | Power BI semantic models | Fabric IQ ontology | Fabric Graph | Fabric data agents, Copilot |
| [Google Knowledge Catalog](../ontologies/implementations/providers/gcp/README.md) | LookML, MetricFlow, … ingested | glossary / context graph | context graph, BigQuery Graph | Gemini agents |
| [Databricks](../ontologies/implementations/providers/databricks/README.md) | metric views | Genie Ontology (learned) / OntoBricks (OWL) | OntoBricks triple store | Genie, MCP |
| [Snowflake](../semantic-models/implementations/providers/snowflake/README.md) | semantic views | Ontology on Snowflake / RelationalAI | KG tables | Cortex Agents |
| [Salesforce](../semantic-models/implementations/providers/salesforce/README.md) | Tableau Semantics | — | — | Agentforce, Tableau Next MCP |
| [Palantir](../ontologies/implementations/providers/palantir/README.md) | — | Foundry Ontology (with actions) | object graph | AIP agents |

The pattern is the same everywhere: **metrics for numbers, an ontology for
meaning, a graph for connections**, served to the agent as tools.

## 4.5 Practical checklist

* **Start with the questions.** Write 20 real questions; classify each as
  *how much*, *what does it mean*, *who/how connected* or *why*.
* **Give metrics names, definitions and synonyms** before giving the agent
  SQL access ([semantic models 1](../semantic-models/concepts/01-what-is-a-semantic-model.md)).
* **Make vocabulary explicit**: labels, synonyms, definitions in the ontology
  or the semantic model's `ai_context`.
* **Link the layers**: ontology IRIs in the semantic model (Ossie `iri`,
  COA `ontologyConcepts`), mappings from tables to the ontology
  ([ontologies 7](../ontologies/concepts/07-mapping-ontology-to-tables.md)).
* **Keep humans in the loop** for generated ontologies and mappings.
* **Test answers against known results**, as this repo's CI does: SPARQL =
  SQL = MetricFlow = Ossie = COA metric SQL.

Next: [5. Why this matters in the AI era](05-ai-era.md) · back to [foundations](README.md)
