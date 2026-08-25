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
系统 MUST 在 Fact Sheet 中保留证据路径或回读提示，使复盘结论可以追溯到 Sprint、Issue、Change 或验收文件；复盘默认路径 MUST 将完整 evidence hints 作为按需回读索引，而不是默认完整输出内容。

#### Scenario: 存在状态不一致或缺失项
- **WHEN** Fact Sheet 发现 Change 缺少 `trace.md`、tasks 未完成、Issue 子文档状态残留或 acceptance report 结论不清晰
- **THEN** 系统 MUST 在 Fact Sheet 中标记风险，并给出建议回读的具体文件路径或关键词

#### Scenario: 无需全文回读
- **WHEN** Fact Sheet 已能提供某项复盘所需的机器事实
- **THEN** `/sprint-exps` MUST 优先使用 Fact Sheet 中的摘要，不得默认全文读取对应四件套、trace 或 tasks 文件
- **AND** `/sprint-exps` MUST NOT 默认输出完整 `evidence_hints`

#### Scenario: 显式请求证据提示
- **WHEN** 用户显式要求证据提示、或 `/sprint-exps` 因 `needs_detail`、warning、missing、inconsistent 类风险需要定位原始证据
- **THEN** 系统 MUST 支持按需输出或读取完整 `evidence_hints`
- **AND** 输出 MUST 保留具体 reason 与相对路径

### Requirement: `/sprint-exps` 优先使用 Fact Sheet
`/sprint-exps` MUST 将自动 Fact Sheet 作为复盘的优先输入，并仅在证据不足、风险项存在或用户要求时读取原始文件片段；默认输入 SHOULD 使用紧凑 summary 模式以降低上下文占用。

#### Scenario: 正常复盘路径
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **THEN** 命令流程 MUST 先运行或读取该 Sprint 的 Fact Sheet summary，再基于 Fact Sheet 生成 Sprint 复盘与模型 Token 使用分析
- **AND** 默认复盘输出 MUST 不包含完整 `evidence_hints` 表

#### Scenario: Fact Sheet 标记需要细节
- **WHEN** Fact Sheet 标记 `needs_detail`、warning、missing 或 inconsistent 类风险
- **THEN** `/sprint-exps` MAY 按 Fact Sheet 的 evidence hints 读取对应原始文件片段
- **AND** `/sprint-exps` MAY 通过字段模式单独获取 `evidence_hints`

### Requirement: Fact Sheet 输出边界受上下文预算约束
Fact Sheet 生成与 `/sprint-exps` 消费流程 MUST 遵守 Agent 上下文预算规则，避免宽泛搜索、长日志、生成物全文 diff、完整 evidence hints 默认输出和历史归档全量展开。

#### Scenario: 大 Sprint 包含多个 Change
- **WHEN** Sprint 包含多个 REQ、BUG、Change 或大量 tasks
- **THEN** Fact Sheet MUST 输出聚合计数和精确证据路径，而不是复制原始 trace、tasks、acceptance report 或 generated 文件全文

#### Scenario: 需要读取 archive 目录
- **WHEN** Fact Sheet 需要读取 Sprint 内已归档 Change
- **THEN** 系统 MUST 从 `sprint.yaml` 的 Change 列表构造精确路径，不得通过宽泛搜索默认扫描整个 `openspec/changes/archive/**`

#### Scenario: 复盘默认输出使用紧凑边界
- **WHEN** `/sprint-exps` 调用 Fact Sheet 辅助脚本且未显式请求细节
- **THEN** 系统 MUST 使用 summary 或等价紧凑输出
- **AND** 输出 MUST 包含风险计数、关键状态与推荐回读信号
- **AND** 输出 MUST NOT 包含完整 `evidence_hints` 明细

### Requirement: Fact Sheet 支持机器可读输出
系统 MUST 支持 Markdown、完整 JSON、summary 与 fields 输出模式，Markdown 用于人工阅读，完整 JSON 用于调试和兼容自动化，summary 用于复盘默认输入，fields 用于按需读取特定字段。

#### Scenario: 请求 JSON 输出
- **WHEN** 用户或测试命令请求 JSON 格式 Fact Sheet
- **THEN** 系统 MUST 输出包含 Sprint、scope、changes、issues、warnings、token_risks 与 evidence_hints 的机器可读结构

#### Scenario: 请求 Summary 输出
- **WHEN** 用户、测试命令或 `/sprint-exps` 请求 summary 格式 Fact Sheet
- **THEN** 系统 MUST 输出包含 Sprint 基础信息、scope 计数、warnings 摘要、`needs_detail`、AI usage 状态和 token risks 的紧凑结构
- **AND** summary MUST NOT 默认包含完整 `evidence_hints`

#### Scenario: 请求 Fields 输出
- **WHEN** 用户、测试命令或 `/sprint-exps` 请求一个或多个字段路径
- **THEN** 系统 MUST 输出所请求字段的机器可读结构
- **AND** 系统 MUST 支持通过 fields 模式单独获取 `evidence_hints`

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
`/sprint-exps` MUST 优先读取 `data/ai-usage/` 的 Sprint 聚合快照，并在 Sprint AI usage snapshot fresh gate 通过后按命令环节维度展示 AI 使用量分析。fresh gate MUST 确认 snapshot 为 `present`、AI usage mode 为 `actual`、`usage_matrices` 存在、关键 totals 非空、当前 Sprint scope 的 requirements、bugs 和 changes coverage 均通过；未通过时默认不得输出真实成本矩阵或宣称完成真实 token 成本量化。Fact Sheet 计算 snapshot freshness baseline 时，未来计划 `sprint.yaml:start_date` 与 `sprint.yaml:end_date` MUST NOT 作为 `min_generated_at` 候选；这些未来计划时间 MUST 作为 skipped candidate 暴露，并使用 `future-planned-time` 或等价 reason。

#### Scenario: 存在新鲜且覆盖完整的 Sprint 使用量快照
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **AND** `data/ai-usage/` 存在对应 Sprint 聚合快照
- **AND** snapshot fresh gate 判定为通过
- **THEN** `/sprint-exps` MUST 展示 command run 数、模型调用次数、工具调用次数、失败重跑次数和 input/cached/output/reasoning/total tokens
- **AND** `/sprint-exps` SHOULD 展示高消耗原因和优化建议

#### Scenario: Snapshot 缺失或不可用
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **AND** Sprint AI usage snapshot 状态为 `missing`、`failed` 或 `unavailable`
- **THEN** `/sprint-exps` MUST 输出 fresh gate blocker、reason、impact 和 recommended_action
- **AND** `/sprint-exps` MUST NOT 默认生成真实 token 成本矩阵
- **AND** `/sprint-exps` MUST NOT 将 `estimated_fallback` 表述为真实成本量化结果

#### Scenario: Snapshot 过期或覆盖不足
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **AND** Sprint AI usage snapshot 状态为 `stale`
- **OR** snapshot coverage 缺少当前 Sprint scope 中的 requirement、bug 或 change
- **OR** snapshot 缺少 `usage_matrices`
- **THEN** `/sprint-exps` MUST 输出 fresh gate blocker，列出 compact warning_count、coverage status 和 recommended_action
- **AND** `/sprint-exps` MUST 要求刷新 snapshot 后再输出真实成本分析

#### Scenario: 用户显式接受估算复盘
- **WHEN** snapshot fresh gate 未通过
- **AND** 用户明确要求继续生成 fallback 复盘
- **THEN** `/sprint-exps` MAY 使用估算模式输出非量化成本风险分析
- **AND** 输出 MUST 明确标注 `ai_usage_mode: estimated_fallback`
- **AND** 输出 MUST 说明该结果不能用于真实 token 成本量化
- **AND** 输出 MUST 保留刷新真实 snapshot 的 recommended_action

#### Scenario: Fresh gate 输出保持紧凑且脱敏
- **WHEN** `/sprint-exps` 报告 Sprint AI usage snapshot fresh gate 结果
- **THEN** 输出 MUST 仅包含 status、usage mode、snapshot status、warning_count、coverage status、usage_matrices presence 和 recommended_action 等 compact 字段
- **AND** 输出 MUST NOT 包含原始 session JSONL、prompt、系统指令、developer 指令、技能全文、本机绝对路径、密钥、Cookie、Authorization header、`.env` 内容或工具输出全文

#### Scenario: 未来计划 start_date 不阻塞完整 snapshot
- **WHEN** Fact Sheet 为 Sprint 计算 AI usage freshness baseline
- **AND** `sprint.yaml:start_date` 晚于当前执行时间
- **AND** snapshot 本身为 `present`、`actual` 且 fresh gate 其他检查均通过
- **THEN** 系统 MUST 将该 `start_date` 记录到 `ai_usage_freshness_baseline.skipped[]`
- **AND** skipped reason MUST 为 `future-planned-time` 或等价说明
- **AND** 系统 MUST NOT 将该 `start_date` 作为 `min_generated_at`
- **AND** 系统 MUST NOT 仅因该未来 `start_date` 将 snapshot 判定为 `stale`

#### Scenario: 事实更新时间仍阻止陈旧 snapshot
- **WHEN** Fact Sheet 为 Sprint 计算 AI usage freshness baseline
- **AND** 四件套 `updated_at` 或其他非未来事实更新时间晚于 snapshot `generated_at`
- **THEN** 系统 MUST 继续将 snapshot 判定为 `stale`
- **AND** 系统 MUST 保留刷新 snapshot 的 recommended action

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
系统 MUST 在 REQ / BUG 迁入 `issues/**/archive/` 前检查 issue 包内维护状态字段的 Markdown 子文档，防止 archive 包残留非闭环状态。系统 MUST 在发现残留状态时输出明确修复命令，并 MUST 提供安全的 reconcile 能力，在 Issue 主状态与关联交付对象已闭环时自动同步子文档残留状态。归档同步阶段或 promote 前置流程 MUST 自动处理已由扫描分类确认可安全同步的 residual 状态残留；不得把这类安全残留继续交给 `promote-issues-for-archive` 作为阻断项。单个 Issue 的归档与子文档 reconcile MUST 以该 Issue 自身闭环为准，不得仅因所属 Sprint 尚未 completed 而阻断；Sprint completed 仅作为 `/sprint-archive` 整体归档门禁。该门禁 MUST 复用或兼容常规子文档 drift check 的扫描分类结果，并 MUST 区分“日常状态传播缺失”与“闭环 residual reconcile”两类问题。

#### Scenario: 归档同步自动清理安全 residual
- **GIVEN** 一个 REQ 或 BUG 已满足关联 Change archived 与 `trace.md` done 条件
- **AND** 子文档仅残留扫描分类为可安全同步的历史主状态，例如 `capture.md` 的 `status: captured`
- **WHEN** 系统执行归档同步或 promote 前置流程
- **THEN** 系统 MUST 自动将该残留同步为闭环目标状态
- **AND** 系统 MUST 刷新被修改 Markdown 的 `updated_at`
- **AND** 随后执行 `promote-issues-for-archive` MUST NOT 因该已安全处理的残留触发 Issue Subdocument Status Gate

#### Scenario: 安全 residual 自动处理保持幂等
- **GIVEN** 一个已闭环 Issue 的安全 residual 已被归档同步处理
- **WHEN** 系统再次执行相同归档同步或 promote 前置流程
- **THEN** 系统 MUST 报告 no delta 或等价摘要
- **AND** 系统 MUST NOT 重复写入无意义变更

#### Scenario: 人工判断 residual 不自动清理
- **GIVEN** 一个 REQ 或 BUG 的子文档状态残留缺少闭环证据、验收结果或字段语义不明
- **WHEN** 系统执行归档同步或 promote 前置流程
- **THEN** 系统 MUST NOT 自动修改该残留
- **AND** 系统 MUST 输出 warning 或 blocker
- **AND** 报告 MUST 包含文件路径、状态来源、当前状态和建议处理命令

#### Scenario: 审计摘要区分 residual 分类
- **WHEN** 归档同步或 promote 前置流程检查 Issue 子文档状态
- **THEN** 报告 MUST 汇总可安全同步、需人工判断、缺验收结果、缺 trace 或交付证据、不建议自动修复项的数量
- **AND** 成功路径 MUST NOT 默认展开全部子文档正文

### Requirement: Archived Change trace 兜底摘要门禁
系统 MUST 在 `/opsx-archive` 单个 Change 归档流程中检查 archived Change 的归档验证证据；系统 MUST 在 Sprint 或 OpenSpec 归档 readiness gate 中继续复核 archived Change 的归档验证证据。归档后的 Change 缺失 `trace.md` 时，系统 MUST 要求 `proposal.md`、`design.md` 或 `tasks.md` 中至少一个文件包含标准化归档验证摘要。

