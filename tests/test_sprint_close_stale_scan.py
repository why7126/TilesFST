from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import sprint_close_stale_scan


SCRIPT = ROOT / "scripts" / "check-sprint-close-stale-scan.py"


def write_sprint(root: Path, *, stage: str = "archive", status: str = "completed") -> Path:
    sprint_dir = root / "iterations" / stage / "sprint-999"
    sprint_dir.mkdir(parents=True)
    (sprint_dir / "sprint.yaml").write_text(
        "\n".join(
            [
                "sprint_id: sprint-999",
                f"status: {status}",
                f"lifecycle_stage: {stage}",
                "requirements:",
                "  - REQ-9999-demo",
                "bugs:",
                "  - BUG-9999-demo",
                "changes:",
                "  - add-demo",
                "  - fix-demo",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (sprint_dir / "sprint.md").write_text("# Sprint\n", encoding="utf-8")
    (sprint_dir / "release-note.md").write_text("# Release\n", encoding="utf-8")
    (sprint_dir / "acceptance-report.md").write_text("# Acceptance\n", encoding="utf-8")
    return sprint_dir


def write_req(root: Path, body: str = "# Trace\n") -> None:
    issue_dir = root / "issues" / "requirements" / "archive" / "REQ-9999-demo"
    issue_dir.mkdir(parents=True)
    (issue_dir / "trace.md").write_text(body, encoding="utf-8")


def write_bug(root: Path, body: str = "# Trace\n") -> None:
    issue_dir = root / "issues" / "bugs" / "archive" / "BUG-9999-demo"
    issue_dir.mkdir(parents=True)
    (issue_dir / "trace.md").write_text(body, encoding="utf-8")


def write_active_change(root: Path, change_id: str, tasks: str = "- [x] implement\n") -> None:
    change_dir = root / "openspec" / "changes" / change_id
    change_dir.mkdir(parents=True)
    (change_dir / "tasks.md").write_text(tasks, encoding="utf-8")


def write_archived_change(root: Path, change_id: str) -> None:
    change_dir = root / "openspec" / "archive" / f"2026-07-04-{change_id}"
    change_dir.mkdir(parents=True)
    (change_dir / "tasks.md").write_text("- [x] implement\n", encoding="utf-8")
    (change_dir / "trace.md").write_text("---\nstatus: done\n---\n# Trace\n", encoding="utf-8")


def req_trace() -> str:
    return """---
status: done
openspec_changes:
  - change_id: add-demo
    status: applied
---
# Trace
"""


def bug_trace() -> str:
    return """---
status: done
related_change: fix-demo
openspec_changes:
  - change_id: fix-demo
    status: archived
---
# Trace
"""


def test_clean_four_piece_passes_and_ignores_unrelated_legacy_fixture(tmp_path: Path) -> None:
    write_sprint(tmp_path)
    write_req(tmp_path, req_trace())
    write_bug(tmp_path, bug_trace())
    write_active_change(tmp_path, "add-demo")
    write_archived_change(tmp_path, "fix-demo")
    unrelated_fixture = tmp_path / "tests" / "fixture.md"
    unrelated_fixture.parent.mkdir()
    unrelated_fixture.write_text("openspec/changes/archive/2026-07-04-fix-demo/\n", encoding="utf-8")

    report = sprint_close_stale_scan.build_report("sprint-999", root=tmp_path)

    assert report.ok is True
    assert report.checked_files == 6
    assert report.hits == []


def test_created_change_blocks_stale_req_and_bug_opsx_wording(tmp_path: Path) -> None:
    sprint_dir = write_sprint(tmp_path)
    write_req(tmp_path, req_trace())
    write_bug(tmp_path, bug_trace())
    write_active_change(tmp_path, "add-demo")
    write_archived_change(tmp_path, "fix-demo")
    (sprint_dir / "sprint.md").write_text(
        "\n".join(
            [
                "REQ-9999-demo 已纳入；待 `/req-opsx` 创建 add-demo。",
                "BUG-9999-demo 已纳入；待 `/bug-opsx` 创建 fix-demo。",
            ]
        ),
        encoding="utf-8",
    )

    report = sprint_close_stale_scan.build_report("sprint-999", root=tmp_path)

    assert report.ok is False
    assert report.blocker_count == 2
    assert {hit.target for hit in report.hits} == {"REQ-9999-demo", "BUG-9999-demo"}
    assert all(hit.kind == "stale-issue-open-change" for hit in report.hits)


def test_applied_or_archived_change_blocks_stale_apply_wording(tmp_path: Path) -> None:
    sprint_dir = write_sprint(tmp_path)
    write_req(tmp_path, req_trace())
    write_bug(tmp_path, bug_trace())
    write_active_change(tmp_path, "add-demo")
    write_archived_change(tmp_path, "fix-demo")
    (sprint_dir / "release-note.md").write_text(
        "\n".join(
            [
                "add-demo 仍待 `/opsx-apply`。",
                "fix-demo proposed；待 archive。",
            ]
        ),
        encoding="utf-8",
    )

    report = sprint_close_stale_scan.build_report("sprint-999", root=tmp_path)

    assert report.ok is False
    assert report.blocker_count == 2
    assert {hit.kind for hit in report.hits} == {"stale-change-apply", "stale-change-archived"}


def test_legacy_archive_path_in_four_piece_blocks(tmp_path: Path) -> None:
    sprint_dir = write_sprint(tmp_path)
    write_req(tmp_path, req_trace())
    write_bug(tmp_path, bug_trace())
    write_active_change(tmp_path, "add-demo")
    write_archived_change(tmp_path, "fix-demo")
    (sprint_dir / "acceptance-report.md").write_text(
        "Archive: openspec/changes/archive/2026-07-04-fix-demo/tasks.md\n",
        encoding="utf-8",
    )

    report = sprint_close_stale_scan.build_report("sprint-999", root=tmp_path)

    assert report.ok is False
    assert report.hits[0].kind == "legacy-change-archive-path"
    assert "openspec/archive" in report.hits[0].suggestion


def test_closed_issue_subdocument_stale_wording_blocks(tmp_path: Path) -> None:
    write_sprint(tmp_path)
    write_req(tmp_path, req_trace())
    write_bug(tmp_path, bug_trace())
    write_archived_change(tmp_path, "add-demo")
    write_archived_change(tmp_path, "fix-demo")
    bug_dir = tmp_path / "issues" / "bugs" / "archive" / "BUG-9999-demo"
    (bug_dir / "acceptance.md").write_text("当前仍待验收，fix-demo 待归档。\n", encoding="utf-8")

    report = sprint_close_stale_scan.build_report("sprint-999", root=tmp_path)

    assert report.ok is False
    assert any(hit.kind == "issue-subdocument-stale-state" for hit in report.hits)
    assert any(hit.file.endswith("BUG-9999-demo/acceptance.md") for hit in report.hits)


def test_auto_sprint_requires_single_in_progress_sprint(tmp_path: Path) -> None:
    write_sprint(tmp_path, stage="archive", status="completed")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--sprint", "auto", "--root", str(tmp_path), "--json"],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 2
    assert "pass --sprint sprint-xxx" in result.stdout


def test_cli_json_returns_nonzero_for_blockers(tmp_path: Path) -> None:
    sprint_dir = write_sprint(tmp_path)
    write_req(tmp_path, req_trace())
    write_bug(tmp_path, bug_trace())
    write_active_change(tmp_path, "add-demo")
    write_archived_change(tmp_path, "fix-demo")
    (sprint_dir / "sprint.md").write_text("add-demo 仍待 `/opsx-apply`。\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--sprint", "sprint-999", "--root", str(tmp_path), "--json"],
        check=False,
        text=True,
        capture_output=True,
    )

    payload = json.loads(result.stdout)
    assert result.returncode == 1
    assert payload["ok"] is False
    assert payload["blocker_count"] == 1
