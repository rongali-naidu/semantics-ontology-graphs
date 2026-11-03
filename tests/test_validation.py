"""SHACL must accept the real data and REJECT each kind of broken data."""
import pytest
from pyshacl import validate
from rdflib import Literal, Namespace
from rdflib.namespace import XSD

R = Namespace("https://example.org/retail/ontology#")
EX = Namespace("https://example.org/retail/data/")


def conforms(data, shapes, ontology):
    ok, _, report = validate(data, shacl_graph=shapes, ont_graph=ontology, inference="rdfs")
    return ok, report


def test_retail_data_conforms(data, shapes, ontology):
    ok, report = conforms(data, shapes, ontology)
    assert ok, report


def _drop(g, s, p):
    for o in list(g.objects(s, p)):
        g.remove((s, p, o))


BROKEN = {
    "rating out of range (7 stars)": lambda g: (_drop(g, EX.R1, R.rating), g.add((EX.R1, R.rating, Literal(7)))),
    "order without a customer": lambda g: _drop(g, EX.O1, R.placedBy),
    "order with two customers": lambda g: g.add((EX.O1, R.placedBy, EX.C2)),
    "order without any line": lambda g: _drop(g, EX.O4, R.hasLine),
    "malformed email": lambda g: (_drop(g, EX.C2, R.email), g.add((EX.C2, R.email, Literal("bob-at-example")))),
    "negative price": lambda g: (_drop(g, EX.P3, R.price), g.add((EX.P3, R.price, Literal("-1.00", datatype=XSD.decimal)))),
    "unknown order status": lambda g: (_drop(g, EX.O2, R.status), g.add((EX.O2, R.status, Literal("LOST")))),
    "premium customer without memberSince": lambda g: _drop(g, EX.C3, R.memberSince),
    "line pointing to a customer instead of a product": lambda g: (_drop(g, EX["O1-L1"], R.forProduct),
                                                                   g.add((EX["O1-L1"], R.forProduct, EX.C1))),
}


@pytest.mark.parametrize("name", list(BROKEN))
def test_broken_data_is_rejected(name, data, shapes, ontology):
    BROKEN[name](data)
    ok, _ = conforms(data, shapes, ontology)
    assert not ok, f"SHACL accepted: {name}"
