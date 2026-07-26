## ADDED Requirements

### Requirement: Sprint 验收报告分层呈现
系统 SHALL 在 Sprint 验收报告中分层呈现最终验收摘要与原始 AC 引用，使最终归档判断不被历史未勾选 AC 干扰。

#### Scenario: 验收报告包含最终摘要和原始引用
- **WHEN** 系统生成或主动更新 `iterations/*/<sprint>/acceptance-report.md`
- **THEN** 报告 MUST 包含最终验收摘要或等价章节
- **AND** 报告 MUST 包含原始 AC 引用或等价章节
- **AND** 最终验收摘要 MUST 位于原始 AC 明细之前
- **AND** 报告 MUST 明确最终摘要用于归档判断，原始 AC 引用用于追溯和人工复核

#### Scenario: 最终摘要展示归档事实
- **WHEN** Sprint 验收报告表达 Sprint 是否可关闭
- **THEN** 最终验收摘要 MUST 展示 readiness gate 结果、Change 归档状态、tasks 完成情况和 Sprint 生命周期状态
- **AND** 最终验收摘要 MUST 支持读者不读取原始 AC 明细即可判断 Sprint 是否满足关闭条件

#### Scenario: 原始 AC 未勾选项有明确语义
- **WHEN** 原始 AC 引用区域包含 `- [ ]` 未勾选项
- **THEN** 系统 MUST 标明未勾选项属于待人工 sign-off、阻断归档或历史追溯
- **AND** 历史追溯类未勾选项 MUST NOT 自动覆盖最终验收摘要中的归档结论

### Requirement: Sprint 归档门禁保持独立
系统 SHALL 保持 `/sprint-archive` 的 readiness gate、Change archive、tasks 完成与 Workflow Sync 门禁独立于原始 AC 引用呈现方式。

#### Scenario: 归档门禁失败时阻断关闭
- **WHEN** `/sprint-archive` readiness gate、Change archive 或 tasks 完成检查失败
- **THEN** 系统 MUST 阻断 Sprint 关闭
- **AND** 最终验收摘要 MUST 记录阻断项

#### Scenario: 归档门禁通过但仍需人工复核
- **WHEN** `/sprint-archive` hard gates 均通过且存在人工 QA 复核项
- **THEN** 系统 MAY 将 Sprint 标记为 completed/archive
- **AND** 报告 MUST 将人工 QA 复核项记录为 sign-off open item 或遗留复核项
- **AND** 系统 MUST NOT 因历史追溯类未勾选 AC 自动回退 Sprint 状态

### Requirement: 验收报告派生同步不覆盖人工结论
系统 SHALL 限制 Workflow Sync 对 `acceptance-report.md` 的写入范围，避免自动刷新覆盖人工最终结论、验收人或 sign-off 说明。

#### Scenario: Workflow Sync 刷新验收报告
- **WHEN** Workflow Sync 更新 `acceptance-report.md`
- **THEN** 系统 MAY 刷新派生 note、issue 状态行和 Change 状态摘要
- **AND** 系统 MUST NOT 覆盖人工填写的最终验收结论、验收人或 sign-off 说明
- **AND** 系统 MUST NOT 将原始 AC 未勾选项自动解释为 Sprint 未完成

#### Scenario: Fact Sheet 提取验收信号
- **WHEN** Fact Sheet 或 Sprint 复盘流程读取 `acceptance-report.md`
- **THEN** 系统 MUST 优先读取最终验收摘要和最终归档检查中的状态信号
- **AND** 系统 SHOULD 将原始 AC 引用中的孤立未完成文本作为证据提示而非 Sprint 完成状态事实源
