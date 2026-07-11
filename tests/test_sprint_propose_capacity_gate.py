from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPRINT_PROPOSE_SKILL = ROOT / ".agents/skills/source-command-sprint-propose/SKILL.md"
ITERATIONS_RULE = ROOT / "rules/iterations-lifecycle.md"
CAPACITY_SPEC = ROOT / "openspec/specs/sprint-planning-governance/spec.md"


def test_sprint_propose_skill_blocks_capacity_above_120_percent() -> None:
    content = SPRINT_PROPOSE_SKILL.read_text(encoding="utf-8")

    assert "estimated_person_days > capacity_person_days * 1.2" in content
    assert "MUST 硬阻断正式规划" in content
    assert "不得生成 `iterations/change/<sprint>/` 四件套" in content
    assert "不得更新 `trace.md` 的 `iteration` 或 Change trace" in content
    assert "拆分 Sprint、移出低优先级项或替换范围后重新运行 `/sprint-propose`" in content


def test_sprint_propose_skill_keeps_capacity_warning_band() -> None:
    content = SPRINT_PROPOSE_SKILL.read_text(encoding="utf-8")

    assert "capacity_person_days < estimated_person_days <= capacity_person_days * 1.2" in content
    assert "MAY 继续" in content
    assert "容量风险、fix 缓冲影响和延后项建议" in content
    assert "estimated_person_days <= capacity_person_days" in content


def test_sprint_capacity_gate_is_backed_by_rule_and_spec() -> None:
    rule = ITERATIONS_RULE.read_text(encoding="utf-8")
    spec = CAPACITY_SPEC.read_text(encoding="utf-8")

    assert "## 3.1 Sprint 容量门禁（MUST）" in rule
    assert "estimated_person_days > capacity_person_days * 1.2" in rule
    assert "### Requirement: Sprint 容量超限硬门禁" in spec
    assert "#### Scenario: 超过 120% 时阻断 Sprint 提议" in spec
    assert "#### Scenario: 100% 到 120% 时允许带风险继续" in spec
    assert "#### Scenario: 不超过容量时正常通过" in spec
