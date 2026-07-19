from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.workflow_sync.collect import IssueRecord  # noqa: E402
from scripts.workflow_sync import collect, issue_status_residuals  # noqa: E402
from scripts.workflow_sync.issue_status_residuals import (  # noqa: E402
    issue_reconcile_blockers,
    reconcile_issue_status_residuals,
    scan_issue_status_residuals,
)

SCRIPT = ROOT / "scripts" / "promote-issues-for-archive.py"
SPEC = importlib.util.spec_from_file_location("promote_issues_for_archive", SCRIPT)
assert SPEC and SPEC.loader
promote_issues_for_archive = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = promote_issues_for_archive
SPEC.loader.exec_module(promote_issues_for_archive)


def test_bug_subdocument_frontmatter_residual_blocks(tmp_path: Path) -> None:
    issue_dir = tmp_path / "issues" / "bugs" / "review" / "BUG-9999-demo"
    issue_dir.mkdir(parents=True)
    (issue_dir / "bug.md").write_text("---\nstatus: draft\n---\n# Bug\n", encoding="utf-8")

    residuals = scan_issue_status_residuals(issue_dir)

    assert len(residuals) == 1
    assert residuals[0].issue_id == "BUG-9999-demo"
    assert residuals[0].file == issue_dir / "bug.md"
    assert residuals[0].source == "frontmatter"
    assert residuals[0].status == "draft"


def test_req_subdocument_yaml_block_residual_blocks(tmp_path: Path) -> None:
    issue_dir = tmp_path / "issues" / "requirements" / "review" / "REQ-9999-demo"
    issue_dir.mkdir(parents=True)
    (issue_dir / "acceptance.md").write_text("# AC\n\n```yaml\nstatus: pending_review\n```\n", encoding="utf-8")

    residuals = scan_issue_status_residuals(issue_dir)

    assert len(residuals) == 1
    assert residuals[0].issue_id == "REQ-9999-demo"
    assert residuals[0].file == issue_dir / "acceptance.md"
    assert residuals[0].source == "yaml_block"
    assert residuals[0].status == "pending_review"


def test_closed_subdocument_statuses_do_not_block(tmp_path: Path) -> None:
    issue_dir = tmp_path / "issues" / "requirements" / "review" / "REQ-9999-demo"
    issue_dir.mkdir(parents=True)
    (issue_dir / "requirement.md").write_text("---\nstatus: done\n---\n# Requirement\n", encoding="utf-8")
    (issue_dir / "trace.md").write_text("# Trace\n\n```yaml\nstatus: archived\n```\n", encoding="utf-8")

    assert scan_issue_status_residuals(issue_dir) == []


def test_promote_gate_report_includes_path_source_and_status(tmp_path: Path, capsys) -> None:
    issue_dir = tmp_path / "issues" / "bugs" / "review" / "BUG-9999-demo"
    issue_dir.mkdir(parents=True)
    (issue_dir / "root-cause.md").write_text("---\nstatus: open\n---\n# Root Cause\n", encoding="utf-8")
    issue = IssueRecord(issue_id="BUG-9999-demo", kind="bug", path=issue_dir, trace_status="done")
    candidate = promote_issues_for_archive.PromotionCandidate(
        issue_id="BUG-9999-demo",
        kind="bug",
        stage="review",
        status="done",
        change_ids=["fix-demo"],
        pending_changes=[],
        reason="all linked changes archived and status done",
    )

    blockers = promote_issues_for_archive.collect_residual_blockers([candidate], {"BUG-9999-demo": issue})
    promote_issues_for_archive.print_residual_blockers(blockers)
    output = capsys.readouterr().out

    assert "Issue Subdocument Status Gate" in output
    assert "BUG-9999-demo" in output
    assert "root-cause.md" in output
    assert "frontmatter" in output
    assert "`open`" in output
    assert "--reconcile-issue-status-residuals --dry-run" in output
    assert "--reconcile-issue-status-residuals --apply-reconcile" in output


