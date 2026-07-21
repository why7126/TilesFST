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

FORCE_PROCEED_GUARDRAIL = """
### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。
"""


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

{FORCE_PROCEED_GUARDRAIL}
- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接。
- Run `cat rules/*.md` before every task.
""".format(FORCE_PROCEED_GUARDRAIL=FORCE_PROCEED_GUARDRAIL),
    )

    errors = validator.validate_skill(path)

    assert any(
        error.endswith("存在默认宽泛读取指令 `- Run `cat rules/*.md` before every task.`")
        for error in errors
    )


def test_missing_force_proceed_follow_up_guardrail_is_reported(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(validator, "ROOT", tmp_path)
    path = write_skill(
        tmp_path,
        """---
name: req-demo
---

## Context Budget Guardrails

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
""",
    )

    errors = validator.validate_skill(path)

    assert f"{path.relative_to(tmp_path)}: 缺少 force-proceed follow-up 不自动落盘门禁" in errors


def test_incomplete_follow_up_capture_fields_are_reported(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(validator, "ROOT", tmp_path)
    path = write_skill(
        tmp_path,
        """---
name: req-demo
---

## Context Budget Guardrails

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
""",
    )

    errors = validator.validate_skill(path)

    assert f"{path.relative_to(tmp_path)}: 缺少标准 follow-up capture 文案字段" in errors


def test_missing_authorized_capture_sync_rule_is_reported(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(validator, "ROOT", tmp_path)
    path = write_skill(
        tmp_path,
        """---
name: req-demo
---

## Context Budget Guardrails

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
""",
    )

    errors = validator.validate_skill(path)

    assert f"{path.relative_to(tmp_path)}: 缺少显式授权自动 capture 后的 Workflow Sync 约束" in errors


def test_compliant_skill_passes(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(validator, "ROOT", tmp_path)
    path = write_skill(
        tmp_path,
        """---
name: req-demo
---

## Context Budget Guardrails

{FORCE_PROCEED_GUARDRAIL}
- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
- 不要默认 `cat rules/*.md`；失败时只补读必要片段。
""".format(FORCE_PROCEED_GUARDRAIL=FORCE_PROCEED_GUARDRAIL),
    )

    assert validator.validate_skill(path) == []
