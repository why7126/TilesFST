from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-agent-context-budget.py"

spec = importlib.util.spec_from_file_location("validate_agent_context_budget", SCRIPT)
assert spec is not None
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


def write_skill(tmp_path: Path, content: str) -> Path:
    skill_dir = tmp_path / ".agents" / "skills" / "req-demo"
    skill_dir.mkdir(parents=True)
    path = skill_dir / "SKILL.md"
    path.write_text(content, encoding="utf-8")
    return path


def test_missing_summary_reuse_constraint_is_reported(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(validator, "ROOT", tmp_path)
    path = write_skill(
        tmp_path,
        """---
name: req-demo
---

## Context Budget Guardrails

- MUST 遵守 `rules/agent-context-budget.md`。
""",
    )

    errors = validator.validate_skill(path)

    assert f"{path.relative_to(tmp_path)}: 缺少规则与 Skill 已读摘要复用约束" in errors


def test_broad_read_fallback_reports_file_and_line(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(validator, "ROOT", tmp_path)
    path = write_skill(
        tmp_path,
        """---
name: req-demo
---

## Context Budget Guardrails

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接。
- Run `cat rules/*.md` before every task.
""",
    )

    errors = validator.validate_skill(path)

    assert any(
        error == f"{path.relative_to(tmp_path)}:8: 存在默认宽泛读取指令 `- Run `cat rules/*.md` before every task.`"
        for error in errors
    )


def test_compliant_skill_passes(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(validator, "ROOT", tmp_path)
    path = write_skill(
        tmp_path,
        """---
name: req-demo
---

## Context Budget Guardrails

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
- 不要默认 `cat rules/*.md`；失败时只补读必要片段。
""",
    )

    assert validator.validate_skill(path) == []