def test_reconcile_dry_run_reports_without_writing(tmp_path: Path) -> None:
    issue_dir = tmp_path / "issues" / "bugs" / "review" / "BUG-9999-demo"
    issue_dir.mkdir(parents=True)
    doc = issue_dir / "acceptance.md"
    doc.write_text(
        "---\nstatus: pending_review\nupdated_at: 2026-07-01 10:00:00\n---\n"
        "# AC\n\n```yaml\nstatus: applied\n```\n",
        encoding="utf-8",
    )
    issue = IssueRecord(issue_id="BUG-9999-demo", kind="bug", path=issue_dir, trace_status="done")

    result = reconcile_issue_status_residuals(issue, write=False)

    assert result.dry_run is True
    assert result.blockers == []
    assert len(result.planned) == 2
    assert result.changed_files == 0
    assert "pending_review" in doc.read_text(encoding="utf-8")
    assert "status: applied" in doc.read_text(encoding="utf-8")


def test_reconcile_write_updates_frontmatter_yaml_block_and_updated_at(tmp_path: Path) -> None:
    issue_dir = tmp_path / "issues" / "requirements" / "review" / "REQ-9999-demo"
    issue_dir.mkdir(parents=True)
    doc = issue_dir / "acceptance.md"
    doc.write_text(
        "---\nstatus: pending_review\nupdated_at: 2026-07-01 10:00:00\n---\n"
        "# AC\n\n```yaml\nstatus: applied\n```\n",
        encoding="utf-8",
    )
    issue = IssueRecord(issue_id="REQ-9999-demo", kind="req", path=issue_dir, trace_status="done")

    result = reconcile_issue_status_residuals(issue, write=True)
    text = doc.read_text(encoding="utf-8")

    assert result.dry_run is False
    assert result.blockers == []
    assert result.changed_files == 1
    assert result.changed_fields == 2
    assert "status: done" in text
    assert "pending_review" not in text
    assert "status: applied" not in text
    assert "updated_at: 2026-07-01 10:00:00" not in text


def test_reconcile_allows_closed_issue_when_linked_sprint_not_completed(tmp_path: Path, monkeypatch) -> None:
    issue_dir = tmp_path / "issues" / "requirements" / "review" / "REQ-9999-demo"
    issue_dir.mkdir(parents=True)
    doc = issue_dir / "acceptance.md"
    doc.write_text("---\nstatus: draft\nupdated_at: 2026-07-01 10:00:00\n---\n# AC\n", encoding="utf-8")
    issue = IssueRecord(
        issue_id="REQ-9999-demo",
        kind="req",
        path=issue_dir,
        trace_status="done",
        openspec_changes=[{"change_id": "add-demo", "status": "archived"}],
    )

    monkeypatch.setattr(issue_status_residuals.collect, "find_archived_change_dir", lambda change_id: tmp_path / "archive" / change_id)
    monkeypatch.setattr(issue_status_residuals.collect, "find_sprints_for_issue", lambda issue_id: ["sprint-999"])
    monkeypatch.setattr(
        issue_status_residuals.collect,
        "load_sprint",
        lambda sprint_id: collect.SprintRecord(
            sprint_id=sprint_id,
            path=tmp_path / "iterations" / "change" / sprint_id,
            status="planning",
        ),
    )

    assert issue_reconcile_blockers(issue) == []

    result = reconcile_issue_status_residuals(issue, write=True)
    text = doc.read_text(encoding="utf-8")

    assert result.blockers == []
    assert result.changed_fields == 1
    assert "status: done" in text
    assert "status: draft" not in text


def test_reconcile_write_rejects_unclosed_issue(tmp_path: Path) -> None:
    issue_dir = tmp_path / "issues" / "bugs" / "review" / "BUG-9999-demo"
    issue_dir.mkdir(parents=True)
    doc = issue_dir / "root-cause.md"
    doc.write_text("---\nstatus: open\n---\n# Root Cause\n", encoding="utf-8")
    issue = IssueRecord(
        issue_id="BUG-9999-demo",
        kind="bug",
        path=issue_dir,
        trace_status="in_sprint",
    )

    result = reconcile_issue_status_residuals(issue, write=True)

    assert result.blockers == ["issue trace status `in_sprint` is not closed"]
    assert result.changed_files == 0
    assert "status: open" in doc.read_text(encoding="utf-8")


def test_opsx_archive_skill_requires_sequential_sync_before_promotion() -> None:
    skill = (ROOT / ".agents" / "skills" / "opsx-archive" / "SKILL.md").read_text(encoding="utf-8")
    rules = (ROOT / "rules" / "issues-lifecycle.md").read_text(encoding="utf-8")

    assert "strictly sequentially" in skill
    assert "Do not use parallel execution" in skill
    assert "promotion depends on the files written by Workflow Sync" in skill
    assert "MUST 严格顺序执行" in rules
    assert "不得并行运行" in rules
