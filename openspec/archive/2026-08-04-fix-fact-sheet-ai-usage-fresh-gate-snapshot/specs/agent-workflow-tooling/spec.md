## MODIFIED Requirements

### Requirement: AI usage snapshot 新鲜度与覆盖校验
系统 MUST 校验 AI usage snapshot 的新鲜度、Sprint 归属、scope 覆盖和必要指标，防止过期或覆盖不足的 snapshot 被当作真实统计使用；fresh gate MUST 使用同一个 Sprint snapshot payload 作为状态、时间戳、coverage 和 usage mode 的事实源，避免已刷新 snapshot 被旧缓存、错误时间源或 fallback mode 误判为 stale。

#### Scenario: snapshot 早于关键变更
- **WHEN** snapshot 生成时间早于目标 Sprint 最近一次 scope、close、archive 或关联 trace 关键更新时间
- **THEN** 系统 MUST 将 snapshot 标记为 `stale` 或输出等价 warning
- **AND** 系统 MUST 提示刷新 snapshot

#### Scenario: snapshot 已刷新且覆盖完整
- **WHEN** snapshot 存在并属于目标 Sprint
- **AND** snapshot 生成时间不早于目标 Sprint scope、关联 Issue trace 和 Change trace 的关键更新时间
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
- **AND** `estimated_fallback`、`skipped`、`unavailable` MUST 保留具体原因和 recommended_action
- **AND** fallback mode MUST NOT 覆盖已通过 fresh gate 的真实 snapshot 状态

#### Scenario: 无法可靠判断
- **WHEN** 系统无法可靠判断 snapshot 是否覆盖所有关键对象
- **THEN** 系统 MUST 输出 blocker 或 warning
- **AND** 系统 MUST 提示刷新 snapshot 或回读具体证据

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
