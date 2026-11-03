# 5. Ontologies for software engineers: from OOP to OWL

If you know object-oriented programming you already know most of an
ontology's vocabulary: classes, instances, attributes, references,
inheritance. The differences are where the power (and the surprises) are.

## 5.1 The same domain as Python classes and as an ontology

**OOP (imperative, closed):**

```python
from dataclasses import dataclass, field

@dataclass
class Customer:
    name: str
    email: str

@dataclass
class PremiumCustomer(Customer):          # nominal inheritance: you must say it
    member_since: str = ""

@dataclass
class Order:
    order_id: str
    placed_by: Customer                    # the reference lives INSIDE Order
    status: str = "PLACED"

alice = PremiumCustomer("Alice Johnson", "alice@example.com", "2024-03-15")
o1 = Order("O1", placed_by=alice, status="DELIVERED")
# alice does not know about o1 unless you write code to keep both sides in sync
```

**Ontology (declarative, open)**, from [`retail-ontology.ttl`](../../examples/retail/ontology/retail-ontology.ttl)
and [`retail-data.ttl`](../../examples/retail/rdf/retail-data.ttl):

```turtle
# --- TBox: the schema ---------------------------------------------------
retail:Customer        a owl:Class .
retail:PremiumCustomer a owl:Class ; rdfs:subClassOf retail:Customer .
retail:Order           a owl:Class .

retail:placedBy a owl:ObjectProperty , owl:FunctionalProperty ;   # a standalone
    rdfs:domain retail:Order ; rdfs:range retail:Customer ;       # contract
    owl:inverseOf retail:placedOrder .

retail:name a owl:DatatypeProperty ; rdfs:range xsd:string .

# --- ABox: the data -----------------------------------------------------
ex:C1 a retail:PremiumCustomer ; retail:name "Alice Johnson" .
ex:O1 a retail:Order ; retail:placedBy ex:C1 ; retail:status "DELIVERED" .
```

## 5.2 Translation table

| OOP | Ontology (OWL / RDFS) | Note |
|---|---|---|
| class `Customer` | class `retail:Customer` (`owl:Class`) | a set of individuals, not a code template |
| object `alice = Customer(...)` | individual `ex:C1` (ABox) | has a global IRI, not a memory address |
| reference `order.placed_by` | object property `retail:placedBy` | an edge between individuals |
| primitive field `order.status` | datatype property `retail:status` | an edge to a literal |
| type annotation `placed_by: Customer` | `rdfs:domain` / `rdfs:range` | **infers types; does not check them** (5.4) |
| inheritance `class B(A)` | `rdfs:subClassOf` | multiple inheritance is normal |
| interface / abstract class | **primitive class** | membership only if asserted (5.5) |
| duck / structural typing | **defined class** (`owl:equivalentClass`) | membership computed by a reasoner (5.5) |
| method that keeps both sides in sync | axiom `owl:inverseOf` | the reasoner derives the other direction |
| computed property | property chain, `derived` rules | `purchased = placedOrder / hasLine / forProduct` |
| validation in setters | SHACL shapes | separate from the ontology |
| unique constraint | `owl:FunctionalProperty`, `owl:hasKey` | but see the open-world catch in [chapter 6](06-properties-restrictions-axioms.md) |

## 5.3 Properties are standalone, not owned by a class

In OOP, `placed_by` belongs to `Order`. In OWL, `retail:placedBy` is its own
first-class thing with an IRI, documentation and rules (functional, inverse
of `placedOrder`). Classes don't "contain" properties; properties point at
classes through domain and range. That's why you can:

* reuse one property across classes (`retail:name` is used for Customers,
  Sellers, Products and Categories, with no domain at all);
* add a new property to existing data without changing any class;
* query "everything connected to Alice" without knowing the class layout.

## 5.4 Domain and range infer; they don't validate

The most common misconception: `rdfs:domain retail:Order` does **not** mean
"only Orders may use placedBy". It means "**whatever** uses placedBy **is**
an Order":

```turtle
ex:Bob retail:placedBy ex:P1 .     # nonsense data
# a reasoner concludes:  ex:Bob a retail:Order .   ex:P1 a retail:Customer .
```

For "reject data that breaks the rules", use **SHACL**
([`retail-shapes.ttl`](../../examples/retail/ontology/retail-shapes.ttl)), the
closed-world counterpart to OWL.

## 5.5 Primitive vs defined classes: nominal vs duck typing

| | Primitive class | Defined class |
|---|---|---|
| OWL | `rdfs:subClassOf` (**necessary** conditions only) | `owl:equivalentClass` (**necessary and sufficient**) |
| OOP analogy | abstract class / interface you must explicitly extend | structural / duck typing: if it has the shape, it *is* one |
| Membership | only individuals you assert | every individual the reasoner can prove matches |
| Retail | `retail:Customer`, `retail:Order` | `retail:DeliveredOrder`, `retail:LaptopBuyer` |

The retail defined classes ([`retail-defined-classes.ttl`](../../examples/retail/ontology/retail-defined-classes.ttl)):

```turtle
# DeliveredOrder ≡ Order ⊓ (status value "DELIVERED")
retail:DeliveredOrder owl:equivalentClass [ owl:intersectionOf ( retail:Order
    [ a owl:Restriction ; owl:onProperty retail:status ; owl:hasValue "DELIVERED" ] ) ] .

# LaptopBuyer ≡ Customer ⊓ ∃purchased.(inCategory value Laptops)
retail:LaptopBuyer owl:equivalentClass [ owl:intersectionOf ( retail:Customer
    [ a owl:Restriction ; owl:onProperty retail:purchased ;
      owl:someValuesFrom [ a owl:Restriction ; owl:onProperty retail:inCategory ;
                           owl:hasValue ex:CAT-LAPTOPS ] ] ) ] .
```

No order or customer in the data is typed with these classes, yet:

```text
$ python scripts/demo_reasoning.py
ok   4a. defined: DeliveredOrder: O1, O3
ok   4b. defined: LaptopBuyer: Alice Johnson
```

The reasoner classified them. In OOP terms, it *re-typed existing objects*
from their properties, which no mainstream OOP runtime does. Two caveats to
the duck-typing analogy:

* it's **logical classification**, not a runtime cast: the individual
  simply also belongs to the class, alongside its other classes;
* the **open world** applies: if the data doesn't *prove* membership, the
  individual isn't classified, but it also isn't proven *not* to belong.

## 5.6 Where OOP intuition breaks

| OOP assumption | Ontology reality |
|---|---|
| An object has exactly one class | An individual can be in many classes at once (Alice: PremiumCustomer, Customer, Party, schema:Person, LaptopBuyer) |
| Missing field = null / false | Missing fact = **unknown** (open world) |
| Two objects are different objects | Two IRIs may denote the **same** thing (no unique-name assumption) unless declared `owl:differentFrom` |
| Constraints reject bad data | OWL axioms **infer** (or report inconsistency); SHACL rejects |
| Schema changes need code changes | Add triples; existing data keeps working |
| Logic lives in methods | Logic lives in declarative axioms, applied by a reasoner |

## 5.7 When to use which

* **OOP / application models** for behaviour, state, transactions, UI,
  algorithms, i.e. running software.
* **Ontologies** for shared meaning across systems and teams, integrating
  data from many sources, and deriving new facts with rules, i.e. describing
  the domain.

Most real systems use both: the ontology is the contract; services map their
objects to it (and generate code from it, e.g. with an Ontology SDK).

Try it: `python scripts/demo_reasoning.py` (all inferences above, checked in CI).

Next: [6. Properties, restrictions and axioms](06-properties-restrictions-axioms.md)
