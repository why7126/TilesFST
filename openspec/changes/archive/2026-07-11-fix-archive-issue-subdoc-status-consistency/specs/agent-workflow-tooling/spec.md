## ADDED Requirements

### Requirement: Issue 归档子文档状态一致性门禁
系统 MUST 在 REQ / BUG 迁入 `issues/**/archive/` 前检查 issue 包内维护状态字段的 Markdown 子文档，防止 archive 包残留非闭环状态。

#### Scenario: BUG 子文档存在非闭环状态
- **GIVEN** 一个 BUG 已满足关联 Change archived 与 `trace.md` done 条件
- **AND** 该 BUG 包内任一 Markdown 子文档的 frontmatter 或 fenced YAML block 包含 `status: draft`、`status: pending_review`、`status: in_sprint`、`status: applied`、`status: todo` 或 `status: open`
- **WHEN** 系统执行 issue archive promote
- **THEN** 系统 MUST 阻断该 BUG 迁入 `issues/bugs/archive/`
- **AND** 报告 MUST 包含 BUG id、文件路径、状态来源与状态值

#### Scenario: REQ 子文档存在非闭环状态
- **GIVEN** 一个 REQ 已满足关联 Change archived 与 `trace.md` done 条件
- **AND** 该 REQ 包内任一 Markdown 子文档的 frontmatter 或 fenced YAML block 包含非闭环状态
- **WHEN** 系统执行 issue archive promote
- **THEN** 系统 MUST 阻断该 REQ 迁入 `issues/requirements/archive/`
- **AND** 报告 MUST 包含 REQ id、文件路径、状态来源与状态值

#### Scenario: 子文档状态均已闭环
- **GIVEN** 一个 REQ 或 BUG 已满足 archive promote 的主状态条件
- **AND** issue 包内 Markdown 子文档不存在非闭环状态残留
- **WHEN** 系统执行 issue archive promote
- **THEN** 系统 MAY 将该 issue 从 `review/` 迁入 `archive/`

#### Scenario: 输出可操作修正建议
- **WHEN** issue archive promote 因子文档状态残留被阻断
- **THEN** 系统 MUST 输出建议，提示先完成评审/验收或将真实已闭环子文档状态同步为闭环状态
