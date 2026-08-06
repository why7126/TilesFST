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


def write_sprint_scope_fixture(
    sprint_dir: Path,
    *,
    target_items: list[str],
    requirements: list[str] | None = None,
    bugs: list[str] | None = None,
    changes: list[str] | None = None,
    scope_estimates: str = "",
) -> None:
    requirements = requirements or []
    bugs = bugs or []
    changes = changes or []
    sprint_dir.mkdir(parents=True)
    target_lines = "\n".join(f"- {item}" for item in target_items)
    main_rows = [
        *(f"| REQ | {item} | Demo requirement | in_sprint | 1 人天 | status `in_sprint` |" for item in requirements),
        *(f"| BUG | {item} | Demo bug | in_sprint | 1 人天 | status `in_sprint` |" for item in bugs),
        *(f"| Change | {item} | Demo change | proposed | 1 人天 | proposed `{item}` |" for item in changes),
    ]
    req_rows = "\n".join(
        f"| {validate_sprint_scope.short_issue_code(item)} | Demo requirement | P1 | in_sprint | status `in_sprint` |"
        for item in requirements
    )
    bug_rows = "\n".join(
        f"| {validate_sprint_scope.short_issue_code(item)} | Demo bug | medium | in_sprint | status `in_sprint` |"
        for item in bugs
    )
    change_rows = "\n".join(
        f"| `{item}` | none | proposed | proposed `{item}` |"
        for item in changes
    )
    (sprint_dir / "sprint.md").write_text(
        f"""# Sprint 999

## 1. 目标

Sprint 目标编号列表：

{target_lines}

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
{chr(10).join(main_rows)}

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
{req_rows}
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
{bug_rows}
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
{change_rows}
<!-- workflow-sync:scope-changes:end -->
""",
        encoding="utf-8",
    )
    (sprint_dir / "sprint.yaml").write_text(
        f"""sprint_id: sprint-999
requirements:
{chr(10).join(f"  - {item}" for item in requirements) or "  []"}
bugs:
{chr(10).join(f"  - {item}" for item in bugs) or "  []"}
changes:
{chr(10).join(f"  - {item}" for item in changes) or "  []"}
scope_estimates:
{scope_estimates or "  []"}
""",
        encoding="utf-8",
    )


def sprint_record_for(sprint_dir: Path, requirements=None, bugs=None, changes=None) -> SprintRecord:
    return SprintRecord(
        sprint_id="sprint-999",
        path=sprint_dir,
        status="planning",
        requirements=requirements or [],
        bugs=bugs or [],
        changes=changes or [],
    )


def test_validate_sprint_scope_rejects_missing_req_target_id(
    tmp_path: Path,
    monkeypatch,
) -> None:
    req_id = "REQ-0100-mintlify-docs-site-ia-content-experience"
    sprint_dir = tmp_path / "iterations/change/sprint-999"
    write_sprint_scope_fixture(sprint_dir, target_items=["BUG-0001-other"], requirements=[req_id])
    monkeypatch.setattr(
        validate_sprint_scope,
        "load_sprint",
        lambda _: sprint_record_for(sprint_dir, requirements=[req_id]),
    )

    failures = validate_sprint_scope.validate_sprint_scope("sprint-999", {req_id})

    assert f"{req_id} missing from sprint.md Sprint target id list" in failures


def test_validate_sprint_scope_accepts_short_req_target_id(
    tmp_path: Path,
    monkeypatch,
) -> None:
    req_id = "REQ-0100-mintlify-docs-site-ia-content-experience"
    sprint_dir = tmp_path / "iterations/change/sprint-999"
    write_sprint_scope_fixture(sprint_dir, target_items=["REQ-0100"], requirements=[req_id])
    monkeypatch.setattr(
        validate_sprint_scope,
        "load_sprint",
        lambda _: sprint_record_for(sprint_dir, requirements=[req_id]),
    )

    failures = validate_sprint_scope.validate_sprint_scope("sprint-999", {req_id})

    assert failures == []


def test_validate_sprint_scope_focus_checks_target_id_list(
    tmp_path: Path,
    monkeypatch,
) -> None:
    bug_id = "BUG-0999-demo-bug"
    sprint_dir = tmp_path / "iterations/change/sprint-999"
    write_sprint_scope_fixture(sprint_dir, target_items=["REQ-0001-other"], bugs=[bug_id])
    monkeypatch.setattr(
        validate_sprint_scope,
        "load_sprint",
        lambda _: sprint_record_for(sprint_dir, bugs=[bug_id]),
    )

    failures = validate_sprint_scope.validate_sprint_scope("sprint-999", {"BUG-0999"})

    assert f"{bug_id} missing from sprint.md Sprint target id list" in failures


def test_validate_sprint_scope_requires_pure_change_target_id(
    tmp_path: Path,
    monkeypatch,
) -> None:
    change_id = "update-demo-governance"
    sprint_dir = tmp_path / "iterations/change/sprint-999"
    write_sprint_scope_fixture(sprint_dir, target_items=["REQ-0001-other"], changes=[change_id])
    monkeypatch.setattr(
        validate_sprint_scope,
        "load_sprint",
        lambda _: sprint_record_for(sprint_dir, changes=[change_id]),
    )

    failures = validate_sprint_scope.validate_sprint_scope("sprint-999", {change_id})

    assert f"{change_id} missing from sprint.md Sprint target id list" in failures
