## ADDED Requirements

### Requirement: 工作流命令自动构建 AI usage 事实源
系统 MUST 为 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 工作流命令提供后置 AI usage fact source 构建流程，并在主命令和 Workflow Sync 成功后尝试生成或刷新脱敏使用量事实。

#### Scenario: 主命令与 Workflow Sync 成功后触发
- **WHEN** 用户执行 `/req-*`、`/bug-*`、`/opsx-*` 或 `/sprint-*` 工作流命令
- **AND** 主命令完成且 Workflow Sync 返回成功
- **THEN** 系统 MUST 触发统一 AI usage fact source hook 或等价共享流程
- **AND** 系统 MUST 输出短摘要，包含 hook status、usage mode、warning 数量和 recommended action

#### Scenario: 主命令失败时跳过
- **WHEN** 工作流命令主流程失败或 Workflow Sync 失败
- **THEN** 系统 MAY 跳过 AI usage fact source hook
- **AND** 系统 MUST 在输出中说明本次未构建 AI usage 事实源的原因

#### Scenario: 无 Sprint 归属时不伪造 snapshot
- **WHEN** 命令可归因到 REQ 或 BUG 但无法解析到 Sprint
- **THEN** 系统 MUST NOT 创建伪造的 Sprint 聚合快照
- **AND** 系统 SHOULD 生成 command run 明细或输出无法生成的原因
- **AND** 输出 MUST 标明 Sprint snapshot skipped 或等价状态

### Requirement: 统一 AI usage post-command hook
系统 MUST 通过统一脚本、函数或等价封装处理工作流命令后的 AI usage 构建，避免 source-command 技能复制复杂 session 解析、归因和脱敏逻辑。

#### Scenario: source-command 技能引用统一 hook
- **WHEN** 任一 source-command 技能需要在命令完成后构建 AI usage 事实源
- **THEN** 技能 MUST 引用统一 hook、共享规则或同一脚本入口
- **AND** 技能 MUST NOT 复制原始 session 解析、prompt 处理或工具输出处理的长逻辑

#### Scenario: hook 输入包含工作流上下文
- **WHEN** 系统调用 AI usage post-command hook
- **THEN** hook MUST 支持 workflow event、REQ ID、BUG ID、Change ID、Sprint ID、session 输入或 manual map 的等价输入
- **AND** hook SHOULD 使用这些输入提升 command run 归因准确性

#### Scenario: hook 支持检查或降级模式
- **WHEN** 本地 session 输入不可用或当前环境无法构建真实事实源
- **THEN** hook MUST 输出 `unavailable` 或 `estimated_fallback` 等价状态
- **AND** hook MUST 给出 reason 和 recommended action

### Requirement: 工作流命令 command run 与 Sprint snapshot 写入
系统 MUST 在可安全解析本地 session 输入时写入脱敏 command run 明细，并在命令可明确关联 Sprint 时生成或刷新 Sprint 聚合快照。

#### Scenario: 写入 command run 明细
- **WHEN** hook 可读取并解析本地 session 输入
- **THEN** 系统 MUST 将脱敏 command run 明细写入 `data/ai-usage/command-runs/` 或等价事实源路径
- **AND** command run MUST 通过 requirements、bugs、changes、sprint_id、workflow_event 或等价字段进行归因

#### Scenario: 刷新 Sprint snapshot
- **WHEN** hook 可明确解析到 `sprint-xxx`
- **THEN** 系统 SHOULD 生成或刷新 `data/ai-usage/sprints/<sprint-id>.json`
- **AND** snapshot MUST 包含 sprint_id、generated_at、coverage、totals、warnings 和 usage mode 所需字段

#### Scenario: snapshot 不满足 actual 条件
- **WHEN** snapshot 覆盖不足、过期、必要指标为空或解析失败
- **THEN** 系统 MUST NOT 将该 snapshot 标记为完整 `actual`
- **AND** 系统 MUST 输出 warning、降级原因和刷新建议

### Requirement: 自动构建继承 AI usage 安全边界
工作流命令自动构建 AI usage 事实源时 MUST 继承 AI 使用量事实源的脱敏、安全和上下文预算边界。

#### Scenario: 持久化安全字段
- **WHEN** hook 写入 command run 明细或 Sprint snapshot
- **THEN** 系统 MUST 仅持久化数字指标、工作流 ID、hash、时间范围、源行号范围、coverage、短安全标签或 warning
- **AND** 系统 MUST NOT 持久化原始 prompt、系统指令、developer 指令、技能全文、原始 session JSONL、本机绝对路径、工具输出正文、密钥、Cookie、Authorization、真实客户数据或 `.env` 内容

#### Scenario: 命令输出保持摘要
- **WHEN** hook 完成检查、生成或降级
- **THEN** 系统 MUST 只输出摘要信息
- **AND** 系统 MUST NOT 默认打印完整 session、prompt、工具日志、OpenAPI/Orval 大 diff、测试日志全文或完整 snapshot 内容

#### Scenario: 重复构建幂等
- **WHEN** 用户或系统重复对同一 session 或同一 command run 执行自动构建
- **THEN** 系统 SHOULD 使用 session hash、turn hash、command run id 或等价来源摘要避免重复累计
- **AND** 系统 SHOULD 为重复、无法归因或疑似敏感内容跳过输出 warning
