---
change_id: add-spec-opt-governance-command
title: 实施任务
status: proposed
created_at: 2026-08-06 13:46:00
updated_at: 2026-08-06 14:20:00
---

# 任务

## 1. 新增命令技能

- [x] 1.1 新建 `.agents/skills/spec-opt/SKILL.md`。
- [x] 1.2 在 Skill 中定义 `/spec-opt` 的输入、适用范围、禁止修改业务代码、OpenSpec Change 创建/复用规则。
- [x] 1.3 在 Skill 中定义文档同步矩阵，覆盖 `AGENTS.md`、`rules/`、`docs/`、`scripts/` 和 OpenSpec Change。
- [x] 1.4 在 Skill 中接入 `Context Budget Guardrails`、force-proceed follow-up 门禁和 Final Output Contract。

## 2. 文档与规则同步

- [x] 2.1 更新 `AGENTS.md`，将 `/spec-opt` 加入命令族速查和 AI 工具入口说明。
- [x] 2.2 更新 `rules/agent-context-budget.md` 或相关规则，说明规范优化命令的同步和校验要求。
- [x] 2.3 更新 `docs/README.md` 或相关 docs 索引，提示规范优化入口以 `AGENTS.md` 和 `/spec-opt` 为准。

## 3. 脚本与校验

- [x] 3.1 评估是否需要扩展 `scripts/validate-agent-context-budget.py`，确保 `spec-opt` 被纳入技能契约校验。
- [x] 3.2 若新增脚本或扩展校验逻辑，补充对应测试或最小验证。
- [x] 3.3 运行 `python scripts/validate-agent-context-budget.py`。
- [x] 3.4 运行 `python scripts/validate-openspec-language.py`。
- [x] 3.5 运行 `python scripts/validate-directory-structure.py`。
- [x] 3.6 运行 `openspec validate add-spec-opt-governance-command`。

## 4. 复核

- [x] 4.1 复核 `/spec-opt` 不修改 `src/` 业务代码。
- [x] 4.2 使用聚焦 `git diff --stat` 确认影响范围只包含治理文档、技能、脚本和本 Change。
- [x] 4.3 最终输出下一步与待用户决策/处理，且两者不重复。
