## ADDED Requirements

### Requirement: Sprint close stale scan 门禁
系统 SHALL 在 Sprint close 或 `/sprint-archive` 归档判断前检查目标 Sprint 四件套中的过期中间态文案和旧归档路径残留，防止 Sprint 完成结论与真实 Issue、Change 生命周期状态不一致。

#### Scenario: 四件套存在过期中间态文案时阻断关闭
- **WHEN** 系统检查目标 Sprint 的 `sprint.md`、`release-note.md`、`acceptance-report.md` 或 `sprint.yaml`
- **AND** 文档中存在与真实状态冲突的“待 `/req-opsx`”、“待 `/bug-opsx`”、“待 `/opsx-apply`”、`proposed`、`applied` 或等价中间态文案
- **AND** 对应 Issue 或 Change 已进入更后续的生命周期状态
- **THEN** 系统 MUST 将该命中标记为 blocker
- **AND** `/sprint-archive` 或 Sprint close 命令 MUST 返回非零退出码
- **AND** 报告 MUST 列出文件路径、命中片段、关联 Issue 或 Change、真实状态和建议修复动作

#### Scenario: 四件套引用旧归档路径时阻断关闭
- **WHEN** 系统检查目标 Sprint 四件套
- **AND** `sprint.md`、`release-note.md`、`acceptance-report.md` 或 `sprint.yaml` 将 `openspec/changes/archive/` 作为归档事实路径或新生成引用
- **THEN** 系统 MUST 将该命中标记为 blocker
- **AND** 报告 MUST 提示使用 `openspec/archive/YYYY-MM-DD-<change-id>/`

#### Scenario: 无 stale 命中时允许继续关闭
- **WHEN** 目标 Sprint 四件套不存在 blocker 级 stale 文案或旧归档路径残留
- **AND** 既有 readiness gate、Change archive、tasks 完成和 Workflow Sync 门禁均通过
- **THEN** 系统 MUST 允许 Sprint close 或 `/sprint-archive` 继续执行

#### Scenario: 允许历史追溯与兼容例外
- **WHEN** stale scan 遇到测试 fixture、迁移脚本、兼容 fallback 说明或明确标注为历史追溯的 legacy 字符串
- **THEN** 系统 MUST NOT 将该命中作为 Sprint close blocker
- **AND** 报告 SHOULD 将该命中归类为 `allowed_legacy` 或等价非阻断级别
