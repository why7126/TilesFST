## ADDED Requirements

### Requirement: Review 命令默认通过
系统 MUST 将 `/req-review <REQ-id>` 与 `/bug-review <BUG-id>` 的无 flag 调用解释为评审通过，并继续执行与显式 `--approve` 相同的状态更新、目录迁移、Workflow Sync 和 AI Usage hook。反向评审结果 MUST 使用显式 flag 表达，包括 `--reject`、`--defer`，以及 BUG 专属的 `--wont-fix`。

#### Scenario: 需求评审无 flag 默认通过
- **WHEN** 用户执行 `/req-review REQ-xxxx`
- **THEN** 系统 MUST 将评审结果设置为 `approved`
- **AND** 系统 MUST 执行与原 `/req-review REQ-xxxx --approve` 相同的 `plan/` 到 `review/` 目录迁移、状态同步和后续门禁提示
- **AND** 后续正向命令示例 SHOULD 使用 `/req-review REQ-xxxx`

#### Scenario: 缺陷评审无 flag 默认通过
- **WHEN** 用户执行 `/bug-review BUG-xxxx`
- **THEN** 系统 MUST 将评审结果设置为 `approved`
- **AND** 系统 MUST 执行与原 `/bug-review BUG-xxxx --approve` 相同的 `plan/` 到 `review/` 目录迁移、状态同步和后续门禁提示
- **AND** 后续正向命令示例 SHOULD 使用 `/bug-review BUG-xxxx`

#### Scenario: 反向评审必须显式选择
- **WHEN** 用户需要拒绝、延后或标记 BUG 不修复
- **THEN** 用户 MUST 显式使用 `/req-review <REQ-id> --reject`、`/req-review <REQ-id> --defer`、`/bug-review <BUG-id> --reject`、`/bug-review <BUG-id> --defer` 或 `/bug-review <BUG-id> --wont-fix`
- **AND** 无 flag 调用 MUST NOT 再触发评审检查清单追问