#### Scenario: opsx-archive 归档后存在 trace
- **WHEN** `/opsx-archive <change-id>` 已将 Change 归档到 `openspec/archive/<date>-<change-id>/`
- **AND** archived Change 目录包含 `trace.md`
- **THEN** 系统 MUST 将该 Change 的归档证据状态记录为 trace-present
- **AND** `/opsx-archive` MUST 不因 fallback summary 缺失而阻断该 Change

#### Scenario: opsx-archive 归档后缺失 trace 但存在兜底摘要
- **WHEN** `/opsx-archive <change-id>` 已将 Change 归档到 `openspec/archive/<date>-<change-id>/`
- **AND** archived Change 目录缺失 `trace.md`
- **AND** `proposal.md`、`design.md` 或 `tasks.md` 中存在标准化归档验证摘要
- **THEN** 系统 MUST 将该 Change 的归档证据状态记录为 fallback summary pass
- **AND** `/opsx-archive` 输出 MUST 展示承载摘要的文件路径

#### Scenario: opsx-archive 归档后缺失 trace 且无兜底摘要
- **WHEN** `/opsx-archive <change-id>` 已将 Change 归档到 `openspec/archive/<date>-<change-id>/`
- **AND** archived Change 目录缺失 `trace.md`
- **AND** `proposal.md`、`design.md`、`tasks.md` 均不存在标准化归档验证摘要
- **THEN** 系统 MUST 输出 blocker 或等价非闭环归档证据失败状态
- **AND** `/opsx-archive` MUST 不得输出归档完全闭环成功结论
- **AND** blocker MUST 包含 Change id、归档路径、检查过的候选文件和缺失的摘要项

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
系统 MUST 为 Workflow Sync 报告提供摘要输出模式，用聚合计数和关键上下文替代成功路径中的长文件明细。摘要输出 MUST 覆盖 Issue 子文档同步结果，包括检查数量、更新数量、验收结果状态或不适用原因、drift warning 数量。系统 MUST 在 `bug.generate` 事件中将已生成 `bug.md` 的目标 BUG 主状态从 `captured` 或等价生成前状态推进为 `draft`，并在摘要中体现状态同步结果。系统 MUST 保证写入后的 Issue `trace.md` frontmatter 是标准 YAML parser 可解析的合法 YAML，且 frontmatter 顶层 Issue 状态不得被 `openspec_changes[].status` 或其他嵌套字段污染。

#### Scenario: 成功同步输出摘要
- **WHEN** 用户或 source-command 执行 `scripts/sync-workflow-status.py` 且同步成功
- **THEN** 系统 MUST 输出 Workflow Sync Report 摘要
- **AND** 摘要 MUST 包含 event、focus issue 或 change、sprint 解析结果、updated 数量、skipped 数量和 errors 数量
- **AND** 当事件关联 REQ 或 BUG 时，摘要 MUST 包含子文档检查数量、子文档更新数量、验收结果状态或不适用原因、drift warning 数量
- **AND** 系统 MUST NOT 默认逐条输出完整 `Skipped (no delta)` 文件列表

#### Scenario: bug.generate 推进 BUG 主状态
- **GIVEN** 一个 BUG 的 `trace.md` 主状态为 `captured` 或等价生成前状态
- **AND** 该 BUG 包含已生成的 `bug.md`
- **WHEN** 用户或 source-command 执行 `scripts/sync-workflow-status.py --event bug.generate --bug <BUG-id> --sprint auto`
- **THEN** 系统 MUST 将该 BUG 主状态推进为 `draft`
- **AND** 系统 MUST 同步 `trace.md` frontmatter 与 fenced YAML 中的 `status`、`updated_at` 和 `lifecycle.generated`
- **AND** 系统 MUST 同步 `issues/bugs/_registry.yaml` 中该 BUG 的 `status`
- **AND** 系统 SHOULD 同步 `issues/bugs/CHANGELOG.md` 当前态行，使下一步指向 `/bug-complete <BUG-id>`
- **AND** 系统 MUST 保持 `bug.md` frontmatter 的 `status: draft`，不得被旧 trace 主状态反向覆盖为 `captured`

#### Scenario: bug.generate 重复运行保持幂等
- **GIVEN** 一个 BUG 已完成 `/bug-generate` 且主状态为 `draft`
- **WHEN** 用户或 source-command 重复执行 `scripts/sync-workflow-status.py --event bug.generate --bug <BUG-id> --sprint auto`
- **THEN** 系统 MUST 保持 trace、registry、CHANGELOG 和 `bug.md` frontmatter 状态一致
- **AND** 系统 MUST NOT 重复追加异常或重复的 `## 变更记录`

#### Scenario: bug.generate 缺少 bug.md 时不误推进
- **GIVEN** 一个 BUG 的 `trace.md` 主状态为 `captured`
- **AND** 该 BUG 缺少 `bug.md`
- **WHEN** 用户或 source-command 执行 `scripts/sync-workflow-status.py --event bug.generate --bug <BUG-id> --sprint auto`
- **THEN** 系统 MUST NOT 将该 BUG 主状态推进为 `draft`
- **AND** 系统 MUST 输出 warning、no-op 摘要或等价诊断，提示缺少 `bug.md`

#### Scenario: Issue trace frontmatter 写入后必须合法
- **WHEN** Workflow Sync 写入 REQ 或 BUG `trace.md` frontmatter
- **THEN** 写入后的 frontmatter MUST 能被标准 YAML parser 解析
- **AND** `lifecycle.generated` MUST 位于 `lifecycle` 父键下
- **AND** `openspec_changes[]` MUST 保留 `openspec_changes:` 父键和合法列表结构
- **AND** 若校验失败，系统 MUST 阻止非法 frontmatter 落盘或报告 blocker，不得静默继续。

#### Scenario: 顶层 Issue 状态不被 Change 状态污染
- **GIVEN** 一个 Issue trace 同时包含顶层 `status` 和 `openspec_changes[].status`
- **WHEN** Workflow Sync 解析或更新该 trace
- **THEN** 顶层 `status` MUST 只表达 Issue 主状态
- **AND** `openspec_changes[].status` MUST 只表达 Change 状态
- **AND** 系统 MUST NOT 将嵌套 Change 状态提升或覆盖为 Issue 主状态。

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
系统 MUST 校验 AI usage snapshot 的新鲜度、Sprint 归属、scope 覆盖和必要指标，防止过期或覆盖不足的 snapshot 被当作真实统计使用；fresh gate MUST 使用同一个 Sprint snapshot payload 作为状态、时间戳、coverage 和 usage mode 的事实源，避免已刷新 snapshot 被旧缓存、错误时间源、未来计划结束时间或 fallback mode 误判为 stale。

#### Scenario: snapshot 早于关键变更
- **WHEN** snapshot 生成时间早于目标 Sprint 最近一次 scope、close、archive、复盘回链或关联 trace 关键更新时间
- **THEN** 系统 MUST 将 snapshot 标记为 `stale` 或输出等价 warning
- **AND** 系统 MUST 提示刷新 snapshot

#### Scenario: 未来计划 end_date 不作为 stale 下限
- **WHEN** 目标 Sprint 已归档或正在复盘
- **AND** `sprint.yaml.end_date` 晚于当前时间，属于计划结束时间而非实际关闭时间
- **THEN** Fact Sheet fresh gate MUST NOT 使用该未来 `end_date` 作为 `min_generated_at`
- **AND** 系统 MUST 改用 Sprint 四件套 frontmatter `updated_at`、非未来 `end_date`、`start_date` 或等价实际更新时间中的最新值作为 freshness baseline
- **AND** fresh gate summary SHOULD 暴露 baseline 来源，便于诊断 stale 判定

#### Scenario: snapshot 已刷新且覆盖完整
- **WHEN** snapshot 存在并属于目标 Sprint
- **AND** snapshot 生成时间不早于目标 Sprint scope、四件套 `updated_at`、关联 Issue trace 和 Change trace 的关键更新时间
- **AND** snapshot 覆盖 Sprint scope 中的 requirements、bugs 和 changes
- **AND** snapshot 包含必要 totals 与 `usage_matrices`
- **AND** AI usage mode 为 `actual`
- **THEN** fresh gate MUST 输出通过状态
- **AND** 系统 MUST NOT 将该 snapshot 标记为 `stale`、`skipped`、`unavailable` 或 `estimated_fallback`

#### Scenario: snapshot 覆盖不足
- **WHEN** snapshot 不包含目标 Sprint ID、无法覆盖 Sprint scope 中的主要 REQ/BUG/Change，或必要 Token 指标为空
- **THEN** 系统 MUST 将 snapshot 标记为覆盖不足或输出等价 blocker
- **AND** 系统 MUST NOT 将该 snapshot 作为完整 `actual` 统计使用

#### Scenario: snapshot 状态与 usage mode 映射
- **WHEN** fresh gate 计算 snapshot status 和 usage mode
- **THEN** `actual` MUST 仅在 snapshot 当前、覆盖完整且必要矩阵存在时成立

### Requirement: `/sprint-exps` 禁止静默 estimated fallback
`/sprint-exps` MUST 优先读取目标 Sprint 的 AI usage snapshot；当真实 snapshot 不可用时，系统 MUST 显式标注估算模式、原因和补救动作。当 Fact Sheet fresh gate 通过时，系统 MUST 允许使用真实 snapshot 统计；当 fresh gate 未通过时必须降级并说明原因。

#### Scenario: fresh gate 通过时使用真实统计
- **WHEN** `/sprint-exps` 或 Fact Sheet summary 读取到目标 Sprint 的 AI usage snapshot
- **AND** fresh gate 输出通过状态
- **AND** AI usage mode 为 `actual`
- **THEN** 系统 MUST 可使用真实 token totals、模型调用统计和 usage matrices
- **AND** 输出 MUST 保留 compact fresh gate 摘要，说明 snapshot status、usage mode、coverage 和矩阵 presence

#### Scenario: fresh gate 未通过时降级
- **WHEN** Sprint snapshot 缺失、过期、覆盖不足或缺少矩阵字段
- **THEN** `/sprint-exps` MUST 明确标注真实统计不可用
- **AND** `/sprint-exps` MUST 提示刷新 `data/ai-usage` snapshot
- **AND** 输出 MUST 包含 blocker reason、impact 和 recommended_action

#### Scenario: compact fresh gate 诊断字段
- **WHEN** Fact Sheet 或 `/sprint-exps` 输出 AI usage fresh gate 结果
- **THEN** 输出 MUST 包含 status、snapshot_status、ai_usage_mode、generated_at、coverage status、usage_matrices presence、warning_count 和 recommended_action
- **AND** 输出 MUST NOT 默认打印完整 snapshot JSON、command run 明细或完整 usage matrices rows

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
系统 MUST 为 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 工作流命令提供后置 AI usage fact source 构建流程，并在主命令和 Workflow Sync 成功后尝试生成或刷新脱敏使用量事实。对于 release 与 image 工作流命令，系统 MUST 提供等价的 post-command hook 归因规则，使发布版本与镜像构建命令可追踪。

#### Scenario: 主命令与 Workflow Sync 成功后触发
- **WHEN** `/req-*`、`/bug-*`、`/opsx-*` 或 `/sprint-*` 工作流命令完成
- **AND** 主命令完成且 Workflow Sync 返回成功
- **THEN** 系统 MUST 触发统一 AI usage fact source hook 或等价共享流程
- **AND** 系统 MUST 输出短摘要，包含 hook status、usage mode、warning 数量和 recommended action

#### Scenario: release 与 image 命令写入版本归因
- **WHEN** `/release-*` or `/image-*` workflow commands run with `--release vX.Y.Z` or `<version>`
- **THEN** their AI usage hook SHALL support release version attribution
- **AND** image command usage records SHALL be attributable to the release version and, when provided, the related image plan or manifest
- **AND** successful output SHALL stay compact and SHALL NOT print raw session content, prompts, local absolute paths, secrets, or full command-run JSON.

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
系统 MUST 为 `/release-propose`、`/release-prepare`、`/release-publish` 提供版本级 AI usage artifact，避免 release 命令只散落在通用 command-runs 或被误归到单一 Sprint snapshot。系统 SHOULD 为 `/image-prepare` 与 `/image-build` 提供同一 release version 目录下的 AI usage artifact，避免镜像构建命令脱离发布版本事实源。

