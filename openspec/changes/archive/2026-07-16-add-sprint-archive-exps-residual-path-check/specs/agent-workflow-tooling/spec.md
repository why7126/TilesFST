## ADDED Requirements

### Requirement: Sprint 归档后旧路径残留检查
系统 MUST 在 `/sprint-archive` 完成 Sprint 目录迁移、Workflow Sync 与关联 Issue promote 后，检查本 Sprint 关联文档中是否残留已迁移前的旧路径引用，防止归档后文档继续指向 `iterations/change/` 或 active Change 目录。

#### Scenario: Sprint 归档后无旧路径残留
- **WHEN** `/sprint-archive sprint-xxx` 已将 Sprint 目录迁移到 `iterations/archive/sprint-xxx/`
- **AND** Sprint 关联文档不包含 `iterations/change/sprint-xxx/` 或已归档 Change 的 active 路径引用
- **THEN** 系统 MUST 在最终报告中展示路径残留检查通过
- **AND** 报告 MUST 包含检查文件数与命中数摘要

#### Scenario: Sprint 归档后仍残留 change 路径
- **WHEN** `/sprint-archive sprint-xxx` 完成目录迁移后执行路径残留检查
- **AND** 任一关联 Markdown 文档仍包含 `iterations/change/sprint-xxx/`
- **THEN** 系统 MUST 将该残留报告为 blocker 或 warning
- **AND** 报告 MUST 包含文件路径、行号、旧路径与建议的新路径 `iterations/archive/sprint-xxx/`
- **AND** `/sprint-archive` MUST 不得静默输出成功闭环结论

#### Scenario: Sprint 归档后仍残留 active Change 路径
- **WHEN** Sprint 范围内的 Change 已归档到 `openspec/changes/archive/<date>-<change-id>/`
- **AND** 任一关联 Markdown 文档仍包含 `openspec/changes/<change-id>/`
- **THEN** 系统 MUST 报告该 Change 路径残留
- **AND** 报告 MUST 包含对应归档路径或说明无法解析归档路径

#### Scenario: 检查范围受 Sprint scope 限制
- **WHEN** 系统执行 Sprint 归档后旧路径残留检查
- **THEN** 系统 MUST 以 `sprint.yaml` 的 `requirements[]`、`bugs[]` 与 `changes[]` 定位检查范围
- **AND** 系统 MUST NOT 默认扫描整个 `openspec/changes/archive/**`、`issues/**` 或生成物目录

### Requirement: Sprint 复盘旧路径残留提示
系统 MUST 在 `/sprint-exps` 为已归档 Sprint 生成复盘前检查旧路径残留，并将残留作为复盘风险或 evidence hint 暴露，避免复盘文档继续传播过期链接。

#### Scenario: 复盘前发现旧路径残留
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **AND** `sprint-xxx` 已位于 `iterations/archive/sprint-xxx/`
- **AND** 路径残留检查发现 `iterations/change/sprint-xxx/` 或 active Change 路径引用
- **THEN** Experience Analysis Report MUST 展示 residual path warning
- **AND** 复盘文档 MUST NOT 将旧路径作为新的证据链接写入
- **AND** 报告 MUST 给出残留文件路径与建议修正路径

#### Scenario: 复盘前未发现旧路径残留
- **WHEN** `/sprint-exps` 的路径残留检查未发现命中
- **THEN** Experience Analysis Report SHOULD 展示检查通过摘要
- **AND** 复盘可继续使用 Fact Sheet 中的归档路径作为证据来源

#### Scenario: Fact Sheet 暴露路径残留证据
- **WHEN** Fact Sheet 或复盘辅助脚本发现旧路径残留
- **THEN** 机器可读输出 MUST 包含 warning 或 evidence hint
- **AND** warning MUST 至少包含残留类型、文件路径、旧路径与建议新路径
