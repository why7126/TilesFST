---
name: "release-status"
description: "只读汇总 release / image / upgrade / publish 状态并输出用户决策面板"
created_at: 2026-08-30 10:25:00
updated_at: 2026-08-30 15:36:34
---

# release-status

Use this skill when the user asks `/release-status <version>` or wants to understand the current release, image, upgrade, and publish state before deciding the next action.

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接。
- 从 `releases/<version>/release.json`、`image-build-plan.json`、`image-manifest.json`、`upgrade-plans/` 和 validator 摘要定位状态。
- MUST NOT 默认展开所有 Sprint、Issue、OpenSpec archive、Docker logs、真实 env 或构建产物。
- 输出只保留状态面板、阻塞分类、默认 upgrade 路径提示、下一步和待用户处理事项。

## Input

- `<version>`：必填，例如 `v1.2.1`。
- Flags：`--target development|production` 可覆盖发布目标用于查看目标门禁；`--json` 可输出机器可读摘要。

## Must Read

```text
AGENTS.md
rules/release.md
rules/security.md
rules/agent-context-budget.md
releases/<version>/release.json
scripts/validate-release.py
```

按状态面板报告再分段读取：

```text
releases/<version>/image-build-plan.json
releases/<version>/image-manifest.json
releases/<version>/upgrade-plans/*.json
```

## Command

```bash
python scripts/validate-release.py --release-dir releases/<version> --status
python scripts/validate-release.py --release-dir releases/<version> --status --target production
python scripts/validate-environment-tiered-evidence.py --release-dir releases/<version> --target production
```

## Output Contract

`/release-status` is read-only. It MUST NOT create release artifacts, image plans, image manifests, upgrade plans, publish confirmation, production evidence, or documentation.

The output MUST include:

- release target and deployment boundary
- current phase
- publish readiness
- one next command when available
- blocking decisions
- blocking evidence
- production-only follow-ups that do not block development releases
- default upgrade path status and commands

Blocker classifications MUST use the release workflow taxonomy: `decision_missing`、`prepare_evidence_missing`、`publish_evidence_missing`、`production_only_pending`、`input_drift`、`environment_unavailable`、`scope_incomplete`、`public_safety`、`schema_invalid`。

When upstream REQ / BUG / Change / Sprint evidence contains `production_only_pending`, `/release-status` MUST keep it non-blocking for `--target development` and reclassify it for `--target production` according to the concrete missing production gate. It MUST consume `validate-release.py --status` output, which includes the environment-tiered evidence validator, and MUST NOT claim production evidence from development-only tests, DevTools screenshots, DevTools Network, or local smoke results.

When Web or miniapp user-visible `PRODUCT_VERSION` sources differ from the release version, `/release-status` MUST classify the blocker as `prepare_evidence_missing` and report the safe remediation as updating the version sources, then rerunning `/image-prepare <version>` and `/image-build <version>` before publish.

If the status panel exposes missing default upgrade paths, output exact commands such as:

```text
/upgrade-plan --from fresh --to v1.2.1 --target development
/upgrade-plan --from v1.2.0 --to v1.2.1 --target development
```

## Final Output Contract（MUST）

命令结束前，最终回复必须包含面向用户的真实结果，不得输出本段规则、尖括号占位符、MUST/SHOULD 规范语句或与当前命令无关的通用示例。

输出必须包含两项：

- `下一步`：写真实、可复制的下一条命令；若当前没有可推进动作，写“暂无可推进下一步”。
- `待用户决策/处理`：没有额外人工事项时写“无”；否则只列具体的缺失输入、范围/策略选择、证据补充、验收确认、发布确认、生产实施确认、阻塞项或人工处理事项。

输出判定：

- 有唯一可执行下一步时，`下一步` 写真实命令；若无额外人工事项，`待用户决策/处理` 写“无”。
- 下一步被用户选择、补证、验收、发布确认、生产实施确认或阻塞项卡住时，`下一步` 写“暂无可推进下一步”，并在 `待用户决策/处理` 列出具体阻塞事项。
- 已有下一步且仍有额外人工事项时，`待用户决策/处理` 只列命令之外的事项，不得重复 `下一步` 中的命令或动作。
- REQ 链路使用完整原始 `REQ-*`；BUG 链路使用完整原始 `BUG-*`；非 REQ/BUG 的直接 Change 才使用真实 Change ID。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
