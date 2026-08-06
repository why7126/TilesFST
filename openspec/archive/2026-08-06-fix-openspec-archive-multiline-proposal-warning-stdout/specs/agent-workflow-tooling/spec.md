# agent-workflow-tooling Delta

## ADDED Requirements

### Requirement: OpenSpec 归档 wrapper 吸收已知 proposal warning
系统 MUST 在 OpenSpec 归档 wrapper 成功路径中吸收项目已确认可忽略的 proposal warning，同时保留未知 stdout/stderr 与失败路径诊断信息。

#### Scenario: 多行 proposal warning stdout 块被整体吸收
- **WHEN** `scripts/archive-change.sh` 执行 OpenSpec CLI 归档成功
- **AND** OpenSpec CLI stdout 输出以 `Proposal warnings in proposal.md` 开始的多行 warning 块
- **THEN** wrapper MUST 不展示该已知 warning 块中的标题行和详情行
- **AND** wrapper MUST 继续完成归档后的目录结构和归档证据校验

#### Scenario: 未知 stdout 继续保留
- **WHEN** OpenSpec CLI 归档成功
- **AND** stdout 中出现不属于已知 proposal warning 块的内容
- **THEN** wrapper MUST 将该未知 stdout 输出给用户

#### Scenario: 未知 stderr 继续保留
- **WHEN** OpenSpec CLI 归档成功
- **AND** stderr 中出现不属于已知 proposal warning 块的内容
- **THEN** wrapper MUST 将该未知 stderr 输出给用户

#### Scenario: 单行 proposal warning 过滤不回归
- **WHEN** OpenSpec CLI 归档成功
- **AND** stdout 或 stderr 输出既有单行 proposal scaffold warning
- **THEN** wrapper MUST 继续吸收该已知 warning

#### Scenario: 失败路径诊断不丢失
- **WHEN** OpenSpec CLI 归档失败
- **THEN** wrapper MUST 输出 OpenSpec CLI 的 stdout/stderr 诊断内容
- **AND** wrapper MUST 返回非零退出码
