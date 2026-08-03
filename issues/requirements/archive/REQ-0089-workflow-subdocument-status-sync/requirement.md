---
requirement_id: REQ-0089-workflow-subdocument-status-sync
title: REQ/BUG 子文档状态同步与验收结果回填机制
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-08-01 09:49:17
updated_at: 2026-08-01 11:46:26
---

# REQ-0089 REQ/BUG 子文档状态同步与验收结果回填机制

## 1. 需求背景

项目已建立 `issues/requirements`、`issues/bugs`、`iterations`、`openspec/changes`、`openspec/archive` 与 Workflow Sync 串联的规范开发流程。当前规则明确 `trace.md` 是 REQ/BUG 状态事实源，Workflow Sync 负责同步 `trace.md`、registry、Sprint 派生块以及归档状态。

实际使用中仍出现文档事实滞后的问题：`bug.md`、`requirement.md`、`acceptance.md`、`root-cause.md`、`workaround.md`、`review.md` 等顶层子文档也包含 `status` 或验收相关信息，但后续 workflow 命令并不总是持续反写这些文档。结果是机器可读事实源可能已经进入 `done` 或归档状态，人打开子文档却仍看到早期非闭环状态。

`acceptance.md` 的问题更明显：它主要承载验收标准，但是否已验收、是否通过、证据在哪里、失败项如何记录、验收结论来自哪个 Change 或 Sprint，目前缺少稳定回填模型。归档阶段已有 residual reconcile 能力，但它更像闭环阻塞后的补救，而不是日常命令状态传播的一等能力。

本需求用于建立 REQ/BUG 子文档状态同步与验收结果回填机制，让 Issue 包内的机器事实源、人类入口文档和归档门禁保持一致，并为历史 archive 漂移提供受控治理路径。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 产品负责人 / 项目负责人 | 打开 REQ/BUG 文档包时能看到当前状态、验收结论和闭环证据，而不是早期草稿状态。 |
| AI / Codex Agent | 在执行 workflow 命令时有明确的子文档同步规则，避免只更新 `trace.md` 后留下文档漂移。 |
| 流程维护者 | 能通过统一脚本和规则维护状态传播逻辑，而不是让每个命令手工处理不同文档。 |
| 评审者 | 能在评审、归档和 Sprint 收尾时快速判断 Issue 包是否一致、是否存在残留状态。 |
| 测试 / 验收人员 | 能在 `acceptance.md` 或等价验收结果文档中追踪 AC 是否通过、证据位置和失败项。 |

## 3. 需求目标

- 明确 REQ/BUG 顶层文档的角色边界：机器事实源、人类摘要入口、验收标准和验收结果。
- 建立子文档状态同步规则，使状态变化后 `bug.md`、`requirement.md`、`acceptance.md` 等文档不再长期滞后。
- 建立验收结果回填模型，记录通过状态、证据、失败项、验收时间和来源命令。
- 增强 drift check，主动发现 `trace.md`、registry、目录阶段、子文档状态和验收结果的不一致。
- 将历史 archive 中的状态漂移纳入受控治理：先 dry-run 报告，再人工确认 apply。
- 保持 OpenSpec 红线：本需求只定义流程治理，后续实现必须通过 OpenSpec Change。

## 4. 范围

### 4.1 包含

| 范围 | 说明 |
|---|---|
| 文档角色定义 | 明确 `trace.md`、`capture.md`、`requirement.md`、`bug.md`、`acceptance.md`、`review.md`、`root-cause.md`、`workaround.md` 的状态字段职责。 |
| 状态传播规则 | 定义哪些 workflow event 必须同步顶层子文档状态。 |
| Workflow Sync 增强 | 扩展 `scripts/sync-workflow-status.py` 或等价模块，使常规状态变化可同步 Issue 子文档。 |
| 验收结果回填 | 为 `acceptance.md` 或等价文档定义验收结论、证据和失败项记录结构。 |
| Drift check | 增加检查能力，发现 archive/review/plan 中 Issue 子文档状态与 `trace.md` 不一致。 |
| 历史治理 | 提供历史 residual 扫描、分类、dry-run、人工确认 apply 的受控修复路径。 |
| 规则与 Skill 同步 | 更新相关 `rules/` 与 `.agents/skills/*`，让命令输出和门禁一致。 |

### 4.2 不包含

| 不包含 | 说明 |
|---|---|
| 直接修复历史所有文档 | 本需求阶段不直接批量改 archive；批量修复应由后续实现命令 dry-run 后确认执行。 |
| 修改业务功能 | 不新增 Web、管理端、小程序业务能力。 |
| API / DB 结构变更 | 不新增接口、数据库表、Pydantic Schema 或 Orval 生成物。 |
| 重写 OpenSpec 流程 | 不替代现有 req/bug/opsx/sprint 命令链，只补齐状态与验收同步。 |
| 自动创建 follow-up Issue | 漂移扫描发现的新问题默认输出报告，不自动 capture。 |
| 改造 Codex 客户端 | 不修改 Codex Desktop、模型 API 或会话机制。 |

