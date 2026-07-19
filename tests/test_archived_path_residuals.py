from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import archived_path_residuals


SCRIPT = ROOT / "scripts" / "check-archived-path-residuals.py"


def write_sprint(root: Path, stage: str = "archive") -> Path:
    sprint_dir = root / "iterations" / stage / "sprint-999"
    sprint_dir.mkdir(parents=True)
    (sprint_dir / "sprint.yaml").write_text(
        "\n".join(
            [
                "sprint_id: sprint-999",
                "status: completed",
                f"lifecycle_stage: {stage}",
                "requirements:",
                "  - REQ-9999-demo",
                "bugs: []",
                "changes:",
                "  - add-demo",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (sprint_dir / "sprint.md").write_text("# Sprint\n", encoding="utf-8")
    (sprint_dir / "release-note.md").write_text("# Release\n", encoding="utf-8")
    (sprint_dir / "acceptance-report.md").write_text("# Acceptance\n", encoding="utf-8")
    return sprint_dir


def write_issue(root: Path, body: str = "# Trace\n") -> None:
    issue_dir = root / "issues" / "requirements" / "archive" / "REQ-9999-demo"
    issue_dir.mkdir(parents=True)
    (issue_dir / "trace.md").write_text(body, encoding="utf-8")


def write_archived_change(root: Path, body: str = "- [x] done\n") -> None:
    change_dir = root / "openspec" / "changes" / "archive" / "2026-07-04-add-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "tasks.md").write_text(body, encoding="utf-8")


def test_report_passes_when_scope_has_no_stale_paths(tmp_path: Path) -> None:
    write_sprint(tmp_path)
    write_issue(tmp_path)
    write_archived_change(tmp_path)

    report = archived_path_residuals.build_report("sprint-999", root=tmp_path)

    assert report.ok is True
    assert report.checked_files == 6
    assert report.residuals == []


def test_report_finds_sprint_change_path_residual(tmp_path: Path) -> None:
    sprint_dir = write_sprint(tmp_path)
    write_issue(tmp_path)
    write_archived_change(tmp_path)
    (sprint_dir / "sprint.md").write_text(
        "Old link: iterations/change/sprint-999/sprint.md\n",
        encoding="utf-8",
    )

    report = archived_path_residuals.build_report("sprint-999", root=tmp_path)

    assert report.ok is False
    assert report.residuals[0].kind == "sprint-change-path"
    assert report.residuals[0].old_path == "iterations/change/sprint-999/"
    assert report.residuals[0].new_path == "iterations/archive/sprint-999/"


def test_report_finds_active_change_path_residual_with_archive_suggestion(tmp_path: Path) -> None:
    write_sprint(tmp_path)
    write_issue(tmp_path, "Old change: openspec/changes/add-demo/tasks.md\n")
    write_archived_change(tmp_path)

    report = archived_path_residuals.build_report("sprint-999", root=tmp_path)

    assert report.ok is False
    hit = report.residuals[0]
    assert hit.kind == "active-change-path"
    assert hit.old_path == "openspec/changes/add-demo/"
    assert hit.new_path == "openspec/changes/archive/2026-07-04-add-demo/"


def test_scope_does_not_scan_unrelated_archive_or_generated_files(tmp_path: Path) -> None:
    write_sprint(tmp_path)
    write_issue(tmp_path)
    write_archived_change(tmp_path)
    unrelated = tmp_path / "openspec" / "changes" / "archive" / "2026-07-04-other"
    unrelated.mkdir(parents=True)
    (unrelated / "notes.md").write_text("iterations/change/sprint-999/\n", encoding="utf-8")
    generated = tmp_path / "src" / "web" / "src" / "generated"
    generated.mkdir(parents=True)
    (generated / "client.md").write_text("openspec/changes/add-demo/\n", encoding="utf-8")

    report = archived_path_residuals.build_report("sprint-999", root=tmp_path)

    assert report.ok is True
    checked = {hit.file for hit in report.residuals}
    assert "openspec/changes/archive/2026-07-04-other/notes.md" not in checked


def test_cli_json_returns_nonzero_for_residuals(tmp_path: Path) -> None:
    sprint_dir = write_sprint(tmp_path)
    write_issue(tmp_path)
    write_archived_change(tmp_path)
    (sprint_dir / "sprint.md").write_text("iterations/change/sprint-999/\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--sprint", "sprint-999", "--root", str(tmp_path), "--json"],
        check=False,
        text=True,
        capture_output=True,
    )

    payload = json.loads(result.stdout)
    assert result.returncode == 1
    assert payload["ok"] is False
    assert payload["residual_count"] == 1
