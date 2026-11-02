# Contributing

Thanks for helping. This repo is useful because **every format describes
the same retail data and gives the same answers**, so most rules below
protect that.

## Setup

```bash
make install        # Python check dependencies (requirements.txt)
make check          # links, SPARQL, SHACL, graph consistency, semantic model
make check-ossie    # + Apache Ossie official schemas (fetches the pinned commit)
pip install -r vendors/dbt-labs/requirements.txt && make dbt   # dbt + MetricFlow
```

CI runs all of these on every pull request
([`.github/workflows/checks.yml`](.github/workflows/checks.yml)).

## The data rule

[`examples/retail/rdf/retail-data.ttl`](examples/retail/rdf/retail-data.ttl)
is the **only** hand-edited data file. Everything else is generated:

```
retail-data.ttl ─► build_rdf_formats.py     ─► rdf/*.nt .nq .trig .rdf .jsonld, vendors/aws/rdf/
                ─► rdf_to_property_graph.py ─► vendors/aws/*-csv/, property-graph/*/01-create-*
                ─► rdf_to_tables.py         ─► warehouse/data/*.csv, vendors/dbt-labs/retail_dbt/seeds/
```

After changing the data, run `make generate`, then update the expected
answers in the check scripts and docs. CI fails (`make check-generated`) if
generated files weren't regenerated.

## Adding a vendor

1. Create `vendors/<name>/README.md`, starting with the verification block:

   ```markdown
   # <Vendor>

   > **Verification:** ⚪ written to documented syntax; not run on <Vendor>.
   > Last reviewed YYYY-MM-DD. Legend: [vendors/README.md](../README.md#verification-levels).
   ```

2. Add a table mapping the generic concepts to the vendor's products, and
   link each row to the concept chapter it implements.
3. Implement the retail example in the vendor's formats against
   [`examples/retail/warehouse/`](examples/retail/warehouse/) (semantic
   models) or the graph files (graph databases). Use the **same metric
   names and definitions** as
   [`metrics.sql`](examples/retail/warehouse/metrics.sql).
4. Add a column to the matrices in [`vendors/README.md`](vendors/README.md).
   Put product status (GA, preview...) **only** in that matrix.
5. If it can run for free (Docker image, local engine, free tier), add a
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