## 5. 功能要求

### FR-001 定义 Issue 文档角色与状态字段边界

系统 MUST 明确 REQ/BUG 文档包内各顶层 Markdown 的角色。

推荐职责：

| 文档 | 职责 | 状态要求 |
|---|---|---|
| `trace.md` | 机器状态事实源、生命周期、关联 Change/Sprint、变更记录 | MUST 保留规范状态字段。 |
| `capture.md` | 原始输入与轻量记录 | MAY 保留 capture 当时状态；不应被误认为当前交付状态。 |
| `requirement.md` / `bug.md` | 人类入口摘要与当前状态概览 | MUST 能反映当前主状态或明确引用 `trace.md`。 |
| `acceptance.md` | 验收标准与验收结果入口 | MUST 能表达验收入口、已通过、未通过或部分通过。 |
| `review.md` | 评审结论 | SHOULD 保留评审结果，并可与当前闭环状态区分。 |
| `root-cause.md` / `workaround.md` | BUG 分析与临时方案 | SHOULD 避免残留阻塞性状态，或明确字段含义。 |

如果某类子文档不再承载当前主状态，系统 MUST 将字段改名、移除或说明，例如使用 `document_status`、`review_result`、`acceptance_status`，避免与 `trace.md status` 混淆。

### FR-002 常规命令必须同步人类入口文档状态

系统 MUST 在状态变化命令后同步人类入口文档。

至少覆盖：

| Event | REQ 文档同步 | BUG 文档同步 |
|---|---|---|
| `req.generate` | `requirement.md` → `draft` | 不适用 |
| `bug.generate` | 不适用 | `bug.md` → `draft` |
| `req.review` / `bug.review` | 主文档、`review.md` | 主文档、`review.md` |
| `req.opsx` / `bug.opsx` | 主文档关联 Change | 主文档关联 Change |
| `opsx.apply` | 主文档、`acceptance.md` 进入实现完成后的验收入口语义 | 主文档、`acceptance.md` 进入修复完成后的验收入口语义 |
| `opsx.archive` / `sprint.archive` | 主文档、`acceptance.md` 闭环 | 主文档、`acceptance.md` 闭环 |

同步 SHOULD 通过 Workflow Sync 或集中脚本完成，MUST NOT 要求每个命令手工编辑同一套派生字段。

### FR-003 验收结果回填模型

系统 MUST 为 `acceptance.md` 或等价文档定义验收结果回填结构。

验收结果 SHOULD 至少包含：

| 字段 | 说明 |
|---|---|
| `acceptance_status` | `not_started`、`ready_for_acceptance`、`passed`、`failed`、`partial`、`waived` 等。 |
| `accepted_at` | 验收完成时间，格式为 `YYYY-MM-DD HH:mm:ss`。 |
| `accepted_by` | 验收记录来源，可为 product/test/AI/manual。 |
| `source_change` | 触发验收的 OpenSpec Change。 |
| `source_sprint` | 所属 Sprint，若无则为 null。 |
| `evidence` | 测试命令、截图、日志、验收报告或人工确认位置。 |
| `failed_items` | 未通过或豁免的 AC 编号与原因。 |
| `notes` | 限制、风险或后续 follow-up。 |

当验收未完成时，文档 MUST 明确当前状态和下一步，不得让读者从 `status: pending_review` 等旧字段猜测。

### FR-004 Drift check 必须覆盖子文档状态

系统 SHOULD 增强 `sync-workflow-status.py --check` 或新增专用校验，使其能发现 Issue 包状态漂移。

校验 SHOULD 覆盖：

- `trace.md` frontmatter 与 fenced yaml `status` 一致；
- registry 中 status 与 `trace.md` 当前状态一致；
- 物理目录阶段 `plan/review/archive` 与 `lifecycle_stage` 一致；
- `requirement.md` / `bug.md` 当前状态或状态引用不与 `trace.md` 冲突；
- `acceptance.md` 在 Issue 闭环后存在验收结论或明确豁免；
- archive 阶段不得残留阻塞性状态，除非字段语义已明确不是当前主状态；
- 报告 MUST 输出文件路径、字段来源、旧值、期望值和建议命令。

成功路径输出 SHOULD 保持摘要化；失败时才展开具体漂移清单。

### FR-005 历史 archive 漂移治理

系统 MUST 支持对历史 archive 子文档漂移做受控治理。

历史治理流程 SHOULD 是：

```text
scan → classify → dry-run report → human confirmation → apply → check
```

