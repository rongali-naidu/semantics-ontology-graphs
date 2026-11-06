# 6. The Semantics Architect: an emerging AI role

Building AI data agents over the last two years has taught me one thing:
the essence of the work is giving the agent the **accurate and complete
meaning of the data**. That meaning comes down to six dimensions.

A **Semantics Architect** designs and governs the shared meaning of an
organization's data across these six dimensions, so that humans and AI
agents get answers that are accurate, explainable and trusted.

![The six dimensions of a Semantics Architect around one semantic layer for humans and AI agents: 1 Metadata (describes the data), 2 Semantic Models (encode business logic), 3 Knowledge Bases (capture context), 4 Ontology and Taxonomy (define meaning), 5 Knowledge Graphs (data graph plus semantic graph), 6 Lineage (proves trust)](../assets/images/semantics-architect-six-dimensions.png)

## 6.1 The six dimensions

### 1. Metadata: describes the data
The foundation. Metadata means:
* business-friendly descriptions of tables and columns;
* data types and valid values;
* freshness and ownership;
* quality signals.

If a column is called `amt_2` and has no description, your agent is flying
blind.

### 2. Semantic models: encode business logic
The translation layer between how data is stored and how the business
talks. Metrics, dimensions, joins and business logic are defined once and
reused everywhere. "Active customer" should mean one thing, whether a
dashboard asks or an agent does.

### 3. Knowledge bases: capture context
The institutional memory:
* business rules, definitions and policies;
* verified query examples;
* the tribal knowledge that usually lives in someone's head or a forgotten
  wiki page.

This is what grounds the agent in how your organization actually works.

### 4. Ontology (including taxonomy): defines meaning
* **Taxonomy** organizes concepts into hierarchies, such as Product →
  Category → Subcategory.
* **Ontology** goes further. It defines what things are and how they
  relate: a Customer places an Order, an Order contains Items, an Item is
  fulfilled by a Warehouse.

This gives agents a shared vocabulary and lets them reason, not just
retrieve.

### 5. Knowledge graphs: the data graph plus the semantic graph
The ontology brought to life in graph form. A knowledge graph can hold two
very different things, and the distinction matters:

* **A data knowledge graph** stores real business entities and their
  relationships: this customer, these orders, that warehouse. It lets an
  agent move from a delayed shipment to the affected customers, their open
  orders and the revenue at risk.
* **A semantic (metadata) knowledge graph** stores meaning, not records. It
  connects business terms, metrics, ontology concepts, tables, columns,
  owners, quality rules and lineage. It lets an agent reason that "net
  revenue" is a governed metric, defined in the semantic model, calculated
  from these three tables, owned by Finance and refreshed daily.

