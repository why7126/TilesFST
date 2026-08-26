---
change_id: refine-skill-final-output-contract
acceptance_status: accepted
created_at: 2026-08-26 20:52:46
updated_at: 2026-08-26 20:58:03
---

# 验收目标

命令最终输出契约应避免把规范模板原样输出给用户，并明确区分【下一步】和【待用户决策/处理】。

## 验收项

- [x] AC-001 `.agents/skills/*/SKILL.md` 不再包含可被最终回复原样照抄的尖括号占位模板。
- [x] AC-002 通用 `/bug-review BUG-0122` 示例不再作为所有命令族的默认示例。
- [x] AC-003 `/sprint-propose`、`/req-opsx`、`/bug-opsx` 的示例不再把同一命令动作同时写入【下一步】和【待用户决策/处理】。
- [x] AC-004 `/upgrade-plan` 与 `/upgrade-validate` 具备完整三态输出契约，能区分可执行校验命令、人工实施确认和阻塞项。
- [x] AC-005 `scripts/validate-agent-context-budget.py` 能检查占位符泄漏、通用示例、重复诱因和规范语气泄漏风险。
- [x] AC-006 入口摘要、规则和 docs 索引与技能契约一致，不复制过长规则正文。

## 验收结果回填

```yaml
acceptance_status: accepted
accepted_at: 2026-08-26 20:58:03
accepted_by: codex
evidence:
  - python scripts/validate-agent-context-budget.py
  - python scripts/validate-openspec-language.py
  - openspec validate refine-skill-final-output-contract --strict
  - python scripts/validate-directory-structure.py
  - python scripts/validate-doc-prose-hygiene.py AGENTS.md rules/agent-context-budget.md docs/README.md docs/spec-logs/CHANGELOG.md openspec/changes/refine-skill-final-output-contract/*.md openspec/changes/refine-skill-final-output-contract/specs/agent-workflow-tooling/spec.md
failed_items: []
notes: 文档卫生脚本返回 7 条启发式 warning，均为规范语境中的历史/待办关键词提示，未阻断本次治理验收。
```