#### Scenario: release 命令写入版本目录
- **WHEN** release post-command hook 提供 `--release vX.Y.Z`
- **AND** hook 可安全解析本地 session 输入
- **THEN** 系统 MUST 写入 release command run 明细 `data/ai-usage/command-runs/releases/vX.Y.Z/<date>--<workflow-event>--<session-hash>.json`
- **AND** 系统 MUST 写入版本级 artifact `data/ai-usage/command-runs/releases/vX.Y.Z/<workflow-event>.json`
- **AND** `<workflow-event>` SHALL 为 `release.propose`、`release.prepare` 或 `release.publish`
- **AND** 版本级 artifact MUST 包含 `release_version`、`workflow_event`、`generated_at`、`coverage`、`totals` 和脱敏 command run 明细或等价安全摘要

#### Scenario: image 命令写入版本目录
- **WHEN** image post-command hook provides `--release vX.Y.Z` or equivalent release version context
- **AND** hook can safely parse local session input
- **THEN** the system SHOULD write image command run details under `data/ai-usage/command-runs/releases/vX.Y.Z/`
- **AND** `<workflow-event>` SHOULD be `image.prepare` or `image.build`
- **AND** the version-level artifact SHOULD include release_version, workflow_event, generated_at, coverage, totals, image_plan or image_manifest summary, and safe command run details.

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
系统 MUST 为 Workflow Sync 与 AI usage post-command hook 建立统一 compact summary 输出契约，使工作流命令成功路径默认只输出聚合状态、关键上下文和推荐动作。Image 命令成功路径 SHALL follow the same compact-output contract and summarize plan/manifest paths, gate status, blocker count, and next command instead of printing full Docker logs or full manifest JSON.

#### Scenario: Workflow Sync 默认成功摘要
- **WHEN** Workflow Sync succeeds
- **THEN** 系统 MUST 默认输出 Workflow Sync Report 摘要

#### Scenario: AI usage hook 输出固定摘要字段
- **WHEN** 工作流命令在 Workflow Sync 成功后执行 AI usage post-command hook
- **THEN** hook output SHALL use a compact summary
- **AND** compact summary MUST 包含 `status`、`usage_mode`、`command_run_count`、`sprint_snapshot`、`warning_count` 和 `recommended_action`
- **AND** 系统 MUST NOT 默认打印完整 session、原始 prompt、系统指令、developer 指令、技能全文、工具输出正文、完整 snapshot JSON 或完整 command run 明细

#### Scenario: image 命令成功输出摘要
- **WHEN** `/image-prepare` or `/image-build` succeeds or records blockers
- **THEN** command output SHALL summarize version, image_required, plan path, manifest path when present, gate status, blocker count, validation summary, and next command
- **AND** it SHALL NOT print full Docker build logs, full tarball contents, full image manifest JSON, raw env files, or secrets on the success path.

### Requirement: Sprint 归档后旧路径残留检查
系统 MUST 在 `/sprint-archive` 完成 Sprint 目录迁移、Workflow Sync 与关联 Issue promote 后，检查本 Sprint 关联文档中是否残留已迁移前的旧路径引用，防止归档后文档继续指向 `iterations/change/`、active Change 目录或 legacy Change archive 目录。

#### Scenario: Sprint 归档后无旧路径残留
- **WHEN** `/sprint-archive sprint-xxx` 已将 Sprint 目录迁移到 `iterations/archive/sprint-xxx/`
- **AND** Sprint 关联文档不包含 `iterations/change/sprint-xxx/`、已归档 Change 的 active 路径引用或 legacy `openspec/changes/archive/` 路径引用
- **THEN** 系统 MUST 在最终报告中展示路径残留检查通过
- **AND** 报告 MUST 包含检查文件数与命中数摘要

#### Scenario: Sprint 归档后仍残留 change 路径
- **WHEN** `/sprint-archive sprint-xxx` 完成目录迁移后执行路径残留检查
- **AND** 任一关联 Markdown 文档仍包含 `iterations/change/sprint-xxx/`
- **THEN** 系统 MUST 将该残留报告为 blocker 或 warning
- **AND** 报告 MUST 包含文件路径、行号、旧路径与建议的新路径 `iterations/archive/sprint-xxx/`
- **AND** `/sprint-archive` MUST 不得静默输出成功闭环结论

#### Scenario: Sprint 归档后仍残留 active Change 路径
- **WHEN** Sprint 范围内的 Change 已归档到 `openspec/archive/<date>-<change-id>/`
- **AND** 任一关联 Markdown 文档仍包含 `openspec/changes/<change-id>/`
- **THEN** 系统 MUST 报告该 Change 路径残留
- **AND** 报告 MUST 包含对应归档路径或说明无法解析归档路径

#### Scenario: Sprint 归档后仍残留 legacy Change archive 路径
- **WHEN** Sprint 范围内的 Change 已归档到 `openspec/archive/<date>-<change-id>/`
- **AND** 任一关联 Markdown 文档仍包含 `openspec/changes/archive/<date>-<change-id>/`
- **THEN** 系统 MUST 报告该 legacy archive 路径残留
- **AND** 报告 MUST 给出建议的新路径 `openspec/archive/<date>-<change-id>/`

#### Scenario: 检查范围受 Sprint scope 限制
- **WHEN** 系统执行 Sprint 归档后旧路径残留检查
- **THEN** 系统 MUST 以 `sprint.yaml` 的 `requirements[]`、`bugs[]` 与 `changes[]` 定位检查范围
- **AND** 系统 MUST NOT 默认扫描整个 `openspec/archive/**`、legacy `openspec/changes/archive/**`、`issues/**` 或生成物目录

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
命令 Skill MUST 在 `Context Budget Guardrails` 或等价章节中表达规则与 Skill 已读摘要复用约束，并保留命令特定门禁。新增或更新 image 命令 Skill SHALL follow the same guardrails and SHALL read release and image artifacts by targeted path rather than scanning all releases or archives.

#### Scenario: 命令 Skill 使用统一预算表述
- **WHEN** 新增或更新 `.agents/skills/{req,bug,opsx,sprint,build}-*`、`.agents/skills/capture`、`.agents/skills/initialize-project` 或 release 命令 Skill
- **THEN** Skill MUST 引用 `rules/agent-context-budget.md`
- **AND** Skill SHOULD 明确同一会话已读且无变更的规则和 Skill 用摘要承接
- **AND** Skill MUST 保留命令特定 Must Read、Workflow Sync、AI usage hook 和业务门禁

#### Scenario: image 命令 Skill 控制读取范围
- **WHEN** `/image-prepare` or `/image-build` Skill is added or updated
- **THEN** the Skill SHALL read `releases/<version>/release.json`, image plan or manifest, targeted Dockerfile, Compose, build script, env example, schema, and migration inputs
- **AND** it SHALL NOT default to reading all `releases/**`, all `openspec/archive/**`, generated OpenAPI clients, full Docker logs, or raw env files.

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

### Requirement: 大 Sprint Change 批次摘要
系统 MUST 为包含 10 个以上 Change 的 Sprint 生成 Change 批次摘要，用聚合事实和证据路径替代一次性展开全部 `tasks.md`、`trace.md` 或验收正文。

#### Scenario: 生成大 Sprint 批次摘要
- **WHEN** Sprint scope 中的 `changes[]` 数量大于等于 10
- **THEN** Fact Sheet 或 readiness 输出 MUST 包含 Change 批次摘要
- **AND** 每个批次 MUST 包含批次标识、Change id 列表、排序依据、tasks 完成计数、trace 状态计数、blocker 数量、warning 数量和 evidence hints
- **AND** 批次摘要 MUST NOT 复制原始 `tasks.md`、`trace.md`、验收报告或测试日志全文

#### Scenario: 小 Sprint 不强制批次摘要
- **WHEN** Sprint scope 中的 `changes[]` 数量少于 10
- **THEN** 系统 MAY 保持现有整体 Fact Sheet 或 readiness 摘要
- **AND** 若输出批次字段，系统 MUST 标记批次摘要不适用或为空

### Requirement: `/sprint-archive` 大 Sprint 分批读取
`/sprint-archive` MUST 在大 Sprint 中优先消费 readiness 与 Fact Sheet 的批次摘要，并按批次定位归档队列、阻断项和必要回读片段。

#### Scenario: 大 Sprint archive 成功路径
- **WHEN** 用户执行 `/sprint-archive sprint-xxx`
- **AND** `sprint-xxx` 包含 10 个以上 Change
- **THEN** 命令流程 MUST 先运行或读取机器可读 readiness 与 Fact Sheet 摘要
- **AND** 输出 MUST 展示批次数、每批 Change 数、archived/skipped/blocked 聚合计数和 warning 数量
- **AND** 成功路径 MUST NOT 默认转述全部 Change 的完整 tasks 或 trace 明细

#### Scenario: 大 Sprint archive 失败路径
- **WHEN** `/sprint-archive` 的批次摘要发现 blocker 或 warning
- **THEN** 报告 MUST 定位到 batch id、Change id、证据文件路径和建议回读片段
- **AND** 命令 MAY 只分段读取该批次相关文件以诊断失败原因
- **AND** 系统 MUST 保留现有 readiness、Issue promote、路径残留和 Workflow Sync 门禁

### Requirement: `/sprint-exps` 大 Sprint 分批复盘
`/sprint-exps` MUST 在大 Sprint 复盘中优先消费 Sprint Fact Sheet 的批次摘要，按 warnings、needs_detail 或 evidence hints 分批回读原始证据。

#### Scenario: 大 Sprint exps 正常路径
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **AND** `sprint-xxx` 包含 10 个以上 Change
- **THEN** 命令流程 MUST 优先读取 Fact Sheet 中的批次摘要
- **AND** 复盘输出 MUST 使用批次聚合事实分析流程、质量、验收和 token 风险
- **AND** 复盘文档 MUST NOT 默认复制全部 Change 的 tasks、trace 或 acceptance report 正文

#### Scenario: 大 Sprint exps 需要细节
- **WHEN** 批次摘要标记 `needs_detail`、blocker、warning、missing 或 inconsistent 类风险
- **THEN** `/sprint-exps` MAY 按 batch id 和 evidence hints 回读对应批次的原始文件片段
- **AND** 复盘报告 MUST 说明该批次的风险、影响和建议后续动作

### Requirement: 批次摘要输出受上下文预算约束
系统 MUST 对批次摘要的命令输出和持久化边界执行上下文预算与脱敏约束，避免 batch summary 退化为长日志或敏感内容载体。

#### Scenario: 批次摘要 compact 输出
- **WHEN** Fact Sheet、readiness、`/sprint-archive` 或 `/sprint-exps` 输出批次摘要
- **THEN** 默认用户可见输出 MUST 使用 compact summary
- **AND** compact summary MUST 包含 Sprint id、change 总数、批次数、blocker 总数、warning 总数和 recommended action
- **AND** 系统 MUST NOT 默认输出完整 batch JSON、完整 `tasks.md`、完整 `trace.md`、完整测试日志或完整 Workflow Sync 派生块

#### Scenario: 机器可读批次摘要
- **WHEN** 用户或测试命令请求 JSON 输出
- **THEN** 系统 MUST 输出可机器校验的批次结构
- **AND** JSON MUST 只包含聚合计数、工作流 ID、仓库相对路径、短 warning 标签和 evidence hints
- **AND** JSON MUST NOT 包含原始 prompt、系统指令、developer 指令、密钥、Cookie、Authorization、`.env` 内容、真实客户数据或工具输出全文

### Requirement: Force-proceed follow-up Issue 默认不自动落盘
系统 MUST 将 `force-proceed` 与 follow-up Issue 创建解耦。命令在 `force-proceed` 场景发现后续需求、缺陷、风险或待办时，默认 MUST 只输出标准 capture 文案；除非用户在当前命令中明确授权自动创建，否则系统 MUST NOT 写入 `issues/requirements/**` 或 `issues/bugs/**`，MUST NOT 更新 Issue registry，MUST NOT 运行 `req.capture` 或 `bug.capture` Workflow Sync。

#### Scenario: force-proceed 未授权自动 capture
- **WHEN** 用户执行带有 `force-proceed` 语义的工作流命令
- **AND** 命令发现需要后续跟进的需求、缺陷或风险
- **AND** 用户未明确要求自动创建 follow-up Issue
- **THEN** 系统 MUST 完成当前命令允许继续的部分
- **AND** 系统 MUST 输出可用于 `/capture` 的标准文案
- **AND** 系统 MUST NOT 创建 REQ 或 BUG 文件

