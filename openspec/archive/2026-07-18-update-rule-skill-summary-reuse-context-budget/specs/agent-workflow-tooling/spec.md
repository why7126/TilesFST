# agent-workflow-tooling Delta Spec

## ADDED Requirements

### Requirement: 规则与 Skill 已读摘要复用

系统 MUST 在 Agent 上下文预算治理中定义同一会话内规则与 Skill 已读摘要复用机制，减少连续工作流命令重复读取相同文件。

#### Scenario: 同一会话复用规则摘要

- **WHEN** Agent 在同一会话中已经读取过 `AGENTS.md`、`openspec/project.md` 或相关 `rules/*.md`
- **AND** 目标文件未显示内容、mtime、hash 或 `updated_at` 变化
- **AND** 已有摘要足以覆盖当前命令的规则门禁
- **THEN** Agent SHOULD 用摘要承接
- **AND** Agent SHOULD NOT 重复全量读取相同文件

#### Scenario: 同一会话复用 Skill 摘要

- **WHEN** Agent 在同一会话中已经读取过当前命令 Skill 或共用 Skill
- **AND** 目标 Skill 未显示内容、mtime、hash 或 `updated_at` 变化
- **AND** 已有摘要足以覆盖当前命令步骤和 Final Step
- **THEN** Agent SHOULD 用摘要承接
- **AND** Agent SHOULD 只补读当前任务缺失的必要片段

#### Scenario: 摘要最小信息

- **WHEN** Agent 使用已读摘要承接规则或 Skill
- **THEN** 摘要 SHOULD 能表达文件路径、版本线索、与当前任务相关的规则/门禁摘要、适用范围和刷新原因或等价信息
- **AND** 摘要 MAY 只存在于同一对话上下文中

### Requirement: 摘要复用失效与补读

系统 MUST 定义摘要复用的失效条件，确保上下文节省不会绕过 OpenSpec、Issue lifecycle、安全、API、DB、上传、Docker、发布或 Workflow Sync 门禁。

#### Scenario: 文件变化触发补读

- **WHEN** 规则或 Skill 文件的内容、mtime、hash、`updated_at` 或等价版本线索显示已变化
- **THEN** Agent MUST 重新读取目标文件或必要片段
- **AND** Agent MUST NOT 继续使用旧摘要作为唯一依据

#### Scenario: 任务风险升级触发补读

- **WHEN** 命令从 capture、explore、generate 等轻量阶段升级到 apply、archive、release 或等价高风险阶段
- **OR** 当前任务涉及权限、安全、API、DB、上传、Docker、发布或 OpenSpec 红线
- **THEN** Agent MUST 补读当前 Change、Issue、Sprint、trace、Final Step 或失败相关片段
- **AND** Agent MUST NOT 仅凭旧摘要继续执行高风险动作

#### Scenario: 用户要求或失败诊断触发补读

- **WHEN** 用户显式要求重新读取或复核原文
- **OR** Workflow Sync、测试、校验脚本或 OpenSpec CLI 返回失败
- **THEN** Agent MUST 回到相关原文或必要片段定位

### Requirement: 命令 Skill 摘要复用 Guardrails

命令 Skill MUST 在 `Context Budget Guardrails` 或等价章节中表达规则与 Skill 已读摘要复用约束，并保留命令特定门禁。

#### Scenario: 命令 Skill 使用统一预算表述

- **WHEN** 新增或更新 `.agents/skills/{req,bug,opsx,sprint,build}-*`、`.agents/skills/capture`、`.agents/skills/initialize-project` 或 release 命令 Skill
- **THEN** Skill MUST 引用 `rules/agent-context-budget.md`
- **AND** Skill SHOULD 明确同一会话已读且无变更的规则和 Skill 用摘要承接
- **AND** Skill MUST 保留命令特定 Must Read、Workflow Sync、AI usage hook 和业务门禁

#### Scenario: 高风险命令保留补读要求

- **WHEN** Skill 对应 apply、archive、release、req-opsx、bug-opsx、sprint-propose 或等价高风险命令
- **THEN** Skill MUST 要求先读取当前 Change、Issue、Sprint、trace/status 或 OpenSpec CLI 输出的必要片段
- **AND** Skill MUST NOT 要求默认全量读取历史归档、所有 specs、generated 文件或大目录

### Requirement: 上下文预算校验覆盖摘要复用

系统 MUST 通过上下文预算校验阻止命令 Skill 缺少预算入口、缺少摘要复用约束或回退到默认宽泛读取。

#### Scenario: 校验命令 Skill 摘要复用约束

- **WHEN** 用户或 CI 执行 `python scripts/validate-agent-context-budget.py`
- **THEN** 脚本 MUST 检查命令 Skill 是否引用 `rules/agent-context-budget.md`
- **AND** 脚本 MUST 检查命令 Skill 是否包含规则与 Skill 已读摘要复用的等价表述
- **AND** 脚本 MUST 报告缺失约束的文件路径

#### Scenario: 校验默认宽泛读取回退

- **WHEN** 命令 Skill 包含默认 `cat rules/*.md`、`ls -R`、无边界 `rg <keyword> .` 或等价宽泛读取指令
- **AND** 该指令不是明确禁止或反例说明
- **THEN** 校验脚本 MUST 返回非零退出码
- **AND** 报告 MUST 包含具体文件路径与行号

### Requirement: 摘要复用安全边界

系统 MUST 确保规则与 Skill 摘要复用不会持久化敏感上下文或扩大成功路径输出。

#### Scenario: 禁止持久化敏感原文

- **WHEN** Agent 使用规则或 Skill 摘要复用机制
- **THEN** 系统 MUST NOT 将原始 prompt、系统指令、developer 指令、完整 session JSONL、工具输出正文、密钥、Cookie、Authorization header、`.env` 内容或真实客户数据写入仓库

#### Scenario: 成功路径输出保持紧凑

- **WHEN** 工作流命令成功复用摘要并完成主流程
- **THEN** Agent SHOULD 只输出复用摘要、补读片段、计数、warning 或 recommended action 的短摘要
- **AND** Agent MUST NOT 默认转述完整规则、完整 Skill、完整测试日志、完整 Workflow Sync 派生块或完整 generated diff
