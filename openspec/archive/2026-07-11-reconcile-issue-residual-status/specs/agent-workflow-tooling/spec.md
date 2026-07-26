## MODIFIED Requirements

### Requirement: Issue 归档子文档状态一致性门禁
系统 MUST 在 REQ / BUG 迁入 `issues/**/archive/` 前检查 issue 包内维护状态字段的 Markdown 子文档，防止 archive 包残留非闭环状态。系统 MUST 在发现残留状态时输出明确修复命令，并 MUST 提供安全的 reconcile 能力，在 Issue 主状态与关联交付对象已闭环时自动同步子文档残留状态。

#### Scenario: BUG 子文档存在非闭环状态
- **GIVEN** 一个 BUG 已满足关联 Change archived 与 `trace.md` done 条件
- **AND** 该 BUG 包内任一 Markdown 子文档的 frontmatter 或 fenced YAML block 包含 `status: draft`、`status: pending_review`、`status: in_sprint`、`status: applied`、`status: todo` 或 `status: open`
- **WHEN** 系统执行 issue archive promote
- **THEN** 系统 MUST 阻断该 BUG 迁入 `issues/bugs/archive/`
- **AND** 报告 MUST 包含 BUG id、文件路径、状态来源与状态值
- **AND** 报告 MUST 包含可直接执行的 dry-run reconcile 命令与实际写入命令

#### Scenario: REQ 子文档存在非闭环状态
- **GIVEN** 一个 REQ 已满足关联 Change archived 与 `trace.md` done 条件
- **AND** 该 REQ 包内任一 Markdown 子文档的 frontmatter 或 fenced YAML block 包含非闭环状态
- **WHEN** 系统执行 issue archive promote
- **THEN** 系统 MUST 阻断该 REQ 迁入 `issues/requirements/archive/`
- **AND** 报告 MUST 包含 REQ id、文件路径、状态来源与状态值
- **AND** 报告 MUST 包含可直接执行的 dry-run reconcile 命令与实际写入命令

#### Scenario: 子文档状态均已闭环
- **GIVEN** 一个 REQ 或 BUG 已满足 archive promote 的主状态条件
- **AND** issue 包内 Markdown 子文档不存在非闭环状态残留
- **WHEN** 系统执行 issue archive promote
- **THEN** 系统 MAY 将该 issue 从 `review/` 迁入 `archive/`

#### Scenario: 输出可操作修正建议
- **WHEN** issue archive promote 因子文档状态残留被阻断
- **THEN** 系统 MUST 输出建议，提示先完成评审/验收或将真实已闭环子文档状态同步为闭环状态
- **AND** 建议 MUST 区分“可自动 reconcile”的闭环 Issue 与“必须先推进上游流程”的未闭环 Issue

#### Scenario: Dry-run 预览子文档状态 reconcile
- **GIVEN** 一个 REQ 或 BUG 的主状态、关联 Change 与必要 Sprint 状态已闭环
- **AND** issue 包内 Markdown 子文档存在非闭环状态残留
- **WHEN** 用户执行子文档状态 reconcile dry-run 命令
- **THEN** 系统 MUST 不写入文件
- **AND** 报告 MUST 列出 issue id、文件路径、状态来源、旧状态、目标状态与将刷新的 `updated_at`

#### Scenario: 写入子文档状态 reconcile
- **GIVEN** 一个 REQ 或 BUG 的主状态、关联 Change 与必要 Sprint 状态已闭环
- **AND** dry-run 报告确认存在可修复的子文档状态残留
- **WHEN** 用户执行子文档状态 reconcile 写入命令
- **THEN** 系统 MUST 将对应 Markdown 子文档 frontmatter 与 fenced YAML block 中的残留状态同步为闭环状态
- **AND** 系统 MUST 刷新被修改 Markdown 的 `updated_at`
- **AND** 系统 MUST 输出修改摘要，包含修改文件数、字段数、issue id、旧状态与新状态

#### Scenario: 未闭环 Issue 禁止 reconcile 写入
- **GIVEN** 一个 REQ 或 BUG 的主状态、关联 Change 或必要 Sprint 状态尚未闭环
- **WHEN** 用户执行子文档状态 reconcile 写入命令
- **THEN** 系统 MUST 拒绝写入并返回非零退出码
- **AND** 报告 MUST 说明阻断原因与应先执行的上游工作流命令
