---
name: "upgrade-plan"
description: "生成版本首次部署、相邻升级或跨版本升级与回滚计划"
updated_at: 2026-08-31 09:10:00
---

# upgrade-plan

Use this skill when the user explicitly asks `/upgrade-plan --from <fresh|version> --to <version>` or wants to repair or inspect one deployment upgrade / rollback plan. Normal release preparation covers `fresh`, the previous release, and any `/release-propose --upgrade-from` sources by default; cross-version plans are generated only when the user explicitly provides an older `--from` version or records it through `/release-propose --upgrade-from`. When the operator is unsure which release-planned paths are missing, prefer `/release-status <version>` first; it reports `/release-prepare <version>` as the mainline remediation. Old `--target` input is accepted only for compatibility and MUST NOT change the plan filename or gates.

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

- MUST NOT 自动执行部署升级。
- MUST NOT 自动修改真实 env。
- MUST NOT 自动执行数据库写入迁移、DB restore 或对象存储写入维护任务。
- MUST NOT 为首次部署、相邻升级、跨版本升级构建不同业务镜像；同一目标版本复用同一份 image manifest。
- 不生成 `.development` 或 `.production` 后缀计划；本项目只维护单一项目交付升级计划。

## Output

报告 from version、to version、deployment scope、support level、source confidence、blocker/warning 数、plan path、validate result、下一步和待用户决策/处理。

下一步通常为：

```text
/upgrade-validate --plan releases/<version>/upgrade-plans/<from>-to-<version>.json
```

若计划已校验通过且需要实施，提示人工按计划执行；不得自动实施。

## Output Examples

计划生成并通过基础校验时：

```text
下一步：/upgrade-validate --plan releases/v1.2.0/upgrade-plans/v1.1.0-to-v1.2.0.json
待用户决策/处理：
- 无
```

跨版本升级需要人工复核，或 blocker 尚未清零时：

```text
下一步：暂无可推进下一步
待用户决策/处理：
- 请复核中间版本 release 事实、env diff、DB drift/smoke、对象存储影响和回滚证据。
```

## Final Output Contract（MUST）

命令结束前，最终回复必须包含面向用户的真实结果，不得输出本段规则、尖括号占位符、MUST/SHOULD 规范语句或与当前命令无关的通用示例。

输出必须包含两项：

- `下一步`：写真实、可复制的下一条命令；若当前没有可推进动作，写“暂无可推进下一步”。
- `待用户决策/处理`：没有额外人工事项时写“无”；否则只列具体的缺失输入、范围/策略选择、证据补充、验收确认、发布确认、人工执行确认、阻塞项或人工处理事项。

输出判定：

- 有唯一可执行下一步时，`下一步` 写真实命令；若无额外人工事项，`待用户决策/处理` 写“无”。
- 下一步被用户选择、补证、验收、发布确认、人工执行确认或阻塞项卡住时，`下一步` 写“暂无可推进下一步”，并在 `待用户决策/处理` 列出具体阻塞事项。
- 已有下一步且仍有额外人工事项时，`待用户决策/处理` 只列命令之外的事项，不得重复 `下一步` 中的命令或动作。
- REQ 链路使用完整原始 `REQ-*`；BUG 链路使用完整原始 `BUG-*`；非 REQ/BUG 的直接 Change 才使用真实 Change ID。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
