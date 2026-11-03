"""Generators are idempotent: running them again changes nothing."""
import hashlib
import subprocess
import sys

from conftest import REPO, RETAIL

GENERATED = ["examples", "graphs/implementations/providers/aws", "semantic-models/implementations/tools/dbt/retail_dbt/seeds",
             "assets/diagrams"]


def snapshot():
    h = {}
    for root in GENERATED:
        for f in sorted((REPO / root).rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                h[str(f.relative_to(REPO))] = hashlib.sha256(f.read_bytes()).hexdigest()
    return h


def test_generators_are_idempotent():
    before = snapshot()
    for script in ("build_rdf_formats.py", "rdf_to_property_graph.py", "rdf_to_tables.py"):
        subprocess.run([sys.executable, f"scripts/{script}"], cwd=RETAIL, check=True, capture_output=True)
    subprocess.run([sys.executable, "tools/diagrams/build_diagrams.py"], cwd=REPO, check=True, capture_output=True)
    after = snapshot()
    changed = [k for k in after if before.get(k) != after[k]]
    assert not changed, f"generators changed files on a second run: {changed[:5]}"
