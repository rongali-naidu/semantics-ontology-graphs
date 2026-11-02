# semantics-ontology-graphs

[![checks](https://github.com/rongali-naidu/semantics-ontology-graphs/actions/workflows/checks.yml/badge.svg)](https://github.com/rongali-naidu/semantics-ontology-graphs/actions/workflows/checks.yml)

A hands-on reference for **semantics**: ontologies, knowledge graphs, graph
databases and semantic models (semantic layers), from first principles to
vendor implementations.

One running example, an **Amazon-style retail ordering domain**, is
expressed in every form: an OWL ontology, RDF in six serializations, a
property graph, warehouse tables, an **Apache Ossie** semantic model, and
vendor formats for AWS, Google Cloud, Microsoft, Oracle, Databricks,
Snowflake, dbt, AtScale, Cube and Neo4j. Scripts check that all of them give the same
answers.

```
              concepts/ (vendor-neutral)                          vendors/ (implementations)
 ┌─────────────────────────────────────────────────────┐   ┌───────────────────────────────────┐
 │ A. Ontologies & graphs     B. Semantic modelling    │   │ aws        Neptune (RDF + LPG)    │
 │  ontology, history,         semantic model basics,  │   │ gcp        Spanner/BigQuery Graph,│
 │  OWL/RDFS/SKOS/SHACL,       BI tools (Power BI,     │   │            Looker                 │
 │  Turtle/JSON-LD/...,        Looker, Tableau...),    │──►│ microsoft  Fabric Graph/IQ, Power │
 │  SPARQL, property graphs,   where models are stored │   │            BI (TMDL/PBIP), DTDL   │
 │  graph DBs, Cypher/Gremlin/ (RPD, PBIP, LookML),    │   │ oracle     RPD / Semantic Modeler │
 │  GQL/SQL-PGQ                Apache Ossie, ontology  │   │ databricks metric views, GraphFr. │
 │                             ⇄ semantic layer        │   │ snowflake  semantic views         │
 └──────────────────────────┬──────────────────────────┘   │ dbt-labs   MetricFlow ✅ executed │
                            │                              │ atscale    SML                    │
         examples/retail/ ◄─┘ one domain, every format     │ cube       Cube data model        │
                                                           │ neo4j      Cypher + n10s (OWL)    │
                                                           └───────────────────────────────────┘
```

## Start here

* **New to ontologies?** → [concepts/ontologies-and-graphs/01](concepts/ontologies-and-graphs/01-what-is-an-ontology.md)
* **Coming from BI / analytics?** → [concepts/semantic-modelling/01](concepts/semantic-modelling/01-what-is-a-semantic-model.md)
* **Want the big picture of how they connect?** → [semantic models and ontologies](concepts/semantic-modelling/05-semantic-models-and-ontologies.md)
* **Looking for a specific platform?** → [vendors/README.md](vendors/README.md) (concept → vendor matrix)
* **Need a spec link or a definition?** → [reference/standards-links-glossary.md](reference/standards-links-glossary.md)

Full table of contents: [concepts/README.md](concepts/README.md).

## Repository layout

```
semantics-ontology-graphs/
├── concepts/
│   ├── ontologies-and-graphs/   9 chapters: ontology → RDF/OWL → SPARQL → property graphs → graph DBs
│   └── semantic-modelling/      6 chapters: semantic layers → BI tools → model repositories → Apache Ossie → ontology ⇄ metrics
├── examples/retail/             the shared example (vendor-neutral)
│   ├── ontology/                OWL 2 ontology + SHACL shapes
│   ├── rdf/                     data in Turtle, N-Triples, N-Quads, TriG, RDF/XML, JSON-LD
│   ├── sparql/                  11 queries + 2 updates
│   ├── property-graph/          Cypher, Gremlin, GQL, SQL/PGQ
│   ├── warehouse/               star schema, data CSVs, canonical metrics.sql
│   ├── semantic-model/ossie/    Apache Ossie semantic model + ontology + mapping
│   └── scripts/                 generators and consistency checks
├── vendors/                     aws · gcp · microsoft · oracle · databricks · snowflake · dbt-labs · atscale · cube · neo4j
├── reference/                   standards, links, tools, reading list, glossary
├── tools/                       repo-wide checks (link checker)
├── Makefile                     generate, check, check-ossie, dbt
└── ROADMAP.md, CONTRIBUTING.md, LICENSE (Apache 2.0), LICENSE-docs.md (CC BY 4.0)
```

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
| Semantic model | 8 datasets, 8 metrics | Ossie / MetricFlow → same |

## Run the checks (no cloud account needed)

```bash
make install          # pinned Python dependencies
make check            # links, SPARQL, SHACL, OWL RL, graph consistency, warehouse + Ossie metrics
make check-ossie      # + official Apache Ossie schemas at the pinned commit
pip install -r vendors/dbt-labs/requirements.txt
make dbt              # dbt build + MetricFlow, results compared with the SPARQL answers
make help             # all targets
```

`examples/retail/rdf/retail-data.ttl` is the only hand-edited data file;
`make generate` rebuilds every other format from it (data flow in the
[Makefile](Makefile) and [CONTRIBUTING.md](CONTRIBUTING.md#the-data-rule)).
CI runs all checks on every push and weekly.

## What's verified, and what isn't

Every vendor folder starts with a verification level and review date
([legend](vendors/README.md#verification-levels)):

| ✅ Executed in CI, compared with the SPARQL answers | 🟡 Checked (parsed / consistency-proven) | ⚪ Written to documented syntax, not run |
|---|---|---|
| SPARQL queries + updates, SHACL, OWL RL reasoning | Neptune CSV + RDF load files | Cypher, Gremlin, GQL, SQL/PGQ |
| 6 RDF serializations (isomorphic) | AtScale SML, Cube model | Neptune loader + Python clients |
| Warehouse `metrics.sql` (SQLite) | | Looker, Power BI TMDL, Oracle (design), Snowflake, Databricks |
| Apache Ossie model, ontology, mapping (official schemas; metrics executed; IRIs resolve in OWL) | | Spanner Graph, BigQuery Graph, Fabric Graph, DTDL, GraphFrames, Neo4j n10s |
| dbt + MetricFlow (DuckDB) | | |

Moving the ⚪ items to ✅ is the plan in [ROADMAP.md](ROADMAP.md). If
something doesn't run on your engine version, please open an issue or PR.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) (data rule, adding a vendor,
verification levels) and [ROADMAP.md](ROADMAP.md) (what's next).

## License

* Code, scripts, queries, data and model files: [Apache 2.0](LICENSE)
* Documentation: [CC BY 4.0](LICENSE-docs.md)

Apache Ossie, AtScale SML, W3C/ISO standards and vendor formats referenced
here remain under their own licenses.