The first helps an agent **answer** business questions. The second helps an
agent **understand how to answer them correctly**. Many enterprises jump to
the first and skip the second, but for AI data agents the semantic graph is
often where the accuracy gains come from. (In
[foundations 4](04-data-agents.md#42-what-goes-in-the-graph-and-what-stays-in-the-warehouse)
these are called the *entity graph* and the *context graph*.)

### 6. Lineage: proves trust
Trust and explainability:
* Where did this number come from?
* What transformations touched it?
* What breaks downstream if this source changes?

An agent that can't explain its answer won't be trusted in a boardroom, and
lineage is how it explains itself.

## 6.2 The six dimensions side by side

The same six dimensions, each shown on this repo's
[retail example](../examples/retail/). The knowledge graph gets two columns
because it comes in the two kinds described above: a **data graph** of
records and a **semantic graph** of metadata. One question needs all of
them:

![Seven columns, one per dimension with the knowledge graph split in two, each with a retail example: metadata (customers.is_premium BOOLEAN, paid membership; order status values), semantic model (revenue = SUM(quantity × unit_price) mapped to order_lines, orders, customers), knowledge base (ai_context rules and verified queries with expected answers), ontology and taxonomy (Electronics → Computers → Laptops; Order placedBy Customer; PremiumCustomer ⊑ Customer), data graph (Alice → O1 → Laptop Pro 14 → Laptops → Computers), semantic graph (metric revenue linked to its synonyms, definitions, ontology concept, dbt model and column), lineage (source tables → dbt model fct_order_lines → measure → metric revenue 1878.43); then the question "revenue from premium customers in Electronics" answered as 1498.97, and a comparison table](../assets/diagrams/six-dimensions.svg)

| | Metadata | Semantic model | Knowledge base | Ontology & taxonomy | Knowledge graph: data | Knowledge graph: semantic | Lineage |
|---|---|---|---|---|---|---|---|
| **Purpose** | describe tables and columns: types, meaning, owners | define metrics, dimensions and joins once, for every tool and agent | capture rules, definitions and verified Q&A the data itself doesn't say | define what things are, how they relate, and the rules (a taxonomy is just the tree) | store real entities and their relationships: customers, orders, products | store meaning, not records: terms, metrics, concepts, tables, owners, lineage | show where a number came from and what depends on it |
| **Form** | catalog entries: schema, descriptions, constraints | datasets, fields, metrics, joins over physical tables | documents, instructions, example questions with SQL | classes, properties, axioms (TBox); a taxonomy is a broader / narrower concept tree | instances (ABox) as triples or a property graph | a metadata graph linking glossary, semantic model, ontology and catalog | a DAG of sources → models → metrics, down to columns |
| **Standards** | DCAT, Dublin Core; catalog APIs | Apache Ossie, MetricFlow, LookML, TMDL, semantic views | none: documents, Ossie `ai_context`, verified queries | OWL 2, RDFS, SHACL; SKOS for taxonomies | RDF + SPARQL, or a property graph + Cypher / ISO GQL | RDF, SKOS, DCAT, PROV-O; or a catalog's graph API | OpenLineage, W3C PROV-O |
| **Reasoning** | none; lookup and search | no logical inference; computes aggregates without double counting | none; retrieved (RAG) and applied by the LLM | a reasoner infers and checks: Alice is a Customer; a Customer who is also a Seller is an error | traversal and paths; inference only when backed by an ontology | navigation of meaning: which metric, which tables, whose, how fresh | impact analysis: what breaks if a source changes |
| **In this repo** | [`schema.sql`](../examples/retail/warehouse/schema.sql), Ossie field descriptions, SHACL `sh:in` | [Ossie model](../examples/retail/semantic-model/ossie/retail.semantic_model.yaml), dbt MetricFlow, LookML, TMDL, COA metrics | Ossie `ai_context`; [SPARQL queries](../examples/retail/sparql/) with expected answers | [`retail-ontology.ttl`](../examples/retail/ontology/retail-ontology.ttl), [`retail-shapes.ttl`](../examples/retail/ontology/retail-shapes.ttl), the category tree (`subCategoryOf` ⊑ `skos:broader`) | [`retail-data.ttl`](../examples/retail/rdf/retail-data.ttl), the property graph, Neptune load files | the links exist in the files ([Ossie mapping](../examples/retail/semantic-model/ossie/retail.mapping.yaml), COA `ontologyConcepts`, dbt `ref()`s); the graph itself isn't built here | [dbt project](../semantic-models/implementations/tools/dbt/README.md): sources → `fct_order_lines` → `revenue`, run in CI |
| **Typical tools** | Unity Catalog, Glue Data Catalog, Dataplex, DataHub | dbt, Looker, Power BI, Cube, AtScale, Snowflake | wikis, vector stores; Genie instructions, Cortex verified queries | Protégé, TopBraid, AWS COA; PoolParty for taxonomies | Neptune, Neo4j, GraphDB, Stardog, Spanner Graph | Knowledge Catalog, AWS COA, Fabric IQ, Genie Ontology, DataHub | OpenLineage / Marquez, dbt docs, catalog lineage views |

**One question, every dimension contributes:** *"What was revenue from
premium customers in Electronics?"*

| Dimension | Contributes | From |
|---|---|---|
| Metadata | `is_premium` means paid membership; `unit_price` is the price actually paid | [`schema.sql`](../examples/retail/warehouse/schema.sql), Ossie descriptions |
| Semantic model | revenue = Σ `quantity × unit_price`, filtered by `is_premium` and Electronics | [Ossie model](../examples/retail/semantic-model/ossie/retail.semantic_model.yaml) |
| Knowledge base | use the price paid, not list price; Electronics is `category_level_1` | Ossie `ai_context` |
| Ontology & taxonomy | premium customers are Customers; Laptops ⊂ Computers ⊂ Electronics | [`retail-ontology.ttl`](../examples/retail/ontology/retail-ontology.ttl), [`retail-data.ttl`](../examples/retail/rdf/retail-data.ttl) |
| Knowledge graph: data | *who*: Alice (orders O1, O3); Carol, the other premium customer, bought Books and Kitchen items | [`retail-data.ttl`](../examples/retail/rdf/retail-data.ttl) |
| Knowledge graph: semantic | "revenue" (also "sales", "GMV") is a governed metric, about `retail:OrderLine`, computed from `fct_order_lines.line_amount` | Ossie synonyms, COA `ontologyConcepts`, dbt model |
| Lineage | the number traces from metric `revenue` ← measure ← `fct_order_lines` ← `order_lines`, `orders`, `products` | [dbt project](../semantic-models/implementations/tools/dbt/README.md) |

Answer: **1498.97**, all from Alice Johnson's orders: Laptop Pro 14 and
2 × USB-C Charger 65W (O1), and Wireless Earbuds X (O3).

## 6.3 One semantic layer, not six projects

These six are not separate projects. Together they form the **semantic
layer of the enterprise**:

* **metadata** describes the data;
* the **semantic model** encodes business logic;
* the **knowledge base** captures context;
* the **ontology** defines meaning;
* **lineage** proves trust;
* the **semantic knowledge graph** connects all of them into one navigable
  map that an agent can reason over.

That layer needs an owner: the **Semantics Architect**. It's a new role at
the intersection of data architecture, data governance, knowledge
engineering and AI. It's not quite a data architect, not quite a data
steward, and not quite an ML/AI engineer. It borrows from all three.

## 6.4 One critical caveat: the dimensions overlap

A business definition could live in metadata, the semantic model, the
knowledge base or the ontology. Lineage can sit in a catalog or inside the
semantic graph. If two of them define "net revenue" differently, the agent
gets conflicting context and quietly picks one.

**Each piece of meaning needs a single source of truth**, with the others
referencing it rather than copying it. This repo shows the pattern on the
retail example: the same relationship appears as an ontology property, an
R2RML mapping, an Ossie relationship and a property-graph edge, and CI
proves they agree
([foundations 4.3](04-data-agents.md#43-isnt-that-redundant-a-semantic-model-and-a-graph-of-semantic-model-information)).

## 6.5 Not every organization needs all six on day one

The right combination depends on the scale and complexity of your data
landscape:

| Landscape | Start with | Why |
|---|---|---|
| **Single domain, small footprint** | rich metadata, a semantic model for core metrics, a knowledge base of verified queries | often gets you most of the accuracy |
| **Multiple domains, growing reuse** | add taxonomy and lineage | terms stay consistent and answers stay traceable across teams |
| **Large enterprise, many domains with conflicting definitions** | add a formal ontology and a semantic knowledge graph | they connect everything into one shared meaning |

Start with what your agents need now, and evolve toward the full layer as
the landscape grows ([foundations 4.4](04-data-agents.md#44-do-you-need-all-three)
makes the same point for ontology, semantic model and knowledge graph).

## 6.6 Where each dimension is covered in this repo

| Dimension | Covered in | Depth |
|---|---|---|
| 1. Metadata | [foundations 4.2](04-data-agents.md#42-what-goes-in-the-graph-and-what-stays-in-the-warehouse) (what a context graph holds), `ai_context` / synonyms in the [semantic models](../semantic-models/README.md) | introduced |
| 2. Semantic models | [semantic models](../semantic-models/README.md): concepts, repositories, vendor products, Apache Ossie, dbt MetricFlow | **in depth** |
| 3. Knowledge bases | [foundations 4.1](04-data-agents.md#41-what-each-component-gives-the-agent) (documents and RAG), [foundations 5](05-ai-era.md) | introduced |
| 4. Ontology & taxonomy | [ontologies](../ontologies/README.md): OWL, SKOS, SHACL, OOP → OWL, mapping to tables | **in depth** |
| 5. Knowledge graphs | [graphs](../graphs/README.md) (property graphs, RDF, Neptune); [foundations 4.2](04-data-agents.md#42-what-goes-in-the-graph-and-what-stays-in-the-warehouse) (data graph vs semantic graph) | **in depth** |
| 6. Lineage | [foundations 4.2](04-data-agents.md#42-what-goes-in-the-graph-and-what-stays-in-the-warehouse) (lineage in the context graph) | introduced |

## 6.7 Why now

For years, metadata and governance were treated as hygiene: important, but
rarely urgent. AI has changed that. The semantic layer is now the difference
between an agent that delights users and one that quietly erodes trust.

> Data engineers moved data. Data architects structured it. Semantics
> Architects will make it understood by agents.

If you're a data architect, governance lead, data engineer or business
intelligence engineer, this role may be relevant to you, and the chapters
above are a place to start.

Back to: [foundations](README.md)
