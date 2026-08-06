## MODIFIED Requirements

### Requirement: Sprint close stale scan 门禁
系统 SHALL 在 Sprint close 或 `/sprint-archive` 归档判断前检查目标 Sprint 四件套和正式范围关联 Issue 子文档中的过期中间态文案和旧归档路径残留，防止 Sprint 完成结论与真实 Issue、Change 生命周期状态不一致。该门禁 SHALL 保留对真实流程中间态的阻断，同时避免把普通业务正文中的 `pending` 等业务词误判为流程状态。

#### Scenario: 四件套存在过期中间态文案时阻断关闭
- **WHEN** 系统检查目标 Sprint 的 `sprint.md`、`release-note.md`、`acceptance-report.md` 或 `sprint.yaml`
- **AND** 文档中存在与真实状态冲突的“待 `/req-opsx`”、“待 `/bug-opsx`”、“待 `/opsx-apply`”、`proposed`、`applied` 或等价中间态文案
- **AND** 对应 Issue 或 Change 已进入更后续的生命周期状态
- **THEN** 系统 MUST 将该命中标记为 blocker
- **AND** `/sprint-archive` 或 Sprint close 命令 MUST 返回非零退出码
- **AND** 报告 MUST 列出文件路径、命中片段、关联 Issue 或 Change、真实状态和建议修复动作

#### Scenario: Issue 子文档普通业务词不阻断关闭
- **WHEN** 系统检查目标 Sprint 正式范围关联的已闭环 Issue 子文档
- **AND** 普通正文中出现“SKU pending 图片正式化”或等价业务词
- **AND** 该内容不表达当前 Issue、验收、Change 或 Sprint 的流程中间态
- **THEN** 系统 MUST NOT 因该业务词阻断 Sprint close

#### Scenario: Issue 子文档状态字段仍阻断关闭
- **WHEN** 系统检查目标 Sprint 正式范围关联的已闭环 Issue 子文档
- **AND** frontmatter、fenced yaml、状态表格或验收结果字段残留 `status: pending_review`、`acceptance_status: pending`、`proposed`、`applied`、`in_sprint` 或等价流程中间态
- **THEN** 系统 MUST 将该命中标记为 blocker
- **AND** 报告 MUST 提供 Workflow Sync/reconcile 或人工修正建议

#### Scenario: 四件套引用旧归档路径时阻断关闭
- **WHEN** 系统检查目标 Sprint 四件套
- **AND** `sprint.md`、`release-note.md`、`acceptance-report.md` 或 `sprint.yaml` 将 `openspec/changes/archive/` 作为归档事实路径或新生成引用
- **THEN** 系统 MUST 将该命中标记为 blocker
- **AND** 报告 MUST 提示使用 `openspec/archive/YYYY-MM-DD-<change-id>/`

#### Scenario: 无 stale 命中时允许继续关闭
- **WHEN** 目标 Sprint 四件套和关联 Issue 子文档不存在 blocker 级 stale 文案或旧归档路径残留
- **AND** 既有 readiness gate、Change archive、tasks 完成和 Workflow Sync 门禁均通过
- **THEN** 系统 MUST 允许 Sprint close 或 `/sprint-archive` 继续执行
