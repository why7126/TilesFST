## MODIFIED Requirements

### Requirement: Sprint close stale scan 回归测试
测试治理 SHALL 要求 Sprint close stale scan、Workflow Sync 四件套刷新、旧归档路径残留检查和 Issue 子文档 residual reconcile 具备聚焦自动化回归覆盖。

#### Scenario: 安全 Issue 子文档 residual 自动清理回归
- **WHEN** pytest fixture 构造一个已闭环 Issue，且 `capture.md` 仅残留可安全同步的 `status: captured`
- **THEN** 测试 MUST 断言归档同步或 promote 前置流程会自动处理该 residual
- **AND** 再次执行 `promote-issues-for-archive` MUST 不因该 residual 返回 Issue Subdocument Status Gate

#### Scenario: 人工判断 Issue 子文档 residual 仍阻断
- **WHEN** pytest fixture 构造一个缺少闭环证据、验收结果或状态字段语义不明的 Issue residual
- **THEN** 测试 MUST 断言归档同步或 promote 前置流程不会自动写入该字段
- **AND** 报告 MUST 包含 warning 或 blocker 以及建议处理命令

#### Scenario: Issue 子文档 residual reconcile 幂等
- **WHEN** 测试对同一已闭环 Issue 重复执行 residual reconcile
- **THEN** 第二次执行 MUST 报告 no delta 或等价摘要
- **AND** 测试 MUST 断言没有重复更新时间戳或产生无意义 diff
