## ADDED Requirements

### Requirement: 工作流成功路径紧凑输出契约
系统 MUST 为 Workflow Sync 与 AI usage post-command hook 建立统一 compact summary 输出契约，使工作流命令成功路径默认只输出聚合状态、关键上下文和推荐动作。

#### Scenario: Workflow Sync 默认成功摘要
- **WHEN** 用户或命令技能执行 `scripts/sync-workflow-status.py` 且命令成功完成
- **THEN** 系统 MUST 默认输出 Workflow Sync Report 摘要
- **AND** 摘要 MUST 至少包含 event、focus 对象、Sprint 解析结果、updated 数量、skipped 数量和 errors 数量
- **AND** 系统 MUST NOT 默认输出完整 `Skipped (no delta)` 文件列表、完整派生 Scope 块或长篇逐文件成功日志

#### Scenario: Workflow Sync 详细模式保留逐文件明细
- **WHEN** 用户或维护者显式请求 Workflow Sync 详细输出模式
- **THEN** 系统 MUST 输出逐文件 updated、skipped 和必要诊断明细
- **AND** 详细模式的同步结果、写入行为和退出码 MUST 与默认摘要模式一致

#### Scenario: Workflow Sync 失败路径保留诊断
- **WHEN** Workflow Sync 发生错误、drift 检查失败或 marker 解析失败
- **THEN** 系统 MUST 输出错误数量和每条错误原因
- **AND** 系统 MUST 返回非零退出码
- **AND** 系统 MUST 提供可定位问题文件或启用详细模式的提示

#### Scenario: AI usage hook 输出固定摘要字段
- **WHEN** 工作流命令在 Workflow Sync 成功后执行 AI usage post-command hook
- **THEN** 用户可见输出 MUST 只展示 compact summary
- **AND** compact summary MUST 包含 `status`、`usage_mode`、`command_run_count`、`sprint_snapshot`、`warning_count` 和 `recommended_action`
- **AND** 系统 MUST NOT 默认打印完整 session、原始 prompt、系统指令、developer 指令、技能全文、工具输出正文、完整 snapshot JSON 或完整 command run 明细

#### Scenario: AI usage hook 降级或不可用摘要
- **WHEN** AI usage hook 因本地 session 输入不可用、无安全记录、Sprint 无法解析或 snapshot 被跳过而降级
- **THEN** 系统 MUST 仍输出 compact summary
- **AND** `usage_mode` MUST 标明 `unavailable`、`estimated_fallback` 或等价降级状态
- **AND** `recommended_action` MUST 说明下一步可执行动作或无法自动恢复的原因
- **AND** 父工作流命令 MUST NOT 因 session 输入不可用而被判定失败

#### Scenario: 成功路径日志长度受上下文预算约束
- **WHEN** Workflow Sync 和 AI usage hook 均成功或以允许的降级状态完成
- **THEN** 命令技能 MUST 只向用户转述 compact summary 和必要的 Change/Sprint/Issue 结果
- **AND** 命令技能 MUST NOT 默认转述完整测试日志、完整 OpenAPI/Orval diff、完整 Workflow Sync 派生块、完整 AI usage JSON 或完整 snapshot 内容
