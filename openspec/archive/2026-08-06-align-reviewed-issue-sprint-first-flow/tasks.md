---
change_id: align-reviewed-issue-sprint-first-flow
title: 实施任务
status: applied
created_at: 2026-08-06 00:00:00
updated_at: 2026-08-06 12:12:40
---

# 任务

## 1. 规则与入口文档

- [x] 1.1 更新 `AGENTS.md` 中 REQ/BUG 总流程和命令速查，将评审后优先 `/sprint-propose` 写为推荐顺序。
- [x] 1.2 更新 `rules/requirement-management.md`，明确已评审 REQ 先进入 Sprint，再 `/req-opsx` 回填 Change。
- [x] 1.3 更新 `rules/bug-management.md`，明确已评审 BUG 先进入 Sprint，再 `/bug-opsx` 回填 Change。
- [x] 1.4 更新 `rules/document-governance.md` 和 `rules/iterations-lifecycle.md` 中与 Sprint scope、Change 回填和 stale 文案相关的描述。

## 2. 技能与命令

- [x] 2.1 更新 `/req-review`、`/bug-review` 的 Next，评审通过后优先提示 `/sprint-propose`。
- [x] 2.2 更新 `/sprint-propose`，允许已评审但尚未 Change 的 REQ/BUG 作为正式范围，并输出后续 `/req-opsx` 或 `/bug-opsx` 引导。
- [x] 2.3 更新 `/req-opsx`、`/bug-opsx`、`/opsx-apply` 中关于 Sprint 门禁和修复路径的说明。
- [x] 2.4 为 `.agents/skills/` 下命令技能补充统一的“下一步”和“待用户决策/处理”输出契约。

## 3. 脚本与校验

- [x] 3.1 更新 `scripts/validate-agent-context-budget.py`，校验命令技能是否包含下一步引导和待决策/待处理输出契约。
- [x] 3.2 运行 `python scripts/validate-agent-context-budget.py`。
- [x] 3.3 运行 `python scripts/validate-directory-structure.py`。
- [x] 3.4 运行 `python scripts/validate-openspec-language.py`。

## 4. 复核

- [x] 4.1 使用 `rg` 复核旧顺序文案，确认评审后优先 `/sprint-propose`。
- [x] 4.2 使用 `git diff --stat` 和聚焦 diff 复核仅改动治理文档、技能、脚本和本 Change。

## 5. 输出去重细化

- [x] 5.1 更新统一 Final Output Contract，明确已出现在「下一步」的命令或动作不得重复进入「待用户决策/处理」。
- [x] 5.2 更新 `agent-workflow-tooling` delta spec 和设计说明，补充输出区块分工与去重要求。
- [x] 5.3 更新 `scripts/validate-agent-context-budget.py`，校验技能契约包含去重约束。

## 6. 入口文档同步

- [x] 6.1 更新 `AGENTS.md`，补充新增/更新命令族、Sprint-first 流程和最终输出契约。
- [x] 6.2 更新 `docs/README.md`，修正 issues 阶段目录路径并指向 `AGENTS.md` 命令入口。
- [x] 6.3 更新 `rules/agent-context-budget.md`，将技能文件要求覆盖范围从部分命令前缀扩展为全部 `.agents/skills/*/SKILL.md`。
