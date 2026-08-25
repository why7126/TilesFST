---
requirement_id: REQ-0116-workflow-opsx-linked-change-backfill
title: 增强 opsx linked Change 自动回填
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-08-22 14:21:37
updated_at: 2026-08-25 14:53:29
related_change: update-workflow-opsx-linked-change-backfill
---

# REQ-0116 增强 opsx linked Change 自动回填

## 1. 需求背景

项目已经通过 `issues/requirements`、`issues/bugs`、`iterations`、`openspec/changes` 与 Workflow Sync 串联 REQ / BUG / Change / Sprint 生命周期。当前规则要求 `/req-opsx` 与 `/bug-opsx` 创建或确认 linked Change 后，后续 `/opsx-apply <REQ-id|BUG-id>`、`/opsx-archive <REQ-id|BUG-id>` 继续使用原始 Issue ID，并由内部解析到真实 `<change-id>`。

实际使用中，linked Change 信息仍可能在多个入口之间漂移：`trace.md` 中的 `openspec_changes[]` 已被写入，但 `requirement.md` / `bug.md` 主文档、`issues/requirements/_registry.yaml`、`issues/bugs/_registry.yaml` 中的 `related_change` 或同等字段可能未同步。人类入口文档和当前态索引滞后后，评审者需要回到 trace 或 Sprint scope 反查；AI 执行后续命令时也更容易依赖不完整状态。

本需求用于增强 Workflow Sync 的 linked Change 自动回填能力：当 `req.opsx` 或 `bug.opsx` 创建、确认或修复 linked Change 后，系统应幂等同步 Issue trace、主文档、registry 与 Sprint scope 中的关联关系，降低后续命令解析、看板推导和人工确认成本。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 产品负责人 / 项目负责人 | 打开 REQ/BUG 主文档或当前态看板时能直接看到 linked Change，而不需要反查 trace。 |
| AI / Codex Agent | 执行 `/opsx-apply <REQ-id|BUG-id>` 和 `/opsx-archive <REQ-id|BUG-id>` 时能稳定从 Issue 链路解析 Change。 |
| 流程维护者 | 将 linked Change 回填逻辑集中在 Workflow Sync，避免每个 opsx 命令分散手工补写。 |
| Sprint 负责人 | 已纳入 Sprint 的 REQ/BUG 创建 Change 后，Sprint scope 能自动补齐 `changes[]` 与估算关联。 |
| 评审与验收人员 | 能从主文档、registry、trace、Sprint scope 多入口看到一致的 Change 关联状态。 |

## 3. 需求目标

- 建立 `req.opsx` 与 `bug.opsx` linked Change 的统一自动回填规则。
- 确保 `trace.md` 的 `openspec_changes[]`、`related_changes[]` / `related_change` 与主文档、registry 保持一致。
- 确保已纳入 Sprint 的 REQ/BUG 创建 Change 后，`sprint.yaml` 的 `changes[]` 与 `scope_estimates[].change` 仍自动补齐。
- 保持后续命令继续使用原始 `REQ-*` / `BUG-*` 参数，由内部解析真实 Change。
- 提供幂等同步与聚焦测试，避免重复追加、过期看板和多入口状态漂移。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| `req.opsx` 回填增强 | REQ 创建或确认 linked Change 后，自动同步 trace、`requirement.md` 和 requirements registry。 |
| `bug.opsx` 回填增强 | BUG 创建或确认 linked Change 后，自动同步 trace、`bug.md` 和 bugs registry。 |
| Workflow Sync 集中实现 | 回填逻辑优先沉到 `scripts/sync-workflow-status.py` 及其共享模块，减少 Skill 手工补写。 |
| Sprint scope 协同 | 已纳入 Sprint 的 Issue 创建 Change 后继续补齐 `sprint.yaml` `changes[]` 与 `scope_estimates[].change`。 |
| 幂等与漂移检查 | 重复运行不会重复追加；必要时报告主文档或 registry 中的 linked Change 漂移。 |
| 测试覆盖 | 增加或更新聚焦测试，覆盖 REQ 与 BUG 两条 opsx 链路的 trace、主文档、registry、Sprint scope 同步。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 批量修复全部历史漂移 | 历史漂移可提供 focused dry-run / apply 入口或后续治理建议，但不默认批量改 archive。 |
| 改造业务功能 | 不新增 Web、管理端、小程序业务能力。 |
| API / DB 结构变更 | 不新增接口、数据库表、Pydantic Schema 或 Orval 生成物。 |
| 直接修改 OpenSpec 正式规格 | 实现前仍需通过 OpenSpec Change，开发中不得直接改 `openspec/specs/`。 |
| 改变命令参数契约 | 后续 `/opsx-apply`、`/opsx-archive` 对 REQ/BUG 来源链路仍使用原始 Issue ID。 |
| 自动创建 follow-up Issue | 同步发现漂移默认报告或由用户确认后另走 capture，不自动落盘新 Issue。 |

