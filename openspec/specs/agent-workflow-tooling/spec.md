# agent-workflow-tooling Specification

## Purpose
TBD - created by archiving change improve-sprint-exps-fact-sheet. Update Purpose after archive.
## Requirements
### Requirement: Sprint Fact Sheet 自动生成
系统 MUST 提供命令式能力，为指定 Sprint 生成自动 Fact Sheet，汇总 Sprint 四件套、Issue、OpenSpec Change、tasks 与验收关键事实。

#### Scenario: 为已归档 Sprint 生成 Fact Sheet
- **WHEN** 用户或 `/sprint-exps` 为存在 `sprint.yaml` 的 `sprint-xxx` 请求生成 Fact Sheet
- **THEN** 系统 MUST 输出包含 Sprint 基础信息、REQ/BUG/Change 范围、Change tasks 完成度、Issue 状态、验收摘要与 token 风险提示的 Fact Sheet

#### Scenario: Sprint 不存在
- **WHEN** 用户请求生成不存在或缺少 `sprint.yaml` 的 Sprint Fact Sheet
- **THEN** 系统 MUST 返回非零退出码并说明缺失的 Sprint 标识或路径

### Requirement: Fact Sheet 可追溯到原始证据
系统 MUST 在 Fact Sheet 中保留证据路径或回读提示，使复盘结论可以追溯到 Sprint、Issue、Change 或验收文件。

#### Scenario: 存在状态不一致或缺失项
- **WHEN** Fact Sheet 发现 Change 缺少 `trace.md`、tasks 未完成、Issue 子文档状态残留或 acceptance report 结论不清晰
- **THEN** 系统 MUST 在 Fact Sheet 中标记风险，并给出建议回读的具体文件路径或关键词

#### Scenario: 无需全文回读
- **WHEN** Fact Sheet 已能提供某项复盘所需的机器事实
- **THEN** `/sprint-exps` MUST 优先使用 Fact Sheet 中的摘要，不得默认全文读取对应四件套、trace 或 tasks 文件

### Requirement: `/sprint-exps` 优先使用 Fact Sheet
`/sprint-exps` MUST 将自动 Fact Sheet 作为复盘的优先输入，并仅在证据不足、风险项存在或用户要求时读取原始文件片段。

#### Scenario: 正常复盘路径
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **THEN** 命令流程 MUST 先运行或读取该 Sprint 的 Fact Sheet，再基于 Fact Sheet 生成 Sprint 复盘与模型 Token 使用分析

#### Scenario: Fact Sheet 标记需要细节
- **WHEN** Fact Sheet 标记 `needs_detail`、warning、missing 或 inconsistent 类风险
- **THEN** `/sprint-exps` MAY 按 Fact Sheet 的 evidence hints 读取对应原始文件片段

### Requirement: Fact Sheet 输出边界受上下文预算约束
Fact Sheet 生成与 `/sprint-exps` 消费流程 MUST 遵守 Agent 上下文预算规则，避免宽泛搜索、长日志、生成物全文 diff 和历史归档全量展开。

#### Scenario: 大 Sprint 包含多个 Change
- **WHEN** Sprint 包含多个 REQ、BUG、Change 或大量 tasks
- **THEN** Fact Sheet MUST 输出聚合计数和精确证据路径，而不是复制原始 trace、tasks、acceptance report 或 generated 文件全文

#### Scenario: 需要读取 archive 目录
- **WHEN** Fact Sheet 需要读取 Sprint 内已归档 Change
- **THEN** 系统 MUST 从 `sprint.yaml` 的 Change 列表构造精确路径，不得通过宽泛搜索默认扫描整个 `openspec/changes/archive/**`

### Requirement: Fact Sheet 支持机器可读输出
系统 MUST 支持 Markdown 与 JSON 两种 Fact Sheet 输出，Markdown 用于人工和模型阅读，JSON 用于脚本验证和后续自动化复用。

#### Scenario: 请求 JSON 输出
- **WHEN** 用户或测试命令请求 JSON 格式 Fact Sheet
- **THEN** 系统 MUST 输出包含 Sprint、scope、changes、issues、warnings、token_risks 与 evidence_hints 的机器可读结构

### Requirement: AI 命令使用量事实源
系统 MUST 使用 `data/ai-usage/` 存放从本地 Codex session 派生的脱敏 AI 命令使用量事实，并且 MUST NOT 将原始 `~/.codex/sessions` JSONL、原始 prompt、系统指令或 developer 指令写入仓库事实源。

#### Scenario: 生成脱敏事实源
- **WHEN** 用户或脚本从本地 `~/.codex/sessions` 提取 AI 命令使用量
- **THEN** 系统 MUST 将派生后的 command run 或 Sprint 聚合记录写入 `data/ai-usage/`
- **AND** 系统 MUST NOT 复制或引用原始 session JSONL 全文

#### Scenario: 明确提交边界
- **WHEN** `data/ai-usage/` 存放 command run 明细或 Sprint 聚合快照
- **THEN** 系统 MUST 通过 README、ignore 规则或等价机制说明哪些文件可提交、哪些文件仅本地保留

### Requirement: 用户消息级命令运行边界
系统 MUST 将“用户一轮消息”定义为 AI command run 边界，并将该轮触发的模型调用、工具调用和中间输出聚合到同一个 command run，直到下一轮用户消息或会话结束。

#### Scenario: 单轮命令聚合
- **WHEN** 一个用户消息触发多次模型调用和工具调用
- **THEN** 系统 MUST 将这些事件聚合为一个 command run
- **AND** command run MUST 包含 started_at、ended_at、command、workflow_event、requirements、bugs、changes、sprint_id 和 attribution_confidence 或等价字段

#### Scenario: 多 Issue 显式关联
- **WHEN** 同一轮用户消息显式处理多个 REQ 或 BUG
- **THEN** command run MUST 支持多值 Issue 关联
- **AND** 系统 MUST 标记归因置信度

