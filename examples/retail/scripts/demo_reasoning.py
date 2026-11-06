#!/usr/bin/env python3
"""Show what an OWL reasoner does with the retail ontology (and check it).

    pip install rdflib owlrl
    python scripts/demo_reasoning.py

Runs OWL 2 RL reasoning (owlrl) over ontology + data and prints:
  1. subclass inference      Naidu and Carol (PremiumCustomer) are Customers
  2. inverse properties      placedBy  ->  placedOrder
  3. property chain          placedOrder / hasLine / forProduct  ->  purchased
  4. defined classes         DeliveredOrder, LaptopBuyer (retail-defined-classes.ttl)
  5. the open-world "functional" catch:
       a second value for a functional OBJECT property  -> owl:sameAs is inferred
       a second value for a functional DATA property    -> "x" owl:sameAs "y" between two
                                                           different literals: inconsistent
"""
import sys
from pathlib import Path

import owlrl
from rdflib import Graph, Literal, Namespace
from rdflib.namespace import OWL, RDF

ROOT = Path(__file__).resolve().parent.parent
R = Namespace("https://example.org/retail/ontology#")
EX = Namespace("https://example.org/retail/data/")


def reason(*extra_triples):
    g = Graph()
    for f in ("ontology/retail-ontology.ttl", "ontology/retail-defined-classes.ttl", "rdf/retail-data.ttl"):
        g.parse(ROOT / f)
    for t in extra_triples:
        g.add(t)
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
    return g


def names(g, s_iter):
    return sorted(str(g.value(s, R.name) or s.split("/")[-1]) for s in set(s_iter))


def main() -> int:
    g = reason()
    checks = [
        ("1. subclass: all Customers", names(g, g.subjects(RDF.type, R.Customer)),
         ["Bob Smith", "Carol Diaz", "Naidu Rongali"]),
        ("2. inverse: Naidu placedOrder", sorted(o.split("/")[-1] for o in g.objects(EX.C1, R.placedOrder)), ["O1", "O3"]),
        ("3. chain: Naidu purchased", sorted(o.split("/")[-1] for o in g.objects(EX.C1, R.purchased)), ["P1", "P2", "P3"]),
        ("4a. defined: DeliveredOrder", sorted(s.split("/")[-1] for s in set(g.subjects(RDF.type, R.DeliveredOrder))), ["O1", "O3"]),
        ("4b. defined: LaptopBuyer", names(g, g.subjects(RDF.type, R.LaptopBuyer)), ["Naidu Rongali"]),
    ]
    # 5a. placedBy is functional: say O1 was ALSO placed by C2 ...
    g2 = reason((EX.O1, R.placedBy, EX.C2))
    same = (EX.C1, OWL.sameAs, EX.C2) in g2
    checks.append(("5a. functional object property, 2 values -> C1 owl:sameAs C2", [str(same)], ["True"]))
    # 5b. email is functional: give Naidu a second, different email ...
    #     OWL RL's functional-property rule concludes the two VALUES are the same
    #     (owl:sameAs). Two different literals can never be equal, so the data is
    #     inconsistent. Complete OWL DL reasoners (HermiT, Pellet) report that;
    #     owlrl only derives the impossible sameAs, which is what we check here.
    g3 = reason((EX.C1, R.email, Literal("naidu@work.example")))
    clash = (Literal("naidu@example.com"), OWL.sameAs, Literal("naidu@work.example")) in g3
    checks.append(("5b. functional data property, 2 values -> impossible \"…\" owl:sameAs \"…\" (inconsistent)",
                   [str(clash)], ["True"]))

    ok = True
    for label, got, want in checks:
        status = "ok  " if got == want else "FAIL"
        ok &= got == want
        print(f"{status} {label}: {', '.join(got)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
