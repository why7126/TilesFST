## ADDED Requirements

### Requirement: Archived Change trace 兜底摘要门禁
系统 MUST 在 Sprint 或 OpenSpec 归档 readiness gate 中检查 archived Change 的归档验证证据；当 archived Change 缺失 `trace.md` 时，系统 MUST 要求 `proposal.md`、`design.md` 或 `tasks.md` 中至少一个文件包含标准化归档验证摘要。

#### Scenario: archived Change 存在 trace
- **WHEN** readiness gate 检查一个 archived Change
- **AND** 该 Change 目录包含 `trace.md`
- **THEN** 系统 MUST 将该 Change 的 trace 状态记录为存在
- **AND** 系统 MUST 不因 fallback summary 缺失而阻断该 Change

#### Scenario: archived Change 缺失 trace 但存在兜底摘要
- **WHEN** readiness gate 检查一个 archived Change
- **AND** 该 Change 目录缺失 `trace.md`
- **AND** `proposal.md`、`design.md` 或 `tasks.md` 中存在标准化归档验证摘要
- **THEN** 系统 MUST 将该 Change 标记为 fallback summary pass
- **AND** readiness 报告 MUST 展示承载摘要的文件路径

#### Scenario: archived Change 缺失 trace 且无兜底摘要
- **WHEN** readiness gate 检查一个 archived Change
- **AND** 该 Change 目录缺失 `trace.md`
- **AND** `proposal.md`、`design.md`、`tasks.md` 均不存在标准化归档验证摘要
- **THEN** 系统 MUST 输出 blocker
- **AND** 系统 MUST 返回非零退出码
- **AND** blocker MUST 包含 Change id、归档路径、检查过的候选文件和缺失的摘要项

#### Scenario: active Change 与 archived Change 语义区分
- **WHEN** readiness gate 同时检查 active Change 与 archived Change
- **THEN** 系统 MUST 在报告中清晰区分 active Change 状态检查与 archived Change 归档证据检查
- **AND** 系统 MUST 仅对 archived Change 强制执行 trace 缺失后的 fallback summary 门禁

#### Scenario: 兜底摘要内容完整性
- **WHEN** archived Change 缺失 `trace.md`
- **AND** 某个候选文件包含标准化归档验证摘要章节
- **THEN** 摘要 MUST 至少覆盖验证命令与结果、验收结论、关联 Issue 或 Sprint 状态、归档路径或归档时间
