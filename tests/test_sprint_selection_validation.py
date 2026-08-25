import importlib.util
import sys
from pathlib import Path

import pytest

SCRIPT_PATH = Path("scripts/validate-sprint-selection.py")
SPEC = importlib.util.spec_from_file_location("validate_sprint_selection", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

SprintInventory = MODULE.SprintInventory
validate_selection = MODULE.validate_selection


@pytest.mark.parametrize(
    ("requested", "inventory", "expected_ok"),
    [
        (None, SprintInventory(active=[], known=["sprint-001"], next_id="sprint-002"), True),
        (None, SprintInventory(active=["sprint-002"], known=["sprint-001", "sprint-002"], next_id="sprint-003"), True),
        (
            None,
            SprintInventory(active=["sprint-002", "sprint-003"], known=["sprint-001", "sprint-002", "sprint-003"], next_id="sprint-004"),
            False,
        ),
        ("sprint-004", SprintInventory(active=["sprint-003"], known=["sprint-001", "sprint-003"], next_id="sprint-004"), True),
        ("sprint-005", SprintInventory(active=["sprint-003"], known=["sprint-001", "sprint-003"], next_id="sprint-004"), False),
        (
            "sprint-004",
            SprintInventory(active=["sprint-002", "sprint-003"], known=["sprint-001", "sprint-002", "sprint-003"], next_id="sprint-004"),
            False,
        ),
    ],
)
def test_validate_selection_rules(requested, inventory, expected_ok):
    ok, _ = validate_selection(requested, inventory)

    assert ok is expected_ok


def test_script_path_exists():
    assert SCRIPT_PATH.exists()
