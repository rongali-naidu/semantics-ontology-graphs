# semantics-ontology-graphs

[![checks](https://github.com/rongali-naidu/semantics-ontology-graphs/actions/workflows/checks.yml/badge.svg)](https://github.com/rongali-naidu/semantics-ontology-graphs/actions/workflows/checks.yml)

A hands-on reference for **semantics** in three topics, **ontologies**,
**graphs** and **semantic models**, from first principles to the products
that implement them.

One running example, an **Amazon-style retail ordering domain**, is
expressed in every form: an OWL ontology, RDF in six serializations, a
property graph, warehouse tables, an **Apache Ossie** semantic model, and
product formats from AWS, Google Cloud, Microsoft, Oracle, Snowflake,
Databricks, SAP, Salesforce, Palantir, dbt, AtScale, Cube and Neo4j. CI checks that they give the same
answers.

> **Early release.** Every implementation page states how far it's verified;
> see [verification levels](#verification-levels).

```
                 foundations/   ontology vs knowledge graph vs graph DB · history · semantic models ⇄ ontologies
                       │
     ┌─────────────────┼──────────────────────┐
     ▼                 ▼                      ▼
 ontologies/        graphs/               semantic-models/
 ├─ concepts/       ├─ concepts/          ├─ concepts/
 └─ implementations ├─ implementations    └─ implementations/
    ├─ providers/   │  ├─ providers/         ├─ providers/   aws · gcp · microsoft · oracle · snowflake · databricks · sap · salesforce · palantir
    └─ tools/       │  └─ tools/             └─ tools/       dbt · atscale · cube
                    │
     examples/retail/   one shared example: ontology, RDF, SPARQL, property graph, warehouse, Ossie, scripts
     reference/         standards, links, glossary
```

## Start here

| If you are... | Read |
|---|---|
| new to all of it | [foundations](foundations/README.md), then any topic |
| new to ontologies / the Semantic Web | [ontologies](ontologies/README.md) |
| a developer looking at graph databases | [graphs](graphs/README.md) |
| from BI / analytics | [semantic models](semantic-models/README.md) |
| choosing between ontology and semantic layer for AI agents | [foundations 3: semantic models and ontologies](foundations/03-semantic-models-and-ontologies.md) |
| looking for one provider | the [provider index](#provider-index) below |
| looking for a spec or a definition | [reference](reference/standards-links-glossary.md) |

## Provider index

The same provider appears in every topic where it has a product, so each
topic's page is complete on its own.

| Provider / tool | Ontologies | Graphs | Semantic models |
|---|---|---|---|
| **AWS** | [Context Ontology Accelerator, Neptune](ontologies/implementations/providers/aws/README.md) | [Neptune, Neptune Analytics, COA knowledge graph](graphs/implementations/providers/aws/README.md) | [COA metrics, QuickSight](semantic-models/implementations/providers/aws/README.md) |
| **Google Cloud** | [Knowledge Catalog context graph](ontologies/implementations/providers/gcp/README.md) | [Spanner Graph, BigQuery Graph](graphs/implementations/providers/gcp/README.md) | [Looker, Knowledge Catalog](semantic-models/implementations/providers/gcp/README.md) |
| **Microsoft** | [Fabric IQ, DTDL](ontologies/implementations/providers/microsoft/README.md) | [Fabric Graph, Cosmos DB](graphs/implementations/providers/microsoft/README.md) | [Power BI / Fabric](semantic-models/implementations/providers/microsoft/README.md) |
| **Oracle** | [RDF Graph](ontologies/implementations/providers/oracle/README.md) | [property graphs, Graph Studio](graphs/implementations/providers/oracle/README.md) | [Oracle Analytics](semantic-models/implementations/providers/oracle/README.md) |
| **Snowflake** | [Ontology on Snowflake, RelationalAI](ontologies/implementations/providers/snowflake/README.md) | [KG tables + graph analytics](graphs/implementations/providers/snowflake/README.md) | [semantic views](semantic-models/implementations/providers/snowflake/README.md) |
| **Databricks** | [Genie Ontology, OntoBricks](ontologies/implementations/providers/databricks/README.md) | [GraphFrames, OntoBricks](graphs/implementations/providers/databricks/README.md) | [metric views](semantic-models/implementations/providers/databricks/README.md) |
| **SAP** | [SAP Knowledge Graph, HANA Cloud](ontologies/implementations/providers/sap/README.md) | [HANA Cloud knowledge graph engine](graphs/implementations/providers/sap/README.md) | [Datasphere / Business Data Cloud](semantic-models/implementations/providers/sap/README.md) |
| **Salesforce** | — | — | [Tableau Semantics](semantic-models/implementations/providers/salesforce/README.md) |
| **Palantir** | [Foundry Ontology](ontologies/implementations/providers/palantir/README.md) | — | — |
| **Neo4j** | [neosemantics](ontologies/implementations/tools/neo4j-neosemantics/README.md) | [Neo4j](graphs/implementations/tools/neo4j/README.md) | — |
| **dbt** | — | — | [Semantic Layer / MetricFlow](semantic-models/implementations/tools/dbt/README.md) ✅ |
| **AtScale** | — | — | [SML](semantic-models/implementations/tools/atscale/README.md) |
| **Cube** | — | — | [Cube](semantic-models/implementations/tools/cube/README.md) |

Full product tables: [ontologies](ontologies/implementations/README.md) ·
[graphs](graphs/implementations/README.md) ·
[semantic models](semantic-models/implementations/README.md).

## The example at a glance

```
(:Customer)-[:PLACED]->(:Order)-[:CONTAINS {quantity, unitPrice}]->(:Product)-[:IN_CATEGORY]->(:Category)-[:SUBCATEGORY_OF]->(:Category)
(:Customer)-[:WROTE]->(:Review {rating})-[:REVIEWS]->(:Product)-[:SOLD_BY]->(:Seller)
```

3 customers · 4 orders · 7 order lines · 6 products · 6 categories (3
levels) · 3 sellers · 4 reviews.

| Same data as... | Size | Revenue by customer |
|---|---|---|
| RDF (+ OWL ontology) | 165 triples (+ 238) | SPARQL → Alice 1498.97 · Bob 199.98 · Carol 179.48 |
| Property graph | 29 nodes / 41 edges | Cypher / Gremlin → same |
| Warehouse tables | 8 tables | SQL → same |
| Semantic model | 8 datasets, 8 metrics | Ossie / MetricFlow / COA metrics → same |

## Run the checks (no cloud account needed)

```bash
make install          # pinned Python dependencies
make check            # links, SPARQL, SHACL, OWL RL, graph consistency, warehouse, Ossie + COA metrics
make check-ossie      # + official Apache Ossie schemas at the pinned commit
pip install -r semantic-models/implementations/tools/dbt/requirements.txt
make dbt              # dbt build + MetricFlow, results compared with the SPARQL answers
make help             # all targets
```

`examples/retail/rdf/retail-data.ttl` is the only hand-edited data file;
`make generate` rebuilds every other format from it (data flow in the
[Makefile](Makefile) and [CONTRIBUTING.md](CONTRIBUTING.md#the-data-rule)).
CI runs all checks on every push and weekly.

## Verification levels

Every implementation page starts with one of these and a review date:

| Level | Meaning |
|---|---|
| ✅ **executed** | runs end to end in CI and is compared with the SPARQL answers |
| 🟡 **checked** | files are parsed or validated in CI, or the generated data or definitions are proven consistent; not run on the product itself |
| ⚪ **documented** | written to the product's documented syntax; not run |

| ✅ Executed | 🟡 Checked | ⚪ Documented |
|---|---|---|
| SPARQL queries + updates, SHACL, OWL RL reasoning | Neptune CSV + RDF load files | Cypher, Gremlin, GQL, SQL/PGQ scripts |
| 6 RDF serializations (isomorphic) | AWS COA metric definitions | COA deployment, Neptune loader + clients |
| Warehouse `metrics.sql` (SQLite) | AtScale SML, Cube model | Looker, Power BI, Oracle (design), Snowflake, Databricks |
| Apache Ossie model, ontology, mapping | | Spanner / BigQuery / Fabric Graph, DTDL, GraphFrames, Neo4j |
| dbt + MetricFlow (DuckDB) | | |

Moving ⚪ items up is the plan in [ROADMAP.md](ROADMAP.md). If something
doesn't run on your product version, please open an issue or PR.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) (data rule, adding a product,
verification levels) and [ROADMAP.md](ROADMAP.md) (what's next).

## License

* Code, scripts, queries, data and model files: [Apache 2.0](LICENSE)
* Documentation: [CC BY 4.0](LICENSE-docs.md)

Apache Ossie, AtScale SML, W3C/ISO standards and product formats referenced
here remain under their own licenses.
