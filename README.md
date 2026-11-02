# semantics-ontology-graphs

A hands-on reference for **semantics**: ontologies, knowledge graphs, graph
databases and semantic models (semantic layers), from first principles to
vendor implementations.

One running example, an **Amazon-style retail ordering domain**, is
expressed in every form: an OWL ontology, RDF in six serializations, a
property graph, warehouse tables, an **Apache Ossie** semantic model, and
vendor formats for AWS, Google Cloud, Microsoft, Databricks, Snowflake, dbt,
AtScale, Cube and Neo4j. Scripts check that all of them give the same
answers.

```
               concepts/ (vendor-neutral)                          vendors/ (implementations)
 ┌──────────────────────────────────────────────────────┐   ┌──────────────────────────────────┐
 │ A. Ontologies & graphs      B. Semantic modelling     │   │ aws        Neptune (RDF + LPG)    │
 │  ontology, history,          semantic model basics,   │   │ gcp        Spanner/BigQuery Graph,│
 │  OWL/RDFS/SKOS/SHACL,        BI tools (Power BI,      │──►│            Looker                 │
 │  Turtle/JSON-LD/...,         Looker, Tableau...),     │   │ microsoft  Fabric Graph/IQ, Power │
 │  SPARQL, property graphs,    Apache Ossie & open      │   │            BI (TMDL), DTDL        │
 │  graph DBs, Cypher/Gremlin/  formats, ontology ⇄      │   │ databricks metric views, GraphFr. │
 │  GQL/SQL-PGQ                 semantic layer           │   │ snowflake  semantic views         │
 └───────────────────────────┬──────────────────────────┘   │ dbt-labs   MetricFlow ✅ executed │
                             │                              │ atscale    SML                    │
          examples/retail/ ◄─┘ one domain, every format     │ cube       Cube data model        │
                                                            │ neo4j      Cypher + n10s (OWL)    │
                                                            └──────────────────────────────────┘
```

## Start here

* **New to ontologies?** → [concepts/ontologies-and-graphs/01](concepts/ontologies-and-graphs/01-what-is-an-ontology.md)
* **Coming from BI / analytics?** → [concepts/semantic-modelling/01](concepts/semantic-modelling/01-what-is-a-semantic-model.md)
* **Want the big picture of how they connect?** → [semantic models and ontologies](concepts/semantic-modelling/04-semantic-models-and-ontologies.md)
* **Looking for a specific platform?** → [vendors/README.md](vendors/README.md) (concept → vendor matrix)
* **Need a spec link or a definition?** → [reference/standards-links-glossary.md](reference/standards-links-glossary.md)

Full table of contents: [concepts/README.md](concepts/README.md).

## Repository layout

```
semantics-ontology-graphs/
├── concepts/
│   ├── ontologies-and-graphs/   9 chapters: ontology → RDF/OWL → SPARQL → property graphs → graph DBs
│   └── semantic-modelling/      5 chapters: semantic layers → BI tools → Apache Ossie → ontology ⇄ metrics
├── examples/retail/             the shared example (vendor-neutral)
│   ├── ontology/                OWL 2 ontology + SHACL shapes
│   ├── rdf/                     data in Turtle, N-Triples, N-Quads, TriG, RDF/XML, JSON-LD
│   ├── sparql/                  11 queries + 2 updates
│   ├── property-graph/          Cypher, Gremlin, GQL, SQL/PGQ
│   ├── warehouse/               star schema, data CSVs, canonical metrics.sql
│   ├── semantic-model/ossie/    Apache Ossie semantic model + ontology + mapping
│   └── scripts/                 generators and consistency checks
├── vendors/                     aws · gcp · microsoft · databricks · snowflake · dbt-labs · atscale · cube · neo4j
└── reference/                   standards, links, tools, reading list, glossary
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
cd examples/retail
pip install rdflib pyshacl owlrl pyyaml jsonschema

python scripts/run_sparql_local.py --shacl     # all SPARQL + SHACL validation
python scripts/check_consistency.py            # 6 RDF formats + Neptune CSVs agree
python scripts/check_semantic_model.py         # warehouse + Ossie metrics = SPARQL answers
git clone https://github.com/apache/ossie /tmp/ossie
python scripts/check_semantic_model.py --ossie-repo /tmp/ossie   # + official Ossie schemas

cd ../../vendors/dbt-labs/retail_dbt           # dbt + MetricFlow on DuckDB
pip install dbt-duckdb "dbt-metricflow[duckdb]" && export DBT_PROFILES_DIR=.
dbt build && mf query --metrics revenue,order_count --group-by customer__customer_name
```

Regenerate derived files after editing `examples/retail/rdf/retail-data.ttl`:

```bash
python scripts/build_rdf_formats.py       # → .nt .nq .trig .rdf .jsonld (+ vendors/aws/rdf)
python scripts/rdf_to_property_graph.py   # → vendors/aws/*-csv, Cypher + Gremlin create scripts
python scripts/rdf_to_tables.py           # → warehouse/data/*.csv
```

## What's verified, and what isn't

| Verified by running | Written to documented syntax, not executed here |
|---|---|
| SPARQL queries/updates, SHACL, OWL RL reasoning (rdflib, pySHACL, owlrl) | Cypher, Gremlin, GQL, SQL/PGQ |
| 6 RDF serializations isomorphic; Neptune CSVs reproduce SPARQL answers | Neptune loader + Python clients |
| Warehouse metrics = SPARQL answers (SQLite) | Looker, Power BI TMDL, Snowflake, Databricks, Cube, AtScale SML |
| Apache Ossie model, ontology and mapping: official JSON schemas; metrics compiled and executed; IRIs resolve in OWL | Spanner Graph, BigQuery Graph, Fabric Graph, DTDL, GraphFrames, Neo4j n10s |
| dbt + MetricFlow: `dbt build`, `mf validate-configs`, `mf query` on DuckDB | |

If something doesn't run on your engine version, please open an issue or a PR.

## Contributing a vendor

Copy an existing `vendors/<name>/` folder, implement the retail example in
that vendor's formats against `examples/retail/warehouse/` (or the graph
files), and add a column to the matrix in [`vendors/README.md`](vendors/README.md).

## License

Text and examples: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Apache Ossie, SML and other specifications referenced here belong to their
respective projects and licenses.
