## ADDED Requirements

### Requirement: Issue 子文档常规状态同步
系统 MUST 在 REQ / BUG 状态变化工作流中同步 Issue 包内的人类入口子文档状态，避免只更新 `trace.md`、registry 或 Sprint 派生块后留下子文档状态漂移。`trace.md` MUST 继续作为机器状态事实源；子文档状态若存在，MUST 要么与当前主状态一致，要么使用不与主状态混淆的语义字段。

#### Scenario: REQ 状态变化同步主文档
- **WHEN** 系统执行 `req.generate`、`req.review`、`req.opsx`、`opsx.apply`、`opsx.archive` 或 `sprint.archive` 并改变目标 REQ 的主状态或关联 Change 状态
- **THEN** 系统 MUST 同步检查 `requirement.md`、`acceptance.md`、`review.md` 与其他维护状态字段的顶层 Markdown 子文档
- **AND** 系统 MUST 更新可安全派生的状态字段或报告需要人工判断的字段
- **AND** `trace.md` MUST 保持 canonical 状态事实源

#### Scenario: BUG 状态变化同步主文档
- **WHEN** 系统执行 `bug.generate`、`bug.review`、`bug.opsx`、`opsx.apply`、`opsx.archive` 或 `sprint.archive` 并改变目标 BUG 的主状态或关联 Change 状态
- **THEN** 系统 MUST 同步检查 `bug.md`、`acceptance.md`、`review.md`、`root-cause.md`、`workaround.md` 与其他维护状态字段的顶层 Markdown 子文档
- **AND** 系统 MUST 更新可安全派生的状态字段或报告需要人工判断的字段
- **AND** `trace.md` MUST 保持 canonical 状态事实源

#### Scenario: 子文档状态字段语义不代表主状态
- **WHEN** 一个 Issue 子文档中的状态字段表达文档草稿、评审结论、验收结论或历史 capture 状态，而不是当前 Issue 主状态
- **THEN** 系统 MUST 将该字段改名、解释或从常规主状态同步目标中排除
- **AND** drift 报告 MUST 不得把已明确豁免或重命名的字段误报为主状态冲突

### Requirement: Issue 验收结果回填
系统 MUST 为 REQ / BUG 的 `acceptance.md` 或等价验收结果文档提供标准化验收结果回填能力，使已实现、已修复或已归档的 Issue 能追踪验收结论、证据、失败项和来源命令。

#### Scenario: opsx apply 后标记待验收
- **WHEN** 来源于 REQ 或 BUG 的 Change 完成 `opsx.apply`
- **THEN** 系统 MUST 能在对应 Issue 的验收入口记录待验收或待确认状态
- **AND** 记录 MUST 包含来源 Change 和可继续补充证据的位置

#### Scenario: opsx archive 后记录验收闭环
- **WHEN** 来源于 REQ 或 BUG 的 Change 完成 `opsx.archive` 并使 Issue 可闭环
- **THEN** 系统 MUST 能在对应 Issue 的验收入口记录 `acceptance_status`、`accepted_at`、`accepted_by`、`source_change`、`source_sprint`、`evidence`、`failed_items` 或等价结构
- **AND** 已归档 Issue MUST 不得只残留旧的 `pending_review`、`draft` 或等价中间态来表达验收状态

#### Scenario: 验收失败或豁免
- **WHEN** 验收结论不是完全通过
- **THEN** 系统 MUST 记录失败、部分通过或豁免状态
- **AND** 系统 MUST 记录失败项、豁免原因或 follow-up 建议
- **AND** 系统 MUST NOT 自动创建 follow-up Issue，除非用户明确授权

### Requirement: Issue 子文档 drift check
系统 MUST 提供 Issue 子文档 drift check 能力，发现 `trace.md`、registry、目录阶段、子文档状态和验收结果之间的不一致，并在失败路径输出可定位的诊断信息。

#### Scenario: check 发现主状态漂移
- **WHEN** 用户执行 Workflow Sync check、Issue drift check、archive readiness 或 Sprint close 检查
- **AND** `trace.md`、registry、`lifecycle_stage`、物理目录阶段或子文档主状态存在冲突
- **THEN** 系统 MUST 报告文件路径、字段来源、当前值、期望值和建议命令
- **AND** 系统 MUST 返回非零退出码或将该项报告为 blocker

#### Scenario: check 发现验收结果缺失
- **WHEN** 一个 Issue 已处于 closed、done、archived、resolved 或等价闭环状态
- **AND** `acceptance.md` 或等价验收入口缺少验收结论、证据或明确豁免
- **THEN** 系统 MUST 报告该验收结果缺失
- **AND** 报告 MUST 包含 Issue ID、文件路径和建议补齐方式

#### Scenario: 成功路径摘要输出
- **WHEN** Issue 子文档 drift check 通过
- **THEN** 系统 MUST 输出检查 Issue 数、检查文件数、更新数、warning 数和 blocker 数摘要
- **AND** 系统 MUST NOT 默认展开全部子文档正文

