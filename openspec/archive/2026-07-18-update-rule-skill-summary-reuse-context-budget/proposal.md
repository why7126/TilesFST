# Proposal: 规则/Skill 已读摘要复用纳入上下文预算治理

## Why

Sprint 007 复盘已将规则/Skill 重复读取识别为中等 Token 浪费来源，并形成行动项 A-004。当前 `rules/agent-context-budget.md` 已要求“已读且无变更的规则用摘要承接”，但缺少可执行定义、Skill 覆盖范围、失效条件和校验门禁，导致连续工作流命令仍容易重复展开相同规则与 Skill。

## What Changes

- 在 Agent 上下文预算规则中明确定义“已读摘要复用”的最小字段、适用范围、失效条件和安全边界。
- 将 `.agents/skills/*/SKILL.md` 与 `rules/` 一起纳入同一会话摘要复用治理。
- 统一命令 Skill 的 `Context Budget Guardrails` 表述，要求规则和 Skill 已读且无变更时用摘要承接。
- 增强 `scripts/validate-agent-context-budget.py`，检查命令 Skill 是否保留摘要复用约束，并继续阻止默认宽泛读取。
- 保持成功路径输出紧凑，不持久化原始 prompt、系统/developer 指令、工具输出正文、密钥或本地绝对路径。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `agent-workflow-tooling`: 增加规则/Skill 已读摘要复用、摘要失效条件、命令 Skill 模板和上下文预算校验要求。

## Impact

- 影响规则文档：`rules/agent-context-budget.md`。
- 影响命令 Skill：`.agents/skills/{req,bug,opsx,sprint,build}-*`、`.agents/skills/capture`、`.agents/skills/initialize-project`，以及需要共享 Final Step 的相关 Skill。
- 影响脚本：`scripts/validate-agent-context-budget.py`。
- 不影响 API、数据库、Web、微信小程序、管理端业务功能、MinIO 或 Docker Compose 编排。
- 不需要 Orval 或数据库迁移。
