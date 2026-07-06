from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.workflow_sync.collect import IssueRecord, resolve_archive_timestamp
from scripts.workflow_sync.patch import persist_markdown


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
