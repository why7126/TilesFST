## ADDED Requirements

### Requirement: Workflow Sync 必须回填 Sprint 正式范围 Issue 的 iteration

当 `/sprint-propose` 或等价 Sprint scope 同步动作已将 REQ/BUG 写入目标 Sprint 的 `sprint.yaml` 正式范围时，Workflow Sync MUST 将对应 Issue `trace.md` 的 `status` 与 `iteration` 同步为同一 Sprint 事实。

#### Scenario: sprint.propose 同步已纳入 REQ

- **WHEN** `iterations/change/sprint-xxx/sprint.yaml` 的 `requirements[]` 包含某个已评审 REQ
- **AND** 运行 `python scripts/sync-workflow-status.py --event sprint.propose --sprint sprint-xxx`
- **THEN** 该 REQ `trace.md` frontmatter 与 fenced YAML 中的 `status` MUST 为 `in_sprint`
- **AND** 该 REQ `trace.md` frontmatter 与 fenced YAML 中的 `iteration` MUST 为 `sprint-xxx`

#### Scenario: 未纳入 Sprint 的 Issue 不回填 iteration

- **WHEN** 某个 REQ/BUG 不在已解析 Sprint 的 `requirements[]` 或 `bugs[]` 中
- **AND** 运行 Workflow Sync
- **THEN** Workflow Sync MUST NOT 为该 Issue 写入目标 Sprint 的 `iteration`