## 5. 功能要求

### FR-001 `req.opsx` 必须同步 REQ linked Change

系统 MUST 在 Workflow Sync 处理 `req.opsx` 且收到 `--req <REQ-id>` 与 `--change <change-id>` 时，确保目标 REQ 的 linked Change 信息完整同步。

至少覆盖：

- `trace.md` frontmatter 的 `openspec_changes[]` 包含当前 `change_id`、`type` 或可推导类型、`status`；
- `trace.md` fenced yaml 状态块包含当前 linked Change，且不与 frontmatter 冲突；
- `trace.md` 的 `related_changes[]` 或等价 linked Change 索引包含当前 Change；
- `requirement.md` 主文档中的 frontmatter 或状态块能够引用当前 linked Change；
- `issues/requirements/_registry.yaml` 对应条目的 `related_change` 自动更新。

如果目标 REQ 已有同一 `change_id`，系统 MUST 更新状态而不是重复追加。

### FR-002 `bug.opsx` 必须同步 BUG linked Change

系统 MUST 在 Workflow Sync 处理 `bug.opsx` 且收到 `--bug <BUG-id>` 与 `--change <change-id>` 时，确保目标 BUG 的 linked Change 信息完整同步。

至少覆盖：

- `trace.md` frontmatter 与 fenced yaml 中的 `openspec_changes[]`；
- BUG 现有 `related_change` 字段或等价 linked Change 索引；
- `bug.md` 主文档中的 `related_change` 或状态块引用；
- `issues/bugs/_registry.yaml` 对应条目的 `related_change`。

如果 BUG 关联父需求，既有父需求 `## 关联缺陷` 索引更新规则 MUST 继续生效，并显示最新 BUG 关联 Change。

### FR-003 主文档字段语义必须稳定

系统 MUST 明确 `requirement.md` / `bug.md` 中 linked Change 的写入策略，避免制造新的事实源冲突。

推荐策略：

| 字段 | 用途 |
|---|---|
| `related_change` | 人类入口和 registry 的单值当前 linked Change。 |
| `openspec_changes[]` | 结构化历史或多 Change 关联列表，优先以 `trace.md` 为机器事实源。 |
| `related_changes[]` | REQ 多 Change 索引或兼容字段，应与 `openspec_changes[]` 可交叉验证。 |

当 Issue 存在多个 linked Change 时，系统 SHOULD 明确 registry 和主文档 `related_change` 选择规则，例如当前 active Change、最新创建 Change 或主交付 Change，并在设计中记录取舍。

### FR-004 Sprint scope 回填必须继续幂等

系统 MUST 保持现有 Sprint scope 回填能力：当目标 REQ/BUG 已在某个 `sprint-xxx` 正式范围内，`req.opsx` / `bug.opsx` 创建 Change 后 Workflow Sync MUST：

- 将 `<change-id>` 写入同一 Sprint 的 `sprint.yaml` `changes[]`；
- 同步匹配 `scope_estimates[].change`；
- 清理该 Issue 对应的 open-change 延后项；
- 刷新 Sprint Scope 派生块；
- 使 `/opsx-apply --sprint auto --change <change-id> --dry-run` 能解析到同一 Sprint。

如果 Issue 未纳入 Sprint，Workflow Sync MAY 跳过 Sprint 同步，但 MUST 仍同步目标 Issue 的 trace、主文档和 registry，并在摘要中说明 Sprint skipped 原因。

### FR-005 回填必须幂等且可检查

系统 MUST 保证 repeated sync 不产生重复 linked Change、重复变更记录或无意义 diff。

幂等要求：

- 同一 `change_id` 不得在 `openspec_changes[]` 重复出现；
- `related_change` 已为目标值时不重复写入；
- `related_changes[]` 已包含目标值时不重复追加；
- Change 生命周期阶段变化时只更新状态字段，避免重复写入 linked Change；
- summary 输出区分 updated、skipped、warnings 和 blockers。

系统 SHOULD 支持 focused dry-run，用于报告目标 Issue 主文档、registry、trace 与 Sprint scope 的 linked Change 漂移。

### FR-006 测试必须覆盖两条 opsx 链路

实现 MUST 增加或更新聚焦测试，至少覆盖：

