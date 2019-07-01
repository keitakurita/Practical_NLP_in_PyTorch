from typing import *
import json
from enum import Enum

class VerificationError(Exception):
    pass

def get_cell_contents_string(cell: dict) -> str:
    if isinstance(cell["source"], str):
        return cell["source"]
    else:
        return "\n".join(cell["source"])

def get_cell_contents_lines(cell: dict) -> str:
    if isinstance(cell["source"], str):
        return cell["source"].split("\n")
    else:
        return cell["source"]

def assert_has_key(d: dict, key: str, dict_name: str):
    if key not in d:
        raise VerificationError(f"{key} needs to be included in {dict_name}")

def verify_notebook(notebook: dict):
    assert_has_key(notebook, "metadata", "notebook")
    assert_has_key(notebook, "cells", "notebook")

    for i, cell in enumerate(notebook["cells"]):
        assert_has_key(cell, "cell_type", f"cell#{i}")
        assert_has_key(cell, "source", f"cell#{i}")

class Notebook:
    def __init__(self, fname: str):
        with open(fname, "rt") as f:
            self.data = json.load(f)
        verify_notebook(self.data)

    def filter(self, predicate: Callable[[dict], bool]):
        new_cells = [cell for cell in self.data["cells"] if predicate(cell)]
        new_data = dict(self.data)
        new_data["cells"] = new_cells
        verify_notebook(new_data)
        self.data = new_data
        return self

    def write(self, fname: str):
        verify_notebook(self.data)
        with open(fname, "wt") as f:
            json.dump(self.data, f)

# scrapping cells that are only for drafts
def _do_not_scrap(cell: dict):
    if cell["cell_type"] == "code":
        lines = get_cell_contents_lines(cell)
        if len(lines) > 0:
            if lines[0].startswith("#scrap"):
                return False
    return True


def scrap_cells(input: str, output: str):
    (Notebook(input)
     .filter(predicate=_do_not_scrap)
     .write(output))

if __name__ == "__main__":
    import fire
    fire.Fire({"scrap": scrap_cells})