#### Scenario: 用户明确授权自动 capture
- **WHEN** 用户在当前命令中明确要求自动创建、记录或生成 follow-up Issue
- **AND** 命令已能判断 follow-up 类型为需求或缺陷
- **THEN** 系统 MAY 按 `/req-capture` 或 `/bug-capture` 规则创建对应 Issue
- **AND** 系统 MUST 运行对应 `req.capture` 或 `bug.capture` Workflow Sync
- **AND** 系统 MUST 在输出中列出创建的 Issue ID 与路径

#### Scenario: 类型不确定的 follow-up
- **WHEN** 命令发现 follow-up 事项但无法可靠判断其为需求或缺陷
- **THEN** 系统 MUST 输出 `/capture` 标准文案并标记类型倾向为 `待分类`
- **AND** 系统 MUST NOT 自动创建 REQ 或 BUG

### Requirement: Follow-up capture 文案标准化
系统 MUST 为未自动落盘的 follow-up 事项输出结构化 capture 文案，使用户可直接交给 `/capture`、`/req-capture` 或 `/bug-capture` 继续处理。

#### Scenario: 输出标准 capture 文案
- **WHEN** 工作流命令输出未落盘 follow-up 事项
- **THEN** 文案 MUST 包含建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令
- **AND** 文案 MUST 明确说明“未自动创建 Issue”

#### Scenario: 多个 follow-up 事项
- **WHEN** 工作流命令发现多个独立 follow-up 事项
- **THEN** 系统 MUST 分条输出标准 capture 文案
- **AND** 每条文案 MUST 能独立用于后续 capture

### Requirement: 小程序环境命令族
系统 MUST 提供两段式小程序环境命令族，用于切换、检查、发布前准备、验证确认和发布后恢复小程序 API 环境策略。

#### Scenario: 命令入口命名
- **WHEN** 用户查看或使用小程序环境命令
- **THEN** 系统 MUST 提供 `/miniapp-env`、`/miniapp-check`、`/miniapp-prepare`、`/miniapp-confirm` 和 `/miniapp-restore`
- **AND** 命令名 MUST 保持两段式 `<domain>-<action>` 风格

#### Scenario: 不越权发布
- **WHEN** 用户执行 `/miniapp-prepare` 或 `/miniapp-confirm`
- **THEN** 系统 MUST 明确这些命令不调用微信平台真实发布动作
- **AND** 系统 MUST 输出需要人工在微信开发者工具或微信公众平台完成的步骤

### Requirement: 小程序环境策略
系统 MUST 支持 `dev`、`prod` 和 `auto` 三种小程序环境策略，并同步维护 TypeScript 源码和微信运行时 JavaScript 文件。

#### Scenario: 切换到开发策略
- **WHEN** 用户执行 `/miniapp-env dev`
- **THEN** 系统 MUST 将小程序环境解析策略设置为使用本地开发 API 地址
- **AND** 系统 MUST 同步更新 `src/miniapp/utils/env.ts` 与 `src/miniapp/utils/env.js`

#### Scenario: 切换到生产策略
- **WHEN** 用户执行 `/miniapp-env prod`
- **THEN** 系统 MUST 将小程序环境解析策略设置为所有运行形态使用生产 API 地址
- **AND** 生产 API 地址 MUST 为 `https://tilesfst.wjoyhappy.site`

#### Scenario: 切换到自动策略
- **WHEN** 用户执行 `/miniapp-env auto`
- **THEN** 系统 MUST 将开发版解析为本地开发 API 地址
- **AND** 系统 MUST 将体验版和正式版解析为生产 API 地址

### Requirement: 小程序环境检查
系统 MUST 提供环境检查命令，验证当前策略、运行入口同步、静态测试和生产公开接口可访问性。

#### Scenario: 检查当前策略
- **WHEN** 用户执行 `/miniapp-check`
- **THEN** 系统 MUST 报告当前小程序环境策略、开发 API 地址、生产 API 地址和 fallback 配置
- **AND** 系统 MUST 检查 `.ts` 与 `.js` 环境配置一致

#### Scenario: 发布前接口 smoke
- **WHEN** 用户执行 `/miniapp-prepare`
- **THEN** 系统 MUST 检查 `GET /api/v1/miniapp/home` 和 `GET /api/v1/miniapp/brands?page=1&pageSize=2` 的生产 HTTPS 响应
- **AND** 任一接口非 `200 OK` 或统一响应 `code != 0` 时 MUST 阻断发布准备

### Requirement: 小程序发布确认与恢复
系统 MUST 支持记录小程序体验版或正式版验证结论，并支持发布后恢复默认环境策略。

#### Scenario: 记录验证确认
- **WHEN** 用户执行 `/miniapp-confirm`
- **THEN** 系统 MUST 记录或输出小程序版本、渠道、验证时间、验证范围、结果和剩余风险
- **AND** 系统 MUST 不记录真实用户隐私、微信会话密钥、Authorization header、Cookie 或 `.env` 内容

#### Scenario: 恢复默认策略
- **WHEN** 用户执行 `/miniapp-restore`
- **THEN** 系统 MUST 将小程序环境策略恢复为项目默认策略
- **AND** 系统 MUST 运行环境静态检查并输出恢复后的策略摘要

### Requirement: Sprint 复盘 AI 使用量矩阵
`/sprint-exps` MUST 基于 `data/ai-usage` 的 Sprint snapshot 展示 AI 使用量矩阵，用于按 Sprint、REQ、BUG 与工作流命令交叉分析 token 与模型调用消耗。

#### Scenario: 输出四张指标矩阵
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **AND** 对应 `data/ai-usage/sprints/<sprint-id>.json` 存在可用真实统计
- **THEN** 复盘文档 MUST 在 `## 模型 Token 使用分析` 中输出 `total_tokens`、`input_tokens`、`output_tokens`、`model_call_count` 四张矩阵表
- **AND** 四张表 MUST 使用相同的行列结构

#### Scenario: 矩阵行列顺序
- **WHEN** `/sprint-exps` 输出 AI 使用量矩阵
- **THEN** 表格最上方 MUST 包含 `Total` 汇总行
- **AND** 纵向对象行 MUST 按 Sprint、REQ、BUG 顺序排列
- **AND** Sprint 行 MUST 使用 `sprint-xxx` 或规范大写展示名，REQ/BUG 行 MUST 使用对应 canonical ID
- **AND** 横向命令列 MUST 按 `Capture`、`BUG-Capture`、`REQ-Capture`、`BUG-Explore`、`REQ-Explore`、`REQ-Generate`、`BUG-Generate`、`REQ-Complete`、`BUG-Complete`、`REQ-Review`、`BUG-Review`、`REQ-Opsx`、`BUG-Opsx`、`Opsx-Explore`、`Opsx-Propose`、`Opsx-Apply`、`Opsx-Archive`、`Sprint-Propose`、`Sprint-Explore`、`Sprint-Apply`、`Sprint-Archive` 的顺序展示

#### Scenario: 缺少矩阵统计
- **WHEN** Sprint snapshot 缺失、过期、覆盖不足或缺少矩阵字段
- **THEN** `/sprint-exps` MUST 标记 `ai_usage_mode: estimated_fallback` 或输出 warning
- **AND** `/sprint-exps` MUST 提示刷新 `data/ai-usage` snapshot
- **AND** `/sprint-exps` MUST NOT 编造矩阵数值

#### Scenario: 对象归因口径
- **WHEN** 同一 command run 同时关联多个 REQ 或 BUG
- **THEN** Sprint 行与 `Total` 行 MUST 按唯一 command run 汇总
- **AND** REQ/BUG 行 MAY 按对象归因分别计入同一 command run
- **AND** 复盘说明 SHOULD 提醒对象行用于归因分析，不代表可与 `Total` 行直接相加

### Requirement: OpenSpec Change 归档根目录独立化
系统 MUST 使用 `openspec/archive/` 作为已完成 OpenSpec Change 的 canonical archive root，并 MUST 将 `openspec/changes/` 保留为 active Change 根目录。新增归档、Workflow Sync 输出、release 事实源、Fact Sheet、AI usage、readiness 报告和技能文档 MUST 使用 canonical archive root；legacy `openspec/changes/archive/` 仅可作为迁移期只读兼容路径。

#### Scenario: 新增 Change 归档写入 canonical archive
- **WHEN** 用户执行 `/opsx-archive <change-id>`、`/sprint-archive <sprint-id>` 或等价 OpenSpec archive 流程
- **THEN** 系统 MUST 将归档 Change 写入 `openspec/archive/<date>-<change-id>/`
- **AND** 系统 MUST NOT 将新增归档 Change 写入 `openspec/changes/archive/<date>-<change-id>/`

#### Scenario: 迁移期读取 legacy archive
- **WHEN** 工具需要读取已归档 Change
- **AND** `openspec/archive/<date>-<change-id>/` 中未找到目标 Change
- **THEN** 系统 MAY 读取 legacy `openspec/changes/archive/<date>-<change-id>/`
- **AND** 报告 MUST 标明该路径是 legacy archive 兼容命中

#### Scenario: archive root 配置一致
- **WHEN** 系统读取 OpenSpec 配置、规则文档、命令技能或路径 helper
- **THEN** canonical archive root MUST 一致指向 `openspec/archive/`
- **AND** 任何 `openspec/changes/archive/` 引用 MUST 明确标注为 legacy 兼容、迁移来源或残留检查目标

#### Scenario: legacy archive 目录不得承载新事实源
- **WHEN** 归档流程完成后执行残留检查
- **THEN** `openspec/changes/archive/` MUST NOT 包含新的 Change 包目录
- **AND** 如发现新增或未迁移 Change 包，系统 MUST 报告 blocker 并给出迁移目标 `openspec/archive/<date>-<change-id>/`

### Requirement: `/opsx-apply` 管理端筛选下拉 Checklist
`/opsx-apply` SHALL include a dedicated checklist gate for Changes that add or modify admin filter dropdown controls, in addition to the existing cross-cutting admin list gate.

#### Scenario: Apply 前识别筛选下拉标签
- **WHEN** `/opsx-apply` reads a Change whose proposal, design, tasks, specs, trace, or affected file paths mention admin filter dropdowns, filter-area Select, Dropdown, Popover, Combobox, date picker, searchable select, `AdminFilterSelect`, `SearchableSelect`, `admin-filter-dropdown`, or equivalent terms
- **THEN** the Cross-cutting Apply Gate MUST add an `admin-filter-dropdown` tag
- **AND** the gate MUST read `docs/knowledge-base/best-practices/admin-list-page-consistency.md` or the successor best-practice document before editing `src/`

#### Scenario: Apply checklist 输出
- **WHEN** the `admin-filter-dropdown` tag is active
- **THEN** `/opsx-apply` MUST report checklist results for best-practice read, shared component reuse or justified equivalent wrapper, page-local overlay CSS absence, state coverage, overlay clipping check, query parameter semantics, and regression test plan
- **AND** the verdict MUST be `BLOCKED` if a new or modified admin filter dropdown lacks both shared-component reuse and an explicit equivalent-wrapper rationale

#### Scenario: Apply 中完成任务
- **WHEN** implementation tasks touch admin filter dropdown UI
- **THEN** tasks MUST include focused verification for component classes or DOM contract, open/select/clear/reset behavior, empty or loading state when applicable, disabled or selected state, and at least one representative affected page
- **AND** tasks MUST record whether visual smoke or Playwright verification is required for desktop and narrow admin viewports

#### Scenario: 非相关 Change 不误阻断
- **WHEN** a Change does not affect admin filter dropdown controls
- **THEN** `/opsx-apply` MAY mark the `admin-filter-dropdown` checklist as `n/a`
- **AND** the checklist MUST NOT block backend-only, database-only, release-only, or non-filter UI Changes solely because the admin list best-practice document exists

### Requirement: Sprint close stale scan 工具输出
系统 SHALL 提供命令式 stale scan 能力，基于目标 Sprint 四件套、`sprint.yaml` 范围和关联 Change 状态输出稳定、可执行的检查报告。

#### Scenario: 扫描指定 Sprint
- **WHEN** 用户或 `/sprint-archive` 调用 stale scan 并指定 `sprint-xxx`
- **THEN** 系统 MUST 只读取该 Sprint 的四件套和由 `sprint.yaml` 指向的关联 Issue、Change 状态证据
- **AND** 系统 MUST NOT 默认扫描全部 `iterations/**`、`openspec/archive/**` 或历史归档目录

