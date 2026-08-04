## MODIFIED Requirements

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