### Requirement: AI 命令 Token 与执行指标聚合
系统 MUST 为每个 command run 聚合模型调用次数、input tokens、cached input tokens、output tokens、reasoning output tokens、total tokens、工具调用次数、工具输出字符数和失败重跑次数。

#### Scenario: 按 last_token_usage 聚合 Token
- **WHEN** command run 内存在 `payload.type == token_count` 的事件
- **THEN** 系统 MUST 使用每个事件的 `last_token_usage` 汇总 Token 指标
- **AND** 系统 MUST NOT 将 session 级 `total_token_usage` 作为单个 command run 成本

#### Scenario: 聚合工具与重跑指标
- **WHEN** command run 内存在工具调用、工具结果或失败后重复执行
- **THEN** 系统 MUST 统计 tool_call_count、tool_output_chars 和 retry_count 或等价指标
- **AND** 如果 retry_count 是近似统计，系统 MUST 记录 retry_count_method 或等价口径说明

#### Scenario: 异常事件兼容
- **WHEN** session JSONL 中存在未知事件类型或单行解析失败
- **THEN** 系统 SHOULD 跳过异常事件并记录 warning
- **AND** 系统 MUST NOT 因单个异常事件中断整个 Sprint 使用量提取

### Requirement: 工作流对象归因
系统 MUST 通过独立字段将 command run 关联到 REQ、BUG、OpenSpec Change、Sprint 和 workflow event，并在归因不唯一时保留多值和置信度。

#### Scenario: 显式 ID 归因
- **WHEN** 用户命令文本或 Workflow Sync 参数包含 REQ、BUG、Change、Sprint 或 workflow event
- **THEN** 系统 MUST 将这些 ID 写入 command run 的结构化关联字段
- **AND** 系统 SHOULD 将归因置信度标记为 high

#### Scenario: 辅助规则归因
- **WHEN** command run 缺少显式 ID 但可由 trace 时间窗口、Sprint scope 反查或人工补录关联
- **THEN** 系统 MAY 关联对应工作流对象
- **AND** 系统 MUST 将 attribution_confidence 标记为 medium 或 low

### Requirement: Sprint 复盘命令环节 Token 分析
`/sprint-exps` MUST 优先读取 `data/ai-usage/` 的 Sprint 聚合快照，并按命令环节维度展示 AI 使用量分析。

#### Scenario: 存在 Sprint 使用量快照
- **WHEN** 用户执行 `/sprint-exps sprint-xxx` 且 `data/ai-usage/` 存在对应 Sprint 聚合快照
- **THEN** `/sprint-exps` MUST 展示 command run 数、模型调用次数、工具调用次数、失败重跑次数和 input/cached/output/reasoning/total tokens
- **AND** `/sprint-exps` SHOULD 展示高消耗原因和优化建议

#### Scenario: 缺少真实计量
- **WHEN** `/sprint-exps` 找不到对应 Sprint 的真实使用量快照
- **THEN** `/sprint-exps` MAY 使用估算模式
- **AND** 输出 MUST 明确标注“无精确 token 计量”或等价说明

### Requirement: AI 使用量事实脱敏
系统 MUST 对 AI 使用量事实源和 Sprint 复盘输出执行脱敏，避免泄露原始 prompt、系统指令、developer 指令、技能全文、本机绝对路径、密钥、Cookie、Authorization、真实客户数据、`.env` 内容和工具输出全文。

#### Scenario: 写入安全元数据
- **WHEN** 系统写入 command run 明细或 Sprint 聚合快照
- **THEN** 系统 MUST 仅保存数字指标、工作流 ID、仓库相对路径、hash、时间范围、短安全标签或 warning
- **AND** 系统 MUST NOT 保存工具输出全文

#### Scenario: 内容安全不确定
- **WHEN** 系统无法确认某段文本是否可以安全持久化
- **THEN** 系统 MUST 默认不写入该文本
- **AND** 系统 SHOULD 写入统计数字或 redaction warning

### Requirement: AI 使用量事实可复跑与校验
系统 MUST 支持可复核的重复提取、聚合再生成和异常告警，以便 Sprint 复盘可以校验 AI 使用量事实。

#### Scenario: 重复提取同一 session
- **WHEN** 用户或脚本重复提取同一 session 文件
- **THEN** 系统 SHOULD 通过 session hash、turn hash、时间范围或等价来源摘要避免重复累计同一 command run

#### Scenario: 由明细重建聚合
- **WHEN** Sprint 聚合快照需要校验或重新生成
- **THEN** 系统 SHOULD 能从 command run 明细重新生成等价聚合结果
- **AND** 系统 SHOULD 输出无法归因、缺少 token_count、发现本地绝对路径或疑似敏感内容被跳过的 warnings

### Requirement: Issue 归档子文档状态一致性门禁
系统 MUST 在 REQ / BUG 迁入 `issues/**/archive/` 前检查 issue 包内维护状态字段的 Markdown 子文档，防止 archive 包残留非闭环状态。系统 MUST 在发现残留状态时输出明确修复命令，并 MUST 提供安全的 reconcile 能力，在 Issue 主状态与关联交付对象已闭环时自动同步子文档残留状态。

#### Scenario: BUG 子文档存在非闭环状态
- **GIVEN** 一个 BUG 已满足关联 Change archived 与 `trace.md` done 条件
- **AND** 该 BUG 包内任一 Markdown 子文档的 frontmatter 或 fenced YAML block 包含 `status: draft`、`status: pending_review`、`status: in_sprint`、`status: applied`、`status: todo` 或 `status: open`
- **WHEN** 系统执行 issue archive promote
- **THEN** 系统 MUST 阻断该 BUG 迁入 `issues/bugs/archive/`
- **AND** 报告 MUST 包含 BUG id、文件路径、状态来源与状态值
- **AND** 报告 MUST 包含可直接执行的 dry-run reconcile 命令与实际写入命令

