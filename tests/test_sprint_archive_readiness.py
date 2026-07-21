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


def archived_change_dir(root: Path, change_id: str) -> Path:
    return root / "openspec" / "changes" / "archive" / f"2026-07-04-{change_id}"


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


def test_archived_change_with_trace_passes_without_fallback_summary(tmp_path: Path) -> None:
    write_sprint(tmp_path, "sprint-999", ["fix-with-trace"])
    write_tasks(tmp_path, "fix-with-trace", ["- [x] implement", "- [x] test"], archived=True)
    (archived_change_dir(tmp_path, "fix-with-trace") / "trace.md").write_text(
        "---\nstatus: done\n---\n# Trace\n",
        encoding="utf-8",
    )

    readiness = validate_sprint_archive_readiness.evaluate_sprint(tmp_path, "sprint-999")

    assert readiness.blockers == []
    assert readiness.changes[0].trace_exists is True
    assert readiness.changes[0].fallback_summary_status == "trace-present"


def test_archived_change_missing_trace_passes_with_complete_fallback_summary(tmp_path: Path) -> None:
    write_sprint(tmp_path, "sprint-999", ["fix-with-summary"])
    write_tasks(tmp_path, "fix-with-summary", ["- [x] implement", "- [x] test"], archived=True)
    summary = """# Proposal

## 归档验证摘要

- 验证命令：`pytest tests/test_demo.py`，验证结果：pass。
- 验收结论：通过。
- Issue/Sprint 状态：BUG-9999 done，Sprint sprint-999 completed。
- 归档路径：openspec/changes/archive/2026-07-04-fix-with-summary。
"""
    (archived_change_dir(tmp_path, "fix-with-summary") / "proposal.md").write_text(summary, encoding="utf-8")

    readiness = validate_sprint_archive_readiness.evaluate_sprint(tmp_path, "sprint-999")

    assert readiness.blockers == []
    assert readiness.changes[0].trace_exists is False
    assert readiness.changes[0].fallback_summary_status == "pass"
    assert readiness.changes[0].fallback_summary_file == (
        "openspec/changes/archive/2026-07-04-fix-with-summary/proposal.md"
    )


def test_archived_change_missing_trace_and_summary_blocks(tmp_path: Path) -> None:
    write_sprint(tmp_path, "sprint-999", ["fix-missing-summary"])
    write_tasks(tmp_path, "fix-missing-summary", ["- [x] implement", "- [x] test"], archived=True)

    readiness = validate_sprint_archive_readiness.evaluate_sprint(tmp_path, "sprint-999")

    assert len(readiness.blockers) == 1
    blocker = readiness.blockers[0].blocker or ""
    assert "missing trace.md" in blocker
    assert "proposal.md" in blocker
    assert "validation" in blocker


def test_archived_change_fallback_summary_missing_required_items_blocks(tmp_path: Path) -> None:
    write_sprint(tmp_path, "sprint-999", ["fix-incomplete-summary"])
    write_tasks(tmp_path, "fix-incomplete-summary", ["- [x] implement", "- [x] test"], archived=True)
    (archived_change_dir(tmp_path, "fix-incomplete-summary") / "tasks.md").write_text(
        "- [x] implement\n\n## 归档验证摘要\n\n- 验收结论：通过。\n",
        encoding="utf-8",
    )

    readiness = validate_sprint_archive_readiness.evaluate_sprint(tmp_path, "sprint-999")

    assert len(readiness.blockers) == 1
    assert readiness.blockers[0].fallback_summary_missing == [
        "validation",
        "issue_or_sprint_status",
        "archive_evidence",
    ]


def test_missing_tasks_file_blocks_archive(tmp_path: Path) -> None:
    write_sprint(tmp_path, "sprint-999", ["add-missing-tasks"])
    (tmp_path / "openspec" / "changes" / "add-missing-tasks").mkdir(parents=True)

    readiness = validate_sprint_archive_readiness.evaluate_sprint(tmp_path, "sprint-999")

    assert len(readiness.blockers) == 1
    assert readiness.blockers[0].blocker == "tasks.md missing"


def test_large_sprint_readiness_exposes_change_batches(tmp_path: Path) -> None:
    change_ids = [f"add-batch-{index:02d}" for index in range(1, 12)]
    write_sprint(tmp_path, "sprint-999", change_ids)
    for index, change_id in enumerate(change_ids, start=1):
        tasks = ["- [x] implement", "- [x] test"]
        if index == 11:
            tasks[-1] = "- [ ] test"
        write_tasks(tmp_path, change_id, tasks)

    readiness = validate_sprint_archive_readiness.evaluate_sprint(tmp_path, "sprint-999")
    payload = validate_sprint_archive_readiness.readiness_to_json(readiness, force=False)

    assert readiness.change_batches["applicable"] is True
    assert readiness.change_batches["batch_count"] == 3
    assert readiness.change_batches["batches"][0]["change_ids"] == change_ids[:5]
    assert readiness.change_batches["batches"][2]["counts"]["blockers"] == 1
    assert "batch-003" in payload