#### Scenario: 报告包含可执行修复建议
- **WHEN** stale scan 发现 blocker
- **THEN** 报告 MUST 包含建议命令或修复路径，例如重新运行 Workflow Sync、运行目录结构校验、执行归档路径 residual 修复或手工更新非派生人工说明
- **AND** 报告 MUST 明确禁止手工编辑 `sprint.md` workflow-sync marker 派生块

#### Scenario: 自动刷新后保持幂等
- **WHEN** Workflow Sync 或 Sprint close 流程刷新四件套派生块
- **THEN** 系统 MUST 清除由机器事实可确定的过期规划文案
- **AND** 再次运行 stale scan MUST 不因同一派生命中重复失败

#### Scenario: 无法解析 Sprint 时失败
- **WHEN** stale scan 通过 `--sprint auto` 或等价方式无法解析唯一目标 Sprint
- **THEN** 系统 MUST 返回非零退出码
- **AND** 报告 MUST 要求显式传入目标 `sprint-xxx`

### Requirement: Sprint close stale scan 例外边界
系统 SHALL 明确定义 legacy 字符串和中间态文案的允许例外，避免自动化误伤迁移、兼容读取和回归测试。

#### Scenario: 测试与迁移文件中的 legacy 字符串不阻断
- **WHEN** stale scan 命中测试 fixture、迁移脚本、兼容读取逻辑或 residual scanner 自身的 `openspec/changes/archive/` 字符串
- **THEN** 系统 MUST 将命中标记为允许例外
- **AND** 系统 MUST NOT 因该例外阻断目标 Sprint close

#### Scenario: 新生成 Sprint 事实不得使用 legacy 路径
- **WHEN** Workflow Sync、Sprint close、Fact Sheet、release note 或 acceptance report 生成新的归档路径事实
- **THEN** 系统 MUST 使用 `openspec/archive/`
- **AND** 系统 MUST NOT 将 `openspec/changes/archive/` 作为 canonical archive path 写入新事实

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
系统 MUST 在 Sprint close、`/sprint-archive` 或等价收尾流程中扫描相关 Issue 包与 Sprint 四件套的中间态残留，防止 completed/archive 状态下仍保留未解释的流程中间态、active Change 路径或等价旧文案。扫描 MUST 区分结构化状态上下文、流程待办说明与普通业务正文；普通业务正文中的业务词 `pending` 不得仅凭独立单词出现就被判定为中间态残留。

#### Scenario: Sprint close 发现中间态文案
- **WHEN** Sprint close 或 `/sprint-archive` 检查关联 Issue 包、`sprint.md`、`acceptance-report.md`、`release-note.md` 或其他 Sprint 四件套
- **AND** 文档仍包含未解释的结构化中间态字段、流程待办语义、active Change 路径或 legacy archive 路径
- **THEN** 系统 MUST 将该命中标记为 blocker
- **AND** 报告 MUST 包含文件路径、行号、命中片段、关联 Issue 或 Change、真实状态和建议修复动作

#### Scenario: 普通业务正文中的 pending 不阻断
- **WHEN** 一个已闭环 Issue 子文档的普通正文包含“SKU pending 图片正式化已完成”或等价业务描述
- **AND** 该行不属于 frontmatter、fenced yaml、状态表格、验收状态字段或流程待办说明
- **THEN** stale scan MUST NOT 仅因该 `pending` 命中产生 `issue-subdocument-stale-state` blocker

#### Scenario: 结构化 pending 状态继续阻断
- **WHEN** 一个已闭环 Issue 子文档的 frontmatter、fenced yaml、状态表格或验收结果字段包含 `status: pending_review`、`acceptance_status: pending` 或等价未闭环状态
- **THEN** stale scan MUST 继续产生 blocker
- **AND** 报告 MUST 建议运行 Workflow Sync/reconcile 或人工修正语义不明的状态字段

#### Scenario: Sprint close stale scan 范围受控
- **WHEN** 系统执行 Sprint close 中间态文案扫描
- **THEN** 系统 MUST 只扫描目标 Sprint 四件套和该 Sprint scope 关联的 Issue 子文档
- **AND** 系统 MUST NOT 默认扫描全部 `iterations/**`、`openspec/archive/**` 或历史归档目录

### Requirement: 大型 Sprint Fact Sheet 默认使用 compact AI usage 摘要
系统 MUST 在 Sprint Fact Sheet summary 中默认输出 compact Token Usage Fact Sheet 摘要，避免 10+ Change Sprint 默认携带完整 `usage_matrices` 明细；完整矩阵 MUST 只能通过 fields、完整 JSON 或用户明确要求的等价路径按需读取。

#### Scenario: 10+ Change Sprint summary 不输出完整矩阵
- **WHEN** 用户、测试命令或 `/sprint-exps` 请求包含 10 个或以上 Change 的 Sprint Fact Sheet summary
- **THEN** summary MUST 输出 AI usage mode、snapshot status、fresh gate、warning_count、coverage status、关键 totals、矩阵可用性、矩阵行列规模、freshness baseline 和 recommended_action
- **AND** summary MUST NOT 默认输出完整 `usage_matrices.rows` 或四张 usage matrix 明细
- **AND** summary MUST 提供获取完整矩阵的 fields 路径提示

#### Scenario: `/sprint-exps` fresh gate 通过后输出矩阵
- **WHEN** `/sprint-exps` 的 compact summary 显示 `fresh_gate.status: pass`
- **AND** `snapshot_status: present`
- **AND** `ai_usage_mode: actual`
- **AND** `usage_matrices_summary.available: true`
- **THEN** `/sprint-exps` MUST 优先通过 Fact Sheet 的 retrospective-ready Markdown 输出生成 token 使用章节
- **AND** 复盘文档 MUST 输出 `Token Usage Fact Sheet` 表格
- **AND** 复盘文档 MUST 输出 `total_tokens`、`input_tokens`、`output_tokens`、`model_call_count` 四张矩阵
- **AND** fields 模式读取 `ai_usage_snapshot.usage_matrices` MUST 仅作为调试或兼容 fallback 使用

#### Scenario: 命令直接输出复盘表格章节
- **WHEN** 用户或 `/sprint-exps` 请求 Sprint AI usage Markdown
- **AND** snapshot fresh gate 通过
- **THEN** Fact Sheet 命令 MUST 输出可直接写入 `docs/knowledge-base/retrospectives/<sprint-id>-retrospective.md` 的 `## 模型 Token 使用分析` 章节
- **AND** 输出 MUST 使用与历史 `sprint-015-retrospective.md` 等价的 Markdown 表格结构
- **AND** 输出 MUST 包含矩阵口径说明，防止将 REQ/BUG 归因行相加后与 `Total` 误比

### Requirement: 归档 Change 缺失 trace 的最小证据补齐
系统 MUST 在校验已归档 OpenSpec Change 的归档证据时处理缺失 `trace.md` 的历史归档目录：当归档目录可写且可从归档路径、`tasks.md`、delta spec、proposal/design 或关联 Issue trace 推断出最小事实时，系统 MUST 自动生成最小归档 `trace.md`；当无法安全写入但可形成完整机器可读事实时，系统 MUST 输出结构化 fallback 摘要；当两者都不可用时，系统 MUST 返回非零退出码并报告 blocker。

#### Scenario: 可写归档目录自动生成最小 trace
- **WHEN** 归档证据校验扫描到 `openspec/archive/YYYY-MM-DD-<change-id>/` 下缺少 `trace.md`
- **AND** 归档目录可写
- **AND** 系统可从归档目录名、`tasks.md`、delta spec 或关联 Issue trace 推断最小归档事实
- **THEN** 系统 MUST 写入最小 `trace.md`
- **AND** `trace.md` MUST 记录 `change_id`、`status: archived`、归档路径、归档时间或时间来源、任务完成摘要、证据来源和自动生成标记
- **AND** 校验报告 MUST 将该结果标记为 `auto-generated-minimal-trace`

#### Scenario: 不可写目录输出结构化 fallback 摘要
- **WHEN** 归档证据校验扫描到已归档 Change 缺少 `trace.md`
- **AND** 系统无法安全写入归档目录
- **AND** 系统仍可形成完整归档证据事实
- **THEN** 系统 MUST 输出结构化 fallback 摘要
- **AND** 摘要 MUST 包含 `change_id`、`archive_path`、`evidence_status`、`archive_timestamp`、`timestamp_source`、`tasks_done`、`tasks_total`、`spec_delta_paths`、`warnings` 和 `recommended_action`
- **AND** 调用方 MUST 能用该摘要判断归档证据闭环，不得只依赖自由文本说明

#### Scenario: 证据不足时保持阻断
- **WHEN** 已归档 Change 缺少 `trace.md`
- **AND** 系统无法生成最小 trace
- **AND** 系统无法形成完整结构化 fallback 摘要
- **THEN** 归档证据校验 MUST 返回非零退出码
- **AND** 报告 MUST 列出缺失字段、已检查路径和建议人工补齐动作

#### Scenario: 不放宽既有归档门禁
- **WHEN** 已归档 Change 存在未完成 tasks、缺失 `tasks.md`、legacy archive path 真实残留或关联 Issue 未闭环
- **THEN** 系统 MUST 保持既有 blocker 语义
- **AND** 自动生成最小 trace 或结构化 fallback 摘要 MUST NOT 将这些 blocker 误判为通过

### Requirement: OpenSpec 归档输出区分兼容 warning 与真实风险
系统 MUST 在 `/opsx-archive` 与底层归档封装流程中区分已知 OpenSpec CLI 兼容 warning 与真实归档风险。对于项目中文语言规范已覆盖且不影响归档结果的英文脚手架标题提示，系统 MUST 在安全条件满足时吸收该提示，即使该提示来自 OpenSpec CLI stdout，也 MUST 避免成功路径反复输出固定非阻塞说明；对于真实错误、未知 stdout、未知 stderr、目录结构错误或中文语言校验失败，系统 MUST 保留阻断或可见 warning。

#### Scenario: 已知英文脚手架 warning 被安全吸收
- **WHEN** `/opsx-archive <change-id>` 或底层归档脚本执行成功
- **AND** OpenSpec CLI stdout 或 stderr 仅包含 `proposal.md` 缺少英文 `## Why` / `## What Changes` 的已知兼容 warning
- **AND** `python scripts/validate-openspec-language.py` 通过
- **THEN** 最终归档说明 MUST NOT 重复展示该固定非阻塞 warning
- **AND** 系统 MUST NOT 要求为消除该 warning 在 Change 文档中回填英文脚手架标题
- **AND** 归档成功结论 MUST 继续清晰表达 Change 已归档

#### Scenario: 未知 stdout 仍然可见
- **WHEN** OpenSpec CLI stdout 包含已知兼容 warning 之外的 warning、error 或诊断文本
- **THEN** 归档最终输出 MUST 保留未知 stdout 的可见诊断信息
- **AND** 系统 MUST NOT 将未知 stdout 当作已知兼容 warning 静默吸收

#### Scenario: 未知 stderr 仍然可见
- **WHEN** OpenSpec CLI stderr 包含已知兼容 warning 之外的 warning 或 error
- **THEN** 归档最终输出 MUST 保留未知 stderr 的可见诊断信息
- **AND** 系统 MUST NOT 将未知 stderr 当作已知兼容 warning 静默吸收

#### Scenario: 语言校验失败仍然阻断
- **WHEN** `python scripts/validate-openspec-language.py` 失败
- **THEN** 归档流程 MUST 按项目语言规范门禁失败处理
- **AND** 最终输出 MUST 包含语言校验失败信息
- **AND** 系统 MUST NOT 因 OpenSpec CLI 兼容 warning 可吸收而覆盖语言校验失败结果

#### Scenario: OpenSpec CLI 失败仍然阻断
- **WHEN** OpenSpec CLI 返回非零退出码
- **THEN** 归档流程 MUST 失败
- **AND** 最终输出 MUST 保留必要错误信息
- **AND** 系统 MUST NOT 将 CLI 失败路径降级为成功 warning

### Requirement: 规范优化命令 spec-opt

`/spec-opt` MUST 作为项目治理规范优化入口，用于新增或修改 `.agents/skills/` 命令、`rules/` 文档、`docs/` 文档规范、`scripts/` 治理脚本、`AGENTS.md` 入口和 active OpenSpec Change 文档。`/spec-opt` MUST 只修改治理资产，不得修改业务 `src/` 运行时代码。`/spec-opt` 完成本项目规范、技能、脚本、目录边界或校验规则迭代后，MUST 在 `docs/spec-logs/` 写入治理迭代日志，并维护 `docs/spec-logs/CHANGELOG.md` 变更历史总账。

