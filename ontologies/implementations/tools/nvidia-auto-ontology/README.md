# NVIDIA Auto Ontology and ontology-sql-eval

> **Verification:** ⚪ written from the projects' READMEs; not run (needs
> Postgres + pgvector, a source database and an LLM API key).
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Project | What it is | Licence |
|---|---|---|
| [**NVIDIA/auto-ontology**](https://github.com/NVIDIA/auto-ontology) | open-source Python framework that builds an ontology-style **context layer for data agents** from enterprise metadata and serves it over MCP, CLI and API | Apache 2.0 |
| [**NVIDIA/ontology-sql-eval**](https://github.com/NVIDIA/ontology-sql-eval) | text-to-SQL **evaluation toolkit**: measures how much the Auto Ontology context improves SQL accuracy over a schema-only LLM | Apache 2.0 |

Both are open source. Auto Ontology is not accepting external contributions;
it has no tagged release (as of November 2026).

## Auto Ontology: five steps

| Step | What it does | In the retail example it would… |
|---|---|---|
| **Discover** | generates an ontology from catalog metadata; connects existing ontologies and semantic models | find `customers`, `orders`, `order_lines` and propose *Customer*, *Order*, *placedBy* |
| **Ground** | gives the agent the business meaning of metrics, entities and relationships; reconciles conflicting definitions | tie "revenue" to `SUM(quantity × unit_price)`, not `SUM(list_price)` |
| **Validate** | checks generated SQL against certified definitions and lineage; returns provenance with answers | reject a join that double counts order lines |
| **Expose** | serves the context to agents via MCP, CLI and an API (`POST /api/chat/completions`, streamed) | answer "revenue by customer" through an agent |
| **Learn** | feeds certified corrections and usage back into the ontology | record that "buyers" means customers |

Sources: Databricks, Postgres, Snowflake and DuckDB. Agent skills ship with
it (`nvidia-ontology-setup`, `nvidia-ontology-management`,
`nvidia-ontology-query`).

**How it differs from the OWL tools in this repo.** The ontology and catalog
are stored in **Postgres with pgvector**, not as RDF/OWL, and there is no
SPARQL or OWL reasoner. It is closer to the **context graph** of
[foundations 4.2](../../../../foundations/04-data-agents.md#42-what-goes-in-the-graph-and-what-stays-in-the-warehouse)
than to a W3C ontology: metadata, definitions and mappings for text-to-SQL,
with transactions left in the source databases. It sits alongside existing
semantic models rather than replacing them.

## ontology-sql-eval: measuring the gain

[Foundations 5.2](../../../../foundations/05-ai-era.md#52-the-evidence-read-with-care)
asks you to read accuracy claims with care. This toolkit is a way to measure
the claim on public benchmarks instead of taking it on trust.

* **Two arms:** a *schema-only* LLM (control) vs the *ontology-grounded*
  Auto Ontology agent. The reported result is the difference.
* **Scoring:** deterministic **execution match** (does the generated SQL
  return the same rows as the reference SQL?); no LLM judge. Metrics are
  execution accuracy and pass@1, overall and by difficulty.
* **Benchmarks:**

  | Benchmark | Size |
  |---|---|
  | BIRD Dev / Mini-Dev | 1,534 / 500 questions, 11 SQLite databases |
  | FDABench-Lite | 169 questions, 15 databases |
  | BEAVER | 100-question `dw` sample by default |
  | WideWorldImporters | Postgres port |
  | BIRD-Interact | Lite ≈300 tasks · Full 600 tasks (query tasks only) |

* **Pipeline:** ingest the schema into Auto Ontology's Postgres/pgvector
  store → build the semantic layer → run the benchmark
  (`uv run python main.py --database-name <db>`). It installs a **pinned**
  Auto Ontology revision, so results are tied to that version.

**Caveats the README itself flags:** optional SQL-example and value-anchor
files go only to the ontology arm, so a measured gain also reflects those
inputs; and health counters should be checked before quoting accuracy. No
headline numbers are published in the README (as of November 2026).

## How it relates to this repo

| This repo | Auto Ontology / ontology-sql-eval |
|---|---|
| CI checks every format gives the **same known answers** (SPARQL = SQL = MetricFlow = Ossie) | measures whether an agent gets the **right answer** to natural-language questions |
| OWL ontology + R2RML mappings, checked by reasoner and SHACL | ontology generated from metadata, stored in Postgres, validated against certified definitions |
| [foundations 4](../../../../foundations/04-data-agents.md): what a data agent needs | a working implementation of that idea, with an evaluation harness |

Compare with [AWS Context Ontology Accelerator](../../providers/aws/README.md)
(OWL + R2RML, MCP serving) and [Databricks Genie Ontology](../../providers/databricks/README.md)
(learned context from metadata and usage).
