## ADDED Requirements

### Requirement: OpenSpec Change 归档根目录独立化
系统 MUST 使用 `openspec/archive/` 作为已完成 OpenSpec Change 的 canonical archive root，并 MUST 将 `openspec/changes/` 保留为 active Change 根目录。新增归档、Workflow Sync 输出、release 事实源、Fact Sheet、AI usage、readiness 报告和技能文档 MUST 使用 canonical archive root；legacy `openspec/changes/archive/` 仅可作为迁移期只读兼容路径。

#### Scenario: 新增 Change 归档写入 canonical archive
- **WHEN** 用户执行 `/opsx-archive <change-id>`、`/sprint-archive <sprint-id>` 或等价 OpenSpec archive 流程
- **THEN** 系统 MUST 将归档 Change 写入 `openspec/archive/<date>-<change-id>/`
- **AND** 系统 MUST NOT 将新增归档 Change 写入 `openspec/changes/archive/<date>-<change-id>/`

#### Scenario: 迁移期读取 legacy archive
- **WHEN** 工具需要读取已归档 Change
- **AND** `openspec/archive/<date>-<change-id>/` 中未找到目标 Change
- **THEN** 系统 MAY 读取 legacy `openspec/changes/archive/<date>-<change-id>/`
- **AND** 报告 MUST 标明该路径是 legacy archive 兼容命中

#### Scenario: archive root 配置一致
- **WHEN** 系统读取 OpenSpec 配置、规则文档、命令技能或路径 helper
- **THEN** canonical archive root MUST 一致指向 `openspec/archive/`
- **AND** 任何 `openspec/changes/archive/` 引用 MUST 明确标注为 legacy 兼容、迁移来源或残留检查目标

#### Scenario: legacy archive 目录不得承载新事实源
- **WHEN** 归档流程完成后执行残留检查
- **THEN** `openspec/changes/archive/` MUST NOT 包含新的 Change 包目录
- **AND** 如发现新增或未迁移 Change 包，系统 MUST 报告 blocker 并给出迁移目标 `openspec/archive/<date>-<change-id>/`

## MODIFIED Requirements

### Requirement: Sprint 归档后旧路径残留检查
系统 MUST 在 `/sprint-archive` 完成 Sprint 目录迁移、Workflow Sync 与关联 Issue promote 后，检查本 Sprint 关联文档中是否残留已迁移前的旧路径引用，防止归档后文档继续指向 `iterations/change/`、active Change 目录或 legacy Change archive 目录。

#### Scenario: Sprint 归档后无旧路径残留
- **WHEN** `/sprint-archive sprint-xxx` 已将 Sprint 目录迁移到 `iterations/archive/sprint-xxx/`
- **AND** Sprint 关联文档不包含 `iterations/change/sprint-xxx/`、已归档 Change 的 active 路径引用或 legacy `openspec/changes/archive/` 路径引用
- **THEN** 系统 MUST 在最终报告中展示路径残留检查通过
- **AND** 报告 MUST 包含检查文件数与命中数摘要

#### Scenario: Sprint 归档后仍残留 change 路径
- **WHEN** `/sprint-archive sprint-xxx` 完成目录迁移后执行路径残留检查
- **AND** 任一关联 Markdown 文档仍包含 `iterations/change/sprint-xxx/`
- **THEN** 系统 MUST 将该残留报告为 blocker 或 warning
- **AND** 报告 MUST 包含文件路径、行号、旧路径与建议的新路径 `iterations/archive/sprint-xxx/`
- **AND** `/sprint-archive` MUST 不得静默输出成功闭环结论

#### Scenario: Sprint 归档后仍残留 active Change 路径
- **WHEN** Sprint 范围内的 Change 已归档到 `openspec/archive/<date>-<change-id>/`
- **AND** 任一关联 Markdown 文档仍包含 `openspec/changes/<change-id>/`
- **THEN** 系统 MUST 报告该 Change 路径残留
- **AND** 报告 MUST 包含对应归档路径或说明无法解析归档路径

#### Scenario: Sprint 归档后仍残留 legacy Change archive 路径
- **WHEN** Sprint 范围内的 Change 已归档到 `openspec/archive/<date>-<change-id>/`
- **AND** 任一关联 Markdown 文档仍包含 `openspec/changes/archive/<date>-<change-id>/`
- **THEN** 系统 MUST 报告该 legacy archive 路径残留
- **AND** 报告 MUST 给出建议的新路径 `openspec/archive/<date>-<change-id>/`

#### Scenario: 检查范围受 Sprint scope 限制
- **WHEN** 系统执行 Sprint 归档后旧路径残留检查
- **THEN** 系统 MUST 以 `sprint.yaml` 的 `requirements[]`、`bugs[]` 与 `changes[]` 定位检查范围
- **AND** 系统 MUST NOT 默认扫描整个 `openspec/archive/**`、legacy `openspec/changes/archive/**`、`issues/**` 或生成物目录
