from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.workflow_sync import collect, engine, patch as sync_patch
from scripts.workflow_sync.collect import IssueRecord, resolve_archive_timestamp
from scripts.workflow_sync.derive import DerivedIssue
from scripts.workflow_sync.engine import SyncEngine
from scripts.workflow_sync.patch import (
    normalize_change_record_table,
    patch_issue_trace,
    persist_markdown,
)


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
