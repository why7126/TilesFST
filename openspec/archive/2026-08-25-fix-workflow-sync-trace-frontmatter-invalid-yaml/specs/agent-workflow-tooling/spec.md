## MODIFIED Requirements

### Requirement: Workflow Sync 支持摘要输出模式
系统 MUST 为 Workflow Sync 报告提供摘要输出模式，用聚合计数和关键上下文替代成功路径中的长文件明细。摘要输出 MUST 覆盖 Issue 子文档同步结果，包括检查数量、更新数量、验收结果状态或不适用原因、drift warning 数量。系统 MUST 在 `bug.generate` 事件中将已生成 `bug.md` 的目标 BUG 主状态从 `captured` 或等价生成前状态推进为 `draft`，并在摘要中体现状态同步结果。系统 MUST 保证写入后的 Issue `trace.md` frontmatter 是标准 YAML parser 可解析的合法 YAML，且 frontmatter 顶层 Issue 状态不得被 `openspec_changes[].status` 或其他嵌套字段污染。

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

#### Scenario: Issue trace frontmatter 写入后必须合法
- **WHEN** Workflow Sync 写入 REQ 或 BUG `trace.md` frontmatter
- **THEN** 写入后的 frontmatter MUST 能被标准 YAML parser 解析
- **AND** `lifecycle.generated` MUST 位于 `lifecycle` 父键下
- **AND** `openspec_changes[]` MUST 保留 `openspec_changes:` 父键和合法列表结构
- **AND** 若校验失败，系统 MUST 阻止非法 frontmatter 落盘或报告 blocker，不得静默继续。

#### Scenario: 顶层 Issue 状态不被 Change 状态污染
- **GIVEN** 一个 Issue trace 同时包含顶层 `status` 和 `openspec_changes[].status`
- **WHEN** Workflow Sync 解析或更新该 trace
- **THEN** 顶层 `status` MUST 只表达 Issue 主状态
- **AND** `openspec_changes[].status` MUST 只表达 Change 状态
- **AND** 系统 MUST NOT 将嵌套 Change 状态提升或覆盖为 Issue 主状态。

### Requirement: opsx linked Change 多入口自动回填
系统 MUST 在 `req.opsx` / `bug.opsx` 创建或确认 linked Change 后，幂等同步 Issue trace、主文档、registry 与 Sprint scope 中的 linked Change 信息，避免后续命令解析、当前态看板和人工入口出现漂移。同步后的 Issue trace frontmatter MUST 是标准 YAML parser 可解析的合法 YAML，并 MUST 保持顶层 Issue 状态与 `openspec_changes[].status` 语义隔离。

#### Scenario: REQ linked Change 回填完整
- **WHEN** Workflow Sync 处理 `req.opsx`
- **AND** 输入包含 `--req <REQ-id>` 与 `--change <change-id>`
- **THEN** 系统 MUST 确保目标 REQ `trace.md` 的 frontmatter 与 fenced yaml 中 `openspec_changes[]` 包含该 Change
- **AND** 系统 MUST 确保目标 REQ 的 `related_changes[]` 或等价索引包含该 Change
- **AND** 系统 MUST 确保 `requirement.md` 的人类入口字段引用该 Change
- **AND** 系统 MUST 确保 `issues/requirements/_registry.yaml` 对应条目的 `related_change` 引用该 Change。

#### Scenario: BUG linked Change 回填完整
- **WHEN** Workflow Sync 处理 `bug.opsx`
- **AND** 输入包含 `--bug <BUG-id>` 与 `--change <change-id>`
- **THEN** 系统 MUST 确保目标 BUG `trace.md` 的 frontmatter 与 fenced yaml 中 `openspec_changes[]` 包含该 Change
- **AND** 系统 MUST 确保目标 BUG 的 `related_change` 或等价索引引用该 Change
- **AND** 系统 MUST 确保 `bug.md` 的人类入口字段引用该 Change
- **AND** 系统 MUST 确保 `issues/bugs/_registry.yaml` 对应条目的 `related_change` 引用该 Change。

#### Scenario: Sprint scope 回填一致
- **WHEN** 目标 REQ 或 BUG 已正式纳入某个 `sprint-xxx`
- **AND** Workflow Sync 处理同一 Issue 的 `req.opsx` 或 `bug.opsx`
- **THEN** 系统 MUST 将 `<change-id>` 写入同一 Sprint 的 `sprint.yaml.changes[]`
- **AND** 系统 MUST 更新匹配的 `scope_estimates[].change`
- **AND** 系统 MUST 刷新 Sprint Scope 派生块
- **AND** `/opsx-apply --sprint auto --change <change-id>` 或等价 dry-run MUST 能解析到该 Sprint。

#### Scenario: linked Change 回填后的 frontmatter 合法
- **WHEN** Workflow Sync 处理 `req.opsx` 或 `bug.opsx` 并写入 linked Change
- **THEN** 目标 Issue `trace.md` frontmatter MUST 能被标准 YAML parser 解析
- **AND** `openspec_changes:` 父键 MUST 存在
- **AND** 重复运行 MUST NOT 产生缺父键缩进列表项或重复 linked Change 条目。
