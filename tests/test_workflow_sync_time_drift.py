from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.workflow_sync import collect, engine, patch as sync_patch
from scripts.workflow_sync.collect import IssueRecord, resolve_archive_timestamp
from scripts.workflow_sync.derive import DerivedChange, DerivedIssue
from scripts.workflow_sync.engine import SyncEngine, SyncReport
from scripts.workflow_sync.patch import (
    PatchResult,
    append_workflow_event_record,
    normalize_change_record_table,
    patch_issue_trace,
    persist_markdown,
)


def load_frontmatter_yaml(text: str) -> dict:
    return yaml.safe_load(text.split("---", 2)[1])


def load_first_fenced_yaml(text: str) -> dict:
    match = re.search(r"```yaml\n(.*?)```", text, re.S)
    assert match is not None
    return yaml.safe_load(match.group(1))


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


def test_main_scope_table_includes_pure_change(tmp_path: Path) -> None:
    sprint_dir = tmp_path / "iterations" / "change" / "sprint-999"
    sprint_dir.mkdir(parents=True)
    (sprint_dir / "sprint.yaml").write_text(
        """changes:
  - auto-archive-trace-fallback
scope_estimates:
  - id: auto-archive-trace-fallback
    estimated_person_days: 3
""",
        encoding="utf-8",
    )
    sprint = collect.SprintRecord(
        sprint_id="sprint-999",
        path=sprint_dir,
        status="planning",
        changes=["auto-archive-trace-fallback"],
    )
    changes = {
        "auto-archive-trace-fallback": DerivedChange(
            change_id="auto-archive-trace-fallback",
            state="proposed",
            display_status="proposed",
            note="proposed `auto-archive-trace-fallback`",
            tasks_done=0,
            tasks_total=13,
            linked_req=None,
            linked_bug=None,
            archive_date=None,
        )
    }

    table = sync_patch.render_main_scope_table(sprint, {}, {}, changes)

    assert "| Change | auto-archive-trace-fallback |" in table
    assert "| proposed | 3 人天 | proposed `auto-archive-trace-fallback` |" in table


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


def test_workflow_sync_records_opsx_apply_for_in_progress_change() -> None:
    text = """# 需求追踪

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-23 10:00:00 | `/sprint-propose` | 纳入 sprint |
"""
    derived = DerivedIssue(
        issue_id="REQ-0001-demo",
        kind="requirement",
        display_status="in_sprint",
        linked_change="add-demo",
        note="in_progress 1/2",
    )

    updated = append_workflow_event_record(
        text,
        event="opsx.apply",
        change_id="add-demo",
        derived=derived,
        change_status_map={"add-demo": "in_progress"},
    )

    assert "| /opsx-apply | Change `add-demo` apply 进行中，待补齐剩余验收。 |" in updated
    assert updated.index("/opsx-apply") < updated.index("/sprint-propose")


def test_workflow_sync_records_opsx_modify_idempotently() -> None:
    text = """# 需求追踪

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
"""
    derived = DerivedIssue(
        issue_id="REQ-0001-demo",
        kind="requirement",
        display_status="in_sprint",
        linked_change="add-demo",
        note="applied",
    )

    first = append_workflow_event_record(
        text,
        event="opsx.modify",
        change_id="add-demo",
        derived=derived,
        change_status_map={"add-demo": "applied"},
    )
    second = append_workflow_event_record(
        first,
        event="opsx.modify",
        change_id="add-demo",
        derived=derived,
        change_status_map={"add-demo": "applied"},
    )

    expected = "| /opsx-modify | Change `add-demo` 验收返修已同步，待复验或 archive。 |"
    assert expected in first
    assert first == second
    assert second.count("/opsx-modify") == 1


