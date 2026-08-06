---
change_id: standardize-next-step-issue-ids
title: 实施任务
status: proposed
created_at: 2026-08-06 14:28:00
updated_at: 2026-08-06 14:28:00
---

# 任务

## 1. 规则与文档同步

- [x] 1.1 更新 `AGENTS.md`，增加下一步命令参数标识规范。
- [x] 1.2 更新 `rules/agent-context-budget.md`，说明下一步输出的 REQ/BUG/Change 参数约束。
- [x] 1.3 更新 `rules/requirement-management.md`，说明 REQ 来源后续 `/opsx-*` 下一步使用 REQ ID。
- [x] 1.4 更新 `rules/bug-management.md`，说明 BUG 来源后续 `/opsx-*` 下一步使用 BUG ID。
- [x] 1.5 更新 `docs/README.md`，同步 AI 命令入口提示。

## 2. 技能同步

- [x] 2.1 更新 `.agents/skills/req-opsx/SKILL.md`，将下一步 `/opsx-apply` 参数改为 REQ ID。
- [x] 2.2 更新 `.agents/skills/bug-opsx/SKILL.md`，将下一步 `/opsx-apply` 参数改为 BUG ID。
- [x] 2.3 更新 `.agents/skills/opsx-apply/SKILL.md`，支持 REQ/BUG target 解析到 linked Change，并要求下一步归档沿用 REQ/BUG ID。
- [x] 2.4 更新 `.agents/skills/opsx-archive/SKILL.md`，支持 REQ/BUG target 解析到 linked Change。
- [x] 2.5 按需更新 `req-generate`、`req-complete`、`req-review`、`bug-review` 等下一步说明，保持 ID 一致。

## 3. 脚本与校验

- [x] 3.1 扩展 `scripts/validate-agent-context-budget.py`，防止 REQ/BUG 来源的下一步回退为 `<change-id>`。
- [x] 3.2 运行 `python scripts/validate-agent-context-budget.py`。
- [x] 3.3 运行 `python scripts/validate-openspec-language.py`。
- [x] 3.4 运行 `python scripts/validate-directory-structure.py`。
- [x] 3.5 运行 `openspec validate standardize-next-step-issue-ids`。
- [x] 3.6 运行 `python scripts/validate-sprint-scope.py sprint-021 --item standardize-next-step-issue-ids`。

## 4. 复核

- [x] 4.1 复核没有修改业务 `src/` 代码。
- [x] 4.2 使用聚焦 `git diff --stat` 确认影响范围只包含治理资产和本 Change。
- [x] 4.3 最终输出下一步与待用户决策/处理，且两者不重复。
