# Roadmap

Goal: a reference where **every format is proven, not just written**, and
where vendor information stays current. Ordered by value per effort.

Legend: ✅ done · 🔜 next · 📋 planned · 💭 idea

## Phase 0: foundations ✅ (November 2026)

- ✅ Concepts / vendors / reference structure; one retail example in every format
- ✅ CI: SPARQL, SHACL, OWL RL, graph consistency, warehouse + Ossie metrics,
  Ossie official schemas (pinned commit), dbt + MetricFlow, link checker,
  "generated files are current" check; weekly scheduled run
- ✅ Verification level + review date on every vendor folder
- ✅ Licensing: Apache 2.0 (code, data, models) + CC BY 4.0 (docs)
- ✅ `Makefile`, `CONTRIBUTING.md`, pinned dependencies
- ✅ Chapter on where semantic models are stored (BI metadata repositories vs
  user-defined git: Oracle Analytics RPD / Semantic Modeler, Power BI PBIP +
  Fabric Git, Looker, BusinessObjects, Cognos, MicroStrategy, Tableau, Qlik,
  ThoughtSpot); Oracle vendor folder (layer mapping); PBIP metadata files for
  the Power BI model

## Phase 1: make more formats executable in CI 🔜

Everything here runs free in GitHub Actions (Docker service containers or
pip packages). Each item raises a vendor folder to ✅ or 🟡.

| Item | How | Raises |
|---|---|---|
| 🔜 SPARQL over HTTP | Apache Jena Fuseki or Oxigraph container; run every `.rq` through the SPARQL 1.1 Protocol, which also exercises the Neptune client code path (`sparql_query.py`, IAM off) | SPARQL server path, aws clients 🟡 |
| 🔜 Gremlin | TinkerPop Gremlin Server container; load `01-create-retail-graph.groovy`, run each traversal in `02-queries.groovy`, compare with SPARQL answers | Gremlin ✅ |
| 🔜 Cypher | Neo4j Community container; run the create + query scripts; install n10s and run `ontology-import.cypher` (OWL import, subclass inference, SHACL) | Cypher ✅, neo4j ✅ |
| 🔜 SQL/PGQ | DuckDB + `duckpgq` extension (adapt syntax where DuckPGQ differs) | SQL/PGQ ✅ |
| 📋 Cube | Cube container over DuckDB/Postgres with `warehouse/`; query the REST/SQL API, compare metrics | cube ✅ |
| 📋 LookML | `lkml` parser in CI (syntax); full validation needs a Looker instance | gcp/looker 🟡 |
| 📋 TMDL | parse with an open-source TMDL tool, or convert with the Ossie Microsoft converter and compare metrics | microsoft 🟡 |
| 📋 GraphFrames | local PySpark in CI (slow, so weekly only) | databricks graph 🟡 |

## Phase 2: round-trips through Apache Ossie 📋

Use [apache/ossie-converters](https://github.com/apache/ossie-converters)
to convert the Ossie model **to** dbt, Cube, Snowflake, Databricks and
TMDL, and the hand-written vendor files **back** to Ossie. Then:

- diff the generated vendor files against the hand-written ones
  (documents real differences between tools);
- run the converted-back Ossie through `check_semantic_model.py` (proves the
  vendor file has the same metrics). This raises Snowflake, Databricks and
  Microsoft to 🟡 without vendor accounts.
- Track converter maturity in a table (alpha / works / lossy on X).

## Phase 3: content gaps 📋

- 📋 **Oracle Analytics**: an SMML example in `vendors/oracle/` (needs
  Oracle's published samples or an OAC instance to verify the syntax).
- 📋 **More BI tools**: Tableau (`.tds` / Tableau Semantics), Qlik (master
  items), ThoughtSpot (TML), MicroStrategy, Omni, Lightdash.
- 📋 **Harder semantics in the example**: a time-intelligence metric (YoY,
  MTD), a **semi-additive** metric (add an inventory snapshot fact),
  **row-level security** (sellers see only their products), a many-to-many
  (products in several categories), role-playing dates (order vs ship date).
- 📋 **GraphRAG / AI chapter**: answer "why did premium Electronics revenue
  drop, and who are those customers?" with the semantic layer (numbers) + the
  knowledge graph (entities, paths), using the Ossie `ai_context` and OWL labels.
- 📋 **Fabric IQ ontology** walkthrough for the retail model, once it's
  generally available.
- 💭 RDF 1.2 / SPARQL 1.2 triple-term version of the order lines, once
  the W3C recommendations are final and rdflib supports them.
- 💭 SHACL shapes → generated data tests for the warehouse (dbt tests,
  Great Expectations), closing the loop between ontology constraints and
  semantic-layer data quality.

## Phase 4: vendor-account verification 📋

For platforms that can't run in CI, record manual verification runs in
`vendors/<name>/VERIFIED.md` (date, product version, who, what passed), and
use free tiers where possible: Neo4j Aura Free, BigQuery sandbox, Databricks
Free Edition, Snowflake trial, Power BI Desktop (free), Neptune (paid; short
serverless run).

## Phase 5: publishing 💭

- 💭 Docs site (MkDocs Material on GitHub Pages) with search and rendered
  Mermaid diagrams.
- 💭 Tagged releases (`v0.1.0`), changelog, issue templates ("vendor info is
  out of date", "example doesn't run").

## Maintenance cadence

| What | When |
|---|---|
| CI (all checks) | every PR + weekly |
| Vendor matrix review (GA / preview, new products) | monthly |
| Vendor folder "last reviewed" dates | when touched, at least quarterly |
| Apache Ossie pinned commit | when Ossie releases a version (0.2.0 next) |
| Pinned Python / dbt versions | quarterly |
