# 5. Querying ontologies and RDF knowledge graphs

The standard query language for RDF is **SPARQL 1.1** (W3C, 2013). The
"ontology" and the "data" are both just triples, so the same language queries
both.

| Spec | What it covers |
|---|---|
| [SPARQL 1.1 Overview](https://www.w3.org/TR/sparql11-overview/) | Index of all parts |
| [SPARQL 1.1 Query](https://www.w3.org/TR/sparql11-query/) | SELECT / CONSTRUCT / ASK / DESCRIBE, property paths, aggregates, subqueries, negation |
| [SPARQL 1.1 Update](https://www.w3.org/TR/sparql11-update/) | INSERT / DELETE / LOAD / CLEAR / DROP |
| [SPARQL 1.1 Protocol](https://www.w3.org/TR/sparql11-protocol/) | How to send queries over HTTP (`query=` / `update=`) |
| [SPARQL 1.1 Results JSON](https://www.w3.org/TR/sparql11-results-json/) / [CSV/TSV](https://www.w3.org/TR/sparql11-results-csv-tsv/) | Result formats |
| [SPARQL 1.1 Federated Query](https://www.w3.org/TR/sparql11-federated-query/) | `SERVICE <endpoint> { ... }` — query several endpoints in one go |
| [SPARQL 1.1 Entailment Regimes](https://www.w3.org/TR/sparql11-entailment/) | Querying with RDFS/OWL inference |
| [SPARQL 1.2](https://www.w3.org/TR/sparql12-query/) (in progress) | Triple terms (RDF 1.2), new functions |
| [GeoSPARQL](https://www.ogc.org/standard/geosparql/) | Spatial queries (OGC) |

## 5.1 Anatomy of a SPARQL query

```sparql
PREFIX retail: <https://example.org/retail/ontology#>      # 1. prefixes

SELECT ?customerName (SUM(?qty * ?price) AS ?totalSpent)    # 2. result form
WHERE {                                                     # 3. graph pattern
  ?order a retail:Order ;                  # triple patterns: ?variables match anything
         retail:placedBy ?customer ;       # ';' = same subject
         retail:hasLine ?line .
  ?line  retail:quantity ?qty ;
         retail:unitPrice ?price .
  ?customer retail:name ?customerName .
}
GROUP BY ?customerName                                      # 4. modifiers
ORDER BY DESC(?totalSpent)
LIMIT 10
```

A query is a **pattern of triples with holes**; the engine finds every way
to fill the holes from the graph.

## 5.2 Four query forms

| Form | Returns | Example file |
|---|---|---|
| `SELECT` | table of variable bindings | [03-order-totals-per-customer.rq](../examples/retail/sparql/03-order-totals-per-customer.rq) |
| `CONSTRUCT` | a new RDF graph | [09-construct-purchased.rq](../examples/retail/sparql/09-construct-purchased.rq) |
| `ASK` | true / false | [10-ask-and-describe.rq](../examples/retail/sparql/10-ask-and-describe.rq) |
| `DESCRIBE` | "everything about" a resource (implementation-defined) | `DESCRIBE <https://example.org/retail/data/P4>` |

## 5.3 The features you'll use most

| Feature | Syntax | Retail example |
|---|---|---|
| Optional parts (left join) | `OPTIONAL { ... }` | products with or without reviews (Q6) |
| Filters | `FILTER(?paid < ?list)` | sale purchases (Q10) |
| Negation | `FILTER NOT EXISTS { ... }` / `MINUS { ... }` | products never ordered (Q7) |
| Alternatives | `{ ... } UNION { ... }` | |
| Aggregates | `COUNT SUM AVG MIN MAX GROUP_CONCAT SAMPLE` + `GROUP BY` / `HAVING` | Q3, Q5, Q6 |
| **Property paths** | `a/b` sequence, `a|b` alt, `^a` inverse, `a*` 0+ hops, `a+` 1+ hops, `a?` 0–1 | `retail:subCategoryOf*` (Q2), `^retail:placedBy/retail:hasLine/retail:forProduct` (Q9) |
| Bind / compute | `BIND(?q * ?p AS ?total)` | Q4 |
| Inline data | `VALUES ?sku { "EAR-X" "KBD-MECH" }` | |
| Subqueries | `{ SELECT ... }` | |
| Named graphs | `GRAPH ?g { ... }`, `FROM`, `FROM NAMED` | Q11 |
| Federation | `SERVICE <https://query.wikidata.org/sparql> { ... }` | |

## 5.4 Querying the ontology itself

Because the schema is in the graph, you can ask questions *about the model*:

```sparql
# all subclasses of Party, any depth
SELECT ?c WHERE { ?c rdfs:subClassOf+ retail:Party }

# properties usable on Orders, with their ranges
SELECT ?p ?range WHERE { ?p rdfs:domain retail:Order ; rdfs:range ?range }

# classes with no definition (documentation lint)
SELECT ?c WHERE { ?c a owl:Class . FILTER NOT EXISTS { ?c skos:definition ?d } FILTER isIRI(?c) }
```

See [01-list-classes-and-properties.rq](../examples/retail/sparql/01-list-classes-and-properties.rq).

## 5.5 Inference: three ways to get "implicit" answers

Alice and Carol are typed **only** as `retail:PremiumCustomer`. Asking for
`?c a retail:Customer` returns only Bob — unless:

1. **Query-time rewriting** with property paths (works on *any* SPARQL
   engine, including Neptune):
   ```sparql
   ?c rdf:type/rdfs:subClassOf* retail:Customer .
   ```
   → [08-all-customers-via-subclass.rq](../examples/retail/sparql/08-all-customers-via-subclass.rq)
2. **Materialisation**: run a reasoner (OWL RL / RDFS) and store the
   inferred triples. Locally:
   `python scripts/run_sparql_local.py --reason` grows 402 → 1184 triples.
   For Neptune, materialise before loading, or write the results back with
   `CONSTRUCT` + `INSERT`.
3. **Store-native reasoning**: GraphDB, Stardog, RDFox, AllegroGraph, Jena
   (InfModel) and Virtuoso can reason at load or query time.
   **Amazon Neptune does not perform OWL/RDFS inference** — use (1) or (2).

## 5.6 Validation with SHACL

SHACL isn't a query language, but it's the other half of "using" an ontology:

```bash
pip install pyshacl
pyshacl -s ontology/retail-shapes.ttl -e ontology/retail-ontology.ttl -i rdfs rdf/retail-data.ttl
# Conforms: True
```

Try breaking the data (e.g. set a rating to 7) and re-run to see the
violation report.

## 5.7 Run everything locally (no database needed)

```bash
cd examples/retail
pip install rdflib pyshacl owlrl
python scripts/run_sparql_local.py --shacl
```

Expected results (abridged):

```
=== 02-electronics-products-incl-subcategories.rq
Laptop Pro 14 | Laptops
Mechanical Keyboard | Computers
USB-C Charger 65W | Electronics
Wireless Earbuds X | Audio

=== 03-order-totals-per-customer.rq
Alice Johnson | 2 | 1498.97
Bob Smith | 1 | 199.98
Carol Diaz | 1 | 179.48

=== 05-customers-who-bought-also-bought.rq
Knowledge Graphs 101 | 1
Laptop Pro 14 | 1
USB-C Charger 65W | 1

=== 07-products-never-ordered.rq
Mechanical Keyboard
```

Other ways to run SPARQL: Apache Jena **Fuseki** (`fuseki-server --file
retail-data.ttl /retail`), **Oxigraph** (`oxigraph serve`), GraphDB Free,
the [Wikidata Query Service](https://query.wikidata.org/) for public data,
and Amazon Neptune ([chapter 12](12-querying-neptune.md)).

## 5.8 Other ways to query RDF

* **GraphQL** over RDF (HyperGraphQL, Stardog, GraphDB, Ontotext Platform).
* **Linked Data Fragments / TPF** — cheap, cacheable server interfaces.
* **SQL over RDF / RDF over SQL**: [R2RML](https://www.w3.org/TR/r2rml/) /
  RML mappings; virtual knowledge graphs with [Ontop](https://ontop-vkg.org/).
* **openCypher over RDF**: Neptune Analytics can load RDF (N-Triples) and
  query it with openCypher (check the current docs for limits).
* **LLM → SPARQL** text-to-query (works best when you feed the model the
  ontology as context).

Next: [6. The retail ordering example, end to end](06-retail-example.md)