- REQ `req.opsx` 后 trace、`requirement.md`、requirements registry 同步；
- BUG `bug.opsx` 后 trace、`bug.md`、bugs registry 同步；
- 已在 Sprint 中的 REQ/BUG 创建 Change 后 `sprint.yaml` scope 同步；
- 重复执行 Workflow Sync 的幂等性；
- 后续 `/opsx-apply --sprint auto --dry-run` 或等价解析门禁不再报告 change 不在 sprint scope。

测试 SHOULD 使用临时 fixture 或聚焦样例，避免批量修改历史 archive。

### FR-007 输出与错误处理必须清晰

Workflow Sync 成功路径 SHOULD 输出紧凑摘要，至少包含：

| 字段 | 说明 |
|---|---|
| focused issue | 当前 REQ/BUG。 |
| focused change | 当前 linked Change。 |
| linked_change_sync | trace、主文档、registry 是否更新。 |
| sprint_sync | Sprint scope 是否更新或 skipped 原因。 |
| subdocuments | 检查和更新数量。 |
| warnings / blockers | 剩余漂移或人工处理项。 |

当主文档字段语义不明、多 Change 选择冲突、Issue 不存在或 Change 不存在时，系统 MUST 报告 warning 或 blocker，不得静默覆盖。

### FR-008 安全与上下文预算约束

同步与测试 MUST 遵守项目安全和上下文预算规则：

- 不读取或输出真实客户数据、密钥、`.env`、Authorization header、Cookie；
- 不持久化原始 Codex session、prompt 或工具输出正文；
- 大范围历史扫描默认只输出计数、分类和样例；
- 成功路径只输出摘要，失败路径输出必要文件路径与字段；
- 不为了修复历史漂移批量改 archive，除非先 dry-run 并由用户确认。

## 6. UI / UE 约束

本需求不新增 Web 管理端、店主 Web 或微信小程序 UI。

若后续需要在管理端展示 workflow linked Change 健康状态，应另行创建需求，并遵守 Design System semantic token、管理端权限边界和 OpenSpec Change 流程。

## 7. 非功能约束

| 项 | 要求 |
|---|---|
| 一致性 | Issue trace、主文档、registry 与 Sprint scope 的 linked Change 不得长期冲突。 |
| 幂等性 | 重复运行 Workflow Sync 不制造重复条目或无意义 diff。 |
| 可追踪 | 每次回填可追溯到 workflow event、Issue、Change 和 Sprint。 |
| 可维护 | linked Change 回填逻辑集中在 Workflow Sync 或共享脚本中。 |
| 可测试 | REQ 与 BUG 两条链路均有聚焦测试覆盖。 |
| 安全 | 不输出敏感信息，不写入会话推理、本机绝对路径或原始工具输出正文。 |

## 8. 关联需求与规则

| 关联项 | 关系 | 说明 |
|---|---|---|
| `REQ-0089-workflow-subdocument-status-sync` | 相关治理需求 | 已建立子文档状态同步与验收结果回填机制，本需求补齐 linked Change 回填一致性。 |
| `rules/requirement-management.md` | 需求状态规则 | 约束 REQ `trace.md`、`requirement.md` 和后续命令参数。 |
| `rules/bug-management.md` | BUG 状态规则 | 约束 BUG `trace.md`、`bug.md`、父需求反向追溯和后续命令参数。 |
| `rules/document-governance.md` | 文档治理规则 | 要求状态变化后通过 Workflow Sync 同步 trace、registry、子文档与 Sprint scope。 |
| `.agents/skills/workflow-sync/SKILL.md` | 执行入口 | 定义 `req.opsx` / `bug.opsx` 与 Sprint scope 同步规则。 |
| `scripts/sync-workflow-status.py` | 脚本入口 | 后续实现 linked Change 自动回填的主要候选入口。 |

## 9. 状态块

```yaml
requirement_id: REQ-0116-workflow-opsx-linked-change-backfill
status: done
lifecycle_stage: archive
iteration: sprint-025
openspec_changes:
  - change_id: update-workflow-opsx-linked-change-backfill
    type: update
    status: archived
related_change: update-workflow-opsx-linked-change-backfill
readiness: Ready
next_command: 暂无可推进下一步
notes:
  - 已根据 capture 生成 requirement.md。
  - 本需求覆盖 REQ 与 BUG 两条 opsx linked Change 自动回填链路。
  - 已补齐 user-stories、business-flow、acceptance 与 trace 扩展信息。
  - 本需求为纯 workflow 治理，不涉及 UI 横切 AC。
  - 已纳入 sprint-025，并创建 linked Change `update-workflow-opsx-linked-change-backfill`。
```