dry-run 报告 SHOULD 分类展示：

- 可安全同步的状态字段；
- 需要人工判断字段语义的文档；
- 缺少 `trace.md` 或关联 Change 证据的文档；
- `acceptance.md` 缺少验收结果的文档；
- 不建议自动修复的旧模板或遗留格式。

apply MUST 只处理 dry-run 中标记为可安全同步的项，并刷新 `updated_at`。不得用批量修复绕过 review、acceptance、OpenSpec archive 或 Sprint archive。

### FR-006 Workflow Sync 输出和命令 Skill 必须提示子文档同步结果

Workflow Sync 在相关事件中 SHOULD 报告子文档同步摘要。

摘要 SHOULD 包含：

| 字段 | 说明 |
|---|---|
| `issue_status` | 目标 REQ/BUG 的当前主状态。 |
| `subdocuments_checked` | 检查过的子文档数量。 |
| `subdocuments_updated` | 更新过的子文档数量。 |
| `acceptance_result` | 验收结果状态或未适用原因。 |
| `drift_warnings` | 剩余漂移数量或风险摘要。 |

命令 Skill 的 Final Step SHOULD 明确：状态变化后不得只依赖手工编辑，必须通过 Workflow Sync 或专用脚本同步子文档。

### FR-007 与归档门禁协同

`/opsx-archive` 和 `/sprint-archive` MUST 在归档前后检查子文档状态与验收结果。

归档门禁 SHOULD 要求：

- Issue 主状态可推导为闭环；
- 关联 Change 已 archive；
- `acceptance.md` 已记录通过、豁免或人工确认的验收结论；
- 子文档不存在未解释的阻塞性状态；
- 若存在历史 residual，必须先 dry-run，再按报告 apply 或记录人工豁免原因。

已有 `--reconcile-issue-status-residuals` 能力 MAY 保留，但 SHOULD 与常规子文档同步能力区分：前者用于闭环残留补救，后者用于日常状态传播。

### FR-008 安全与上下文预算约束

子文档同步和历史扫描 MUST 遵守上下文预算与安全规则。

要求：

- 默认只扫描 `issues/requirements` 和 `issues/bugs`，并按阶段和文件类型限制范围；
- 大量历史漂移只输出计数、分类和样例，不默认展开全部文件；
- 不读取或输出真实客户数据、密钥、`.env`、Authorization header、Cookie；
- 成功路径只输出摘要，失败路径输出必要文件路径与字段；
- 不把原始 Codex session、prompt、工具输出正文写入 Issue 文档。

## 6. UI / UE 约束

本需求不新增 Web 管理端、店主 Web 或微信小程序 UI。

若后续需要在管理端展示流程治理结果，应另行创建需求，并遵守 Design System semantic token、管理端权限边界和 OpenSpec Change 流程。

## 7. 非功能约束

| 项 | 要求 |
|---|---|
| 一致性 | Issue 包内机器事实源、人类入口文档和验收结果不得长期冲突。 |
| 可追踪 | 每次状态同步应能追溯到 workflow event、命令、Change 或 Sprint。 |
| 幂等性 | 重复运行 Workflow Sync 不应制造重复记录或无意义 diff。 |
| 可审计 | 历史批量修复必须先 dry-run，apply 后保留变更摘要。 |
| 安全 | 不输出敏感信息，不持久化 prompt、session 或本地绝对路径。 |
| 可维护 | 状态传播逻辑应集中在 Workflow Sync 或共享脚本中，避免 Skill 分散手写。 |

## 8. 关联需求与规则

| 关联项 | 关系 | 说明 |
|---|---|---|
| `rules/requirement-management.md` | 需求状态规则 | 已定义 `trace.md` 为事实源，并要求 `requirement.md` frontmatter 同步。 |
| `rules/bug-management.md` | BUG 状态规则 | 定义 BUG 状态机和 BUG 文档包结构。 |
| `rules/issues-lifecycle.md` | 阶段目录规则 | 定义 `plan/review/archive` 与 promote 门禁。 |
| `rules/document-governance.md` | 文档治理规则 | 定义 Workflow Sync 与归档前文档同步要求。 |
| `.agents/skills/workflow-sync/SKILL.md` | 执行入口 | 当前同步范围和 residual reconcile 的主要说明位置。 |
| `scripts/sync-workflow-status.py` | 脚本入口 | 后续实现状态同步和 drift check 的主要候选位置。 |
| `scripts/promote-issues-for-archive.py` | 归档入口 | 当前会检查子文档 residual，可与本需求协同。 |

## 9. 状态块

```yaml
status: done
lifecycle_stage: plan
iteration: null
openspec_changes: []
next: /req-opsx REQ-0089-workflow-subdocument-status-sync
```