### Requirement: 历史 Issue 子文档漂移受控治理
系统 MUST 为历史 `issues/**/archive/` 中的子文档状态漂移提供受控治理流程。历史治理 MUST 先 dry-run，再由人工确认 apply；apply MUST 只处理可安全同步项。

#### Scenario: 历史扫描分类输出
- **WHEN** 用户执行历史 Issue 子文档漂移扫描
- **THEN** 系统 MUST 按可安全同步、需人工判断、缺少 trace 或交付证据、缺少验收结果、不建议自动修复等类别输出报告
- **AND** 报告 MUST 包含计数、样例路径和建议下一步
- **AND** 成功路径 MUST NOT 默认展开全部历史文档正文

#### Scenario: 历史 dry-run 不写入
- **WHEN** 用户执行历史漂移修复 dry-run
- **THEN** 系统 MUST 报告将被更新的文件、字段来源、旧值、目标值和原因
- **AND** 系统 MUST NOT 写入文件

#### Scenario: 历史 apply 只处理安全项
- **WHEN** 用户确认执行历史漂移修复 apply
- **THEN** 系统 MUST 只写入 dry-run 中标记为可安全同步的项
- **AND** 系统 MUST 刷新被修改 Markdown 的 `updated_at`
- **AND** 系统 MUST NOT 使用批量修复绕过 review、acceptance、OpenSpec archive 或 Sprint archive

### Requirement: Workflow Sync 子文档摘要输出
系统 MUST 在 Workflow Sync 相关事件的成功摘要中提供 Issue 子文档同步结果，使用户能知道是否检查、更新或留下 drift warning，而无需阅读详细逐文件输出。

#### Scenario: Workflow Sync 成功摘要包含子文档结果
- **WHEN** Workflow Sync 处理会影响 REQ 或 BUG 状态的事件
- **THEN** 摘要 MUST 包含子文档检查数量、子文档更新数量、验收结果状态或不适用原因、drift warning 数量
- **AND** 摘要 MUST 保留现有 event、focus issue 或 change、sprint 解析结果、updated、skipped 和 errors 聚合信息

#### Scenario: 详细模式保留逐文件诊断
- **WHEN** 用户显式请求 Workflow Sync 详细输出
- **THEN** 系统 MUST 输出子文档 updated、skipped、warning 或 blocker 的逐文件明细
- **AND** 摘要模式和详细模式的退出码 MUST 一致

### Requirement: Sprint close 中间态文案扫描
系统 MUST 在 Sprint close、`/sprint-archive` 或等价收尾流程中扫描相关 Issue 包与 Sprint 四件套的中间态残留，防止 completed/archive 状态下仍保留 `planned`、`pending`、`待验收`、`待实现`、active Change 路径或等价旧文案。

#### Scenario: Sprint close 发现中间态文案
- **WHEN** Sprint close 或 `/sprint-archive` 检查关联 Issue 包、`sprint.md`、`acceptance-report.md`、`release-note.md` 或其他 Sprint 四件套
- **AND** 文档仍包含未解释的中间态词、active Change 路径或 legacy archive 路径
- **THEN** 系统 MUST 报告文件路径、行号、命中内容类别和建议修复方式
- **AND** `/sprint-archive` MUST 不得静默输出完成闭环结论

#### Scenario: Sprint close stale scan 范围受控
- **WHEN** 系统执行 Sprint close 中间态文案扫描
- **THEN** 系统 MUST 以目标 Sprint 的 `sprint.yaml`、关联 REQ、BUG 与 Change 定位检查范围
- **AND** 系统 MUST NOT 默认扫描整个 `issues/**`、`openspec/archive/**`、generated 文件或无关历史目录

## MODIFIED Requirements

### Requirement: Issue 归档子文档状态一致性门禁
系统 MUST 在 REQ / BUG 迁入 `issues/**/archive/` 前检查 issue 包内维护状态字段的 Markdown 子文档，防止 archive 包残留非闭环状态。系统 MUST 在发现残留状态时输出明确修复命令，并 MUST 提供安全的 reconcile 能力，在 Issue 主状态与关联交付对象已闭环时自动同步子文档残留状态。单个 Issue 的归档与子文档 reconcile MUST 以该 Issue 自身闭环为准，不得仅因所属 Sprint 尚未 completed 而阻断；Sprint completed 仅作为 `/sprint-archive` 整体归档门禁。该门禁 MUST 复用或兼容常规子文档 drift check 的扫描分类结果，并 MUST 区分“日常状态传播缺失”与“闭环 residual reconcile”两类问题。

#### Scenario: BUG 子文档残留状态阻断归档
- **GIVEN** 一个 BUG 已满足关联 Change archived 与 `trace.md` done 条件
- **AND** `bug.md`、`root-cause.md`、`acceptance.md`、`workaround.md` 或其他维护状态字段的子文档仍包含 `draft`、`pending_review`、`in_sprint`、`applied`、`todo`、`open` 或等价非闭环状态
- **WHEN** 系统执行 issue archive promote
- **THEN** 系统 MUST 阻断该 BUG 迁入 `issues/bugs/archive/`
- **AND** 报告 MUST 列出 issue id、文件路径、状态来源、当前状态
- **AND** 报告 MUST 包含可直接执行的 dry-run reconcile 命令与实际写入命令
- **AND** 报告 MUST 标明该残留属于闭环 residual、常规状态传播缺失还是需要人工判断

