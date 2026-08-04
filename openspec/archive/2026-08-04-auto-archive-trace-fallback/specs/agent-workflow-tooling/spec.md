## ADDED Requirements

### Requirement: 归档 Change 缺失 trace 的最小证据补齐
系统 MUST 在校验已归档 OpenSpec Change 的归档证据时处理缺失 `trace.md` 的历史归档目录：当归档目录可写且可从归档路径、`tasks.md`、delta spec、proposal/design 或关联 Issue trace 推断出最小事实时，系统 MUST 自动生成最小归档 `trace.md`；当无法安全写入但可形成完整机器可读事实时，系统 MUST 输出结构化 fallback 摘要；当两者都不可用时，系统 MUST 返回非零退出码并报告 blocker。

#### Scenario: 可写归档目录自动生成最小 trace
- **WHEN** 归档证据校验扫描到 `openspec/archive/YYYY-MM-DD-<change-id>/` 下缺少 `trace.md`
- **AND** 归档目录可写
- **AND** 系统可从归档目录名、`tasks.md`、delta spec 或关联 Issue trace 推断最小归档事实
- **THEN** 系统 MUST 写入最小 `trace.md`
- **AND** `trace.md` MUST 记录 `change_id`、`status: archived`、归档路径、归档时间或时间来源、任务完成摘要、证据来源和自动生成标记
- **AND** 校验报告 MUST 将该结果标记为 `auto-generated-minimal-trace`

#### Scenario: 不可写目录输出结构化 fallback 摘要
- **WHEN** 归档证据校验扫描到已归档 Change 缺少 `trace.md`
- **AND** 系统无法安全写入归档目录
- **AND** 系统仍可形成完整归档证据事实
- **THEN** 系统 MUST 输出结构化 fallback 摘要
- **AND** 摘要 MUST 包含 `change_id`、`archive_path`、`evidence_status`、`archive_timestamp`、`timestamp_source`、`tasks_done`、`tasks_total`、`spec_delta_paths`、`warnings` 和 `recommended_action`
- **AND** 调用方 MUST 能用该摘要判断归档证据闭环，不得只依赖自由文本说明

#### Scenario: 证据不足时保持阻断
- **WHEN** 已归档 Change 缺少 `trace.md`
- **AND** 系统无法生成最小 trace
- **AND** 系统无法形成完整结构化 fallback 摘要
- **THEN** 归档证据校验 MUST 返回非零退出码
- **AND** 报告 MUST 列出缺失字段、已检查路径和建议人工补齐动作

#### Scenario: 不放宽既有归档门禁
- **WHEN** 已归档 Change 存在未完成 tasks、缺失 `tasks.md`、legacy archive path 真实残留或关联 Issue 未闭环
- **THEN** 系统 MUST 保持既有 blocker 语义
- **AND** 自动生成最小 trace 或结构化 fallback 摘要 MUST NOT 将这些 blocker 误判为通过
