---
requirement_id: REQ-0040-rule-skill-read-summary-reuse-context-budget
title: 规则/Skill 已读摘要复用纳入命令上下文预算治理 - 用户故事
status: done
created_at: 2026-07-16 09:07:01
updated_at: 2026-07-18 09:18:43
---

# 用户故事

## US-001 连续命令复用已读规则摘要

作为 AI / Codex Agent，我希望在同一会话内连续执行 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 命令时，可以复用已读取且未变更的规则摘要，以便减少重复全量读取 `AGENTS.md`、`rules/*.md` 造成的上下文消耗。

验收要点：

- 同一会话已读且无变更的规则文件 SHOULD 用摘要承接。
- 若命令风险升级或摘要不足以支撑判断，MUST 补读必要片段。
- 用户显式要求重读时，MUST 重新读取目标文件或片段。

## US-002 Skill 文件也进入摘要复用治理

作为流程维护者，我希望 `.agents/skills/*/SKILL.md` 与 `rules/` 一样纳入摘要复用机制，以便连续命令不反复展开相同 Skill 的通用预算、Workflow Sync 和 AI usage hook 说明。

验收要点：

- 当前命令 Skill 和共用 Skill MAY 在同一会话内复用摘要。
- 高风险命令仍 MUST 补读该命令专属步骤、Final Step 或任务相关片段。
- Skill 摘要不得替代 OpenSpec、Issue lifecycle、安全、API、DB 等强门禁判断。

## US-003 明确摘要失效条件

作为评审者，我希望规则明确摘要何时失效，以便摘要复用不会因为文件更新、任务类型变化或证据不足而漏掉关键约束。

验收要点：

- 文件 `updated_at`、mtime、hash 或内容变化时 MUST 触发补读。
- 从 capture/explore/generate 升级到 apply/archive/release 等高风险命令时 MUST 重新确认关键门禁。
- Workflow Sync、测试或校验失败时 MUST 回到原文或相关片段定位问题。

## US-004 统一命令 Skill 表述与校验

作为流程维护者，我希望命令 Skill 使用统一的 `Context Budget Guardrails` 表述，并通过校验脚本发现回退，以便长期维护时不再出现宽泛读取模式。

验收要点：

- 命令 Skill MUST 引用 `rules/agent-context-budget.md`。
- 命令 Skill SHOULD 明确“规则和 Skill 已读摘要复用”。
- 校验脚本 SHOULD 能发现缺少摘要复用约束或默认宽泛读取指令的 Skill。

## US-005 保持安全与输出节制

作为安全 / 治理负责人，我希望摘要复用机制只保存必要摘要，不保存原始 prompt、系统/developer 指令、工具输出正文或密钥，以便降低上下文成本时不扩大敏感信息暴露面。

验收要点：

- 摘要复用输出 MUST 保持短摘要化。
- 不得持久化原始 session、完整规则全文、完整 Skill 全文或本地敏感路径。
- 成功路径不得输出完整测试日志、完整 Workflow Sync 派生块或 generated 文件 diff。