#### Scenario: REQ 子文档存在非闭环状态
- **GIVEN** 一个 REQ 已满足关联 Change archived 与 `trace.md` done 条件
- **AND** 该 REQ 包内任一 Markdown 子文档的 frontmatter 或 fenced YAML block 包含非闭环状态
- **WHEN** 系统执行 issue archive promote
- **THEN** 系统 MUST 阻断该 REQ 迁入 `issues/requirements/archive/`
- **AND** 报告 MUST 包含 REQ id、文件路径、状态来源与状态值
- **AND** 报告 MUST 包含可直接执行的 dry-run reconcile 命令与实际写入命令

#### Scenario: 子文档状态均已闭环
- **GIVEN** 一个 REQ 或 BUG 已满足 archive promote 的主状态条件
- **AND** issue 包内 Markdown 子文档不存在非闭环状态残留
- **WHEN** 系统执行 issue archive promote
- **THEN** 系统 MAY 将该 issue 从 `review/` 迁入 `archive/`

#### Scenario: 输出可操作修正建议
- **WHEN** issue archive promote 因子文档状态残留被阻断
- **THEN** 系统 MUST 输出建议，提示先完成评审/验收或将真实已闭环子文档状态同步为闭环状态
- **AND** 建议 MUST 区分“可自动 reconcile”的闭环 Issue 与“必须先推进上游流程”的未闭环 Issue

#### Scenario: Dry-run 预览子文档状态 reconcile
- **GIVEN** 一个 REQ 或 BUG 的主状态、关联 Change 与必要 Sprint 状态已闭环
- **AND** issue 包内 Markdown 子文档存在非闭环状态残留
- **WHEN** 用户执行子文档状态 reconcile dry-run 命令
- **THEN** 系统 MUST 不写入文件
- **AND** 报告 MUST 列出 issue id、文件路径、状态来源、旧状态、目标状态与将刷新的 `updated_at`

#### Scenario: 写入子文档状态 reconcile
- **GIVEN** 一个 REQ 或 BUG 的主状态、关联 Change 与必要 Sprint 状态已闭环
- **AND** dry-run 报告确认存在可修复的子文档状态残留
- **WHEN** 用户执行子文档状态 reconcile 写入命令
- **THEN** 系统 MUST 将对应 Markdown 子文档 frontmatter 与 fenced YAML block 中的残留状态同步为闭环状态
- **AND** 系统 MUST 刷新被修改 Markdown 的 `updated_at`
- **AND** 系统 MUST 输出修改摘要，包含修改文件数、字段数、issue id、旧状态与新状态

#### Scenario: 未闭环 Issue 禁止 reconcile 写入
- **GIVEN** 一个 REQ 或 BUG 的主状态、关联 Change 或必要 Sprint 状态尚未闭环
- **WHEN** 用户执行子文档状态 reconcile 写入命令
- **THEN** 系统 MUST 拒绝写入并返回非零退出码
- **AND** 报告 MUST 说明阻断原因与应先执行的上游工作流命令

### Requirement: Archived Change trace 兜底摘要门禁
系统 MUST 在 Sprint 或 OpenSpec 归档 readiness gate 中检查 archived Change 的归档验证证据；当 archived Change 缺失 `trace.md` 时，系统 MUST 要求 `proposal.md`、`design.md` 或 `tasks.md` 中至少一个文件包含标准化归档验证摘要。

#### Scenario: archived Change 存在 trace
- **WHEN** readiness gate 检查一个 archived Change
- **AND** 该 Change 目录包含 `trace.md`
- **THEN** 系统 MUST 将该 Change 的 trace 状态记录为存在
- **AND** 系统 MUST 不因 fallback summary 缺失而阻断该 Change

#### Scenario: archived Change 缺失 trace 但存在兜底摘要
- **WHEN** readiness gate 检查一个 archived Change
- **AND** 该 Change 目录缺失 `trace.md`
- **AND** `proposal.md`、`design.md` 或 `tasks.md` 中存在标准化归档验证摘要
- **THEN** 系统 MUST 将该 Change 标记为 fallback summary pass
- **AND** readiness 报告 MUST 展示承载摘要的文件路径

#### Scenario: archived Change 缺失 trace 且无兜底摘要
- **WHEN** readiness gate 检查一个 archived Change
- **AND** 该 Change 目录缺失 `trace.md`
- **AND** `proposal.md`、`design.md`、`tasks.md` 均不存在标准化归档验证摘要
- **THEN** 系统 MUST 输出 blocker
- **AND** 系统 MUST 返回非零退出码
- **AND** blocker MUST 包含 Change id、归档路径、检查过的候选文件和缺失的摘要项

#### Scenario: active Change 与 archived Change 语义区分
- **WHEN** readiness gate 同时检查 active Change 与 archived Change
- **THEN** 系统 MUST 在报告中清晰区分 active Change 状态检查与 archived Change 归档证据检查
- **AND** 系统 MUST 仅对 archived Change 强制执行 trace 缺失后的 fallback summary 门禁

#### Scenario: 兜底摘要内容完整性
- **WHEN** archived Change 缺失 `trace.md`
- **AND** 某个候选文件包含标准化归档验证摘要章节
- **THEN** 摘要 MUST 至少覆盖验证命令与结果、验收结论、关联 Issue 或 Sprint 状态、归档路径或归档时间

### Requirement: Workflow Sync 支持摘要输出模式
系统 MUST 为 Workflow Sync 报告提供摘要输出模式，用聚合计数和关键上下文替代成功路径中的长文件明细。

#### Scenario: 成功同步输出摘要
- **WHEN** 用户或 source-command 执行 `scripts/sync-workflow-status.py` 且同步成功
- **THEN** 系统 MUST 输出 Workflow Sync Report 摘要
- **AND** 摘要 MUST 包含 event、focus issue 或 change、sprint 解析结果、updated 数量、skipped 数量和 errors 数量
- **AND** 系统 MUST NOT 默认逐条输出完整 `Skipped (no delta)` 文件列表

