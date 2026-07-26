## ADDED Requirements

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