def test_patch_issue_trace_backfills_iteration_for_sprint_scope(
    tmp_path: Path,
    monkeypatch,
) -> None:
    req_dir = tmp_path / "issues/requirements/review/REQ-0001-demo"
    req_dir.mkdir(parents=True)
    trace_path = req_dir / "trace.md"
    trace_path.write_text(
        """---
requirement_id: REQ-0001-demo
status: approved
created_at: 2026-08-26 10:00:00
updated_at: 2026-08-26 10:00:00
iteration: null
openspec_changes: []
---

# 需求追踪

```yaml
requirement_id: REQ-0001-demo
status: approved
iteration: null
openspec_changes: []
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(sync_patch, "ROOT", tmp_path)

    result = patch_issue_trace(
        IssueRecord(
            issue_id="REQ-0001-demo",
            kind="req",
            path=req_dir,
            trace_status="approved",
        ),
        DerivedIssue(
            issue_id="REQ-0001-demo",
            kind="req",
            display_status="in_sprint",
            linked_change=None,
            note="status `in_sprint`",
        ),
        {},
        event="sprint.propose",
        sprint_id="sprint-999",
        write=True,
    )

    text = trace_path.read_text(encoding="utf-8")
    assert result.changed
    assert load_frontmatter_yaml(text)["status"] == "in_sprint"
    assert load_frontmatter_yaml(text)["iteration"] == "sprint-999"
    assert load_first_fenced_yaml(text)["status"] == "in_sprint"
    assert load_first_fenced_yaml(text)["iteration"] == "sprint-999"


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
    frontmatter = load_frontmatter_yaml(text)
    assert frontmatter["status"] == "in_sprint"
    assert frontmatter["openspec_changes"] == [
        {"change_id": "add-example", "type": "add", "status": "applied"}
    ]


def test_patch_issue_trace_repairs_orphan_frontmatter_change_entries(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(sync_patch, "ROOT", tmp_path)
    req_dir = tmp_path / "issues/requirements/review/REQ-0002-example"
    req_dir.mkdir(parents=True)
    (req_dir / "trace.md").write_text(
        """---
requirement_id: REQ-0002-example
status: in_sprint
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
  - change_id: add-example
    type: add
    status: proposed
---

# Trace
""",
        encoding="utf-8",
    )
    issue = IssueRecord(
        issue_id="REQ-0002-example",
        kind="req",
        path=req_dir,
        trace_status="in_sprint",
        openspec_changes=[{"change_id": "add-example", "status": "proposed"}],
    )
    derived = DerivedIssue(
        issue_id="REQ-0002-example",
        kind="req",
        display_status="in_sprint",
        linked_change="add-example",
        note="apply 完成；待 archive `add-example`",
    )

    result = patch_issue_trace(
        issue,
        derived,
        {"add-example": "applied"},
        event="opsx.apply",
        focus_change="add-example",
        write=True,
    )

    text = (req_dir / "trace.md").read_text(encoding="utf-8")
    frontmatter = load_frontmatter_yaml(text)
    assert result.changed is True
    assert frontmatter["status"] == "in_sprint"
    assert frontmatter["openspec_changes"] == [
        {"change_id": "add-example", "type": "update", "status": "applied"}
    ]
    assert "updated_at: 2026-07-03 10:00:00\n  - change_id:" not in text


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


def test_patch_sprint_md_rewrites_legacy_scope_table_from_derived_state(
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

| 类型 | ID | Change | 优先级 | 估算 | 状态 | 说明 |
|---|---|---|---|---:|---|---|
| BUG | BUG-9999-demo | fix-demo | high | 1.0 人天 | in_sprint | stale |

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
        priority="high",
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
    assert "| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |" in text
    assert "| BUG | BUG-9999-demo | Demo bug | done | 1.0 人天 | archived `fix-demo`" in text
    assert "| 类型 | ID | Change | 优先级 | 估算 | 状态 | 说明 |" not in text
    assert "stale" not in text


def test_patch_sprint_md_rewrites_compact_scope_table_to_canonical_columns(
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

| 类型 | 范围项 | 状态 | 估算 |
|---|---|---|---:|
| BUG | BUG-9999-demo / fix-demo | done / archived | 1.0 人天 |

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
        priority="high",
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
    assert "| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |" in text
    assert "| BUG | BUG-9999-demo | Demo bug | done | 1.0 人天 | archived `fix-demo`" in text
    assert "| 类型 | 范围项 | 状态 | 估算 |" not in text


def test_render_changes_table_prefers_source_bug_over_related_requirement() -> None:
    sprint = collect.SprintRecord(
        sprint_id="sprint-999",
        path=Path("iterations/change/sprint-999"),
        status="planning",
        requirements=[],
        bugs=["BUG-9999-demo"],
        changes=["fix-demo"],
    )
    change = DerivedChange(
        change_id="fix-demo",
        state="archived",
        display_status="archived",
        note="archived `fix-demo`（2026-07-19 23:59:59）",
        tasks_done=5,
        tasks_total=5,
        linked_req="REQ-9999-parent",
        linked_bug="BUG-9999-demo",
        archive_date="2026-07-19 23:59:59",
    )

    table = sync_patch.render_changes_table(sprint, {"fix-demo": change})

    assert "| `fix-demo` | BUG-9999-demo | archived |" in table
    assert "REQ-9999-parent" not in table


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

    archived_change = tmp_path / "openspec/archive/2026-07-03-fix-example"
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
openspec_changes: []
---

```yaml
status: in_sprint
iteration: sprint-999
openspec_changes: []
related_changes: []
```

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
    trace_text = (req_dir / "trace.md").read_text(encoding="utf-8")
    assert trace_text.count("change_id: add-demo") == 2
    assert trace_text.count("  - add-demo") == 2
    trace_frontmatter = load_frontmatter_yaml(trace_text)
    trace_fenced = load_first_fenced_yaml(trace_text)
    assert trace_frontmatter["status"] == "in_sprint"
    assert trace_frontmatter["openspec_changes"] == [
        {"change_id": "add-demo", "type": "update", "status": "proposed"}
    ]
    assert trace_fenced["openspec_changes"] == [
        {"change_id": "add-demo", "type": "update", "status": "proposed"}
    ]
    req_text = (req_dir / "requirement.md").read_text(encoding="utf-8")
    assert "related_change: add-demo" in req_text
    assert "openspec_changes:\n  - change_id: add-demo" in req_text
    registry_text = (tmp_path / "issues/requirements/_registry.yaml").read_text(encoding="utf-8")
    assert "related_change: add-demo" in registry_text

    apply_gate_report = SyncEngine(dry_run=True).run(
        sprint_id="auto",
        event="opsx.apply",
        change_id="add-demo",
    )

    assert apply_gate_report.ok
    assert apply_gate_report.sprint_id == "sprint-999"
    assert apply_gate_report.sprint_skip_reason is None

    second_report = SyncEngine().run(
        sprint_id="auto",
        event="req.opsx",
        req_id="REQ-9999-demo",
        change_id="add-demo",
    )
    assert second_report.ok
    assert (req_dir / "trace.md").read_text(encoding="utf-8").count("change_id: add-demo") == 2

    third_report = SyncEngine().run(
        sprint_id="auto",
        event="req.opsx",
        req_id="REQ-9999-demo",
        change_id="add-demo",
    )
    assert third_report.ok
    assert not third_report.updated


def test_bug_opsx_sync_backfills_bug_doc_trace_registry_and_sprint_scope(
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
requirements: []
bugs:
  - BUG-9999-demo
changes: []

scope_estimates:
  - id: BUG-9999-demo
    change:
    size: S
    story_points: 1
    estimated_person_days: 1.0
    rationale: "demo"
""",
        encoding="utf-8",
    )
    (sprint_dir / "sprint.md").write_text("# Sprint\n", encoding="utf-8")
    (sprint_dir / "release-note.md").write_text("# Release\n", encoding="utf-8")
    (sprint_dir / "acceptance-report.md").write_text("# Acceptance\n", encoding="utf-8")

    bug_dir = tmp_path / "issues/bugs/review/BUG-9999-demo"
    bug_dir.mkdir(parents=True)
    (bug_dir / "bug.md").write_text(
        """---
title: Demo bug
severity: high
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
---

# Bug
""",
        encoding="utf-8",
    )
    (bug_dir / "trace.md").write_text(
        """---
bug_id: BUG-9999-demo
status: in_sprint
iteration: sprint-999
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
openspec_changes: []
---

```yaml
status: in_sprint
iteration: sprint-999
openspec_changes: []
related_change: null
```

# Trace
""",
        encoding="utf-8",
    )
    (tmp_path / "issues/bugs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "issues/bugs/_registry.yaml").write_text(
        """entries:
  - id: BUG-9999-demo
    status: in_sprint
    iteration: sprint-999
    related_change: null
""",
        encoding="utf-8",
    )
    change_dir = tmp_path / "openspec/changes/fix-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "proposal.md").write_text("## Why\n\nBUG-9999-demo\n", encoding="utf-8")
    (change_dir / "tasks.md").write_text("- [ ] 1.1 Demo\n", encoding="utf-8")

    report = SyncEngine().run(
        sprint_id="auto",
        event="bug.opsx",
        bug_id="BUG-9999-demo",
        change_id="fix-demo",
    )

    assert report.ok
    sprint_yaml = (sprint_dir / "sprint.yaml").read_text(encoding="utf-8")
    assert "changes:\n  - fix-demo" in sprint_yaml
    assert "    change: fix-demo" in sprint_yaml
    trace_text = (bug_dir / "trace.md").read_text(encoding="utf-8")
    assert trace_text.count("change_id: fix-demo") == 2
    assert "related_change: fix-demo" in trace_text
    bug_text = (bug_dir / "bug.md").read_text(encoding="utf-8")
    assert "related_change: fix-demo" in bug_text
    assert "openspec_changes:\n  - change_id: fix-demo" in bug_text
    registry_text = (tmp_path / "issues/bugs/_registry.yaml").read_text(encoding="utf-8")
    assert "related_change: fix-demo" in registry_text

    apply_gate_report = SyncEngine(dry_run=True).run(
        sprint_id="auto",
        event="opsx.apply",
        change_id="fix-demo",
    )
    assert apply_gate_report.ok
    assert apply_gate_report.sprint_id == "sprint-999"


