from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.workflow_sync import collect, engine, patch as sync_patch
from scripts.workflow_sync.collect import IssueRecord, resolve_archive_timestamp
from scripts.workflow_sync.derive import DerivedChange, DerivedIssue
from scripts.workflow_sync.engine import SyncEngine, SyncReport
from scripts.workflow_sync.patch import (
    PatchResult,
    normalize_change_record_table,
    patch_issue_trace,
    persist_markdown,
)


def test_workflow_sync_summary_hides_skipped_file_list() -> None:
    report = SyncReport(
        sprint_id="sprint-999",
        event="opsx.propose",
        focus_change="add-demo",
        updated=[PatchResult("issues/requirements/review/REQ-0001-demo/trace.md", True)],
        skipped=[
            PatchResult("iterations/change/sprint-999/sprint.md", False),
            PatchResult("iterations/change/sprint-999/release-note.md", False),
        ],
    )

    text = report.format_text()

    assert "**Summary:**" in text
    assert "- Updated: 1" in text
    assert "- Skipped (no delta): 2" in text
    assert "- Errors: 0" in text
    assert "**Skipped (no delta):**\n- `iterations/change/sprint-999/sprint.md`" not in text
    assert "use `--output detail`" in text


def test_workflow_sync_detail_keeps_file_lists() -> None:
    report = SyncReport(
        sprint_id="sprint-999",
        event="opsx.propose",
        focus_change="add-demo",
        updated=[PatchResult("issues/requirements/review/REQ-0001-demo/trace.md", True)],
        skipped=[PatchResult("iterations/change/sprint-999/sprint.md", False)],
    )

    text = report.format_text("detail")

    assert "**Updated:**" in text
    assert "- `issues/requirements/review/REQ-0001-demo/trace.md`" in text
    assert "**Skipped (no delta):**" in text
    assert "- `iterations/change/sprint-999/sprint.md`" in text


def test_workflow_sync_summary_keeps_error_diagnostics() -> None:
    report = SyncReport(
        event="sprint.apply",
        updated=[PatchResult("iterations/change/sprint-999/sprint.md", True, "marker drift")],
        skipped=[PatchResult("iterations/change/sprint-999/release-note.md", False)],
        errors=["Drift detected in 1 file(s); run without --check to fix"],
    )

    text = report.format_text()

    assert "- Errors: 1" in text
    assert "**Errors:**" in text
    assert "- Drift detected in 1 file(s); run without --check to fix" in text
    assert "**Updated / drift files:**" in text
    assert "- `iterations/change/sprint-999/sprint.md` — marker drift" in text
    assert "**Skipped (no delta):** 1 file(s)" in text


def test_workflow_sync_main_returns_nonzero_for_errors(monkeypatch, capsys) -> None:
    def fake_run(self, **kwargs):
        return SyncReport(
            event=kwargs.get("event"),
            updated=[PatchResult("iterations/change/sprint-999/sprint.md", True)],
            errors=["Drift detected in 1 file(s); run without --check to fix"],
        )

    monkeypatch.setattr(SyncEngine, "run", fake_run)

    exit_code = engine.main(["--event", "sprint.apply", "--check"])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "**Errors:**" in output
    assert "Drift detected in 1 file(s)" in output


def test_archive_timestamp_ignores_mutable_issue_updated_at(tmp_path: Path) -> None:
    archived_change = tmp_path / "2026-07-03-fix-example"
    archived_change.mkdir()
    (archived_change / "trace.md").write_text(
        """---
change_id: fix-example
status: proposed
created_at: 2026-07-03 18:41:48
updated_at: 2026-07-03 23:36:41
---

# OpenSpec Change Trace
""",
        encoding="utf-8",
    )

    bug_dir = tmp_path / "BUG-0001-example"
    bug_dir.mkdir()
    (bug_dir / "trace.md").write_text(
        """---
bug_id: BUG-0001-example
status: done
created_at: 2026-07-03 13:15:19
updated_at: 2026-07-04 08:16:02
---

```yaml
status: done
related_change: fix-example
```

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-07-03 23:47:04 | workflow-sync | 状态同步为 done（Change archived） |
""",
        encoding="utf-8",
    )
    issues = {
        "BUG-0001-example": IssueRecord(
            issue_id="BUG-0001-example",
            kind="bug",
            path=bug_dir,
            trace_status="done",
            related_change="fix-example",
        )
    }

    timestamp = resolve_archive_timestamp(
        archived_change,
        "fix-example",
        linked_req=None,
        linked_bug="BUG-0001-example",
        issues=issues,
    )

    assert timestamp == "2026-07-03 23:47:04"