#### Scenario: 无变化文件较多
- **WHEN** Workflow Sync 产生多个 skipped no-delta 结果且没有错误
- **THEN** 摘要 MUST 仅展示 skipped 聚合数量或等价短提示
- **AND** 输出 MUST 提供查看详细模式的提示或保留可发现的详细模式参数

### Requirement: Workflow Sync 保留详细输出模式
系统 MUST 保留详细输出模式，用于需要逐文件 updated/skipped 结果的调试、兼容或人工核查场景。

#### Scenario: 显式请求详细输出
- **WHEN** 用户使用详细输出参数执行 `scripts/sync-workflow-status.py`
- **THEN** 系统 MUST 输出逐文件 updated 明细
- **AND** 系统 MUST 输出逐文件 skipped no-delta 明细
- **AND** 输出的同步结果和退出码 MUST 与摘要模式一致

### Requirement: Workflow Sync 失败路径保留诊断信息
系统 MUST 在失败或 drift 检查失败时保留足够诊断信息，不能因为摘要模式隐藏错误原因。

#### Scenario: 同步产生错误
- **WHEN** Workflow Sync 报告包含 errors
- **THEN** 系统 MUST 输出每条错误原因
- **AND** 系统 MUST 返回非零退出码
- **AND** 系统 MAY 展开相关 updated 或 skipped 文件线索以帮助定位

#### Scenario: check 模式发现 drift
- **WHEN** 用户执行 `scripts/sync-workflow-status.py --check` 且发现 drift
- **THEN** 系统 MUST 报告 drift 文件数量和错误说明
- **AND** 系统 MUST 提供能定位 drift 文件的详细输出路径或详细模式

### Requirement: Sprint close 默认检查 AI usage snapshot
系统 MUST 在 Sprint close、Sprint archive 或等价收尾流程中检查目标 Sprint 的 AI usage snapshot 状态，并输出可追踪的状态摘要。

#### Scenario: snapshot 存在且可用
- **WHEN** 用户执行 Sprint close、`/sprint-archive` 或等价收尾流程
- **AND** `data/ai-usage/sprints/<sprint-id>.json` 存在且通过新鲜度与覆盖范围校验
- **THEN** 系统 MUST 输出 snapshot 状态摘要，包含 snapshot_status、snapshot_path、coverage、usage_mode、generated_at 和 warning 数量
- **AND** usage_mode MUST 为 `actual`

#### Scenario: snapshot 缺失
- **WHEN** 用户执行 Sprint close、`/sprint-archive` 或等价收尾流程
- **AND** 目标 Sprint 缺少 AI usage snapshot
- **THEN** 系统 SHOULD 尝试生成或刷新目标 Sprint 的 snapshot
- **AND** 若无法自动生成，系统 MUST 输出 warning、缺失原因和 recommended action

#### Scenario: snapshot 生成失败
- **WHEN** Sprint close 或 archive 流程尝试生成 AI usage snapshot
- **AND** 生成失败、session 数据不可访问或解析失败
- **THEN** 系统 MUST 将 snapshot_status 标记为 `failed`
- **AND** 系统 MUST NOT 输出或写入“真实统计已使用”的结论

### Requirement: AI usage snapshot 新鲜度与覆盖校验
系统 MUST 校验 AI usage snapshot 的新鲜度、Sprint 归属、scope 覆盖和必要指标，防止过期或覆盖不足的 snapshot 被当作真实统计使用。

#### Scenario: snapshot 早于关键变更
- **WHEN** snapshot 生成时间早于目标 Sprint 最近一次 scope、close、archive 或关联 trace 关键更新时间
- **THEN** 系统 MUST 将 snapshot 标记为 `stale` 或输出等价 warning
- **AND** 系统 MUST 提示刷新 snapshot

#### Scenario: snapshot 覆盖不足
- **WHEN** snapshot 不包含目标 Sprint ID、无法覆盖 Sprint scope 中的主要 REQ/BUG/Change，或必要 Token 指标为空
- **THEN** 系统 MUST 输出覆盖不足 warning
- **AND** 系统 MUST NOT 将该 snapshot 作为完整 `actual` 统计使用

#### Scenario: 无法完全判定新鲜度
- **WHEN** 系统无法可靠判断 snapshot 是否覆盖所有关键对象
- **THEN** 系统 MUST 输出 warning
- **AND** 系统 MUST 在复盘输出中保留该不确定性说明

### Requirement: `/sprint-exps` 禁止静默 estimated fallback
`/sprint-exps` MUST 优先读取目标 Sprint 的 AI usage snapshot；当真实 snapshot 不可用时，系统 MUST 显式标注估算模式、原因和补救动作。

#### Scenario: 使用真实 snapshot 复盘
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **AND** 目标 Sprint 存在可用 AI usage snapshot
- **THEN** `/sprint-exps` MUST 使用 `actual` 口径展示 command run 数、模型调用次数、工具调用次数、失败重跑次数和 input/cached/output/reasoning/total tokens
- **AND** `/sprint-exps` SHOULD 展示高消耗原因和优化建议

#### Scenario: 真实 snapshot 不可用
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **AND** 目标 Sprint 缺少可用 AI usage snapshot
- **THEN** `/sprint-exps` MAY 使用估算 fallback
- **AND** 输出 MUST 包含 `ai_usage_mode: estimated_fallback`、reason 和 recommended_action 或等价结构化说明

#### Scenario: snapshot 过期或失败
- **WHEN** `/sprint-exps` 读取到 stale、failed 或覆盖不足的 snapshot
- **THEN** `/sprint-exps` MUST NOT 静默按真实统计输出
- **AND** `/sprint-exps` MUST 显示 snapshot 状态、降级原因和刷新建议

### Requirement: AI usage snapshot 默认流程继承安全边界
Sprint close、Sprint archive 与 `/sprint-exps` 中的 AI usage snapshot 生成和消费流程 MUST 继承 AI 使用量事实源的脱敏和上下文预算边界。

