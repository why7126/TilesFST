# agent-workflow-tooling 规格变更

## ADDED Requirements

### Requirement: 所有 Change 纳入 Sprint 后才能 apply
系统 MUST 要求任意 OpenSpec Change 在执行 `/opsx-apply` 前已经纳入某个 Sprint 的正式范围。该规则 MUST 同时适用于来源于 REQ/BUG 的 Change，以及通过 `/opsx-propose`、`/spec-opt` 或其他治理流程直接创建的非 REQ/BUG Change。

#### Scenario: 非 REQ/BUG Change 未纳入 Sprint 时阻断 apply
- **WHEN** 用户请求 `/opsx-apply <change-id>`
- **AND** `<change-id>` 未出现在任何 `iterations/change|archive/<sprint>/sprint.yaml` 的 `changes[]`
- **THEN** 系统 MUST 阻断实现
- **AND** 系统 MUST 提示先通过 `/sprint-propose` 或等价 Sprint scope 修复流程纳入 Sprint
- **AND** 系统 MUST NOT 因该 Change 无 REQ/BUG 来源而豁免 Sprint Inclusion Gate

#### Scenario: 非 REQ/BUG Change 已纳入 Sprint 后允许 apply
- **WHEN** 用户请求 `/opsx-apply <change-id>`
- **AND** `<change-id>` 已出现在某个 `iterations/change|archive/<sprint>/sprint.yaml` 的 `changes[]`
- **AND** `python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto --dry-run` 能解析到该 Sprint
- **THEN** 系统 MAY 继续执行 `/opsx-apply`
- **AND** 若该 Change 不关联 REQ/BUG，系统 MUST 不要求额外创建 REQ/BUG

#### Scenario: REQ/BUG Change 继续保持双向一致门禁
- **WHEN** `<change-id>` 关联 REQ 或 BUG
- **THEN** 系统 MUST 继续要求 Sprint `requirements[]` 或 `bugs[]` 包含对应 Issue
- **AND** 系统 MUST 继续要求 Issue `trace.md` 的 `iteration` 指向同一 Sprint
- **AND** 系统 MUST 继续要求 Issue 状态为 `in_sprint` 或后续交付态

#### Scenario: spec-opt 不再豁免纯治理 Change
- **WHEN** `/spec-opt` 创建或复用纯治理 Change
- **THEN** 系统 MUST 提示该 Change 仍需纳入 Sprint 后才能 `/opsx-apply`
- **AND** 系统 MUST NOT 输出“纯治理 Change 可豁免 Sprint Gate”或等价表述
