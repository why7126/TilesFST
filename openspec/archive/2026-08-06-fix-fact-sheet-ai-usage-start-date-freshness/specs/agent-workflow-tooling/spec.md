## MODIFIED Requirements

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
