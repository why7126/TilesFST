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

