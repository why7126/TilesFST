## MODIFIED Requirements

### Requirement: Issue 归档子文档状态一致性门禁
系统 MUST 在 REQ / BUG 迁入 `issues/**/archive/` 前检查 issue 包内维护状态字段的 Markdown 子文档，防止 archive 包残留非闭环状态。系统 MUST 在发现残留状态时输出明确修复命令，并 MUST 提供安全的 reconcile 能力，在 Issue 主状态与关联交付对象已闭环时自动同步子文档残留状态。单个 Issue 的归档与子文档 reconcile MUST 以该 Issue 自身闭环为准，不得仅因所属 Sprint 尚未 completed 而阻断；Sprint completed 仅作为 `/sprint-archive` 整体归档门禁。

#### Scenario: BUG 子文档残留状态阻断归档
- **GIVEN** 一个 BUG 已满足关联 Change archived 与 `trace.md` done 条件
- **AND** `bug.md`、`root-cause.md`、`acceptance.md`、`workaround.md` 或其他维护状态字段的子文档仍包含 `draft`、`pending_review`、`in_sprint`、`applied`、`todo`、`open` 或等价非闭环状态
- **WHEN** 系统执行 issue archive promote
- **THEN** 系统 MUST 阻断该 BUG 迁入 `issues/bugs/archive/`
- **AND** 报告 MUST 列出 issue id、文件路径、状态来源、当前状态
- **AND** 报告 MUST 包含可直接执行的 dry-run reconcile 命令与实际写入命令

#### Scenario: REQ 子文档残留状态阻断归档
- **GIVEN** 一个 REQ 已满足关联 Change archived 与 `trace.md` done 条件
- **AND** `requirement.md`、`acceptance.md`、`user-stories.md`、`business-flow.md`、`capture.md` 或其他维护状态字段的子文档仍包含非闭环状态
- **WHEN** 系统执行 issue archive promote
- **THEN** 系统 MUST 阻断该 REQ 迁入 `issues/requirements/archive/`
- **AND** 报告 MUST 列出所有残留状态字段
- **AND** 报告 MUST 包含可直接执行的 dry-run reconcile 命令与实际写入命令

#### Scenario: 子文档状态全部闭环后允许归档
- **GIVEN** 一个 REQ 或 BUG 已满足 archive promote 的主状态条件
- **AND** issue 包内所有维护状态字段均为 `done`、`archived`、`resolved`、`closed` 或等价闭环状态
- **WHEN** 系统执行 issue archive promote
- **THEN** 系统 MAY 将该 issue 从 `review/` 迁入 `archive/`

#### Scenario: Reconcile 建议区分自动修复与上游阻断
- **WHEN** issue archive promote 因子文档状态残留被阻断
- **THEN** 报告 MUST 提示先 dry-run 再 apply reconcile
- **AND** 建议 MUST 区分“可自动 reconcile”的闭环 Issue 与“必须先推进上游流程”的未闭环 Issue

#### Scenario: Dry-run 预览子文档状态 reconcile
- **GIVEN** 一个 REQ 或 BUG 的主状态与关联 Change 已闭环
- **AND** 所属 Sprint 尚未 completed
- **WHEN** 用户执行子文档状态 reconcile dry-run 命令
- **THEN** 系统 MUST 报告将被更新的文件、字段来源、旧状态与目标状态
- **AND** 系统 MUST NOT 写入文件
- **AND** 系统 MUST NOT 仅因所属 Sprint 尚未 completed 阻断 dry-run

#### Scenario: 写入子文档状态 reconcile
- **GIVEN** 一个 REQ 或 BUG 的主状态与关联 Change 已闭环
- **AND** 所属 Sprint 尚未 completed
- **WHEN** 用户执行子文档状态 reconcile 写入命令
- **THEN** 系统 MUST 将子文档残留状态更新为该 issue 的闭环目标状态
- **AND** 系统 MUST 刷新被修改 Markdown 的 `updated_at`
- **AND** 系统 MUST NOT 仅因所属 Sprint 尚未 completed 阻断写入

#### Scenario: 未闭环 Issue 禁止 reconcile 写入
- **GIVEN** 一个 REQ 或 BUG 的主状态或关联 Change 尚未闭环
- **WHEN** 用户执行子文档状态 reconcile 写入命令
- **THEN** 系统 MUST 阻断写入
- **AND** 报告 MUST 指出需要先完成的上游命令或状态