#### Scenario: 输出治理迭代日志

- **WHEN** `/spec-opt` 完成本项目规范、技能、脚本、目录边界或校验规则迭代
- **THEN** `/spec-opt` MUST 在 `docs/spec-logs/` 写入治理迭代日志
- **AND** 日志文件名 MUST 使用 `YYYYMMDDhhmmss-governance-xxx.md`
- **AND** `YYYYMMDDhhmmss` MUST 使用日志生成时刻的 `Asia/Shanghai` 日期时间，精确到秒
- **AND** `xxx` MUST 使用小写 kebab-case 表达治理主题
- **AND** 日志 MUST 包含迭代目标、变更摘要、影响范围、更新文件、验证结果和后续建议
- **AND** 日志 MUST NOT 包含用户隐私数据、真实客户数据、密钥、访问令牌、未脱敏日志、订单原文、聊天原文、工单原文、截图中的个人信息或学习对象源码
- **AND** 如需说明隐私相关风险，日志 MUST 使用脱敏占位符或聚合描述

#### Scenario: 维护治理变更历史总账

- **WHEN** `/spec-opt` 新增或更新本项目规范、技能、脚本、目录边界或校验规则
- **THEN** `/spec-opt` MUST 新增或更新 `docs/spec-logs/CHANGELOG.md`
- **AND** `CHANGELOG.md` MUST 按倒序记录治理资产变更历史
- **AND** 每条记录 MUST 至少包含时间、来源命令、关联 Change、类型、影响范围、更新文件、验证结果、详细日志链接和跨项目落地提示词
- **AND** 跨项目落地提示词 MUST 说明其他项目要落地同类规范时可直接给 AI 的 Prompt
- **AND** 跨项目落地提示词 MUST 可复制、脱敏、项目无关
- **AND** `CHANGELOG.md` MUST NOT 替代单次 `YYYYMMDDhhmmss-governance-*.md` 详细日志、OpenSpec Change、Sprint 或 Issue 事实源
- **AND** `CHANGELOG.md` MUST NOT 包含用户隐私数据、真实客户数据、密钥、访问令牌、未脱敏日志、订单原文、聊天原文、工单原文、截图中的个人信息或学习对象源码

### Requirement: 所有 Change 纳入 Sprint 后才能 apply
系统 MUST 要求任意 OpenSpec Change 在执行 `/opsx-apply` 前已经纳入某个 Sprint 的正式范围。该规则 MUST 同时适用于来源于 REQ/BUG 的 Change，以及通过 `/opsx-propose`、`/spec-opt` 或其他治理流程直接创建的非 REQ/BUG Change。

#### Scenario: 非 REQ/BUG Change 未纳入 Sprint 时阻断 apply
- **WHEN** 用户请求 `/opsx-apply <change-id>`
- **AND** `<change-id>` 未出现在任何 `iterations/change|archive/<sprint>/sprint.yaml` 的 `changes[]`
- **THEN** 系统 MUST 阻断实现
- **AND** 系统 MUST 提示先通过 `/sprint-propose` 或等价 Sprint scope 修复流程纳入 Sprint
- **AND** 系统 MUST NOT 因该 Change 无 REQ/BUG 来源而豁免 Sprint Inclusion Gate

#### Scenario: 非 REQ/BUG Change 已纳入 Sprint 后允许 apply
- **WHEN** 用户请求 `/opsx-apply <change-id>`
- **AND** `<change-id>` 已出现在某个 `iterations/change|archive/<sprint>/sprint.yaml` 的 `changes[]`
- **AND** `python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto --dry-run` 能解析到该 Sprint
- **THEN** 系统 MAY 继续执行 `/opsx-apply`
- **AND** 若该 Change 不关联 REQ/BUG，系统 MUST 不要求额外创建 REQ/BUG

#### Scenario: REQ/BUG Change 继续保持双向一致门禁
- **WHEN** `<change-id>` 关联 REQ 或 BUG
- **THEN** 系统 MUST 继续要求 Sprint `requirements[]` 或 `bugs[]` 包含对应 Issue
- **AND** 系统 MUST 继续要求 Issue `trace.md` 的 `iteration` 指向同一 Sprint
- **AND** 系统 MUST 继续要求 Issue 状态为 `in_sprint` 或后续交付态

#### Scenario: spec-opt 不再豁免纯治理 Change
- **WHEN** `/spec-opt` 创建或复用纯治理 Change
- **THEN** 系统 MUST 提示该 Change 仍需纳入 Sprint 后才能 `/opsx-apply`
- **AND** 系统 MUST NOT 输出“纯治理 Change 可豁免 Sprint Gate”或等价表述

### Requirement: 下一步命令参数标识规范
系统 MUST 统一命令最终输出中的下一步可执行命令参数。REQ 来源的后续命令 MUST 使用原始 `REQ-*` 标识，BUG 来源的后续命令 MUST 使用原始 `BUG-*` 标识，非 REQ/BUG 的直接 Change MUST 使用 `<change-id>`。

#### Scenario: REQ 来源后续 opsx 命令使用 REQ ID
- **WHEN** `/req-opsx <REQ-id>` 创建或确认 linked Change
- **THEN** 系统输出的下一步 `/opsx-apply` MUST 使用 `<REQ-id>`
- **AND** 后续 `/opsx-apply` 完成后输出的 `/opsx-archive` MUST 继续使用 `<REQ-id>`
- **AND** 系统 MUST NOT 在 REQ 来源链路中把下一步引导改为真实 `<change-id>`

#### Scenario: BUG 来源后续 opsx 命令使用 BUG ID
- **WHEN** `/bug-opsx <BUG-id>` 创建或确认 linked Change
- **THEN** 系统输出的下一步 `/opsx-apply` MUST 使用 `<BUG-id>`
- **AND** 后续 `/opsx-apply` 完成后输出的 `/opsx-archive` MUST 继续使用 `<BUG-id>`
- **AND** 系统 MUST NOT 在 BUG 来源链路中把下一步引导改为真实 `<change-id>`

#### Scenario: 非 REQ/BUG Change 使用 change id
- **WHEN** Change 不关联 REQ 或 BUG
- **THEN** 系统输出的 `/opsx-apply`、`/opsx-archive` 下一步 MUST 使用真实 `<change-id>`

#### Scenario: opsx 命令解析 REQ 或 BUG target
- **WHEN** 用户执行 `/opsx-apply <REQ-id>`、`/opsx-archive <REQ-id>`、`/opsx-apply <BUG-id>` 或 `/opsx-archive <BUG-id>`
- **THEN** 系统 MUST 从对应 Issue `trace.md` 的 `openspec_changes[]` 解析 linked Change
- **AND** 内部 OpenSpec CLI、Workflow Sync 和 AI Usage hook MUST 使用解析后的真实 `<change-id>`
- **AND** 最终下一步展示 MUST 继续使用原始 `<REQ-id>` 或 `<BUG-id>`

#### Scenario: 多个候选 Change 需要用户决策
- **WHEN** 一个 REQ 或 BUG 关联多个符合当前阶段的候选 Change
- **THEN** 系统 MUST 列出候选 Change
- **AND** 系统 MUST 要求用户选择目标 Change
- **AND** 系统 MUST NOT 猜测其中一个 Change 继续执行

### Requirement: OpenSpec 归档 wrapper 吸收已知 proposal warning
系统 MUST 在 OpenSpec 归档 wrapper 成功路径中吸收项目已确认可忽略的 proposal warning，同时保留未知 stdout/stderr 与失败路径诊断信息。

#### Scenario: 多行 proposal warning stdout 块被整体吸收
- **WHEN** `scripts/archive-change.sh` 执行 OpenSpec CLI 归档成功
- **AND** OpenSpec CLI stdout 输出以 `Proposal warnings in proposal.md` 开始的多行 warning 块
- **THEN** wrapper MUST 不展示该已知 warning 块中的标题行和详情行
- **AND** wrapper MUST 继续完成归档后的目录结构和归档证据校验

#### Scenario: 未知 stdout 继续保留
- **WHEN** OpenSpec CLI 归档成功
- **AND** stdout 中出现不属于已知 proposal warning 块的内容
- **THEN** wrapper MUST 将该未知 stdout 输出给用户

#### Scenario: 未知 stderr 继续保留
- **WHEN** OpenSpec CLI 归档成功
- **AND** stderr 中出现不属于已知 proposal warning 块的内容
- **THEN** wrapper MUST 将该未知 stderr 输出给用户

#### Scenario: 单行 proposal warning 过滤不回归
- **WHEN** OpenSpec CLI 归档成功
- **AND** stdout 或 stderr 输出既有单行 proposal scaffold warning
- **THEN** wrapper MUST 继续吸收该已知 warning

#### Scenario: 失败路径诊断不丢失
- **WHEN** OpenSpec CLI 归档失败
- **THEN** wrapper MUST 输出 OpenSpec CLI 的 stdout/stderr 诊断内容
- **AND** wrapper MUST 返回非零退出码

### Requirement: 命令技能输出下一步引导
系统 MUST 要求 `.agents/skills/` 下每个命令技能在命令完成输出中提供明确可执行的下一步引导。若存在可推进的下一步，输出 MUST 给出可直接复制执行的命令；若没有明确下一步，输出 MUST 说明“暂无可推进下一步”或等价结论。

#### Scenario: 命令成功且存在单一下一步
- **WHEN** 任一命令技能完成执行
- **AND** 当前状态存在明确可推进的下一命令
- **THEN** 最终输出 MUST 包含 `下一步` 或等价字段
- **AND** 该字段 MUST 包含可直接复制执行的命令，例如 `/bug-review BUG-0122 --approve`

#### Scenario: 命令成功且存在多个分支
- **WHEN** 任一命令技能完成执行
- **AND** 下一步取决于用户选择、评审结论、目标 Sprint、容量或验收结果
- **THEN** 最终输出 MUST 用条件化方式列出可选下一步
- **AND** 每个可选下一步 SHOULD 包含可直接复制执行的命令或明确处理动作

#### Scenario: 命令完成但暂无下一步
- **WHEN** 任一命令技能完成执行
- **AND** 当前状态没有明确可推进的下一步
- **THEN** 最终输出 MUST 明确说明暂无可推进下一步
- **AND** 输出 MUST NOT 编造不适用的命令

### Requirement: 命令技能输出待决策或待处理点
系统 MUST 要求 `.agents/skills/` 下每个命令技能在命令完成输出中明确列出待用户决策或处理的点。若没有待决策或待处理点，输出 MUST 明确写明“无”或等价结论。

#### Scenario: 存在用户决策点
- **WHEN** 命令执行后仍需用户选择目标 Sprint、评审结论、范围取舍、容量调整、验收确认、发布确认或环境策略
- **THEN** 最终输出 MUST 包含 `待用户决策`、`待用户处理`、`决策点` 或等价字段
- **AND** 输出 MUST 用清晰条目列出每个待决策或待处理点

#### Scenario: 不存在用户决策点
- **WHEN** 命令执行后无需用户额外决策或处理即可继续
- **THEN** 最终输出 MUST 包含待决策/待处理字段
- **AND** 该字段 MUST 标明无待决策或待处理点

#### Scenario: 下一步命令不得重复为待处理项
- **WHEN** 最终输出的 `下一步` 字段已经给出可直接执行的命令或明确动作
- **THEN** `待用户决策/处理` 字段 MUST NOT 重复该命令或动作
- **AND** 只有仍缺少的用户输入、范围选择、策略确认、证据补充、验收确认、发布确认、阻塞项或人工处理事项 MAY 出现在 `待用户决策/处理`
- **AND** 如果没有这些额外事项，`待用户决策/处理` MUST 写明“无”

#### Scenario: 技能校验发现缺少输出契约
- **WHEN** 技能校验脚本扫描 `.agents/skills/*/SKILL.md`
- **AND** 某个命令技能缺少下一步引导、待决策/待处理输出契约或去重约束
- **THEN** 校验 MUST 返回非零退出码
- **AND** 报告 MUST 列出不符合要求的技能文件

### Requirement: Harness 学习同步技能

系统 MUST 提供 `/spec-study` 技能，用于学习其他项目的 Harness 工程，并在用户确认后将可复用的治理经验应用到本项目。

#### Scenario: 默认自动学习

- **WHEN** 用户执行 `/spec-study <学习对象>` 且未指定学习模式
- **THEN** 系统 MUST 默认使用自动学习模式
- **AND** 系统 MUST 综合分析项目入口、全局规范、Agent 能力目录、脚本、部署与环境示例
- **AND** 系统 MUST 输出候选学习内容，等待用户确认后才能应用

