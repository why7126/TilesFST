## MODIFIED Requirements

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
