# Contributing

Thanks for helping. This repo is useful because **every format describes
the same retail data and gives the same answers**, so most rules below
protect that.

## Setup

```bash
make install        # Python check dependencies (requirements.txt)
make check          # links, SPARQL, SHACL, graph consistency, semantic model
make check-ossie    # + Apache Ossie official schemas (fetches the pinned commit)
pip install -r semantic-models/implementations/tools/dbt/requirements.txt && make dbt   # dbt + MetricFlow
```

CI runs all of these on every pull request
([`.github/workflows/checks.yml`](.github/workflows/checks.yml)).

## The data rule

[`examples/retail/rdf/retail-data.ttl`](examples/retail/rdf/retail-data.ttl)
is the **only** hand-edited data file. Everything else is generated:

```
retail-data.ttl ─► build_rdf_formats.py     ─► rdf/*.nt .nq .trig .rdf .jsonld, graphs/implementations/providers/aws/rdf/
                ─► rdf_to_property_graph.py ─► graphs/implementations/providers/aws/*-csv/, property-graph/*/01-create-*
                ─► rdf_to_tables.py         ─► warehouse/data/*.csv, semantic-models/implementations/tools/dbt/retail_dbt/seeds/
```

After changing the data, run `make generate`, then update the expected
answers in the check scripts and docs. CI fails (`make check-generated`) if
generated files weren't regenerated.

## Adding a product

Implementations are organised **by topic**, then **providers** (cloud and
data platforms) or **tools** (software you can run anywhere, commercial or
open source):

```
<topic>/implementations/providers/<provider>/README.md     e.g. graphs/implementations/providers/aws/
<topic>/implementations/tools/<tool>/README.md             e.g. semantic-models/implementations/tools/dbt/
```

where `<topic>` is `ontologies`, `graphs` or `semantic-models`.

1. **One entry per topic the product serves.** If a provider has products in
   several topics (AWS: COA + Neptune in ontologies, Neptune in graphs, COA
   metrics in semantic models), write a complete entry in **each** topic,
   focused on that topic, and link the entries to each other. Keep runnable
   files (scripts, load files) in **one** place and link to them, so copies
   don't drift.
2. Start the README with the verification block:

   ```markdown
   # <Provider>: <topic>

   > **Verification:** ⚪ written to documented syntax; not run on <product>.
   > Last reviewed YYYY-MM-DD. Legend: [verification levels](../../../../README.md#verification-levels).
   ```

3. Follow it with the **products table** (product · role in this topic ·
   retail example), the "also appears in" links, and then two sections that
   every provider page has:
   * `## Overview`: how the product implements the topic: what it is
     (service, feature, app or reference architecture), where the model or
     graph lives, how you build and query it, how agents use it, and its
     status with a date.
   * `## Product documentation` (last section): official docs as a list,
     `* [Title](url): what it covers`.
4. Add a table mapping the topic's concepts to the products, linking each
   row to the concept chapter it implements.
5. Implement the retail example in the product's formats against
   [`examples/retail/`](examples/retail/), using the **same metric names and
   definitions** as [`metrics.sql`](examples/retail/warehouse/metrics.sql)
   for semantic models.
6. Add a row to that topic's `implementations/README.md` and to the
   [provider index](README.md#provider-index). Put the one-word **status**
   (GA, preview, open source, Labs...) in the topic table's Status column, and
   any detail ("workload GA, ontology item still preview, as of Oct 2026")
   with a date and source on the product page.
7. If it can run for free (Docker image, local engine, free tier), add a
   check and a CI job, and raise the verification level.

### Verification levels

| Level | Requirement |
|---|---|
| ✅ executed | Runs end to end in CI and its results are compared with the SPARQL answers |
| 🟡 checked | Files are parsed or validated (schema, linter) in CI, or generated data is proven consistent |
| ⚪ documented | Written to the vendor's documented syntax, not run. Say so. |

Never claim a higher level than CI proves.

## Writing style

* Explain the concept first, then the vendor detail.
* Link specs and official docs; mark anything from secondary sources.
* Date claims that will age ("as of November 2026").
* Keep examples small enough to read in one screen.

## Licensing

By contributing you agree that documentation is licensed under CC BY 4.0
([LICENSE-docs.md](LICENSE-docs.md)) and code, data and model files under
Apache 2.0 ([LICENSE](LICENSE)).
