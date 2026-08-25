## MODIFIED Requirements

### Requirement: Workflow Sync 支持摘要输出模式
系统 MUST 为 Workflow Sync 报告提供摘要输出模式，用聚合计数和关键上下文替代成功路径中的长文件明细。摘要输出 MUST 覆盖 Issue 子文档同步结果，包括检查数量、更新数量、验收结果状态或不适用原因、drift warning 数量。系统 MUST 在 `bug.generate` 事件中将已生成 `bug.md` 的目标 BUG 主状态从 `captured` 或等价生成前状态推进为 `draft`，并在摘要中体现状态同步结果。

#### Scenario: 成功同步输出摘要
- **WHEN** 用户或 source-command 执行 `scripts/sync-workflow-status.py` 且同步成功
- **THEN** 系统 MUST 输出 Workflow Sync Report 摘要
- **AND** 摘要 MUST 包含 event、focus issue 或 change、sprint 解析结果、updated 数量、skipped 数量和 errors 数量
- **AND** 当事件关联 REQ 或 BUG 时，摘要 MUST 包含子文档检查数量、子文档更新数量、验收结果状态或不适用原因、drift warning 数量
- **AND** 系统 MUST NOT 默认逐条输出完整 `Skipped (no delta)` 文件列表

#### Scenario: bug.generate 推进 BUG 主状态
- **GIVEN** 一个 BUG 的 `trace.md` 主状态为 `captured` 或等价生成前状态
- **AND** 该 BUG 包含已生成的 `bug.md`
- **WHEN** 用户或 source-command 执行 `scripts/sync-workflow-status.py --event bug.generate --bug <BUG-id> --sprint auto`
- **THEN** 系统 MUST 将该 BUG 主状态推进为 `draft`
- **AND** 系统 MUST 同步 `trace.md` frontmatter 与 fenced YAML 中的 `status`、`updated_at` 和 `lifecycle.generated`
- **AND** 系统 MUST 同步 `issues/bugs/_registry.yaml` 中该 BUG 的 `status`
- **AND** 系统 SHOULD 同步 `issues/bugs/CHANGELOG.md` 当前态行，使下一步指向 `/bug-complete <BUG-id>`
- **AND** 系统 MUST 保持 `bug.md` frontmatter 的 `status: draft`，不得被旧 trace 主状态反向覆盖为 `captured`

#### Scenario: bug.generate 重复运行保持幂等
- **GIVEN** 一个 BUG 已完成 `/bug-generate` 且主状态为 `draft`
- **WHEN** 用户或 source-command 重复执行 `scripts/sync-workflow-status.py --event bug.generate --bug <BUG-id> --sprint auto`
- **THEN** 系统 MUST 保持 trace、registry、CHANGELOG 和 `bug.md` frontmatter 状态一致
- **AND** 系统 MUST NOT 重复追加异常或重复的 `## 变更记录`

#### Scenario: bug.generate 缺少 bug.md 时不误推进
- **GIVEN** 一个 BUG 的 `trace.md` 主状态为 `captured`
- **AND** 该 BUG 缺少 `bug.md`
- **WHEN** 用户或 source-command 执行 `scripts/sync-workflow-status.py --event bug.generate --bug <BUG-id> --sprint auto`
- **THEN** 系统 MUST NOT 将该 BUG 主状态推进为 `draft`
- **AND** 系统 MUST 输出 warning、no-op 摘要或等价诊断，提示缺少 `bug.md`
