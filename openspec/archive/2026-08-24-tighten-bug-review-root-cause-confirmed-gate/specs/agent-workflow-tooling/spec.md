## MODIFIED Requirements

### Requirement: 证据化根因分析
系统 MUST 在问题排查、BUG 完善、BUG 来源实现、验收返修和效果不如预期场景中区分根因状态，并且 MUST 要求 confirmed 根因绑定证据链。

#### Scenario: BUG 评审通过要求 confirmed 根因
- **WHEN** 用户执行 `/bug-review <BUG-id>` 默认 approve 或显式执行 `/bug-review <BUG-id> --approve`
- **THEN** 系统 MUST 在写入评审结果、状态变更、目录迁移和 Workflow Sync 前校验目标 BUG 的 `root_cause_status`
- **AND** `root_cause_status` MUST 为 `confirmed`
- **AND** confirmed 根因 MUST 包含可定位证据链
- **AND** 若 `root_cause_status` 为 `unknown`、`hypothesis`、`probable`，或缺少 `root-cause.md`、缺少根因状态、confirmed 缺少证据链，系统 MUST 阻断 approve
- **AND** 阻断输出 MUST 提示先补齐根因证据或显式选择 `--defer`、`--reject`、`--wont-fix`

### Requirement: Review 命令默认通过
系统 MUST 将 `/req-review <REQ-id>` 与 `/bug-review <BUG-id>` 的无 flag 调用解释为评审通过，并继续执行与显式 `--approve` 相同的状态更新、目录迁移、Workflow Sync 和 AI Usage hook。反向评审结果 MUST 使用显式 flag 表达，包括 `--reject`、`--defer`，以及 BUG 专属的 `--wont-fix`。

#### Scenario: 缺陷评审无 flag 默认通过
- **WHEN** 用户执行 `/bug-review BUG-xxxx`
- **THEN** 系统 MUST 将评审结果设置为 `approved`
- **AND** 系统 MUST 先通过 BUG 根因 confirmed 门禁
- **AND** 系统 MUST 执行与原 `/bug-review BUG-xxxx --approve` 相同的 `plan/` 到 `review/` 目录迁移、状态同步和后续门禁提示
- **AND** 后续正向命令示例 SHOULD 使用 `/bug-review BUG-xxxx`