#### Scenario: 指定学习内容

- **WHEN** 用户执行 `/spec-study <学习对象> <指定学习内容>`
- **THEN** 系统 MUST 以指定主题为主线学习
- **AND** 系统 MUST 仍横向检查 `AGENTS.md`、`project.yaml`、`DOCUMENT_METADATA_INDEX.md`、`rules/`、`docs/`、Agent 目录、`scripts/`、部署与环境模块中的相关内容
- **AND** 系统 MUST NOT 只读取单一目录后得出迁移结论

#### Scenario: 支持本地项目和 GitHub URL

- **WHEN** 学习对象是本地项目路径
- **THEN** 系统 MUST 以只读方式扫描该路径的治理资产
- **AND** 系统 MUST 遵守上下文预算，先列清单、摘要，再按需读取片段
- **AND** 系统 MUST NOT 修改学习对象中的代码、文档、配置、依赖锁文件、Git 状态、缓存、生成物或运行时数据

- **WHEN** 学习对象是 GitHub 项目 URL
- **THEN** 系统 MUST 先说明需要获取远端只读快照
- **AND** 如需网络访问或 clone，系统 MUST 按当前权限策略请求批准
- **AND** 系统 MUST NOT 对学习对象执行 push、commit、checkout 覆盖、reset、clean 或任何写入远端/快照的操作

#### Scenario: 学习对象只读保护

- **WHEN** 系统学习任何本地项目、临时克隆目录或远端快照
- **THEN** 系统 MUST 把学习对象作为外部只读输入
- **AND** 系统 MUST NOT 在学习对象路径下运行安装依赖、格式化、迁移、生成、测试修复、提交、分支、清理或重置命令
- **AND** 学习报告 MUST 说明学习对象只读保护结果

#### Scenario: 应用前用户确认

- **WHEN** 系统完成学习阶段
- **THEN** 系统 MUST 告知用户学习到了哪些内容建议应用到本项目
- **AND** 系统 MUST 列出每项内容的理由、风险、拟更新目标文件和是否需要 OpenSpec/Sprint 承载
- **AND** 系统 MUST 等待用户确认学习内容，不得默认直接应用

#### Scenario: 确认后应用到本项目治理资产

- **WHEN** 用户确认应用某些学习内容
- **THEN** 系统 MUST 通过当前项目的 OpenSpec Change 和 Sprint Inclusion Gate 承载变更
- **AND** 系统 MAY 更新 `.agents/skills/`、`AGENTS.md`、`rules/`、`docs/`、`scripts/`、部署治理文件和 active Change 文档
- **AND** 系统 MUST NOT 修改 `src/` 目录下任何业务运行时代码

#### Scenario: 输出学习报告

- **WHEN** 系统完成应用阶段
- **THEN** 系统 MUST 输出学习报告
- **AND** 学习报告 MUST 写入 `docs/spec-logs/YYYYMMDDhhmmss-study-xxx.md`
- **AND** 同一次学习应用流程 MUST 只生成一份正式 `study` 报告
- **AND** 如同一流程已有学习报告，系统 MUST 更新该报告而不是创建第二份 `study` 报告
- **AND** 学习阶段候选内容 MUST NOT 另行落盘为第二份正式 `study` 报告
- **AND** `/spec-study` 触发的治理资产应用结果 MUST 汇总到同一份 `study` 报告
- **AND** 系统 MUST NOT 为同一 `/spec-study` 流程额外生成内容重复的 `YYYYMMDDhhmmss-governance-xxx.md`
- **AND** `YYYYMMDDhhmmss` MUST 使用报告生成时刻的 `Asia/Shanghai` 日期时间，精确到秒
- **AND** `xxx` MUST 使用小写 kebab-case 表达学习对象或主题
- **AND** 学习报告 MUST 包含学习对象、学习模式、采纳内容、未采纳内容、更新文件、验证结果和后续建议
- **AND** 学习报告 MUST NOT 包含用户隐私数据、真实客户数据、密钥、访问令牌、本机绝对路径、未脱敏日志、订单原文、聊天原文、工单原文、截图中的个人信息或学习对象源码
- **AND** 如需说明隐私相关风险或路径证据，学习报告 MUST 使用仓库相对路径、脱敏占位符或聚合描述
- **AND** 最终回复 MUST 摘要说明学习到什么、具体应用了哪些内容、分别更新了哪些文档

### Requirement: 推送前 Git 安全检测

系统 SHALL 提供 `/git-check` 治理命令，用于在提交或推送前检测 staged、modified tracked 和 untracked 文件中的真实环境文件、运行时数据、大文件、密钥、Token、连接串、本机绝对路径和不应进入 Git 的本地数据。

#### Scenario: 默认安全扫描

- **GIVEN** 用户运行 `/git-check`
- **WHEN** 当前 staged 或 tracked 文件包含真实 `.env`、数据库文件、运行时数据、密钥、Token、连接串或本机绝对路径
- **THEN** 命令 SHALL 输出脱敏 error 并返回非 0
- **AND** 命令不得删除文件、修改 `.gitignore` 或自动 unstage

#### Scenario: 安全通过

- **GIVEN** 用户运行 `/git-check`
- **WHEN** 扫描范围没有阻断项
- **THEN** 命令 SHALL 返回 0
- **AND** 输出扫描摘要、warning 摘要和后续建议

### Requirement: 跨项目学习应用命令

系统 SHALL 通过 `/spec-study` 支持跨项目 Harness / OpenSpec / Agent 治理学习，并在用户确认后按本项目 OpenSpec 与 Sprint 门禁应用治理资产。

#### Scenario: 日志优先学习

- **GIVEN** 用户运行 `/spec-study <学习对象>`
- **WHEN** 学习对象存在 `docs/spec-logs/CHANGELOG.md`
- **THEN** 命令 SHALL 先读取该总账作为治理演进入口地图
- **AND** 再按主题读取相关 `study` 或 `governance` 单次日志
- **AND** 再横向校验 `AGENTS.md`、`rules/`、`docs/`、Agent 目录、`scripts/`、部署与环境示例等真实治理资产
- **AND** 若日志与真实资产存在漂移，候选清单 SHALL 标注漂移风险并以当前真实资产为最终依据

#### Scenario: 学习对象只读保护

- **GIVEN** 用户运行 `/spec-study` 或 `/spec-study apply`
- **WHEN** 学习对象为本地路径
- **THEN** 命令 SHALL 只读访问学习对象
- **AND** 不得在学习对象内写入、安装、生成、格式化、迁移、清理、提交、切换分支或修改 Git 状态

### Requirement: 命令引导式反馈

系统 SHALL 在命令需要用户选择、确认、补充信息或处理阻塞时提供结构化反馈，并避免用大段开放式追问替代关键决策。

#### Scenario: 使用原生交互卡片或降级文本

- **GIVEN** 命令需要用户做出 1 到 3 个关键决策
- **WHEN** 当前客户端或工具层支持原生交互卡片
- **THEN** 命令 SHOULD 使用原生交互卡片展示结构化选项、推荐项和可补充说明入口
- **AND** 当原生交互卡片不可用时，命令 SHALL 降级为文本结构化选项并说明降级原因

### Requirement: Agent 命令需求偏差阶段分流

`/capture`、`/explore` 与 `/opsx-modify` MUST 在处理已有关联 REQ、BUG、Change 或 Sprint 的“不如预期”反馈时，先判断目标 Change 与 Sprint 生命周期阶段，再决定使用验收返修、BUG capture 或 REQ capture。

#### Scenario: Active Change 内验收返修

- **GIVEN** 反馈关联的 Change 已完成 `/opsx-apply`
- **AND** 该 Change 尚未 `/opsx-archive`
- **AND** 反馈仍属于原需求、原 Change、原验收项或原能力边界
- **WHEN** AI 判断后续命令
- **THEN** AI MUST 推荐 `/opsx-modify <REQ-id|BUG-id|change-id> <反馈>`
- **AND** `/capture` MUST NOT 为该反馈自动创建新的 REQ 或 BUG

#### Scenario: Active Change 范围外反馈

- **GIVEN** 反馈关联的 Change 尚未归档
- **AND** 反馈新增原需求未包含的功能，或改变 API、DB、权限、部署、对象存储边界，或构成影响范围超出当前 Change 的独立缺陷
- **WHEN** AI 判断后续命令
- **THEN** AI MUST 停止 `/opsx-modify`
- **AND** AI MUST 推荐 `/capture`、`/req-capture` 或 `/bug-capture`
- **AND** 若反馈是已承诺行为的偏差，BUG SHOULD 记录 `related_requirement`

#### Scenario: Change 已归档但 Sprint 未归档

- **GIVEN** 原 REQ 或 Change 已归档
- **AND** 所属 Sprint 仍在 `iterations/change/`
- **WHEN** 用户发现已交付能力与预期不符
- **THEN** AI MUST NOT 推荐 `/opsx-modify`
- **AND** AI SHOULD 推荐 `/bug-capture` 并关联原 REQ
- **AND** 若反馈是新增能力或体验增强，AI SHOULD 推荐 `/req-capture`

#### Scenario: Sprint 已归档后的反馈

- **GIVEN** 所属 Sprint 已归档到 `iterations/archive/`
- **WHEN** 用户提出已交付能力偏差或新增期望
- **THEN** AI MUST 将该反馈作为新的生命周期输入处理
- **AND** 已交付能力偏差 SHOULD 走 `/bug-capture`
- **AND** 新增期望 SHOULD 走 `/req-capture`

### Requirement: Release workflow commands provide explicit operator decision summaries

Release workflow commands SHALL preserve and echo operator decisions for usage documentation, public announcement generation, and image build requirements before moving to the next release stage.

#### Scenario: Release proposal captures publication decisions
- **GIVEN** an operator proposes a release
- **WHEN** usage docs, announcement, or image build decisions are known
- **THEN** the command SHALL record those decisions in the release artifact
- **AND** the final response SHALL summarize each decision and any remaining missing decision.

### Requirement: Release blockers include actionable remediation paths

Release prepare and image commands SHALL distinguish resolved blockers, true release blockers, and warnings, and SHALL provide an actionable next command or remediation path when one is known.

#### Scenario: Prepare finds target MySQL drift
- **GIVEN** release preparation detects target MySQL schema drift
- **WHEN** the command records the blocker
- **THEN** the output SHALL identify the missing table or field category without exposing credentials
- **AND** SHALL suggest a safe migration or drift-check rerun path.

### Requirement: Publish confirmation avoids image evidence loops

Release publish SHALL write publish confirmation only to non-stable publish metadata and SHALL NOT require image rebuild for status-only announcement generation after publish.

#### Scenario: Operator requests public announcement after publish
- **GIVEN** image manifest validation already passed
- **WHEN** the operator asks to generate public announcement copy after publish
- **THEN** the workflow MAY update announcement content and non-stable release metadata
- **AND** SHALL re-run publish validation and image manifest validation
- **AND** SHALL NOT require image rebuild unless stable release scope or image input files changed.

### Requirement: Sprint retrospective AI usage matrices require a fresh gate pass

`/sprint-exps` and its Sprint Fact Sheet tooling SHALL NOT output real AI usage cost matrices unless the AI usage snapshot passes the fresh gate.

#### Scenario: Snapshot is stale before retrospective matrix rendering
- **GIVEN** a Sprint Fact Sheet summary reports `ai_usage_snapshot.fresh_gate.status` as `blocker`
- **WHEN** `/sprint-exps` prepares the model token usage analysis
- **THEN** the command SHALL show the blocker reason, impact, freshness baseline, and recommended action
- **AND** SHALL request or run the snapshot refresh path before rendering real matrices
- **AND** SHALL rerun `generate-sprint-fact-sheet.py --summary` after refresh
- **AND** SHALL NOT output real `total_tokens`, `input_tokens`, `output_tokens`, or `model_call_count` matrices until the rerun summary reports `fresh_gate.status=pass`.

#### Scenario: Markdown rendering is requested with a blocked gate
- **GIVEN** `generate-sprint-fact-sheet.py --ai-usage-markdown` is run for a Sprint whose snapshot is missing, stale, failed, estimated, coverage-incomplete, metrics-empty, or matrix-missing
- **WHEN** the script renders the model token usage section
- **THEN** it SHALL output a blocker-oriented Token Usage Fact Sheet with recommended refresh action
- **AND** it SHALL NOT render any real matrix table.

