# Oracle: graphs

> **Verification:** ⚪ documented; no Oracle-specific example file yet.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for graphs | Retail example |
|---|---|---|
| **Oracle Database property graphs** | SQL/PGQ property graph views over relational tables (Oracle Database 23ai), plus PGQL | [`retail-pgq.sql`](../../../../examples/retail/property-graph/sql-pgq/retail-pgq.sql) (ISO SQL/PGQ; Oracle 23ai implements it) |
| **Oracle Graph Server (PGX)** | in-memory graph analytics and algorithms | — |
| **Oracle RDF Graph** | RDF store with SPARQL inside Oracle Database | covered under [ontologies](../../../../ontologies/implementations/providers/oracle/README.md) |

Oracle also appears in
[ontologies (RDF Graph)](../../../../ontologies/implementations/providers/oracle/README.md) and
[semantic models (Oracle Analytics)](../../../../semantic-models/implementations/providers/oracle/README.md).

## How the concepts map

The repo's [SQL/PGQ file](../../../../examples/retail/property-graph/sql-pgq/retail-pgq.sql)
is the closest match: `CREATE PROPERTY GRAPH` over the retail tables, then
`SELECT … FROM GRAPH_TABLE (retail MATCH …)`. Oracle-specific syntax
differences are on the [roadmap](../../../../ROADMAP.md).

Docs: [Oracle Database graph](https://docs.oracle.com/en/database/oracle/property-graph/)
