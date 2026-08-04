from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.workflow_sync import collect


SCRIPT = ROOT / "scripts" / "add-sprint-scope-item.py"
SPEC = importlib.util.spec_from_file_location("add_sprint_scope_item", SCRIPT)
add_sprint_scope_item = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = add_sprint_scope_item
SPEC.loader.exec_module(add_sprint_scope_item)


def test_add_sprint_scope_item_persists_bug_and_change_for_apply_gate(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(collect, "ROOT", tmp_path)
    monkeypatch.setitem(add_sprint_scope_item.load_sprint.__globals__, "ROOT", tmp_path)
    monkeypatch.setitem(add_sprint_scope_item.read_text.__globals__, "ROOT", tmp_path)
    sprint_dir = tmp_path / "iterations/change/sprint-999"
    sprint_dir.mkdir(parents=True)
    (sprint_dir / "sprint.yaml").write_text(
        """sprint_id: sprint-999
status: planning
lifecycle_stage: change
capacity:
  developers: 2
  testers: 1
  capacity_person_days: 30
requirements: []
bugs:
  - BUG-0001-existing
changes:
  - fix-existing
estimated_story_points: 3
estimated_person_days: 3
capacity_usage: 0.1
fix_buffer_person_days: 27
fix_buffer_ratio: 0.9
scope_estimates:
  - id: BUG-0001-existing
    bug: BUG-0001-existing
    change: fix-existing
    size: M
    story_points: 3
    estimated_person_days: 3
    rationale: existing
capacity_gate:
  result: pass
  capacity_person_days: 30
  estimated_person_days: 3
  capacity_usage: 0.1
  note: existing
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(add_sprint_scope_item, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", [
        str(SCRIPT),
        "--sprint",
        "sprint-999",
        "--bug",
        "BUG-0111-usage-docs-previous-version-semver-sort",
        "--change",
        "fix-usage-docs-previous-version-semver-sort",
        "--size",
        "S",
        "--story-points",
        "1",
        "--person-days",
        "1",
        "--rationale",
        "usage docs SemVer source version fix",
    ])

    assert add_sprint_scope_item.main() == 0
    text = (sprint_dir / "sprint.yaml").read_text(encoding="utf-8")
    assert "  - BUG-0111-usage-docs-previous-version-semver-sort" in text
    assert "  - fix-usage-docs-previous-version-semver-sort" in text
    assert "    bug: BUG-0111-usage-docs-previous-version-semver-sort" in text
    assert "    change: fix-usage-docs-previous-version-semver-sort" in text
    assert "estimated_story_points: 4" in text
    assert "estimated_person_days: 4" in text
    assert "capacity_usage: 0.1333" in text

    assert collect.find_sprints_for_change("fix-usage-docs-previous-version-semver-sort") == [
        "sprint-999"
    ]