#### Scenario: 成功路径摘要输出
- **WHEN** snapshot 检查、生成或读取成功
- **THEN** 系统 MUST 输出摘要信息
- **AND** 系统 MUST NOT 默认展开完整 session、prompt、trace、tasks 或工具日志

#### Scenario: 持久化安全元数据
- **WHEN** 系统生成或刷新 AI usage snapshot
- **THEN** 系统 MUST NOT 写入原始 prompt、系统指令、developer 指令、技能全文、`~/.codex/sessions` 原始 JSONL、本机绝对路径、工具输出全文、密钥、Cookie、Authorization、真实客户数据或 `.env` 内容
- **AND** 系统 MUST 优先保存数字指标、工作流 ID、仓库相对路径、hash、时间范围、短安全标签或 warning

### Requirement: 工作流命令自动构建 AI usage 事实源
系统 MUST 为 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 工作流命令提供后置 AI usage fact source 构建流程，并在主命令和 Workflow Sync 成功后尝试生成或刷新脱敏使用量事实。

#### Scenario: 主命令与 Workflow Sync 成功后触发
- **WHEN** 用户执行 `/req-*`、`/bug-*`、`/opsx-*` 或 `/sprint-*` 工作流命令
- **AND** 主命令完成且 Workflow Sync 返回成功
- **THEN** 系统 MUST 触发统一 AI usage fact source hook 或等价共享流程
- **AND** 系统 MUST 输出短摘要，包含 hook status、usage mode、warning 数量和 recommended action

#### Scenario: 主命令失败时跳过
- **WHEN** 工作流命令主流程失败或 Workflow Sync 失败
- **THEN** 系统 MAY 跳过 AI usage fact source hook
- **AND** 系统 MUST 在输出中说明本次未构建 AI usage 事实源的原因

#### Scenario: 无 Sprint 归属时不伪造 snapshot
- **WHEN** 命令可归因到 REQ 或 BUG 但无法解析到 Sprint
- **THEN** 系统 MUST NOT 创建伪造的 Sprint 聚合快照
- **AND** 系统 SHOULD 生成 command run 明细或输出无法生成的原因
- **AND** 输出 MUST 标明 Sprint snapshot skipped 或等价状态

### Requirement: 统一 AI usage post-command hook
系统 MUST 通过统一脚本、函数或等价封装处理工作流命令后的 AI usage 构建，避免 命令技能复制复杂 session 解析、归因和脱敏逻辑。

#### Scenario: 命令技能引用统一 hook
- **WHEN** 任一命令技能需要在命令完成后构建 AI usage 事实源
- **THEN** 技能 MUST 引用统一 hook、共享规则或同一脚本入口
- **AND** 技能 MUST NOT 复制原始 session 解析、prompt 处理或工具输出处理的长逻辑

#### Scenario: hook 输入包含工作流上下文
- **WHEN** 系统调用 AI usage post-command hook
- **THEN** hook MUST 支持 workflow event、REQ ID、BUG ID、Change ID、Sprint ID、session 输入或 manual map 的等价输入
- **AND** hook SHOULD 使用这些输入提升 command run 归因准确性

#### Scenario: hook 支持检查或降级模式
- **WHEN** 本地 session 输入不可用或当前环境无法构建真实事实源
- **THEN** hook MUST 输出 `unavailable` 或 `estimated_fallback` 等价状态
- **AND** hook MUST 给出 reason 和 recommended action

#### Scenario: hook 安全扫描失败时隔离记录
- **WHEN** hook 可读取 session 且部分 command run 通过归因
- **AND** 其中一条或多条 command run 因本机绝对路径、认证头、`.env`、密钥或其他不允许持久化内容未通过安全扫描
- **THEN** 系统 MUST 跳过不安全 command run 并输出 `unsafe-records-skipped:<count>` 或等价 warning
- **AND** 系统 MUST 继续写入其余安全 command run 并按安全记录刷新 Sprint snapshot
- **AND** 系统 MUST NOT 因单条不安全记录抛出未处理异常导致父命令误判为未执行

#### Scenario: 合法工作流 ID 不因业务词误判为敏感
- **WHEN** REQ、BUG 或 Change ID 中包含 `password`、`token` 等业务词
- **THEN** hook MUST 允许这些 ID 作为工作流元数据持久化
- **AND** 只有认证头、赋值形态的密钥字段、`.env` 内容、本机绝对路径或等价敏感值 SHALL 阻断持久化

### Requirement: 工作流命令 command run 与 Sprint snapshot 写入
系统 MUST 在可安全解析本地 session 输入时写入脱敏 command run 明细，并在命令可明确关联 Sprint 时生成或刷新 Sprint 聚合快照。

#### Scenario: 写入 command run 明细
- **WHEN** hook 可读取并解析本地 session 输入
- **THEN** 系统 MUST 将脱敏 command run 明细写入 `data/ai-usage/command-runs/` 或等价事实源路径
- **AND** command run MUST 通过 requirements、bugs、changes、sprint_id、workflow_event 或等价字段进行归因

#### Scenario: command run 按对象类型分组
- **WHEN** command run 是 release 命令且提供 `--release vX.Y.Z`
- **THEN** 系统 MUST 写入 `data/ai-usage/command-runs/releases/vX.Y.Z/`
- **AND** 即使 release 命令同时关联 REQ、BUG 或 Change，也 MUST 优先归入版本目录，不得落入 `issues/` 或 `opsxs/`
- **WHEN** command run 关联 REQ 或 BUG
- **THEN** 系统 MUST 写入 `data/ai-usage/command-runs/issues/<REQ-or-BUG-id>/`
- **AND** REQ/BUG ID MUST 使用完整 canonical issue ID
- **WHEN** command run 是无 REQ/BUG 关联的纯 OpenSpec / opsx 命令
- **THEN** 系统 MUST 写入 `data/ai-usage/command-runs/opsxs/<change-id>/`
- **AND** 能从 Change 反查 REQ/BUG 的 opsx 命令 MUST 优先归入 `issues/`，不得落入 `opsxs/`

