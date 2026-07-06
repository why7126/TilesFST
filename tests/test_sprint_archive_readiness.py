from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-sprint-archive-readiness.py"
SPEC = importlib.util.spec_from_file_location("validate_sprint_archive_readiness", SCRIPT)
assert SPEC and SPEC.loader
validate_sprint_archive_readiness = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_sprint_archive_readiness
SPEC.loader.exec_module(validate_sprint_archive_readiness)


def write_sprint(root: Path, sprint_id: str, changes: list[str], stage: str = "change") -> None:
    sprint_dir = root / "iterations" / stage / sprint_id
    sprint_dir.mkdir(parents=True)
    body = "\n".join(f"  - {change}" for change in changes)
    (sprint_dir / "sprint.yaml").write_text(
        f"status: in_progress\nchanges:\n{body}\n",
        encoding="utf-8",
    )


def write_tasks(root: Path, change_id: str, tasks: list[str], archived: bool = False) -> None:
    if archived:
        change_dir = root / "openspec" / "changes" / "archive" / f"2026-07-04-{change_id}"
    else:
        change_dir = root / "openspec" / "changes" / change_id
    change_dir.mkdir(parents=True)
    (change_dir / "tasks.md").write_text("\n".join(tasks) + "\n", encoding="utf-8")


def test_ready_sprint_passes_when_all_tasks_complete(tmp_path: Path) -> None:
    write_sprint(tmp_path, "sprint-999", ["add-ready"])
    write_tasks(tmp_path, "add-ready", ["- [x] implement", "- [x] test"])

    readiness = validate_sprint_archive_readiness.evaluate_sprint(tmp_path, "sprint-999")

    assert readiness.blockers == []
    assert readiness.changes[0].tasks.done == 2
    assert readiness.changes[0].tasks.total == 2


def test_incomplete_active_change_blocks_sprint_archive(tmp_path: Path) -> None:
    write_sprint(tmp_path, "sprint-999", ["add-not-ready"])
    write_tasks(tmp_path, "add-not-ready", ["- [x] implement", "- [ ] test"])

    readiness = validate_sprint_archive_readiness.evaluate_sprint(tmp_path, "sprint-999")

    assert len(readiness.blockers) == 1
    assert readiness.blockers[0].change_id == "add-not-ready"
    assert readiness.blockers[0].blocker == "1 incomplete task(s)"


def test_incomplete_archived_change_still_blocks_sprint_close(tmp_path: Path) -> None:
    write_sprint(tmp_path, "sprint-999", ["fix-archived-too-early"], stage="archive")
    write_tasks(
        tmp_path,
        "fix-archived-too-early",
        ["- [x] implement", "- [ ] regression test"],
        archived=True,
    )

    readiness = validate_sprint_archive_readiness.evaluate_sprint(tmp_path, "sprint-999")

    assert len(readiness.blockers) == 1
    assert readiness.blockers[0].location == "archived"
    assert readiness.blockers[0].blocker == "1 incomplete task(s)"


def test_missing_tasks_file_blocks_archive(tmp_path: Path) -> None:
    write_sprint(tmp_path, "sprint-999", ["add-missing-tasks"])
    (tmp_path / "openspec" / "changes" / "add-missing-tasks").mkdir(parents=True)

    readiness = validate_sprint_archive_readiness.evaluate_sprint(tmp_path, "sprint-999")

    assert len(readiness.blockers) == 1
    assert readiness.blockers[0].blocker == "tasks.md missing"
