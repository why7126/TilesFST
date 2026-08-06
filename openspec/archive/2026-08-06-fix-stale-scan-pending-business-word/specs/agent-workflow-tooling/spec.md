## MODIFIED Requirements

### Requirement: Sprint close 中间态文案扫描
系统 MUST 在 Sprint close、`/sprint-archive` 或等价收尾流程中扫描相关 Issue 包与 Sprint 四件套的中间态残留，防止 completed/archive 状态下仍保留未解释的流程中间态、active Change 路径或等价旧文案。扫描 MUST 区分结构化状态上下文、流程待办说明与普通业务正文；普通业务正文中的业务词 `pending` 不得仅凭独立单词出现就被判定为中间态残留。

#### Scenario: Sprint close 发现中间态文案
- **WHEN** Sprint close 或 `/sprint-archive` 检查关联 Issue 包、`sprint.md`、`acceptance-report.md`、`release-note.md` 或其他 Sprint 四件套
- **AND** 文档仍包含未解释的结构化中间态字段、流程待办语义、active Change 路径或 legacy archive 路径
- **THEN** 系统 MUST 将该命中标记为 blocker
- **AND** 报告 MUST 包含文件路径、行号、命中片段、关联 Issue 或 Change、真实状态和建议修复动作

#### Scenario: 普通业务正文中的 pending 不阻断
- **WHEN** 一个已闭环 Issue 子文档的普通正文包含“SKU pending 图片正式化已完成”或等价业务描述
- **AND** 该行不属于 frontmatter、fenced yaml、状态表格、验收状态字段或流程待办说明
- **THEN** stale scan MUST NOT 仅因该 `pending` 命中产生 `issue-subdocument-stale-state` blocker

#### Scenario: 结构化 pending 状态继续阻断
- **WHEN** 一个已闭环 Issue 子文档的 frontmatter、fenced yaml、状态表格或验收结果字段包含 `status: pending_review`、`acceptance_status: pending` 或等价未闭环状态
- **THEN** stale scan MUST 继续产生 blocker
- **AND** 报告 MUST 建议运行 Workflow Sync/reconcile 或人工修正语义不明的状态字段

#### Scenario: Sprint close stale scan 范围受控
- **WHEN** 系统执行 Sprint close 中间态文案扫描
- **THEN** 系统 MUST 只扫描目标 Sprint 四件套和该 Sprint scope 关联的 Issue 子文档
- **AND** 系统 MUST NOT 默认扫描全部 `iterations/**`、`openspec/archive/**` 或历史归档目录