#### Scenario: 刷新 Sprint snapshot
- **WHEN** hook 可明确解析到 `sprint-xxx`
- **THEN** 系统 SHOULD 生成或刷新 `data/ai-usage/sprints/<sprint-id>.json`
- **AND** snapshot MUST 包含 sprint_id、generated_at、coverage、totals、warnings 和 usage mode 所需字段

#### Scenario: snapshot 不满足 actual 条件
- **WHEN** snapshot 覆盖不足、过期、必要指标为空或解析失败
- **THEN** 系统 MUST NOT 将该 snapshot 标记为完整 `actual`
- **AND** 系统 MUST 输出 warning、降级原因和刷新建议

### Requirement: Release 命令 AI usage 版本级存储
系统 MUST 为 `/release-propose`、`/release-prepare`、`/release-publish` 提供版本级 AI usage artifact，避免 release 命令只散落在通用 command-runs 或被误归到单一 Sprint snapshot。

#### Scenario: release 命令写入版本目录
- **WHEN** release post-command hook 提供 `--release vX.Y.Z`
- **AND** hook 可安全解析本地 session 输入
- **THEN** 系统 MUST 写入 release command run 明细 `data/ai-usage/command-runs/releases/vX.Y.Z/<date>--<workflow-event>--<session-hash>.json`
- **AND** 系统 MUST 写入版本级 artifact `data/ai-usage/command-runs/releases/vX.Y.Z/<workflow-event>.json`
- **AND** `<workflow-event>` SHALL 为 `release.propose`、`release.prepare` 或 `release.publish`
- **AND** 版本级 artifact MUST 包含 `release_version`、`workflow_event`、`generated_at`、`coverage`、`totals` 和脱敏 command run 明细或等价安全摘要

#### Scenario: release 范围 Sprint 与 Sprint snapshot 分离
- **WHEN** release 对象包含一个或多个 Sprint
- **THEN** hook MUST 支持重复 `--release-sprint <sprint-id>` 或等价输入记录版本覆盖范围
- **AND** `--release-sprint` MUST 写入 release artifact 的 `coverage.sprints`
- **AND** `--sprint` MUST 仅表示单个 Sprint snapshot 刷新目标，不得作为多 Sprint release 范围的唯一表达

#### Scenario: release 命令输出版本 artifact 摘要
- **WHEN** release post-command hook 完成生成、dry-run 或降级
- **THEN** 输出 MUST 包含 `release_artifact` 摘要
- **AND** 摘要 MUST 标明 status、path 和 reason
- **AND** 若缺少 `--release`，`release_artifact` MUST 为 `skipped` 且 reason 为 `no-release` 或等价说明

#### Scenario: 多 Sprint release 不伪造单 Sprint 快照
- **WHEN** 一个 release 对象关联多个 Sprint
- **THEN** release 命令的版本级 artifact MUST 作为该命令的主事实源
- **AND** 系统 MUST NOT 仅因 release 覆盖多个 Sprint 就把同一 command run 复制成多个 Sprint snapshot
- **AND** 如调用方需要刷新 Sprint snapshot，MUST 按 Sprint 单独执行或明确说明刷新范围

#### Scenario: 全部候选记录不安全
- **WHEN** hook 找到目标 session 和目标 command run
- **AND** 所有候选 command run 都未通过持久化安全扫描
- **THEN** 系统 MUST NOT 写入 command run 或 Sprint snapshot
- **AND** 系统 MUST 输出 `usage_mode: unavailable`、`no-safe-command-runs` 和 recommended action
- **AND** 调用方 MUST 报告该 blocker，不得改用不存在的 session 输入伪造成功摘要

### Requirement: 自动构建继承 AI usage 安全边界
工作流命令自动构建 AI usage 事实源时 MUST 继承 AI 使用量事实源的脱敏、安全和上下文预算边界。

#### Scenario: 持久化安全字段
- **WHEN** hook 写入 command run 明细或 Sprint snapshot
- **THEN** 系统 MUST 仅持久化数字指标、工作流 ID、hash、时间范围、源行号范围、coverage、短安全标签或 warning
- **AND** 系统 MUST NOT 持久化原始 prompt、系统指令、developer 指令、技能全文、原始 session JSONL、本机绝对路径、工具输出正文、密钥、Cookie、Authorization、真实客户数据或 `.env` 内容

#### Scenario: 命令输出保持摘要
- **WHEN** hook 完成检查、生成或降级
- **THEN** 系统 MUST 只输出摘要信息
- **AND** 系统 MUST NOT 默认打印完整 session、prompt、工具日志、OpenAPI/Orval 大 diff、测试日志全文或完整 snapshot 内容

#### Scenario: 重复构建幂等
- **WHEN** 用户或系统重复对同一 session 或同一 command run 执行自动构建
- **THEN** 系统 SHOULD 使用 session hash、turn hash、command run id 或等价来源摘要避免重复累计
- **AND** 系统 SHOULD 为重复、无法归因或疑似敏感内容跳过输出 warning

### Requirement: 工作流成功路径紧凑输出契约
系统 MUST 为 Workflow Sync 与 AI usage post-command hook 建立统一 compact summary 输出契约，使工作流命令成功路径默认只输出聚合状态、关键上下文和推荐动作。

#### Scenario: Workflow Sync 默认成功摘要
- **WHEN** 用户或命令技能执行 `scripts/sync-workflow-status.py` 且命令成功完成
- **THEN** 系统 MUST 默认输出 Workflow Sync Report 摘要
- **AND** 摘要 MUST 至少包含 event、focus 对象、Sprint 解析结果、updated 数量、skipped 数量和 errors 数量
- **AND** 系统 MUST NOT 默认输出完整 `Skipped (no delta)` 文件列表、完整派生 Scope 块或长篇逐文件成功日志

