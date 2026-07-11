## ADDED Requirements

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
