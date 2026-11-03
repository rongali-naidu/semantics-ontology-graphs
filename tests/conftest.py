"""Shared fixtures. The checks live in examples/retail/scripts; tests import them."""
import sys
from pathlib import Path

import pytest
from rdflib import Graph

REPO = Path(__file__).resolve().parent.parent
RETAIL = REPO / "examples/retail"
sys.path.insert(0, str(RETAIL / "scripts"))


@pytest.fixture
def ontology() -> Graph:
    return Graph().parse(RETAIL / "ontology/retail-ontology.ttl")


@pytest.fixture
def data() -> Graph:
    return Graph().parse(RETAIL / "rdf/retail-data.ttl")


@pytest.fixture
def shapes() -> Graph:
    return Graph().parse(RETAIL / "ontology/retail-shapes.ttl")
