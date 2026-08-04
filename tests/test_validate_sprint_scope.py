from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.workflow_sync.collect import SprintRecord

SCRIPT = ROOT / "scripts" / "validate-sprint-scope.py"
SPEC = importlib.util.spec_from_file_location("validate_sprint_scope", SCRIPT)
validate_sprint_scope = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = validate_sprint_scope
SPEC.loader.exec_module(validate_sprint_scope)


def test_validate_sprint_scope_rejects_compact_main_scope_table(
    tmp_path: Path,
    monkeypatch,
) -> None:
    sprint_dir = tmp_path / "iterations/change/sprint-999"
    sprint_dir.mkdir(parents=True)
    (sprint_dir / "sprint.md").write_text(
        """# Sprint 999

## 2. Scope

| 类型 | 范围项 | 状态 | 估算 |
|---|---|---|---:|
| BUG | BUG-9999-demo / fix-demo | done / archived | 1 人天 |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-9999 | Demo bug | high | done | archived `fix-demo` |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `fix-demo` | BUG-9999-demo | archived | archived `fix-demo` |
<!-- workflow-sync:scope-changes:end -->
""",
        encoding="utf-8",
    )
    sprint = SprintRecord(
        sprint_id="sprint-999",
        path=sprint_dir,
        status="planning",
        requirements=[],
        bugs=["BUG-9999-demo"],
        changes=["fix-demo"],
    )
    monkeypatch.setattr(validate_sprint_scope, "load_sprint", lambda _: sprint)

    failures = validate_sprint_scope.validate_sprint_scope("sprint-999", set())

    assert any("main table header must be" in failure for failure in failures)

