---
name: "upgrade-plan"
description: "生成版本首次部署、相邻升级或跨版本升级与回滚计划"
---

# upgrade-plan

Use this skill when the user asks `/upgrade-plan --from <fresh|version> --to <version>` or wants to generate a deployment upgrade / rollback plan. Normal release preparation should cover `fresh` and the previous release by default; cross-version plans are generated only when the user explicitly provides an older `--from` version.

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- force-proceed 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。
- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接。
- 从 `releases/<to-version>/release.json` 与目标 plan/manifest 开始，只按 `from_version` 与 `to_version` 定位必要 release 目录。
- 跨版本分析先列版本范围和影响摘要，不默认全量展开所有历史 release、OpenSpec archive、生成物、大日志或完整 manifest。
- 输出只展示 compact summary，不打印完整 env、真实 `.env`、密钥、连接串、Cookie、Authorization header、本机绝对路径或真实客户数据。

## Must Read

```text
AGENTS.md
rules/release.md
rules/environment.md
rules/database.md
rules/security.md
docs/02-deployment.md
docs/08-production-image-release.md
releases/<to-version>/release.json
releases/<to-version>/image-manifest.json（若存在）
```

## Command

```bash
python scripts/validate-release-upgrade.py plan --from <fresh|version> --to <version>
python scripts/validate-release-upgrade.py validate-plan --plan releases/<version>/upgrade-plans/<from>-to-<version>.json
```

## Boundaries

- MUST NOT 自动执行生产升级。
- MUST NOT 自动修改真实生产 env。
- MUST NOT 自动执行数据库写入迁移、DB restore 或对象存储写入维护任务。
- MUST NOT 为首次部署、相邻升级、跨版本升级构建不同业务镜像；同一目标版本复用同一份 image manifest。

## Output

报告 from version、to version、support level、source confidence、blocker/warning 数、plan path、validate result、下一步和待用户决策/处理。

下一步通常为：

```text
/upgrade-validate --plan releases/<version>/upgrade-plans/<from>-to-<version>.json
```

若计划已校验通过且需要实施，提示人工按计划执行；不得自动实施。

## Final Output Contract（MUST）

命令结束前最终回复 MUST 明确包含：

```text
下一步：<可直接执行的命令；若没有则写“暂无可推进下一步”>
待用户决策/处理：
- <需要用户选择、确认、补充或处理的事项；若没有则写“无”>
```

若下一步字段已经给出可执行命令，不得在「待用户决策/处理」中重复同一命令或动作。
