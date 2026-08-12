# agent-context-governance Specification

## Purpose
TBD - created by archiving change optimize-agent-context-budget-harness. Update Purpose after archive.
## Requirements
### Requirement: Agent 命令 MUST 遵守上下文预算

项目级命令技能 MUST 引用统一的 Agent 上下文预算规则，并在执行时优先使用定位、摘要、片段读取，而不是全量读取规则、历史归档、生成物或大目录。

#### Scenario: 技能引用统一预算规则

- **WHEN** 新增或更新 `.agents/skills/{req,bug,opsx,sprint,build}-*`、`.agents/skills/capture` 或 `.agents/skills/initialize-project` 命令技能
- **THEN** 技能 MUST 明确引用 `rules/agent-context-budget.md`
- **AND** 技能 MUST 避免要求默认全量读取 `rules/*`、`docs/**`、`issues/**`、`iterations/**` 或 `openspec/specs/**`

#### Scenario: 大范围检索默认排除高噪音目录

- **WHEN** Agent 对项目执行大范围 `rg`、`find` 或文件清单扫描
- **THEN** 默认 MUST 排除 Harness/模板工程、历史 agent 目录、构建产物、依赖目录、归档目录与生成物
- **AND** 只有任务明确需要时 MAY 放开排除范围
- **AND** 放开前 MUST 说明原因并优先输出清单或命中数

### Requirement: 生成物与大 diff MUST 先摘要后展开

Agent 在检查 OpenAPI、Orval、构建产物、Workflow Sync 输出或大 diff 时，MUST 先使用摘要级输出；只有定位到具体失败、具体 schema 或具体文件片段后才展开读取。

#### Scenario: OpenAPI 与 Orval 生成物不默认全文展开

- **WHEN** API 变更导致 `src/web/openapi.json` 或 Orval 生成文件变化
- **THEN** Agent MUST NOT 默认输出生成物全文或完整 diff
- **AND** Agent SHOULD 使用 `git diff --stat`、`git diff --name-only` 或 schema 相关片段进行复核

#### Scenario: 校验脚本阻止预算规则回退

- **WHEN** 运行 `python scripts/validate-agent-context-budget.py`
- **THEN** 脚本 MUST 检查 `.agents/skills/{req,bug,opsx,sprint,build}-*`、`.agents/skills/capture` 与 `.agents/skills/initialize-project` 是否引用 `rules/agent-context-budget.md`
- **AND** 脚本 MUST 报告缺少预算入口或出现默认宽泛读取指令的技能文件

### Requirement: 上下文预算与命令输出治理

系统 SHALL 约束 AI 在命令执行中的读取范围、输出体量、摘要复用、用户反馈和后续动作生成方式。

#### Scenario: 日志优先降低跨项目学习读取成本

- **GIVEN** `/spec-study` 学习对象包含治理日志总账
- **WHEN** AI 需要识别可迁移治理能力
- **THEN** AI SHALL 先读取日志总账和相关单次日志摘要
- **AND** 只在证据不足时读取真实规则、技能、脚本或部署片段补证

#### Scenario: 需要用户决策时收敛问题

- **GIVEN** 命令遇到需要用户选择、确认、补充或处理的事项
- **WHEN** 命令不能继续自动执行
- **THEN** AI SHALL 每轮只聚焦 1 到 3 个关键决策
- **AND** 每个决策 SHOULD 提供互斥选项、推荐项和可补充说明入口

