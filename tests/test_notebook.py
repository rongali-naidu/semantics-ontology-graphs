"""The quickstart notebook runs top to bottom without errors."""
import nbformat
from nbclient import NotebookClient

from conftest import REPO


def test_quickstart_notebook_runs():
    path = REPO / "notebooks/quickstart.ipynb"
    nb = nbformat.read(path, as_version=4)
    NotebookClient(nb, timeout=300, kernel_name="python3",
                   resources={"metadata": {"path": str(path.parent)}}).execute()
    errors = [o for c in nb.cells for o in c.get("outputs", []) if o.get("output_type") == "error"]
    assert not errors, errors
