## ADDED Requirements

### Requirement: opsx linked Change 多入口自动回填
系统 MUST 在 `req.opsx` / `bug.opsx` 创建或确认 linked Change 后，幂等同步 Issue trace、主文档、registry 与 Sprint scope 中的 linked Change 信息，避免后续命令解析、当前态看板和人工入口出现漂移。

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

#### Scenario: 未纳入 Sprint 时仍同步 Issue 入口
- **WHEN** Workflow Sync 处理 `req.opsx` 或 `bug.opsx`
- **AND** 目标 Issue 尚未出现在任何 active Sprint scope 中
- **THEN** 系统 MAY 跳过 Sprint scope 同步
- **AND** 系统 MUST 仍同步目标 Issue trace、主文档和 registry
- **AND** 输出摘要 MUST 说明 Sprint skipped 原因。

#### Scenario: 重复运行保持幂等
- **WHEN** 同一个 `req.opsx` 或 `bug.opsx` Workflow Sync 被重复运行
- **AND** 目标 Issue 已经引用同一个 `<change-id>`
- **THEN** 系统 MUST NOT 重复追加 `openspec_changes[]`
- **AND** 系统 MUST NOT 重复追加 `related_changes[]` 或重复改写相同 `related_change`
- **AND** 系统 MUST 将无变化文件计入 skipped 或 no-delta 摘要。

#### Scenario: 多候选 Change 阻断自动猜测
- **WHEN** 一个 REQ 或 BUG 存在多个可作为当前主 linked Change 的 active 候选
- **THEN** 系统 MUST 报告候选 Change 列表
- **AND** 系统 MUST 要求用户或调用方明确选择
- **AND** 系统 MUST NOT 静默覆盖 `related_change` 为猜测值。

#### Scenario: linked Change 漂移检查
- **WHEN** 用户执行 focused Workflow Sync dry-run、Issue drift check 或 Sprint scope 校验
- **AND** trace、主文档、registry 或 Sprint scope 中 linked Change 不一致
- **THEN** 系统 MUST 报告 Issue ID、Change ID、文件路径、字段来源、当前值、期望值和建议修复命令
- **AND** 对阻断后续 `/opsx-apply` 的漂移 MUST 标记为 blocker。
