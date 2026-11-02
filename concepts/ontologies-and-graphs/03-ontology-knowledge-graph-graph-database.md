# 3. Ontology vs knowledge graph vs graph database

These three terms get mixed up all the time. They live at different layers:

```
 ┌──────────────────────────────────────────────────────────────┐
 │  Ontology            the MEANING layer (schema + rules)      │  retail-ontology.ttl
 │  "Orders are placed by exactly one Customer;                 │
 │   subCategoryOf is transitive"                               │
 ├──────────────────────────────────────────────────────────────┤
 │  Knowledge graph     ontology + instance data (+ inferences) │  retail-ontology.ttl
 │  "O1 placedBy Alice; Alice is a PremiumCustomer;             │  + retail-data.ttl
 │   therefore Alice is a Customer"                             │
 ├──────────────────────────────────────────────────────────────┤
 │  Graph data model    how the graph is represented            │  RDF triples
 │                                                              │  or labeled property graph
 ├──────────────────────────────────────────────────────────────┤
 │  Graph database      the software that stores + queries it   │  Neptune, Neo4j, GraphDB,
 │                                                              │  Jena, Stardog, ...
 └──────────────────────────────────────────────────────────────┘
```

| | Ontology | Knowledge graph | Graph database |
|---|---|---|---|
| What is it | A specification (a model) | A dataset (model + facts) | A piece of software |
| Answers | "What *can* exist and what must be true?" | "What *do* we know?" | "How do I store/query it fast?" |
| Size | Tens to thousands of terms | Thousands to billions of facts | n/a |
| Example | schema.org, FIBO, our retail TBox | Google KG, Wikidata, our retail graph | Neptune, Neo4j |
| Without the others? | Yes — you can publish an ontology as a file | Yes — a KG can live in files or even a relational DB | Yes — many graph DBs have no ontology at all |

### Key point: you need none of them to use the others

* You can store an RDF knowledge graph **in a relational DB** (Ontop /
  R2RML virtual graphs) or just in **files**.
* You can run a **graph database without an ontology** — most Neo4j/Gremlin
  apps do: the "schema" is implicit in the code.
* An **ontology can sit over a property graph** too: the labels and
  relationship types *are* a vocabulary; you just don't get standard OWL
  reasoning over it.

### What makes a graph a *knowledge* graph?

There is no single official definition. Common requirements (Hogan et al.,
*Knowledge Graphs*, 2021; Ehrlinger & Wöß, 2016):

1. Entities and relationships of the real world, **as a graph**
2. A **schema/ontology** that defines types and relations
3. **Identity**: entities have stable, ideally global, identifiers (IRIs)
4. **Context/provenance**: where facts came from, when they're valid
5. Ability to **derive new knowledge** (reasoning, rules, ML/embeddings)
6. **Integrates** many sources

Under that lens: a property graph of orders in Neo4j is a *graph*; add a
governed vocabulary, global identifiers, provenance and reasoning and it
becomes a *knowledge graph*.

## Why graphs at all? The retail case

Questions like these are painful in SQL and natural in a graph:

| Question | SQL | Graph |
|---|---|---|
| All products under *Electronics*, any depth | recursive CTE | `subCategoryOf*` / `[:SUBCATEGORY_OF*0..]` |
| "Customers who bought X also bought..." | 4–5 self-joins | 4-hop path pattern |
| How is customer A connected to customer B? | very hard | path query |
| Add a new relation type (e.g. *gift for*) | schema migration | just add edges |

See [`retail-pgq.sql`](../../examples/retail/property-graph/sql-pgq/retail-pgq.sql)
for the side-by-side.

**When NOT to use a graph:** simple CRUD on independent records, heavy
aggregate reporting over a few big tables (that's a warehouse's job), or when
you have no multi-hop questions.

## RDF graph vs property graph — preview

The same fact, "Alice placed order O1 which contains 2 × USB-C Charger at
29.99", in the two models:

**RDF (triples)** — every fact is subject–predicate–object; the line item must
be a node of its own to carry `quantity` and `unitPrice`:

```turtle
ex:O1     retail:placedBy   ex:C1 .
ex:O1     retail:hasLine    ex:O1-L2 .
ex:O1-L2  retail:forProduct ex:P3 ;
          retail:quantity   2 ;
          retail:unitPrice  29.99 .
```

**Property graph** — relationships can have properties directly:

```cypher
(alice:Customer)-[:PLACED]->(o1:Order)-[:CONTAINS {quantity: 2, unitPrice: 29.99}]->(charger:Product)
```

Full comparison in [chapter 7](07-property-graphs.md).

Next: [4. Documenting (writing down) an ontology](04-documenting-ontologies.md)
