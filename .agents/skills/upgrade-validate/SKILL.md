---
name: "upgrade-validate"
description: "校验版本部署升级与回滚计划"
---

# upgrade-validate

Use this skill when the user asks `/upgrade-validate --plan <path>` or wants to validate a generated upgrade / rollback plan.

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- force-proceed 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。
- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接；只读取指定 plan 和必要的目标 release/image 证据。
- 校验成功默认输出摘要；失败时只展开 blocker/warning 和修复命令。
- 不输出真实 `.env`、密钥、连接串、Cookie、Authorization header、本机绝对路径或真实客户数据。

## Must Read

```text
AGENTS.md
rules/release.md
rules/environment.md
rules/database.md
rules/security.md
<plan path>
```

## Command

```bash
python scripts/validate-release-upgrade.py validate-plan --plan <path>
```

## Boundaries

- MUST NOT 自动执行生产升级。
- MUST NOT 自动修改真实 env。
- MUST NOT 自动执行 DB restore、写入型 migration 或对象存储维护任务。

## Output

报告 plan path、from version、to version、support level、blocker/warning 数、校验结果、下一步和待用户决策/处理。

当 `support_level=cross-version-upgrade-requires-manual-review` 时，输出必须提醒人工复核中间版本 release 事实、env diff、DB drift/smoke、对象存储影响和回滚证据。

## Final Output Contract（MUST）

命令结束前最终回复 MUST 明确包含：

```text
下一步：<可直接执行的命令；若没有则写“暂无可推进下一步”>
待用户决策/处理：
- <需要用户选择、确认、补充或处理的事项；若没有则写“无”>
```

若下一步字段已经给出可执行命令，不得在「待用户决策/处理」中重复同一命令或动作。