#### Scenario: Workflow Sync 详细模式保留逐文件明细
- **WHEN** 用户或维护者显式请求 Workflow Sync 详细输出模式
- **THEN** 系统 MUST 输出逐文件 updated、skipped 和必要诊断明细
- **AND** 详细模式的同步结果、写入行为和退出码 MUST 与默认摘要模式一致

#### Scenario: Workflow Sync 失败路径保留诊断
- **WHEN** Workflow Sync 发生错误、drift 检查失败或 marker 解析失败
- **THEN** 系统 MUST 输出错误数量和每条错误原因
- **AND** 系统 MUST 返回非零退出码
- **AND** 系统 MUST 提供可定位问题文件或启用详细模式的提示

#### Scenario: AI usage hook 输出固定摘要字段
- **WHEN** 工作流命令在 Workflow Sync 成功后执行 AI usage post-command hook
- **THEN** 用户可见输出 MUST 只展示 compact summary
- **AND** compact summary MUST 包含 `status`、`usage_mode`、`command_run_count`、`sprint_snapshot`、`warning_count` 和 `recommended_action`
- **AND** 系统 MUST NOT 默认打印完整 session、原始 prompt、系统指令、developer 指令、技能全文、工具输出正文、完整 snapshot JSON 或完整 command run 明细

#### Scenario: AI usage hook 降级或不可用摘要
- **WHEN** AI usage hook 因本地 session 输入不可用、无安全记录、Sprint 无法解析或 snapshot 被跳过而降级
- **THEN** 系统 MUST 仍输出 compact summary
- **AND** `usage_mode` MUST 标明 `unavailable`、`estimated_fallback` 或等价降级状态
- **AND** `recommended_action` MUST 说明下一步可执行动作或无法自动恢复的原因
- **AND** 父工作流命令 MUST NOT 因 session 输入不可用而被判定失败

#### Scenario: 成功路径日志长度受上下文预算约束
- **WHEN** Workflow Sync 和 AI usage hook 均成功或以允许的降级状态完成
- **THEN** 命令技能 MUST 只向用户转述 compact summary 和必要的 Change/Sprint/Issue 结果
- **AND** 命令技能 MUST NOT 默认转述完整测试日志、完整 OpenAPI/Orval diff、完整 Workflow Sync 派生块、完整 AI usage JSON 或完整 snapshot 内容

### Requirement: Sprint 归档后旧路径残留检查
系统 MUST 在 `/sprint-archive` 完成 Sprint 目录迁移、Workflow Sync 与关联 Issue promote 后，检查本 Sprint 关联文档中是否残留已迁移前的旧路径引用，防止归档后文档继续指向 `iterations/change/` 或 active Change 目录。

#### Scenario: Sprint 归档后无旧路径残留
- **WHEN** `/sprint-archive sprint-xxx` 已将 Sprint 目录迁移到 `iterations/archive/sprint-xxx/`
- **AND** Sprint 关联文档不包含 `iterations/change/sprint-xxx/` 或已归档 Change 的 active 路径引用
- **THEN** 系统 MUST 在最终报告中展示路径残留检查通过
- **AND** 报告 MUST 包含检查文件数与命中数摘要

#### Scenario: Sprint 归档后仍残留 change 路径
- **WHEN** `/sprint-archive sprint-xxx` 完成目录迁移后执行路径残留检查
- **AND** 任一关联 Markdown 文档仍包含 `iterations/change/sprint-xxx/`
- **THEN** 系统 MUST 将该残留报告为 blocker 或 warning
- **AND** 报告 MUST 包含文件路径、行号、旧路径与建议的新路径 `iterations/archive/sprint-xxx/`
- **AND** `/sprint-archive` MUST 不得静默输出成功闭环结论

#### Scenario: Sprint 归档后仍残留 active Change 路径
- **WHEN** Sprint 范围内的 Change 已归档到 `openspec/changes/archive/<date>-<change-id>/`
- **AND** 任一关联 Markdown 文档仍包含 `openspec/changes/<change-id>/`
- **THEN** 系统 MUST 报告该 Change 路径残留
- **AND** 报告 MUST 包含对应归档路径或说明无法解析归档路径

#### Scenario: 检查范围受 Sprint scope 限制
- **WHEN** 系统执行 Sprint 归档后旧路径残留检查
- **THEN** 系统 MUST 以 `sprint.yaml` 的 `requirements[]`、`bugs[]` 与 `changes[]` 定位检查范围
- **AND** 系统 MUST NOT 默认扫描整个 `openspec/changes/archive/**`、`issues/**` 或生成物目录

### Requirement: Sprint 复盘旧路径残留提示
系统 MUST 在 `/sprint-exps` 为已归档 Sprint 生成复盘前检查旧路径残留，并将残留作为复盘风险或 evidence hint 暴露，避免复盘文档继续传播过期链接。

#### Scenario: 复盘前发现旧路径残留
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **AND** `sprint-xxx` 已位于 `iterations/archive/sprint-xxx/`
- **AND** 路径残留检查发现 `iterations/change/sprint-xxx/` 或 active Change 路径引用
- **THEN** Experience Analysis Report MUST 展示 residual path warning
- **AND** 复盘文档 MUST NOT 将旧路径作为新的证据链接写入
- **AND** 报告 MUST 给出残留文件路径与建议修正路径

#### Scenario: 复盘前未发现旧路径残留
- **WHEN** `/sprint-exps` 的路径残留检查未发现命中
- **THEN** Experience Analysis Report SHOULD 展示检查通过摘要
- **AND** 复盘可继续使用 Fact Sheet 中的归档路径作为证据来源

#### Scenario: Fact Sheet 暴露路径残留证据
- **WHEN** Fact Sheet 或复盘辅助脚本发现旧路径残留
- **THEN** 机器可读输出 MUST 包含 warning 或 evidence hint
- **AND** warning MUST 至少包含残留类型、文件路径、旧路径与建议新路径

### Requirement: 规则与 Skill 已读摘要复用

