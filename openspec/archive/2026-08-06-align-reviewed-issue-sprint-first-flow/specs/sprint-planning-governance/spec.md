# sprint-planning-governance 规格变更

## ADDED Requirements

### Requirement: 已评审 Issue 优先纳入 Sprint
系统 SHALL 将已评审 REQ/BUG 的推荐推进顺序定义为先纳入 Sprint 正式范围，再创建或回填 OpenSpec Change。未评审 REQ/BUG 仍不得进入 Sprint 正式范围；已纳入 Sprint 的 REQ/BUG 在后续 `/req-opsx` 或 `/bug-opsx` 创建 Change 时，系统 MUST 将 Change 回填到同一 Sprint 的机器事实源。

#### Scenario: REQ 评审通过后的推荐下一步
- **WHEN** `/req-review REQ-xxxx --approve` 成功将需求评审为 `approved`
- **THEN** 命令输出 MUST 将 `/sprint-propose <sprint-id> --req REQ-xxxx` 作为优先下一步
- **AND** 命令输出 MUST NOT 将 `/req-opsx REQ-xxxx` 表达为优先下一步
- **AND** 若缺少目标 Sprint、容量或范围信息，输出 MUST 将这些内容列为待用户决策或处理点

#### Scenario: BUG 评审通过后的推荐下一步
- **WHEN** `/bug-review BUG-xxxx --approve` 成功将缺陷评审为 `approved`
- **THEN** 命令输出 MUST 将 `/sprint-propose <sprint-id> --bug BUG-xxxx` 作为优先下一步
- **AND** 命令输出 MUST NOT 将 `/bug-opsx BUG-xxxx` 表达为优先下一步
- **AND** 若缺少目标 Sprint、修复优先级或容量信息，输出 MUST 将这些内容列为待用户决策或处理点

#### Scenario: Sprint 已纳入后创建 Change
- **WHEN** 已评审 REQ/BUG 已通过 `/sprint-propose` 纳入 `iterations/change/<sprint-id>/sprint.yaml`
- **AND** 用户执行 `/req-opsx` 或 `/bug-opsx`
- **THEN** Workflow Sync MUST 将新建 Change 写入同一 Sprint 的 `changes[]`
- **AND** Workflow Sync MUST 同步对应 `scope_estimates[].change`
- **AND** 系统 MUST 移除或更新该 Issue 的“待创建 Change”提示

#### Scenario: 未评审 Issue 仍被阻断
- **WHEN** REQ/BUG 未处于 `approved`、`in_sprint` 或后续交付态
- **AND** 用户尝试执行 `/sprint-propose` 将其纳入正式范围
- **THEN** 系统 MUST 阻断正式纳入
- **AND** 输出 MUST 提供可执行评审命令作为下一步

### Requirement: Sprint scope 支持待 Change 的已评审 Issue
系统 SHALL 允许 `/sprint-propose` 将已评审但尚未创建 OpenSpec Change 的 REQ/BUG 纳入正式 Sprint 范围，并在 Sprint 文档和机器事实源中保留后续 `/req-opsx` 或 `/bug-opsx` 的可执行引导。

#### Scenario: 已评审 REQ 尚未创建 Change
- **WHEN** `/sprint-propose` 纳入一个 `approved` REQ
- **AND** 该 REQ 的 `openspec_changes` 为空
- **THEN** `sprint.yaml` MUST 在 `requirements[]` 中记录该 REQ
- **AND** Sprint 输出 MUST 提示下一步执行 `/req-opsx REQ-xxxx`
- **AND** 后续 `/opsx-apply` 仍 MUST 等待 Change 回填到 `changes[]` 后才能继续

#### Scenario: 已评审 BUG 尚未创建 Change
- **WHEN** `/sprint-propose` 纳入一个 `approved` BUG
- **AND** 该 BUG 的 `openspec_changes` 为空
- **THEN** `sprint.yaml` MUST 在 `bugs[]` 中记录该 BUG
- **AND** Sprint 输出 MUST 提示下一步执行 `/bug-opsx BUG-xxxx`
- **AND** 后续 `/opsx-apply` 仍 MUST 等待 Change 回填到 `changes[]` 后才能继续
