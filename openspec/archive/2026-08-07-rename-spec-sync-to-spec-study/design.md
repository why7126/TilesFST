## 设计

本变更仅调整命令命名，不改变 Harness 学习工作流语义。

## 命名策略

- 目录名：`.agents/skills/spec-study/`
- 技能名：`spec-study`
- 命令入口：`/spec-study`
- 原 `spec-sync` 不保留为正式命令入口，避免用户继续使用容易误解的旧名称。

## 不变边界

- 学习对象仍全程只读。
- 学习阶段仍必须先输出候选内容并等待用户确认。
- 应用阶段仍只允许更新本项目治理资产。
- 应用阶段仍禁止修改 `src/`。
- 当前 Change 仍纳入 `sprint-022`。

## 文档同步

本次必须同步：

- `.agents/skills/spec-study/SKILL.md`
- `AGENTS.md`
- `rules/agent-context-budget.md`
- `scripts/validate-agent-context-budget.py`
- `openspec/specs/agent-workflow-tooling/spec.md`
- `iterations/archive/sprint-022/` 四件套中的命令名称
- `rules/directory-structure.md`、`docs/README.md` 与 `docs/spec-logs/README.md` 中的学习报告目录规则
