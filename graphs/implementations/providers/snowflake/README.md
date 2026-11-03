# Snowflake: graphs

> **Verification:** ⚪ documented; nothing run on Snowflake.
> Last reviewed 2026-11-03. Legend: [verification levels](../../../../README.md#verification-levels).

| Product | Role for graphs | Retail example |
|---|---|---|
| **KG_NODE / KG_EDGE tables** ([Ontology on Snowflake](https://github.com/snowflake-Labs/ontology-on-snowflake)) | property graph stored as two relational tables (VARIANT properties); traversal via SQL / Snowpark UDFs | load the [openCypher CSVs](../aws/opencypher-csv/) (nodes → `KG_NODE`, relationships → `KG_EDGE`) |
| **Snowpark Container Services** | runs graph analytics (NetworkX: centrality, Louvain, shortest path) as agent tools | — |
| RelationalAI (native app) | knowledge graph + reasoning engine on Snowflake data | — |
| Native graph database | none | — |

Snowflake also appears in
[ontologies (Ontology on Snowflake, RelationalAI)](../../../../ontologies/implementations/providers/snowflake/README.md) and
[semantic models (semantic views)](../../../../semantic-models/implementations/providers/snowflake/README.md).

## How the concepts map

A two-table node/edge layout is the simplest way to put a property graph in
a warehouse ([graphs concepts 1](../../../concepts/01-property-graphs.md)):

```sql
CREATE TABLE kg_node (node_id STRING, label STRING, props VARIANT);
CREATE TABLE kg_edge (edge_id STRING, src STRING, dst STRING, label STRING, props VARIANT);
-- C1 -PLACED-> O1 ;  O1 -CONTAINS {quantity:2, unitPrice:29.99}-> P3
```

Multi-hop questions become recursive CTEs or UDFs; heavier algorithms run in
containers. That's fine for agent tools and analytics, not a substitute for a
native graph database at high traversal volume.
