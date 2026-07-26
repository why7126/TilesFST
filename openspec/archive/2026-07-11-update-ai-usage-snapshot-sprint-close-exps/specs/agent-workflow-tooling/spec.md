## ADDED Requirements

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