#### Scenario: REQ 子文档残留状态阻断归档
- **GIVEN** 一个 REQ 已满足关联 Change archived 与 `trace.md` done 条件
- **AND** `requirement.md`、`acceptance.md`、`user-stories.md`、`business-flow.md`、`capture.md` 或其他维护状态字段的子文档仍包含非闭环状态
- **WHEN** 系统执行 issue archive promote
- **THEN** 系统 MUST 阻断该 REQ 迁入 `issues/requirements/archive/`
- **AND** 报告 MUST 列出所有残留状态字段
- **AND** 报告 MUST 包含可直接执行的 dry-run reconcile 命令与实际写入命令
- **AND** 报告 MUST 标明该残留属于闭环 residual、常规状态传播缺失还是需要人工判断

#### Scenario: 子文档状态全部闭环后允许归档
- **GIVEN** 一个 REQ 或 BUG 已满足 archive promote 的主状态条件
- **AND** issue 包内所有维护状态字段均为 `done`、`archived`、`resolved`、`closed` 或等价闭环状态
- **AND** `acceptance.md` 或等价验收入口已记录通过、失败、部分通过或豁免结论
- **WHEN** 系统执行 issue archive promote
- **THEN** 系统 MAY 将该 issue 从 `review/` 迁入 `archive/`

#### Scenario: Reconcile 建议区分自动修复与上游阻断
- **WHEN** issue archive promote 因子文档状态残留被阻断
- **THEN** 报告 MUST 提示先 dry-run 再 apply reconcile
- **AND** 建议 MUST 区分“可自动 reconcile”的闭环 Issue 与“必须先推进上游流程”的未闭环 Issue
- **AND** 建议 MUST 标明是否还缺少验收结果回填

#### Scenario: Dry-run 预览子文档状态 reconcile
- **GIVEN** 一个 REQ 或 BUG 的主状态与关联 Change 已闭环
- **AND** 所属 Sprint 尚未 completed
- **WHEN** 用户执行子文档状态 reconcile dry-run 命令
- **THEN** 系统 MUST 报告将被更新的文件、字段来源、旧状态与目标状态
- **AND** 系统 MUST NOT 写入文件
- **AND** 系统 MUST NOT 仅因所属 Sprint 尚未 completed 阻断 dry-run

#### Scenario: 写入子文档状态 reconcile
- **GIVEN** 一个 REQ 或 BUG 的主状态与关联 Change 已闭环
- **AND** 所属 Sprint 尚未 completed
- **WHEN** 用户执行子文档状态 reconcile 写入命令
- **THEN** 系统 MUST 将子文档残留状态更新为该 issue 的闭环目标状态
- **AND** 系统 MUST 刷新被修改 Markdown 的 `updated_at`
- **AND** 系统 MUST NOT 仅因所属 Sprint 尚未 completed 阻断写入
- **AND** 系统 MUST NOT 写入未在 dry-run 中分类为可安全同步的历史字段

#### Scenario: 未闭环 Issue 禁止 reconcile 写入
- **GIVEN** 一个 REQ 或 BUG 的主状态或关联 Change 尚未闭环
- **WHEN** 用户执行子文档状态 reconcile 写入命令
- **THEN** 系统 MUST 阻断写入
- **AND** 报告 MUST 指出需要先完成的上游命令或状态

### Requirement: Workflow Sync 支持摘要输出模式
系统 MUST 为 Workflow Sync 报告提供摘要输出模式，用聚合计数和关键上下文替代成功路径中的长文件明细。摘要输出 MUST 覆盖 Issue 子文档同步结果，包括检查数量、更新数量、验收结果状态或不适用原因、drift warning 数量。

#### Scenario: 成功同步输出摘要
- **WHEN** 用户或 source-command 执行 `scripts/sync-workflow-status.py` 且同步成功
- **THEN** 系统 MUST 输出 Workflow Sync Report 摘要
- **AND** 摘要 MUST 包含 event、focus issue 或 change、sprint 解析结果、updated 数量、skipped 数量和 errors 数量
- **AND** 当事件关联 REQ 或 BUG 时，摘要 MUST 包含子文档检查数量、子文档更新数量、验收结果状态或不适用原因、drift warning 数量
- **AND** 系统 MUST NOT 默认逐条输出完整 `Skipped (no delta)` 文件列表

#### Scenario: 无变化文件较多
- **WHEN** Workflow Sync 产生多个 skipped no-delta 结果且没有错误
- **THEN** 摘要 MUST 仅展示 skipped 聚合数量或等价短提示
- **AND** 输出 MUST 提供查看详细模式的提示或保留可发现的详细模式参数
