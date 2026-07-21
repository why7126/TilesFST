## MODIFIED Requirements

### Requirement: Fact Sheet 可追溯到原始证据
系统 MUST 在 Fact Sheet 中保留证据路径或回读提示，使复盘结论可以追溯到 Sprint、Issue、Change 或验收文件；复盘默认路径 MUST 将完整 evidence hints 作为按需回读索引，而不是默认完整输出内容。

#### Scenario: 存在状态不一致或缺失项
- **WHEN** Fact Sheet 发现 Change 缺少 `trace.md`、tasks 未完成、Issue 子文档状态残留或 acceptance report 结论不清晰
- **THEN** 系统 MUST 在 Fact Sheet 中标记风险，并给出建议回读的具体文件路径或关键词

#### Scenario: 无需全文回读
- **WHEN** Fact Sheet 已能提供某项复盘所需的机器事实
- **THEN** `/sprint-exps` MUST 优先使用 Fact Sheet 中的摘要，不得默认全文读取对应四件套、trace 或 tasks 文件
- **AND** `/sprint-exps` MUST NOT 默认输出完整 `evidence_hints`

#### Scenario: 显式请求证据提示
- **WHEN** 用户显式要求证据提示、或 `/sprint-exps` 因 `needs_detail`、warning、missing、inconsistent 类风险需要定位原始证据
- **THEN** 系统 MUST 支持按需输出或读取完整 `evidence_hints`
- **AND** 输出 MUST 保留具体 reason 与相对路径

### Requirement: `/sprint-exps` 优先使用 Fact Sheet
`/sprint-exps` MUST 将自动 Fact Sheet 作为复盘的优先输入，并仅在证据不足、风险项存在或用户要求时读取原始文件片段；默认输入 SHOULD 使用紧凑 summary 模式以降低上下文占用。

#### Scenario: 正常复盘路径
- **WHEN** 用户执行 `/sprint-exps sprint-xxx`
- **THEN** 命令流程 MUST 先运行或读取该 Sprint 的 Fact Sheet summary，再基于 Fact Sheet 生成 Sprint 复盘与模型 Token 使用分析
- **AND** 默认复盘输出 MUST 不包含完整 `evidence_hints` 表

#### Scenario: Fact Sheet 标记需要细节
- **WHEN** Fact Sheet 标记 `needs_detail`、warning、missing 或 inconsistent 类风险
- **THEN** `/sprint-exps` MAY 按 Fact Sheet 的 evidence hints 读取对应原始文件片段
- **AND** `/sprint-exps` MAY 通过字段模式单独获取 `evidence_hints`

### Requirement: Fact Sheet 输出边界受上下文预算约束
Fact Sheet 生成与 `/sprint-exps` 消费流程 MUST 遵守 Agent 上下文预算规则，避免宽泛搜索、长日志、生成物全文 diff、完整 evidence hints 默认输出和历史归档全量展开。

#### Scenario: 大 Sprint 包含多个 Change
- **WHEN** Sprint 包含多个 REQ、BUG、Change 或大量 tasks
- **THEN** Fact Sheet MUST 输出聚合计数和精确证据路径，而不是复制原始 trace、tasks、acceptance report 或 generated 文件全文

#### Scenario: 需要读取 archive 目录
- **WHEN** Fact Sheet 需要读取 Sprint 内已归档 Change
- **THEN** 系统 MUST 从 `sprint.yaml` 的 Change 列表构造精确路径，不得通过宽泛搜索默认扫描整个 `openspec/changes/archive/**`

#### Scenario: 复盘默认输出使用紧凑边界
- **WHEN** `/sprint-exps` 调用 Fact Sheet 辅助脚本且未显式请求细节
- **THEN** 系统 MUST 使用 summary 或等价紧凑输出
- **AND** 输出 MUST 包含风险计数、关键状态与推荐回读信号
- **AND** 输出 MUST NOT 包含完整 `evidence_hints` 明细

### Requirement: Fact Sheet 支持机器可读输出
系统 MUST 支持 Markdown、完整 JSON、summary 与 fields 输出模式，Markdown 用于人工阅读，完整 JSON 用于调试和兼容自动化，summary 用于复盘默认输入，fields 用于按需读取特定字段。

#### Scenario: 请求 JSON 输出
- **WHEN** 用户或测试命令请求 JSON 格式 Fact Sheet
- **THEN** 系统 MUST 输出包含 Sprint、scope、changes、issues、warnings、token_risks 与 evidence_hints 的机器可读结构

#### Scenario: 请求 Summary 输出
- **WHEN** 用户、测试命令或 `/sprint-exps` 请求 summary 格式 Fact Sheet
- **THEN** 系统 MUST 输出包含 Sprint 基础信息、scope 计数、warnings 摘要、`needs_detail`、AI usage 状态和 token risks 的紧凑结构
- **AND** summary MUST NOT 默认包含完整 `evidence_hints`

#### Scenario: 请求 Fields 输出
- **WHEN** 用户、测试命令或 `/sprint-exps` 请求一个或多个字段路径
- **THEN** 系统 MUST 输出所请求字段的机器可读结构
- **AND** 系统 MUST 支持通过 fields 模式单独获取 `evidence_hints`
