from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-root-cause-evidence.py"
SPEC = importlib.util.spec_from_file_location("validate_root_cause_evidence", SCRIPT)
assert SPEC and SPEC.loader
validate_root_cause_evidence = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_root_cause_evidence
SPEC.loader.exec_module(validate_root_cause_evidence)


def test_require_confirmed_blocks_probable_root_cause(tmp_path: Path) -> None:
    root_cause = tmp_path / "root-cause.md"
    root_cause.write_text(
        "---\nroot_cause_status: probable\n---\n"
        "# Root Cause\n\n## 人工补证步骤\n\n需要补证。\n",
        encoding="utf-8",
    )

    findings = validate_root_cause_evidence.validate_root_cause_file(
        root_cause,
        require_confirmed=True,
    )

    assert any(item.level == "blocker" and "要求 root_cause_status 为 `confirmed`" in item.message for item in findings)


def test_require_confirmed_blocks_missing_root_cause_file(tmp_path: Path) -> None:
    findings = validate_root_cause_evidence.validate_root_cause_file(
        tmp_path / "root-cause.md",
        require_confirmed=True,
    )

    assert findings[0].level == "blocker"
    assert "不存在" in findings[0].message


def test_confirmed_with_evidence_passes_require_confirmed(tmp_path: Path) -> None:
    root_cause = tmp_path / "root-cause.md"
    root_cause.write_text(
        "---\nroot_cause_status: confirmed\n---\n"
        "# Root Cause\n\n## 证据链\n\n| 证据入口 | 类型 | 摘要 |\n|---|---|---|\n"
        "| `tests/test_demo.py::test_demo` | 测试 | 已复现并验证。 |\n",
        encoding="utf-8",
    )

    findings = validate_root_cause_evidence.validate_root_cause_file(
        root_cause,
        require_confirmed=True,
    )

    assert [item for item in findings if item.level == "blocker"] == []


def test_default_mode_keeps_probable_as_non_blocking_warning(tmp_path: Path) -> None:
    root_cause = tmp_path / "root-cause.md"
    root_cause.write_text(
        "---\nroot_cause_status: probable\n---\n# Root Cause\n",
        encoding="utf-8",
    )

    findings = validate_root_cause_evidence.validate_root_cause_file(root_cause)

    assert [item for item in findings if item.level == "blocker"] == []
    assert any(item.level == "warning" for item in findings)