def write_bug_generate_fixture(tmp_path: Path, *, with_bug_doc: bool = True) -> Path:
    bug_dir = tmp_path / "issues/bugs/plan/BUG-9998-generate-demo"
    bug_dir.mkdir(parents=True)
    (bug_dir / "capture.md").write_text(
        """---
bug_id: BUG-9998-generate-demo
title: Generate demo
status: captured
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
---

# Capture
""",
        encoding="utf-8",
    )
    if with_bug_doc:
        (bug_dir / "bug.md").write_text(
            """---
bug_id: BUG-9998-generate-demo
title: Generate demo
status: draft
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
---

# Bug
""",
            encoding="utf-8",
        )
    (bug_dir / "trace.md").write_text(
        """---
bug_id: BUG-9998-generate-demo
status: captured
severity: medium
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
lifecycle:
  captured: 2026-07-03 10:00:00
iteration: null
openspec_changes: []
related_change: null
---

# BUG Trace

```yaml
bug_id: BUG-9998-generate-demo
status: captured
severity: medium
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
lifecycle:
  captured: 2026-07-03 10:00:00
iteration: null
openspec_changes: []
related_change: null
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-03 10:00:00 | `/capture` | 记录问题。 |
""",
        encoding="utf-8",
    )
    (tmp_path / "issues/bugs/_registry.yaml").write_text(
        """entries:
  - id: BUG-9998-generate-demo
    title: Generate demo
    status: captured
    iteration: null
    related_change: null
""",
        encoding="utf-8",
    )
    (tmp_path / "issues/bugs/CHANGELOG.md").write_text(
        """---
created_at: 2026-07-03 10:00:00
updated_at: 2026-07-03 10:00:00
---

# 缺陷当前态看板索引

| BUG | 标题 | 状态 | 阶段 | Sprint | Change | 最近更新时间 | 下一步 | 事实源 |
|---|---|---|---|---|---|---|---|---|
| BUG-9998-generate-demo | Generate demo | captured | plan | — | — | 2026-07-03 10:00:00 | `/bug-generate BUG-9998-generate-demo` | `issues/bugs/plan/BUG-9998-generate-demo/trace.md` |
""",
        encoding="utf-8",
    )
    return bug_dir


