# Oracle: graphs

> **Verification:** ⚪ documented; no Oracle-specific example file yet.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for graphs | Retail example |
|---|---|---|
| **Oracle Database property graphs** (Oracle AI Database 26ai, 19c+) | SQL:2023 property graph views over relational tables (SQL/PGQ); PGQL on 19c and earlier; GraphRAG + vector search in the same database | [`retail-pgq.sql`](../../../../examples/retail/property-graph/sql-pgq/retail-pgq.sql) (ISO SQL/PGQ; Oracle 23ai implements it) |
| **Oracle Graph Server (PGX)** / in-database algorithms | 80+ algorithms (PageRank, Louvain, Dijkstra, betweenness) | — |
| **Graph Studio** | browser IDE to build, query and visualize graphs | — |
| **Oracle RDF Graph** | RDF store with SPARQL inside Oracle Database | covered under [ontologies](../../../../ontologies/implementations/providers/oracle/README.md) |

Oracle also appears in
[ontologies (RDF Graph)](../../../../ontologies/implementations/providers/oracle/README.md) and
[semantic models (Oracle Analytics)](../../../../semantic-models/implementations/providers/oracle/README.md).

## How the concepts map

The repo's [SQL/PGQ file](../../../../examples/retail/property-graph/sql-pgq/retail-pgq.sql)
is the closest match: `CREATE PROPERTY GRAPH` over the retail tables, then
`SELECT … FROM GRAPH_TABLE (retail MATCH …)`. Oracle-specific syntax
differences are on the [roadmap](../../../../ROADMAP.md).

Docs: [Oracle Database graph](https://docs.oracle.com/en/database/oracle/property-graph/) ·
[oracle-samples/oracle-graph](https://github.com/oracle-samples/oracle-graph) (demos, GraphRAG notebooks, 80+ algorithm samples)
