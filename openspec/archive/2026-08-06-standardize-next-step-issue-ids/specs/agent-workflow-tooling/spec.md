# agent-workflow-tooling 规格变更

## ADDED Requirements

### Requirement: 下一步命令参数标识规范
系统 MUST 统一命令最终输出中的下一步可执行命令参数。REQ 来源的后续命令 MUST 使用原始 `REQ-*` 标识，BUG 来源的后续命令 MUST 使用原始 `BUG-*` 标识，非 REQ/BUG 的直接 Change MUST 使用 `<change-id>`。

#### Scenario: REQ 来源后续 opsx 命令使用 REQ ID
- **WHEN** `/req-opsx <REQ-id>` 创建或确认 linked Change
- **THEN** 系统输出的下一步 `/opsx-apply` MUST 使用 `<REQ-id>`
- **AND** 后续 `/opsx-apply` 完成后输出的 `/opsx-archive` MUST 继续使用 `<REQ-id>`
- **AND** 系统 MUST NOT 在 REQ 来源链路中把下一步引导改为真实 `<change-id>`

#### Scenario: BUG 来源后续 opsx 命令使用 BUG ID
- **WHEN** `/bug-opsx <BUG-id>` 创建或确认 linked Change
- **THEN** 系统输出的下一步 `/opsx-apply` MUST 使用 `<BUG-id>`
- **AND** 后续 `/opsx-apply` 完成后输出的 `/opsx-archive` MUST 继续使用 `<BUG-id>`
- **AND** 系统 MUST NOT 在 BUG 来源链路中把下一步引导改为真实 `<change-id>`

#### Scenario: 非 REQ/BUG Change 使用 change id
- **WHEN** Change 不关联 REQ 或 BUG
- **THEN** 系统输出的 `/opsx-apply`、`/opsx-archive` 下一步 MUST 使用真实 `<change-id>`

#### Scenario: opsx 命令解析 REQ 或 BUG target
- **WHEN** 用户执行 `/opsx-apply <REQ-id>`、`/opsx-archive <REQ-id>`、`/opsx-apply <BUG-id>` 或 `/opsx-archive <BUG-id>`
- **THEN** 系统 MUST 从对应 Issue `trace.md` 的 `openspec_changes[]` 解析 linked Change
- **AND** 内部 OpenSpec CLI、Workflow Sync 和 AI Usage hook MUST 使用解析后的真实 `<change-id>`
- **AND** 最终下一步展示 MUST 继续使用原始 `<REQ-id>` 或 `<BUG-id>`

#### Scenario: 多个候选 Change 需要用户决策
- **WHEN** 一个 REQ 或 BUG 关联多个符合当前阶段的候选 Change
- **THEN** 系统 MUST 列出候选 Change
- **AND** 系统 MUST 要求用户选择目标 Change
- **AND** 系统 MUST NOT 猜测其中一个 Change 继续执行
