# 1. Property graphs

A **labeled property graph (LPG)** has:

* **Nodes** (vertices) with one or more **labels** (`:Customer`) and a map of
  **properties** (`{name: 'Alice Johnson', premium: true}`)
* **Relationships** (edges) that are **directed**, have exactly one **type**
  (`:PLACED`), and can have **properties** too (`{quantity: 2}`)
* Every node and edge has an internal **id**

```
 (:Customer {name:'Alice Johnson', premium:true})
        │
        │ :PLACED
        ▼
 (:Order {orderDate: 2026-09-01, status:'DELIVERED'})
        │
        │ :CONTAINS {quantity: 2, unitPrice: 29.99}      ← properties on the edge
        ▼
 (:Product {name:'USB-C Charger 65W', price: 29.99})
```

The property graph model came from the database/developer world (Neo4j,
TinkerPop) and optimises for **traversal**: following an edge is a pointer
hop ("index-free adjacency"), not a join.

## 7.1 RDF vs property graph

| | RDF | Labeled property graph |
|---|---|---|
| Atomic unit | triple (s, p, o) | node, edge, property |
| Identity | global **IRIs** | local ids (strings/ints) |
| Edge attributes | not directly: reify (OrderLine node), named graphs, or **RDF 1.2 triple terms** | ✅ native |
| Multiple edges of the same type between two nodes | one triple per (s,p,o) — duplicates collapse | ✅ distinct edges |
| Node attributes | triples with literal objects | properties map |
| Multi-valued attributes | natural (several triples) | lists / Neptune set cardinality |
| Schema | ontology (RDFS/OWL) + SHACL — open world, inference | optional; constraints, indexes, GQL graph types — closed |
| Semantics | formal (model theory) | operational |
| Standards | W3C RDF, SPARQL, OWL, SHACL | ISO GQL (2024), SQL/PGQ (2023); openCypher; Apache TinkerPop |
| Query | SPARQL | Cypher / openCypher, Gremlin, GQL |
| Data exchange | many standard formats | mostly vendor CSV/JSON (GraphML, GraphSON) |
| Strengths | integration, shared meaning, reasoning, publishing linked data | developer ergonomics, deep traversals, graph algorithms, app back-ends |

**Rule of thumb:** RDF when *meaning, integration and standards* matter most
(master data, life sciences, publishing, regulatory); property graph when
*application performance and developer speed* matter most (recommendations,
fraud rings, network/IT topology, identity graphs). Many teams keep the
ontology as the **conceptual model** and implement it as a property graph.

## 7.2 Mapping RDF ↔ property graph

The mapping used in this repo
([`rdf_to_property_graph.py`](../../examples/retail/scripts/rdf_to_property_graph.py)):

| RDF | Property graph |
|---|---|
| resource with `rdf:type retail:Product` | node with label `Product` |
| `ex:P1` | node id `P1` |
| `ex:P1 retail:name "Laptop Pro 14"` (literal) | property `name: 'Laptop Pro 14'` |
| `ex:P1 retail:inCategory ex:CAT-LAPTOPS` (resource) | edge `(P1)-[:IN_CATEGORY]->(CAT-LAPTOPS)` |
| `ex:O1 retail:placedBy ex:C1` | edge `(C1)-[:PLACED]->(O1)` (direction flipped to read naturally) |
| `retail:OrderLine` node with quantity/unitPrice | **edge** `(O1)-[:CONTAINS {quantity, unitPrice}]->(P1)` |
| `rdf:type retail:PremiumCustomer` | label `Customer` + `premium: true` (or a 2nd label) |
| `xsd:decimal` | `Double` (Neptune CSV has no decimal type) |
| `xsd:date` | `Date` (Gremlin CSV) / `DateTime` (openCypher CSV) |
| the ontology (classes, domains, axioms) | *lost* — becomes documentation, constraints and code conventions |

The last row is the important one: **a property graph holds the data, not the
semantics.** Keep the OWL file as the documented contract.

Standard-ish mappings exist too: Neptune Analytics and other engines can load
RDF directly into a property-graph view, and the W3C/ISO communities are
aligning through **RDF 1.2** ("triple terms" make statement annotation look a
lot like edge properties) — e.g.

```turtle
# RDF 1.2 style: annotate the relationship itself
ex:O1 retail:contains ex:P3 ~ ex:line2 {| retail:quantity 2 ; retail:unitPrice 29.99 |} .
```

## 7.3 Schemas in the property-graph world

Property graphs are often called "schema-less" but every app has a schema —
it's just implicit. Ways to make it explicit:

* **Constraints & indexes** — Neo4j: `CREATE CONSTRAINT FOR (p:Product) REQUIRE p.sku IS UNIQUE`,
  property type constraints, existence constraints.
* **GQL graph types** — `CREATE GRAPH TYPE` declares node/edge types and their
  properties ([`queries.gql`](../../examples/retail/property-graph/gql/queries.gql)).
* **JanusGraph schema** (`mgmt.makeVertexLabel`, `makePropertyKey`), **TigerGraph** (GSQL is schema-first).
* **Documentation**: a diagram + the OWL ontology as the conceptual model.
* **Validation in code / pipeline** (Great Expectations-style checks on the CSVs, or SHACL on an RDF export).

## 7.4 Graph algorithms

Property-graph platforms usually ship analytics libraries: PageRank,
community detection (Louvain, label propagation), similarity (Jaccard,
node2vec embeddings), shortest paths, centrality. Examples: Neo4j Graph Data
Science, **Neptune Analytics** (algorithms callable from openCypher, e.g.
`CALL neptune.algo.pageRank(...)`), TigerGraph GDS library, Memgraph MAGE,
Apache Spark GraphFrames.

Retail uses: "similar products" (Jaccard on co-purchase), influential
reviewers (PageRank), fraud rings (connected components over shared cards/
addresses).

Next: [2. Graph databases](02-graph-databases.md)