系统 MUST 在 Agent 上下文预算治理中定义同一会话内规则与 Skill 已读摘要复用机制，减少连续工作流命令重复读取相同文件。

#### Scenario: 同一会话复用规则摘要

- **WHEN** Agent 在同一会话中已经读取过 `AGENTS.md`、`openspec/project.md` 或相关 `rules/*.md`
- **AND** 目标文件未显示内容、mtime、hash 或 `updated_at` 变化
- **AND** 已有摘要足以覆盖当前命令的规则门禁
- **THEN** Agent SHOULD 用摘要承接
- **AND** Agent SHOULD NOT 重复全量读取相同文件

#### Scenario: 同一会话复用 Skill 摘要

- **WHEN** Agent 在同一会话中已经读取过当前命令 Skill 或共用 Skill
- **AND** 目标 Skill 未显示内容、mtime、hash 或 `updated_at` 变化
- **AND** 已有摘要足以覆盖当前命令步骤和 Final Step
- **THEN** Agent SHOULD 用摘要承接
- **AND** Agent SHOULD 只补读当前任务缺失的必要片段

#### Scenario: 摘要最小信息

- **WHEN** Agent 使用已读摘要承接规则或 Skill
- **THEN** 摘要 SHOULD 能表达文件路径、版本线索、与当前任务相关的规则/门禁摘要、适用范围和刷新原因或等价信息
- **AND** 摘要 MAY 只存在于同一对话上下文中

### Requirement: 摘要复用失效与补读

系统 MUST 定义摘要复用的失效条件，确保上下文节省不会绕过 OpenSpec、Issue lifecycle、安全、API、DB、上传、Docker、发布或 Workflow Sync 门禁。

#### Scenario: 文件变化触发补读

- **WHEN** 规则或 Skill 文件的内容、mtime、hash、`updated_at` 或等价版本线索显示已变化
- **THEN** Agent MUST 重新读取目标文件或必要片段
- **AND** Agent MUST NOT 继续使用旧摘要作为唯一依据

#### Scenario: 任务风险升级触发补读

- **WHEN** 命令从 capture、explore、generate 等轻量阶段升级到 apply、archive、release 或等价高风险阶段
- **OR** 当前任务涉及权限、安全、API、DB、上传、Docker、发布或 OpenSpec 红线
- **THEN** Agent MUST 补读当前 Change、Issue、Sprint、trace、Final Step 或失败相关片段
- **AND** Agent MUST NOT 仅凭旧摘要继续执行高风险动作

#### Scenario: 用户要求或失败诊断触发补读

- **WHEN** 用户显式要求重新读取或复核原文
- **OR** Workflow Sync、测试、校验脚本或 OpenSpec CLI 返回失败
- **THEN** Agent MUST 回到相关原文或必要片段定位

### Requirement: 命令 Skill 摘要复用 Guardrails

命令 Skill MUST 在 `Context Budget Guardrails` 或等价章节中表达规则与 Skill 已读摘要复用约束，并保留命令特定门禁。

#### Scenario: 命令 Skill 使用统一预算表述

- **WHEN** 新增或更新 `.agents/skills/{req,bug,opsx,sprint,build}-*`、`.agents/skills/capture`、`.agents/skills/initialize-project` 或 release 命令 Skill
- **THEN** Skill MUST 引用 `rules/agent-context-budget.md`
- **AND** Skill SHOULD 明确同一会话已读且无变更的规则和 Skill 用摘要承接
- **AND** Skill MUST 保留命令特定 Must Read、Workflow Sync、AI usage hook 和业务门禁

#### Scenario: 高风险命令保留补读要求

- **WHEN** Skill 对应 apply、archive、release、req-opsx、bug-opsx、sprint-propose 或等价高风险命令
- **THEN** Skill MUST 要求先读取当前 Change、Issue、Sprint、trace/status 或 OpenSpec CLI 输出的必要片段
- **AND** Skill MUST NOT 要求默认全量读取历史归档、所有 specs、generated 文件或大目录

### Requirement: 上下文预算校验覆盖摘要复用

系统 MUST 通过上下文预算校验阻止命令 Skill 缺少预算入口、缺少摘要复用约束或回退到默认宽泛读取。

#### Scenario: 校验命令 Skill 摘要复用约束

- **WHEN** 用户或 CI 执行 `python scripts/validate-agent-context-budget.py`
- **THEN** 脚本 MUST 检查命令 Skill 是否引用 `rules/agent-context-budget.md`
- **AND** 脚本 MUST 检查命令 Skill 是否包含规则与 Skill 已读摘要复用的等价表述
- **AND** 脚本 MUST 报告缺失约束的文件路径

#### Scenario: 校验默认宽泛读取回退

- **WHEN** 命令 Skill 包含默认 `cat rules/*.md`、`ls -R`、无边界 `rg <keyword> .` 或等价宽泛读取指令
- **AND** 该指令不是明确禁止或反例说明
- **THEN** 校验脚本 MUST 返回非零退出码
- **AND** 报告 MUST 包含具体文件路径与行号

### Requirement: 摘要复用安全边界

系统 MUST 确保规则与 Skill 摘要复用不会持久化敏感上下文或扩大成功路径输出。

#### Scenario: 禁止持久化敏感原文

- **WHEN** Agent 使用规则或 Skill 摘要复用机制
- **THEN** 系统 MUST NOT 将原始 prompt、系统指令、developer 指令、完整 session JSONL、工具输出正文、密钥、Cookie、Authorization header、`.env` 内容或真实客户数据写入仓库

#### Scenario: 成功路径输出保持紧凑

- **WHEN** 工作流命令成功复用摘要并完成主流程
- **THEN** Agent SHOULD 只输出复用摘要、补读片段、计数、warning 或 recommended action 的短摘要
- **AND** Agent MUST NOT 默认转述完整规则、完整 Skill、完整测试日志、完整 Workflow Sync 派生块或完整 generated diff

