## ADDED Requirements

### Requirement: Sprint Fact Sheet 自动生成
系统 MUST 提供命令式能力，为指定 Sprint 生成自动 Fact Sheet，汇总 Sprint 四件套、Issue、OpenSpec Change、tasks 与验收关键事实。

#### Scenario: 为已归档 Sprint 生成 Fact Sheet
- **WHEN** 用户或 `/sprint-exps` 为存在 `sprint.yaml` 的 `sprint-xxx` 请求生成 Fact Sheet
- **THEN** 系统 MUST 输出包含 Sprint 基础信息、REQ/BUG/Change 范围、Change tasks 完成度、Issue 状态、验收摘要与 token 风险提示的 Fact Sheet

#### Scenario: Sprint 不存在
- **WHEN** 用户请求生成不存在或缺少 `sprint.yaml` 的 Sprint Fact Sheet
- **THEN** 系统 MUST 返回非零退出码并说明缺失的 Sprint 标识或路径

### Requirement: Fact Sheet 可追溯到原始证据
系统 MUST 在 Fact Sheet 中保留证据路径或回读提示，使复盘结论可以追溯到 Sprint、Issue、Change 或验收文件。

#### Scenario: 存在状态不一致或缺失项
- **WHEN** Fact Sheet 发现 Change 缺少 `trace.md`、tasks 未完成、Issue 子文档状态残留或 acceptance report 结论不清晰
- **THEN** 系统 MUST 在 Fact Sheet 中标记风险，并给出建议回读的具体文件路径或关键词

#### Scenario: 无需全文回读
- **WHEN** Fact Sheet 已能提供某项复盘所需的机器事实
- **THEN** `/sprint-exps` MUST 优先使用 Fact Sheet 中的摘要，不得默认全文读取对应四件套、trace 或 tasks 文件

### Requirement: `/sprint-exps` 优先使用 Fact Sheet
`/sprint-exps` MUST 将自动 Fact Sheet 作为复盘的优先输入，并仅在证据不足、风险项存在或用户要求时读取原始文件片段。

#### Scenario: 正常复盘路径
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **THEN** 命令流程 MUST 先运行或读取该 Sprint 的 Fact Sheet，再基于 Fact Sheet 生成 Sprint 复盘与模型 Token 使用分析

#### Scenario: Fact Sheet 标记需要细节
- **WHEN** Fact Sheet 标记 `needs_detail`、warning、missing 或 inconsistent 类风险
- **THEN** `/sprint-exps` MAY 按 Fact Sheet 的 evidence hints 读取对应原始文件片段

### Requirement: Fact Sheet 输出边界受上下文预算约束
Fact Sheet 生成与 `/sprint-exps` 消费流程 MUST 遵守 Agent 上下文预算规则，避免宽泛搜索、长日志、生成物全文 diff 和历史归档全量展开。

#### Scenario: 大 Sprint 包含多个 Change
- **WHEN** Sprint 包含多个 REQ、BUG、Change 或大量 tasks
- **THEN** Fact Sheet MUST 输出聚合计数和精确证据路径，而不是复制原始 trace、tasks、acceptance report 或 generated 文件全文

#### Scenario: 需要读取 archive 目录
- **WHEN** Fact Sheet 需要读取 Sprint 内已归档 Change
- **THEN** 系统 MUST 从 `sprint.yaml` 的 Change 列表构造精确路径，不得通过宽泛搜索默认扫描整个 `openspec/changes/archive/**`

### Requirement: Fact Sheet 支持机器可读输出
系统 MUST 支持 Markdown 与 JSON 两种 Fact Sheet 输出，Markdown 用于人工和模型阅读，JSON 用于脚本验证和后续自动化复用。

#### Scenario: 请求 JSON 输出
- **WHEN** 用户或测试命令请求 JSON 格式 Fact Sheet
- **THEN** 系统 MUST 输出包含 Sprint、scope、changes、issues、warnings、token_risks 与 evidence_hints 的机器可读结构
