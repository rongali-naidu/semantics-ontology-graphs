# Ontology & Knowledge Graph Reference

A hands-on reference for **ontologies, knowledge graphs, graph databases and
Amazon Neptune**. One running example, an **Amazon-style retail ordering
domain**, is modelled as an OWL ontology, expressed as RDF in six
serializations, turned into a property graph, queried in **SPARQL, openCypher,
Gremlin, GQL and SQL/PGQ**, and loaded into **Amazon Neptune** in every
supported format.

```
 concepts ─────────────► RDF world ─────────────► property-graph world ───► Neptune
 1 What is an ontology   4 Documenting (OWL,      7 Property graphs          10 Neptune intro
 2 History                 RDFS, SKOS, SHACL,     8 Graph databases          11 Loading (6 formats
 3 Ontology vs KG vs DB    Turtle, JSON-LD ...)   9 Cypher, Gremlin,            + by query)
                         5 Querying (SPARQL)        GQL, SQL/PGQ             12 Querying (SPARQL,
                         6 Retail example                                       openCypher, Gremlin)
                                                                             13 Standards & links
```

## Contents

| # | Chapter | What you'll learn |
|---|---|---|
| 1 | [What is an ontology?](docs/01-what-is-an-ontology.md) | Definitions, classes/properties/axioms, TBox vs ABox, open-world assumption, kinds of ontologies |
| 2 | [History](docs/02-history.md) | Aristotle → semantic networks → Semantic Web → Google KG → GQL → GraphRAG |
| 3 | [Ontology vs knowledge graph vs graph database](docs/03-ontology-knowledge-graph-graph-database.md) | The layers, and why graphs at all |
| 4 | [Documenting ontologies](docs/04-documenting-ontologies.md) | RDFS, OWL 2, SKOS, SHACL; Turtle, N-Triples, N-Quads, TriG, RDF/XML, JSON-LD, Manchester, Functional; diagrams, doc generators, best practice |
| 5 | [Querying RDF with SPARQL](docs/05-querying-rdf-sparql.md) | SELECT/CONSTRUCT/ASK, property paths, aggregates, inference, SHACL validation |
| 6 | [Retail example end to end](docs/06-retail-example.md) | The domain, modelling decisions, competency questions → queries |
| 7 | [Property graphs](docs/07-property-graphs.md) | LPG model, RDF vs LPG, mapping between them, schemas, algorithms |
| 8 | [Graph databases](docs/08-graph-databases.md) | Triple stores, property-graph DBs, SQL/PGQ, how to choose |
| 9 | [Querying property graphs](docs/09-querying-property-graphs.md) | Cypher, Gremlin, GQL, SQL/PGQ cheat sheets and phrasebook |
| 10 | [Amazon Neptune](docs/10-amazon-neptune.md) | Neptune Database vs Analytics, endpoints, setup, ontologies on Neptune |
| 11 | [Loading into Neptune](docs/11-loading-into-neptune.md) | Gremlin CSV, openCypher CSV, Turtle, N-Triples, N-Quads, RDF/XML, by-query loads |
| 12 | [Querying Neptune](docs/12-querying-neptune.md) | SPARQL, openCypher (HTTPS/boto3/Bolt), Gremlin (WebSocket/HTTPS), notebooks |
| 13 | [Standards, links & glossary](docs/13-standards-links-glossary.md) | Every spec, Neptune doc, tool and term in one place |

## The example at a glance

```
(:Customer)-[:PLACED]->(:Order)-[:CONTAINS {quantity, unitPrice}]->(:Product)-[:IN_CATEGORY]->(:Category)
     │                     │                                           │                  │
 [:HAS_ADDRESS]        [:SHIPS_TO]                                 [:SOLD_BY]     [:SUBCATEGORY_OF]
     ▼                     ▼                                           ▼                  ▼
 (:Address)            (:Address)                                  (:Seller)         (:Category)

(:Customer)-[:WROTE]->(:Review {rating})-[:REVIEWS]->(:Product)
```

3 customers · 4 orders · 7 order lines · 6 products · 6 categories (3 levels)
· 3 sellers · 4 reviews → **165 RDF triples** (+ 237-triple ontology) or
**29 nodes / 41 edges**.

| Folder | Contents |
|---|---|
| [`examples/retail/ontology/`](examples/retail/ontology/) | OWL 2 ontology (Turtle + N-Triples) and SHACL shapes |
| [`examples/retail/rdf/`](examples/retail/rdf/) | Instance data in Turtle, N-Triples, N-Quads, TriG, RDF/XML, JSON-LD |
| [`examples/retail/sparql/`](examples/retail/sparql/) | 11 queries + 2 updates |
| [`examples/retail/property-graph/`](examples/retail/property-graph/) | Cypher, Gremlin, GQL, SQL/PGQ versions |
| [`examples/retail/neptune/`](examples/retail/neptune/) | Bulk-load CSVs, RDF files, `bulk-load.sh`, Python clients |
| [`examples/retail/scripts/`](examples/retail/scripts/) | Generators, local SPARQL runner, consistency checker |

## Try it locally in two minutes (no database)

```bash
cd ontology-knowledge-graphs/examples/retail
pip install rdflib pyshacl owlrl

python scripts/run_sparql_local.py --shacl    # run all SPARQL + validate with SHACL
python scripts/run_sparql_local.py --reason   # same, after OWL RL inference
python scripts/check_consistency.py           # prove every format holds the same data
```

Regenerate the derived files after editing `rdf/retail-data.ttl`:

```bash
python scripts/build_rdf_formats.py           # → .nt .nq .trig .rdf .jsonld
python scripts/rdf_to_property_graph.py       # → Neptune CSVs, Cypher + Gremlin create scripts
```

## Load and query on Amazon Neptune

```bash
export NEPTUNE_ENDPOINT=... BUCKET=... LOADER_ROLE_ARN=... AWS_REGION=us-east-1
./examples/retail/neptune/bulk-load.sh                     # S3 upload + loader jobs

cd examples/retail/neptune/python && pip install -r requirements.txt
python sparql_query.py ../../sparql/05-customers-who-bought-also-bought.rq
python opencypher_query.py boto3
python gremlin_query.py ws
```

## What's verified

* All SPARQL queries/updates and the SHACL shapes run with rdflib/pySHACL
  (`run_sparql_local.py`).
* The six RDF serializations are graph-isomorphic, and both Neptune CSV sets
  reproduce the SPARQL answers (`check_consistency.py`).
* The Cypher, Gremlin, GQL, SQL/PGQ and Neptune client code is written to the
  documented syntax but was **not executed** against a live Neo4j, TinkerPop
  server or Neptune cluster. If something doesn't run on your engine
  version, open an issue or PR.

## License

Text and examples: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