### Requirement: Workflow 命令完成复盘
系统 MUST 在 workflow 命令完成输出中提供执行链路复盘，复盘内容 MUST 基于脚本、校验、文件、日志、截图、验收记录、用户补证、Workflow Sync 或 AI Usage 等证据，不得凭空猜测。

#### Scenario: 命令成功完成
- **WHEN** `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*`、`/release-*`、`/image-*`、`/usage-docs-*`、`/spec-opt` 或 `/spec-study apply` 完成
- **THEN** 最终输出 MUST 包含链路状态、问题证据、规范优化建议和 follow-up 自动创建状态
- **AND** 若没有明确可复用沉淀，规范优化建议 MUST 写为“无明显优化点”

#### Scenario: 发现可沉淀问题
- **WHEN** 命令执行发现可复用的流程、规则、脚本或文档优化点
- **THEN** 输出 MUST 给出建议命令或标准 capture 文案
- **AND** 系统 MUST NOT 自动创建 follow-up Issue 或 Change，除非用户在当前命令中明确授权

### Requirement: 证据化根因分析
系统 MUST 在问题排查、BUG 完善、BUG 来源实现、验收返修和效果不如预期场景中区分根因状态，并且 MUST 要求 confirmed 根因绑定证据链。

#### Scenario: BUG 评审通过要求 confirmed 根因
- **WHEN** 用户执行 `/bug-review <BUG-id>` 默认 approve 或显式执行 `/bug-review <BUG-id> --approve`
- **THEN** 系统 MUST 在写入评审结果、状态变更、目录迁移和 Workflow Sync 前校验目标 BUG 的 `root_cause_status`
- **AND** `root_cause_status` MUST 为 `confirmed`
- **AND** confirmed 根因 MUST 包含可定位证据链
- **AND** 若 `root_cause_status` 为 `unknown`、`hypothesis`、`probable`，或缺少 `root-cause.md`、缺少根因状态、confirmed 缺少证据链，系统 MUST 阻断 approve
- **AND** 阻断输出 MUST 提示先补齐根因证据或显式选择 `--defer`、`--reject`、`--wont-fix`

### Requirement: UI 返修截图逐项对照
系统 MUST 在 UI 型 `/opsx-modify` 中先处理验收反馈证据，再修改实现。若反馈包含附件截图、标注图、原型截图或实际截图，系统 MUST 建立逐项视觉对照表。

#### Scenario: 附件截图反馈
- **WHEN** `/opsx-modify` 的验收反馈包含附件截图、标注图、原型截图或实际截图
- **THEN** 系统 MUST 在返修前记录截图编号、页面或状态、期望表现、实际表现、偏差项、检查方式、处置结论和证据入口
- **AND** 若证据不足以定位偏差，系统 MUST 先请求补证或说明补证步骤，不得直接返修

#### Scenario: UI 返修完成
- **WHEN** UI 返修修改完成
- **THEN** 系统 MUST 将相关旧截图视为 stale
- **AND** 系统 MUST 重新取证或记录等价视觉验证，并更新 Change trace、验收记录或测试证据入口

### Requirement: Workflow Sync next 推导复核
Workflow Sync MUST 在 `req.opsx` / `bug.opsx` 创建或确认 Change 后刷新 Issue 当前态看板的下一步推导，避免派生态继续提示已完成的 `/req-opsx` 或 `/bug-opsx`。

#### Scenario: REQ 或 BUG 回填 Change
- **WHEN** Workflow Sync 处理 `req.opsx` 或 `bug.opsx`
- **AND** 同轮已经将 Change 回填到 Issue trace、registry 或 Sprint scope
- **THEN** `issues/requirements/CHANGELOG.md` 或 `issues/bugs/CHANGELOG.md` 的下一步 MUST 推导为后续 `/opsx-apply <REQ-id|BUG-id>` 或等价下一阶段命令
- **AND** 若仍提示 `/req-opsx` 或 `/bug-opsx`，系统 MUST 报告派生态漂移并修复后再完成父命令

### Requirement: 治理脚本门禁矩阵
系统 MUST 维护命令阶段到最小相关治理脚本的门禁矩阵，帮助 Agent 在不全量运行无关测试的前提下选择必要验证。

#### Scenario: 治理资产变更
- **WHEN** 命令修改 `.agents/skills/`、`rules/`、`docs/`、`scripts/` 或 OpenSpec Change 文档
- **THEN** 系统 MUST 按治理脚本门禁矩阵选择最小相关验证
- **AND** 输出 MUST 说明未运行业务测试的原因（如不涉及 API、DB、Web、小程序、管理端或 Docker）

### Requirement: 文档事实唯一归属
系统 MUST 为长期治理事实维护唯一事实源；入口文档和命令技能可以摘要引用，但不得复制完整规则导致漂移。

#### Scenario: 新增或更新长期治理规则
- **WHEN** 命令修改 `AGENTS.md`、`rules/`、`docs/`、`.agents/skills/` 或 `scripts/`
- **THEN** 系统 MUST 判断该事实的唯一归属位置
- **AND** 其他位置 SHOULD 使用短摘要和相对链接指向事实源

### Requirement: 治理决策记录字段
系统 MUST 在治理类 Change、`/spec-study` 学习报告和 `/spec-opt` 治理日志中记录关键决策，而不是只记录文件清单。

#### Scenario: 应用治理学习或规范优化
- **WHEN** `/spec-study apply` 或 `/spec-opt` 完成治理资产更新
- **THEN** 报告 MUST 包含采纳原因、未采纳原因、替代方案或取舍、验证责任和后续触发条件
- **AND** 报告 MUST 不包含会话推理、未脱敏路径、密钥、用户隐私或学习对象源码

### Requirement: 文档 slop 与 CoT 泄漏审计
系统 MUST 提供长期文档卫生规则和轻量校验，帮助发现会话推理残留、临时草稿引用、review 对话、不可解析内部引用和不必要历史叙事。

#### Scenario: 修改长期治理文档
- **WHEN** 命令新增或修改 `docs/`、`rules/`、`AGENTS.md` 或 `.agents/skills/`
- **THEN** 系统 SHOULD 运行文档卫生校验或说明不适用原因
- **AND** 发现项 MUST 由人工或 Agent 语义判断后处理，不得由脚本自动删除事实性内容

### Requirement: 最小相关验证选择
系统 MUST 根据实际 diff scope 和影响面选择最小相关证据，同时不得跳过项目强制门禁。

#### Scenario: 治理变更完成
- **WHEN** 变更只触达治理文档、技能或校验脚本
- **THEN** 系统 SHOULD 运行治理相关脚本、目标 Change 校验和脚本自身校验
- **AND** 系统 SHOULD 明确业务测试不适用的原因
- **AND** 系统 MUST NOT 仅因为提交、归档或输出报告而重复运行已通过且未被新改动影响的无关检查

### Requirement: 防御性模式知识库模板
系统 MUST 支持将已发生或险些发生的问题沉淀为防御性模式，记录缺陷类别、预防规则和验证方式。

#### Scenario: 问题具备复用价值
- **WHEN** BUG、返修、发布事故、验收失败或治理复盘发现可复用的预防规则
- **THEN** 系统 SHOULD 建议写入 `docs/knowledge-base/best-practices/`
- **AND** 条目 SHOULD 使用防御性模式模板，避免写成长篇事故叙事

### Requirement: Review 命令默认通过
系统 MUST 将 `/req-review <REQ-id>` 与 `/bug-review <BUG-id>` 的无 flag 调用解释为评审通过，并继续执行与显式 `--approve` 相同的状态更新、目录迁移、Workflow Sync 和 AI Usage hook。反向评审结果 MUST 使用显式 flag 表达，包括 `--reject`、`--defer`，以及 BUG 专属的 `--wont-fix`。

#### Scenario: 缺陷评审无 flag 默认通过
- **WHEN** 用户执行 `/bug-review BUG-xxxx`
- **THEN** 系统 MUST 将评审结果设置为 `approved`
- **AND** 系统 MUST 先通过 BUG 根因 confirmed 门禁
- **AND** 系统 MUST 执行与原 `/bug-review BUG-xxxx --approve` 相同的 `plan/` 到 `review/` 目录迁移、状态同步和后续门禁提示
- **AND** 后续正向命令示例 SHOULD 使用 `/bug-review BUG-xxxx`

### Requirement: opsx linked Change 多入口自动回填
系统 MUST 在 `req.opsx` / `bug.opsx` 创建或确认 linked Change 后，幂等同步 Issue trace、主文档、registry 与 Sprint scope 中的 linked Change 信息，避免后续命令解析、当前态看板和人工入口出现漂移。同步后的 Issue trace frontmatter MUST 是标准 YAML parser 可解析的合法 YAML，并 MUST 保持顶层 Issue 状态与 `openspec_changes[].status` 语义隔离。

#### Scenario: REQ linked Change 回填完整
- **WHEN** Workflow Sync 处理 `req.opsx`
- **AND** 输入包含 `--req <REQ-id>` 与 `--change <change-id>`
- **THEN** 系统 MUST 确保目标 REQ `trace.md` 的 frontmatter 与 fenced yaml 中 `openspec_changes[]` 包含该 Change
- **AND** 系统 MUST 确保目标 REQ 的 `related_changes[]` 或等价索引包含该 Change
- **AND** 系统 MUST 确保 `requirement.md` 的人类入口字段引用该 Change
- **AND** 系统 MUST 确保 `issues/requirements/_registry.yaml` 对应条目的 `related_change` 引用该 Change。

#### Scenario: BUG linked Change 回填完整
- **WHEN** Workflow Sync 处理 `bug.opsx`
- **AND** 输入包含 `--bug <BUG-id>` 与 `--change <change-id>`
- **THEN** 系统 MUST 确保目标 BUG `trace.md` 的 frontmatter 与 fenced yaml 中 `openspec_changes[]` 包含该 Change
- **AND** 系统 MUST 确保目标 BUG 的 `related_change` 或等价索引引用该 Change
- **AND** 系统 MUST 确保 `bug.md` 的人类入口字段引用该 Change
- **AND** 系统 MUST 确保 `issues/bugs/_registry.yaml` 对应条目的 `related_change` 引用该 Change。

#### Scenario: Sprint scope 回填一致
- **WHEN** 目标 REQ 或 BUG 已正式纳入某个 `sprint-xxx`
- **AND** Workflow Sync 处理同一 Issue 的 `req.opsx` 或 `bug.opsx`
- **THEN** 系统 MUST 将 `<change-id>` 写入同一 Sprint 的 `sprint.yaml.changes[]`
- **AND** 系统 MUST 更新匹配的 `scope_estimates[].change`
- **AND** 系统 MUST 刷新 Sprint Scope 派生块
- **AND** `/opsx-apply --sprint auto --change <change-id>` 或等价 dry-run MUST 能解析到该 Sprint。

#### Scenario: linked Change 回填后的 frontmatter 合法
- **WHEN** Workflow Sync 处理 `req.opsx` 或 `bug.opsx` 并写入 linked Change
- **THEN** 目标 Issue `trace.md` frontmatter MUST 能被标准 YAML parser 解析
- **AND** `openspec_changes:` 父键 MUST 存在
- **AND** 重复运行 MUST NOT 产生缺父键缩进列表项或重复 linked Change 条目。

### Requirement: upgrade 命令必须遵守工作流输出契约
Agent workflow tooling SHALL support upgrade planning and validation commands with Workflow Sync, AI Usage, context budget, and safe output contracts.

#### Scenario: upgrade 命令成功输出摘要
- **WHEN** `/upgrade-plan`、`/upgrade-validate` 或等价命令成功完成
- **THEN** 命令输出 SHALL 包含目标版本、来源版本、支持级别、blocker 数、warning 数、证据摘要、计划路径和下一步
- **AND** 命令 SHALL 默认输出 compact summary，不输出完整 manifest、完整 env、完整日志或大体积历史归档内容。

#### Scenario: upgrade 命令接入审计钩子
- **WHEN** upgrade 命令完成并且主校验成功
- **THEN** 命令 SHALL 运行 Workflow Sync 或等价状态同步
- **AND** 命令 SHALL 运行 AI Usage post-command hook，并按 release version、from version、to version 或 upgrade plan 归因。

#### Scenario: upgrade 命令保持生产安全边界
- **WHEN** upgrade 命令生成计划、校验计划或提示人工步骤
- **THEN** 命令 SHALL NOT 自动修改真实生产 env、自动执行生产升级、自动执行数据库写入迁移或对象存储写入维护任务
- **AND** 需要人工确认时 SHALL 输出结构化选项、推荐项、阻塞项和风险说明。

