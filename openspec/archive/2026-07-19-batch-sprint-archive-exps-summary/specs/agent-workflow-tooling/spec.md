## ADDED Requirements

### Requirement: 大 Sprint Change 批次摘要
系统 MUST 为包含 10 个以上 Change 的 Sprint 生成 Change 批次摘要，用聚合事实和证据路径替代一次性展开全部 `tasks.md`、`trace.md` 或验收正文。

#### Scenario: 生成大 Sprint 批次摘要
- **WHEN** Sprint scope 中的 `changes[]` 数量大于等于 10
- **THEN** Fact Sheet 或 readiness 输出 MUST 包含 Change 批次摘要
- **AND** 每个批次 MUST 包含批次标识、Change id 列表、排序依据、tasks 完成计数、trace 状态计数、blocker 数量、warning 数量和 evidence hints
- **AND** 批次摘要 MUST NOT 复制原始 `tasks.md`、`trace.md`、验收报告或测试日志全文

#### Scenario: 小 Sprint 不强制批次摘要
- **WHEN** Sprint scope 中的 `changes[]` 数量少于 10
- **THEN** 系统 MAY 保持现有整体 Fact Sheet 或 readiness 摘要
- **AND** 若输出批次字段，系统 MUST 标记批次摘要不适用或为空

### Requirement: `/sprint-archive` 大 Sprint 分批读取
`/sprint-archive` MUST 在大 Sprint 中优先消费 readiness 与 Fact Sheet 的批次摘要，并按批次定位归档队列、阻断项和必要回读片段。

#### Scenario: 大 Sprint archive 成功路径
- **WHEN** 用户执行 `/sprint-archive sprint-xxx`
- **AND** `sprint-xxx` 包含 10 个以上 Change
- **THEN** 命令流程 MUST 先运行或读取机器可读 readiness 与 Fact Sheet 摘要
- **AND** 输出 MUST 展示批次数、每批 Change 数、archived/skipped/blocked 聚合计数和 warning 数量
- **AND** 成功路径 MUST NOT 默认转述全部 Change 的完整 tasks 或 trace 明细

#### Scenario: 大 Sprint archive 失败路径
- **WHEN** `/sprint-archive` 的批次摘要发现 blocker 或 warning
- **THEN** 报告 MUST 定位到 batch id、Change id、证据文件路径和建议回读片段
- **AND** 命令 MAY 只分段读取该批次相关文件以诊断失败原因
- **AND** 系统 MUST 保留现有 readiness、Issue promote、路径残留和 Workflow Sync 门禁

### Requirement: `/sprint-exps` 大 Sprint 分批复盘
`/sprint-exps` MUST 在大 Sprint 复盘中优先消费 Sprint Fact Sheet 的批次摘要，按 warnings、needs_detail 或 evidence hints 分批回读原始证据。

#### Scenario: 大 Sprint exps 正常路径
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **AND** `sprint-xxx` 包含 10 个以上 Change
- **THEN** 命令流程 MUST 优先读取 Fact Sheet 中的批次摘要
- **AND** 复盘输出 MUST 使用批次聚合事实分析流程、质量、验收和 token 风险
- **AND** 复盘文档 MUST NOT 默认复制全部 Change 的 tasks、trace 或 acceptance report 正文

#### Scenario: 大 Sprint exps 需要细节
- **WHEN** 批次摘要标记 `needs_detail`、blocker、warning、missing 或 inconsistent 类风险
- **THEN** `/sprint-exps` MAY 按 batch id 和 evidence hints 回读对应批次的原始文件片段
- **AND** 复盘报告 MUST 说明该批次的风险、影响和建议后续动作

### Requirement: 批次摘要输出受上下文预算约束
系统 MUST 对批次摘要的命令输出和持久化边界执行上下文预算与脱敏约束，避免 batch summary 退化为长日志或敏感内容载体。

#### Scenario: 批次摘要 compact 输出
- **WHEN** Fact Sheet、readiness、`/sprint-archive` 或 `/sprint-exps` 输出批次摘要
- **THEN** 默认用户可见输出 MUST 使用 compact summary
- **AND** compact summary MUST 包含 Sprint id、change 总数、批次数、blocker 总数、warning 总数和 recommended action
- **AND** 系统 MUST NOT 默认输出完整 batch JSON、完整 `tasks.md`、完整 `trace.md`、完整测试日志或完整 Workflow Sync 派生块

#### Scenario: 机器可读批次摘要
- **WHEN** 用户或测试命令请求 JSON 输出
- **THEN** 系统 MUST 输出可机器校验的批次结构
- **AND** JSON MUST 只包含聚合计数、工作流 ID、仓库相对路径、短 warning 标签和 evidence hints
- **AND** JSON MUST NOT 包含原始 prompt、系统指令、developer 指令、密钥、Cookie、Authorization、`.env` 内容、真实客户数据或工具输出全文
