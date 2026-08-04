## ADDED Requirements

### Requirement: 大型 Sprint Fact Sheet 默认使用 compact AI usage 摘要
系统 MUST 在 Sprint Fact Sheet summary 中默认输出 compact Token Usage Fact Sheet 摘要，避免 10+ Change Sprint 默认携带完整 `usage_matrices` 明细；完整矩阵 MUST 只能通过 fields、完整 JSON 或用户明确要求的等价路径按需读取。

#### Scenario: 10+ Change Sprint summary 不输出完整矩阵
- **WHEN** 用户、测试命令或 `/sprint-exps` 请求包含 10 个或以上 Change 的 Sprint Fact Sheet summary
- **THEN** summary MUST 输出 AI usage mode、snapshot status、fresh gate、warning_count、coverage status、关键 totals、矩阵可用性、矩阵行列规模和 recommended_action
- **AND** summary MUST NOT 默认输出完整 `usage_matrices.rows` 或四张 usage matrix 明细
- **AND** summary MUST 提供获取完整矩阵的 fields 路径提示

#### Scenario: 按需读取完整 usage matrices
- **WHEN** 用户、测试命令或 `/sprint-exps` 明确请求 `ai_usage_snapshot.usage_matrices` 字段
- **THEN** 系统 MUST 返回完整 `usage_matrices` 结构
- **AND** 返回内容 MUST 继续遵守 AI 使用量事实脱敏要求，不得包含原始 prompt、系统指令、developer 指令、本机绝对路径、密钥或工具输出全文

#### Scenario: `/sprint-exps` 默认消费 compact summary
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **THEN** `/sprint-exps` MUST 先使用 Fact Sheet summary 的 compact AI usage 摘要判断 fresh gate 和矩阵可用性
- **AND** `/sprint-exps` MUST NOT 在默认路径中读取或转述完整 `usage_matrices`
- **AND** 仅当用户明确要求矩阵明细或复盘文档确需写入真实矩阵时，`/sprint-exps` MAY 通过 fields 模式读取完整矩阵