def test_archive_timestamp_falls_back_to_archive_dir_date(tmp_path: Path) -> None:
    archived_change = tmp_path / "2026-07-03-fix-example"
    archived_change.mkdir()
    (archived_change / "trace.md").write_text(
        """---
change_id: fix-example
status: proposed
updated_at: 2026-07-04 08:16:02
---

# OpenSpec Change Trace
""",
        encoding="utf-8",
    )

    timestamp = resolve_archive_timestamp(
        archived_change,
        "fix-example",
        linked_req=None,
        linked_bug=None,
        issues={},
    )

    assert timestamp == "2026-07-03 23:59:59"


def test_persist_markdown_does_not_touch_unchanged_updated_at(tmp_path: Path) -> None:
    path = tmp_path / "trace.md"
    original = """---
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
---

# Trace
"""
    path.write_text(original, encoding="utf-8")

    changed = persist_markdown(path, original, original, write=True)

    assert changed is False
    assert path.read_text(encoding="utf-8") == original


def test_patch_issue_trace_syncs_frontmatter_change_status_and_apply_record(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(sync_patch, "ROOT", tmp_path)
    req_dir = tmp_path / "issues/requirements/review/REQ-0001-example"
    req_dir.mkdir(parents=True)
    (req_dir / "trace.md").write_text(
        """---
requirement_id: REQ-0001-example
status: in_sprint
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
openspec_changes:
  - change_id: add-example
    type: add
    status: proposed
---

# Trace

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-03 10:00:00 | /req-opsx | 创建 OpenSpec Change `add-example`。 |
""",
        encoding="utf-8",
    )
    issue = IssueRecord(
        issue_id="REQ-0001-example",
        kind="req",
        path=req_dir,
        trace_status="in_sprint",
        openspec_changes=[{"change_id": "add-example", "status": "proposed"}],
    )
    loaded_issue = collect.load_issue_record(req_dir, "req")
    assert loaded_issue is not None
    assert loaded_issue.openspec_changes == [
        {"change_id": "add-example", "type": "add", "status": "proposed"}
    ]

    derived = DerivedIssue(
        issue_id="REQ-0001-example",
        kind="req",
        display_status="in_sprint",
        linked_change="add-example",
        note="apply 完成；待 archive `add-example`",
    )

    first = patch_issue_trace(
        issue,
        derived,
        {"add-example": "applied"},
        event="opsx.apply",
        focus_change="add-example",
        write=True,
    )
    second = patch_issue_trace(
        issue,
        derived,
        {"add-example": "applied"},
        event="opsx.apply",
        focus_change="add-example",
        write=True,
    )

    text = (req_dir / "trace.md").read_text(encoding="utf-8")
    assert first.changed is True
    assert second.changed is False
    assert "status: applied" in text
    assert "| /opsx-apply | Change `add-example` apply 完成，待 archive。 |" in text
    assert text.count("/opsx-apply") == 1


def test_patch_acceptance_report_updates_layered_scope_table(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(sync_patch, "ROOT", tmp_path)
    sprint_dir = tmp_path / "iterations/change/sprint-999"
    sprint_dir.mkdir(parents=True)
    report = sprint_dir / "acceptance-report.md"
    report.write_text(
        """---
note: old
---

# Acceptance

## 最终验收摘要

人工结论保留。

## 原始 AC 引用

<!-- workflow-sync:acceptance-scope:start -->
| 类型 | ID | Acceptance 来源 | 当前状态 | 说明 |
|---|---|---|---|---|
| REQ | REQ-9999-demo | issues/requirements/review/REQ-9999-demo/acceptance.md | planning | demo |
<!-- workflow-sync:acceptance-scope:end -->

## 人工 Sign-off

| 验收人 | 时间 | 结论 | 说明 |
|---|---|---|---|
| Alice | 2026-07-03 10:00:00 | PASS | keep me |
""",
        encoding="utf-8",
    )
    issue_dir = tmp_path / "issues/requirements/review/REQ-9999-demo"
    issue_dir.mkdir(parents=True)
    issue = IssueRecord(issue_id="REQ-9999-demo", kind="req", path=issue_dir, trace_status="in_sprint")
    sprint = collect.SprintRecord(
        sprint_id="sprint-999",
        path=sprint_dir,
        status="in_progress",
        requirements=["REQ-9999-demo"],
        bugs=[],
        changes=["add-demo"],
    )
    derived_issue = DerivedIssue(
        issue_id="REQ-9999-demo",
        kind="req",
        display_status="in_sprint",
        linked_change="add-demo",
        note="apply 完成",
    )
    change = DerivedChange(
        change_id="add-demo",
        state="applied",
        display_status="applied",
        note="apply 2/2",
        tasks_done=2,
        tasks_total=2,
        linked_req="REQ-9999-demo",
        linked_bug=None,
        archive_date=None,
    )

    sync_patch.patch_acceptance_report(
        sprint,
        {"REQ-9999-demo": issue},
        {"REQ-9999-demo": derived_issue},
        {"add-demo": change},
    )

    text = report.read_text(encoding="utf-8")
    assert "applied，待归档（`add-demo` 2/2）" in text
    assert "| Alice | 2026-07-03 10:00:00 | PASS | keep me |" in text


def test_patch_sprint_md_updates_main_scope_table_from_derived_state(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(sync_patch, "ROOT", tmp_path)
    sprint_dir = tmp_path / "iterations/change/sprint-999"
    sprint_dir.mkdir(parents=True)
    (sprint_dir / "sprint.yaml").write_text(
        """sprint_id: sprint-999
status: planning
requirements: []
bugs:
  - BUG-9999-demo
changes:
  - fix-demo

scope_estimates:
  - id: BUG-9999-demo
    change: fix-demo
    size: S
    story_points: 1
    estimated_person_days: 1.0
    rationale: "demo"
""",
        encoding="utf-8",
    )
    (sprint_dir / "sprint.md").write_text(
        """---
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
---

# Sprint 999

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| BUG | BUG-9999-demo | Demo bug | approved | 1.0 人天 | 已评审通过；待 `/bug-opsx` 创建修复 Change |

### 包含需求

### 包含 BUG

### 包含 Change
""",
        encoding="utf-8",
    )
    bug_dir = tmp_path / "issues/bugs/archive/BUG-9999-demo"
    bug_dir.mkdir(parents=True)
    issue = IssueRecord(
        issue_id="BUG-9999-demo",
        kind="bug",
        path=bug_dir,
        title="Demo bug",
        priority="medium",
        trace_status="done",
        openspec_changes=[{"change_id": "fix-demo", "status": "archived"}],
    )
    sprint = collect.SprintRecord(
        sprint_id="sprint-999",
        path=sprint_dir,
        status="planning",
        requirements=[],
        bugs=["BUG-9999-demo"],
        changes=["fix-demo"],
    )
    derived_issue = DerivedIssue(
        issue_id="BUG-9999-demo",
        kind="bug",
        display_status="done",
        linked_change="fix-demo",
        note="archived `fix-demo`（2026-07-19 23:59:59）",
    )
    change = DerivedChange(
        change_id="fix-demo",
        state="archived",
        display_status="archived",
        note="archived `fix-demo`（2026-07-19 23:59:59）",
        tasks_done=5,
        tasks_total=5,
        linked_req=None,
        linked_bug="BUG-9999-demo",
        archive_date="2026-07-19 23:59:59",
    )

    result = sync_patch.patch_sprint_md(
        sprint,
        {"BUG-9999-demo": issue},
        {"BUG-9999-demo": derived_issue},
        {"fix-demo": change},
        "workflow-sync 自动同步 — 1/1 Change archived；0 applied；Sprint `planning`",
        write=True,
    )

    text = (sprint_dir / "sprint.md").read_text(encoding="utf-8")
    assert result.changed is True
    assert "| BUG | BUG-9999-demo | Demo bug | done | 1.0 人天 | archived `fix-demo`" in text
    assert "待 `/bug-opsx` 创建修复 Change" not in text
    assert "BUG：`BUG-9999` 已纳入正式范围" in text
    assert "所有已纳入范围项均已关联 Change" in text
    assert "<!-- workflow-sync:scope-bugs:start -->" in text


def test_normalize_change_record_table_moves_header_before_rows() -> None:
    text = """# Trace

## 变更记录

| 2026-07-05 14:37:59 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-10 20:26:45 | /sprint-propose | 纳入 sprint-005 正式范围。 |
| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-04 15:17:26 | /req-capture | 创建需求记录。 |
"""

    normalized = normalize_change_record_table(text)
    normalized_again = normalize_change_record_table(normalized)

    assert normalized == normalized_again
    assert normalized.index("| 时间 | 命令 | 说明 |") < normalized.index(
        "| 2026-07-05 14:37:59 | lifecycle-stage-migrate |"
    )
    assert "| 2026-07-10 20:26:45 | /sprint-propose | 纳入 sprint-005 正式范围。 |" in normalized


def test_sync_then_consecutive_checks_have_no_delta(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(collect, "ROOT", tmp_path)
    monkeypatch.setattr(sync_patch, "ROOT", tmp_path)
    monkeypatch.setattr(engine, "ROOT", tmp_path)
    monkeypatch.setattr(engine, "run_openspec_list", lambda: {"changes": []})

    sprint_dir = tmp_path / "iterations/change/sprint-999"
    sprint_dir.mkdir(parents=True)
    (sprint_dir / "sprint.yaml").write_text(
        """sprint_id: sprint-999
status: planning
requirements: []
bugs:
  - BUG-0001-example
changes:
  - fix-example
""",
        encoding="utf-8",
    )
    (sprint_dir / "sprint.md").write_text(
        """---
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
---

# Sprint 999

### 包含需求

### 包含 BUG

### 包含 Change
""",
        encoding="utf-8",
    )
    (sprint_dir / "release-note.md").write_text(
        """---
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
---

# Release

| 计划周期 | 2026-07-03 10:00:00 |
""",
        encoding="utf-8",
    )
    (sprint_dir / "acceptance-report.md").write_text(
        """---
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
---

# Acceptance
""",
        encoding="utf-8",
    )

    bug_dir = tmp_path / "issues/bugs/review/BUG-0001-example"
    bug_dir.mkdir(parents=True)
    (bug_dir / "bug.md").write_text(
        """---
title: Example bug
severity: medium
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
---

# Bug
""",
        encoding="utf-8",
    )
    (bug_dir / "trace.md").write_text(
        """---
bug_id: BUG-0001-example
status: in_sprint
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-04 08:16:02
---

```yaml
status: in_sprint
openspec_changes:
  - change_id: fix-example
    status: proposed
related_change: fix-example
```

# Trace
""",
        encoding="utf-8",
    )
    (tmp_path / "issues/bugs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "issues/bugs/_registry.yaml").write_text(
        """entries:
  - id: BUG-0001-example
    status: in_sprint
""",
        encoding="utf-8",
    )

    archived_change = tmp_path / "openspec/changes/archive/2026-07-03-fix-example"
    archived_change.mkdir(parents=True)
    (archived_change / "tasks.md").write_text("- [x] Done\n", encoding="utf-8")
    (archived_change / "trace.md").write_text(
        """---
change_id: fix-example
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-04 08:16:02
---

```yaml
lifecycle:
  archived: 2026-07-03 23:47:04
```
""",
        encoding="utf-8",
    )

    sync_report = SyncEngine().run(
        sprint_id="sprint-999",
        event="opsx.apply",
        change_id="fix-example",
    )
    assert sync_report.ok
    assert sync_report.updated

    first_check = SyncEngine(check=True).run(sprint_id="sprint-999")
    second_check = SyncEngine(check=True).run(sprint_id="sprint-999")

    assert first_check.ok
    assert second_check.ok
    assert first_check.updated == []
    assert second_check.updated == []


def test_patch_sprint_yaml_scope_links_req_opsx_change(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(sync_patch, "ROOT", tmp_path)
    sprint_dir = tmp_path / "iterations/change/sprint-999"
    sprint_dir.mkdir(parents=True)
    (sprint_dir / "sprint.yaml").write_text(
        """sprint_id: sprint-999
status: planning
requirements:
  - REQ-9999-demo
bugs: []
changes:
  - add-existing

scope_estimates:
  - id: REQ-9999-demo
    change:
    size: S
    story_points: 1
    estimated_person_days: 1.0
    rationale: "demo"

deferred_items:
  - id: REQ-9999-open-change
    source: REQ-9999-demo
    priority: P1
    status: action_required
    title: 创建 demo OpenSpec Change
    recommended_next_step: "/req-opsx REQ-9999-demo"
""",
        encoding="utf-8",
    )
    sprint = collect.SprintRecord(
        sprint_id="sprint-999",
        path=sprint_dir,
        status="planning",
        requirements=["REQ-9999-demo"],
        bugs=[],
        changes=["add-existing"],
    )

    result = sync_patch.patch_sprint_yaml_scope(
        sprint,
        "REQ-9999-demo",
        "add-demo",
        write=True,
    )

    text = (sprint_dir / "sprint.yaml").read_text(encoding="utf-8")
    assert result.changed is True
    assert "  - add-demo" in text
    assert "    change: add-demo" in text
    assert "REQ-9999-open-change" not in text
    assert sprint.changes == ["add-existing", "add-demo"]


def test_req_opsx_sync_adds_change_to_sprint_scope_for_apply_gate(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(collect, "ROOT", tmp_path)
    monkeypatch.setattr(sync_patch, "ROOT", tmp_path)
    monkeypatch.setattr(engine, "ROOT", tmp_path)
    monkeypatch.setattr(engine, "run_openspec_list", lambda: {"changes": []})

    sprint_dir = tmp_path / "iterations/change/sprint-999"
    sprint_dir.mkdir(parents=True)
    (sprint_dir / "sprint.yaml").write_text(
        """sprint_id: sprint-999
status: planning
requirements:
  - REQ-9999-demo
bugs: []
changes: []

scope_estimates:
  - id: REQ-9999-demo
    change:
    size: S
    story_points: 1
    estimated_person_days: 1.0
    rationale: "demo"

deferred_items:
  - id: REQ-9999-open-change
    source: REQ-9999-demo
    priority: P1
    status: action_required
    title: 创建 demo OpenSpec Change
    recommended_next_step: "/req-opsx REQ-9999-demo"
""",
        encoding="utf-8",
    )
    (sprint_dir / "sprint.md").write_text("# Sprint\n", encoding="utf-8")
    (sprint_dir / "release-note.md").write_text("# Release\n", encoding="utf-8")
    (sprint_dir / "acceptance-report.md").write_text("# Acceptance\n", encoding="utf-8")

    req_dir = tmp_path / "issues/requirements/review/REQ-9999-demo"
    req_dir.mkdir(parents=True)
    (req_dir / "requirement.md").write_text(
        """---
title: Demo requirement
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
---

# Requirement
""",
        encoding="utf-8",
    )
    (req_dir / "trace.md").write_text(
        """---
requirement_id: REQ-9999-demo
status: in_sprint
iteration: sprint-999
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
openspec_changes:
  - change_id: add-demo
    type: add
    status: proposed
---

# Trace
""",
        encoding="utf-8",
    )
    (tmp_path / "issues/requirements").mkdir(parents=True, exist_ok=True)
    (tmp_path / "issues/requirements/_registry.yaml").write_text(
        """entries:
  - id: REQ-9999-demo
    status: in_sprint
    iteration: sprint-999
""",
        encoding="utf-8",
    )
    change_dir = tmp_path / "openspec/changes/add-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "proposal.md").write_text(
        """## Why

Demo.
""",
        encoding="utf-8",
    )
    (change_dir / "tasks.md").write_text("- [ ] 1.1 Demo\n", encoding="utf-8")
    (change_dir / "trace.md").write_text(
        """---
change_id: add-demo
source_requirement: REQ-9999-demo
status: proposed
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
---

# Trace
""",
        encoding="utf-8",
    )

    req_opsx_report = SyncEngine().run(
        sprint_id="auto",
        event="req.opsx",
        req_id="REQ-9999-demo",
        change_id="add-demo",
    )

    assert req_opsx_report.ok
    sprint_yaml = (sprint_dir / "sprint.yaml").read_text(encoding="utf-8")
    assert "changes:\n  - add-demo" in sprint_yaml
    assert "    change: add-demo" in sprint_yaml
    assert "REQ-9999-open-change" not in sprint_yaml

    apply_gate_report = SyncEngine(dry_run=True).run(
        sprint_id="auto",
        event="opsx.apply",
        change_id="add-demo",
    )

    assert apply_gate_report.ok
    assert apply_gate_report.sprint_id == "sprint-999"
    assert apply_gate_report.sprint_skip_reason is None
