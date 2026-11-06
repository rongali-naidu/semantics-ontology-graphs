"""OWL RL inferences the docs rely on (ontologies chapters 1, 5, 6)."""
import demo_reasoning as d
from rdflib import Literal
from rdflib.namespace import OWL, RDF


def test_subclass_inference():
    g = d.reason()
    assert set(d.names(g, g.subjects(RDF.type, d.R.Customer))) == {"Naidu Rongali", "Bob Smith", "Carol Diaz"}


def test_inverse_and_chain():
    g = d.reason()
    assert set(g.objects(d.EX.C1, d.R.placedOrder)) == {d.EX.O1, d.EX.O3}
    assert set(g.objects(d.EX.C1, d.R.purchased)) == {d.EX.P1, d.EX.P2, d.EX.P3}


def test_transitive_categories():
    g = d.reason()
    assert (d.EX["CAT-LAPTOPS"], d.R.subCategoryOf, d.EX["CAT-ELECTRONICS"]) in g


def test_defined_classes_classify_individuals():
    g = d.reason()
    assert set(g.subjects(RDF.type, d.R.DeliveredOrder)) == {d.EX.O1, d.EX.O3}
    assert set(g.subjects(RDF.type, d.R.LaptopBuyer)) == {d.EX.C1}


def test_functional_object_property_infers_sameas():
    g = d.reason((d.EX.O1, d.R.placedBy, d.EX.C2))
    assert (d.EX.C1, OWL.sameAs, d.EX.C2) in g


def test_functional_data_property_conflict_is_detectable():
    g = d.reason((d.EX.C1, d.R.email, Literal("naidu@work.example")))
    assert (Literal("naidu@example.com"), OWL.sameAs, Literal("naidu@work.example")) in g


def test_demo_script_passes():
    assert d.main() == 0