def test_bug_generate_sync_advances_captured_bug_to_draft(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(collect, "ROOT", tmp_path)
    monkeypatch.setattr(sync_patch, "ROOT", tmp_path)
    monkeypatch.setattr(engine, "ROOT", tmp_path)
    monkeypatch.setattr(engine, "run_openspec_list", lambda: {"changes": []})
    bug_dir = write_bug_generate_fixture(tmp_path)

    report = SyncEngine().run(
        sprint_id="auto",
        event="bug.generate",
        bug_id="BUG-9998-generate-demo",
    )

    assert report.ok
    trace_text = (bug_dir / "trace.md").read_text(encoding="utf-8")
    assert "status: draft" in trace_text
    assert "generated:" in trace_text
    trace_frontmatter = load_frontmatter_yaml(trace_text)
    trace_fenced = load_first_fenced_yaml(trace_text)
    assert trace_frontmatter["status"] == "draft"
    assert "generated" in trace_frontmatter["lifecycle"]
    assert "generated" in trace_fenced["lifecycle"]
    assert (bug_dir / "bug.md").read_text(encoding="utf-8").count("status: draft") == 1
    assert "status: draft" in (tmp_path / "issues/bugs/_registry.yaml").read_text(encoding="utf-8")
    changelog = (tmp_path / "issues/bugs/CHANGELOG.md").read_text(encoding="utf-8")
    assert "| BUG-9998-generate-demo | Generate demo | draft | plan | — | — |" in changelog
    assert "`/bug-complete BUG-9998-generate-demo`" in changelog

    second_report = SyncEngine().run(
        sprint_id="auto",
        event="bug.generate",
        bug_id="BUG-9998-generate-demo",
    )
    assert second_report.ok
    assert (bug_dir / "trace.md").read_text(encoding="utf-8").count("generated:") == 2


def test_bug_generate_sync_does_not_advance_without_bug_doc(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(collect, "ROOT", tmp_path)
    monkeypatch.setattr(sync_patch, "ROOT", tmp_path)
    monkeypatch.setattr(engine, "ROOT", tmp_path)
    monkeypatch.setattr(engine, "run_openspec_list", lambda: {"changes": []})
    bug_dir = write_bug_generate_fixture(tmp_path, with_bug_doc=False)

    report = SyncEngine().run(
        sprint_id="auto",
        event="bug.generate",
        bug_id="BUG-9998-generate-demo",
    )

    assert report.ok
    trace_text = (bug_dir / "trace.md").read_text(encoding="utf-8")
    assert "status: captured" in trace_text
    assert "generated:" not in trace_text
    assert "status: captured" in (tmp_path / "issues/bugs/_registry.yaml").read_text(encoding="utf-8")
    changelog = (tmp_path / "issues/bugs/CHANGELOG.md").read_text(encoding="utf-8")
    assert "| BUG-9998-generate-demo | Generate demo | captured | plan | — | — |" in changelog
    assert "`/bug-generate BUG-9998-generate-demo`" in changelog
