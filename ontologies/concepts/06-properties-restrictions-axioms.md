# 6. Properties, restrictions and axioms

Three words that get blurred:

| | What it is | Retail example |
|---|---|---|
| **Property** | the vocabulary: a kind of relationship or attribute | `retail:placedBy`, `retail:price` |
| **Restriction** | a *condition* built from a property, describing an anonymous class ("all things that…") | `placedBy exactly 1 Customer` |
| **Axiom** | a statement asserted as **true** in the ontology: subclass, equivalence, property characteristics, facts | `Order ⊑ (placedBy exactly 1 Customer)`, `placedBy` is functional |

So a restriction on its own says nothing; an axiom that uses it does.
Declaring a property functional is itself an axiom (a *property axiom*).

## 6.1 TBox, ABox, RBox

| Box | Letter | Holds | Retail |
|---|---|---|---|
| **TBox** | **T**erminological | class axioms: subclass, equivalence, disjointness, restrictions | `PremiumCustomer ⊑ Customer` |
| **RBox** | **R**ole | property axioms: characteristics, sub-properties, inverses, chains | `subCategoryOf` is transitive; `placedOrder` inverse of `placedBy` |
| **ABox** | **A**ssertional | facts about individuals: class and property assertions | `Alice : PremiumCustomer`, `placedBy(O1, Alice)` |

Many texts fold the RBox into the TBox (schema = TBox + RBox).

## 6.2 Kinds of properties

| Kind | Connects | Retail |
|---|---|---|
| **Object property** | individual → individual | `ex:O1 retail:placedBy ex:C1` |
| **Datatype property** | individual → literal (string, number, date…) | `ex:P1 retail:price 1299.00` |
| **Annotation property** | anything → documentation; ignored by reasoning | `rdfs:label`, `skos:definition` |

## 6.3 Property characteristics

| Characteristic | Meaning | Applies to | Retail / example |
|---|---|---|---|
| **Functional** | at most one value per subject (0..1) | object **and** datatype | `placedBy`, `email`, `price` |
| **Inverse functional** | at most one subject per value (the value identifies the subject) | object only (for data values use `owl:hasKey`) | `hasLine`: a line belongs to one order |
| **Transitive** | A→B and B→C ⇒ A→C | object | `subCategoryOf`: Laptops → Computers → Electronics |
| **Symmetric** | A→B ⇒ B→A | object | `isSiblingOf`, `hasNeighbor` |
| **Asymmetric** | A→B ⇒ never B→A | object | `isParentOf` |
| **Reflexive** | every individual relates to itself | object | rare; it applies to *everything*, so use with care |
| **Irreflexive** | nothing relates to itself | object | `isStrictlyTallerThan` |
| **Inverse of** | P(a,b) ⇔ Q(b,a) | object | `placedBy` ⇔ `placedOrder` |
| **Property chain** | P1 ∘ P2 ∘ … ⊑ Q | object | `placedOrder ∘ hasLine ∘ forProduct ⊑ purchased` |
| **Sub-property** | P ⊑ Q | both | `subCategoryOf ⊑ skos:broader` |

(OWL 2 DL also bans some combinations, e.g. a transitive property can't be
functional or used in a cardinality restriction.)

## 6.4 The functional-property catch (open world)

**Functional = "at most one", i.e. 0..1.** It does not make the property
mandatory, and a second value does **not** get rejected the way a database
would reject it. What happens depends on the property kind:

| Second value for… | What an OWL reasoner concludes | Demo |
|---|---|---|
| a functional **object** property | the two individuals are **the same thing** (`owl:sameAs`) | O1 placedBy C1 *and* C2 ⇒ `C1 owl:sameAs C2` |
| a functional **datatype** property | the two literals would have to be equal; they can't be, so the ontology is **inconsistent** | two different emails for Alice ⇒ inconsistency |

```text
$ python scripts/demo_reasoning.py
ok   5a. functional object property, 2 values -> C1 owl:sameAs C2: True
ok   5b. functional data property, 2 values -> impossible "…" owl:sameAs "…" (inconsistent): True
```

(Complete OWL DL reasoners such as HermiT and Pellet *report* the
inconsistency in 5b. The lightweight OWL RL reasoner used in CI derives the
impossible equality, which is the same signal.)

**Making it mandatory (exactly 1):** functional isn't enough. Either add a
cardinality restriction to the class (what the retail ontology does for
orders):

```turtle
retail:Order rdfs:subClassOf [ a owl:Restriction ;
    owl:onProperty retail:placedBy ; owl:qualifiedCardinality 1 ; owl:onClass retail:Customer ] .
```

…which in the open world still *infers* that some customer exists rather
than rejecting an order without one, or, to actually **reject** bad data,
add a SHACL shape (`sh:minCount 1 ; sh:maxCount 1`), as
[`retail-shapes.ttl`](../../examples/retail/ontology/retail-shapes.ttl) does.

## 6.5 Restrictions

A restriction = property + condition, describing the set of individuals that
satisfy it.

| Restriction | Manchester syntax | Reads as |
|---|---|---|
| `owl:someValuesFrom` | `purchased some LaptopProduct` | at least one value is a … (existential) |
| `owl:allValuesFrom` | `hasLine only OrderLine` | every value, if any, is a … (universal; true with zero values) |
| `owl:hasValue` | `status value "DELIVERED"` | has this specific value |
| `owl:minCardinality` / `min` | `hasLine min 1` | at least n values |
| `owl:maxCardinality` / `max` | `placedBy max 1` | at most n values |
| `owl:cardinality` / `exactly` | `placedBy exactly 1 Customer` | exactly n (qualified with a class) |

Used on the right of `rdfs:subClassOf` they're **necessary** conditions
(primitive class). Used inside `owl:equivalentClass` they're **necessary and
sufficient** (defined class), and the reasoner classifies individuals into
them. See [chapter 5](05-ontology-for-software-engineers.md#55-primitive-vs-defined-classes-nominal-vs-duck-typing).

## 6.6 Where each appears in the retail ontology

| Construct | In [`retail-ontology.ttl`](../../examples/retail/ontology/retail-ontology.ttl) |
|---|---|
| subclass axioms | `PremiumCustomer ⊑ Customer ⊑ Party`, `Seller ⊑ Party` |
| equivalence | `retail:Product ≡ schema:Product`; defined classes in `retail-defined-classes.ttl` |
| disjointness | `AllDisjointClasses(Party Product Category Order OrderLine Address Review)`, `Customer ⊥ Seller` |
| functional | `placedBy`, `forProduct`, `email`, `price`, `orderDate`, `quantity`, ... |
| inverse functional | `hasLine` |
| transitive | `subCategoryOf` |
| inverse | `placedBy` ⇔ `placedOrder` |
| property chain | `purchased` |
| cardinality restrictions | `Order ⊑ placedBy exactly 1 Customer`, `Order ⊑ hasLine min 1 OrderLine`, `OrderLine ⊑ forProduct exactly 1 Product` |
| datatype restrictions | `rating` ∈ integer[1..5]; `status` ∈ {PLACED, SHIPPED, DELIVERED, CANCELLED} |

Next: [7. Mapping an ontology to tables and columns](07-mapping-ontology-to-tables.md)
