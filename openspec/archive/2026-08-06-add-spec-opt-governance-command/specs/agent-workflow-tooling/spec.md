# agent-workflow-tooling 规格变更

## ADDED Requirements

### Requirement: 规范优化命令 spec-opt
系统 MUST 提供 `/spec-opt` 命令作为项目治理规范优化入口。该命令 MUST 允许创建或复用 OpenSpec Change，并且 MUST 仅服务治理规范优化，不得修改业务运行时代码。治理规范优化包括新增或修改 `.agents/skills` 命令、`rules/` 文档、`docs/` 文档和 `scripts/` 治理脚本。

#### Scenario: 新增治理命令
- **WHEN** 用户请求 `/spec-opt` 新增一个项目级命令
- **THEN** 系统 MUST 在 `.agents/skills/<command>/SKILL.md` 创建或更新对应 Skill
- **AND** 系统 MUST 创建或复用 OpenSpec Change 记录该治理变更
- **AND** 系统 MUST 同步更新 `AGENTS.md` 的命令入口和命令速查
- **AND** 系统 MUST 同步相关 `rules/`、`docs/` 或 `scripts/` 说明

#### Scenario: 修改文档规范
- **WHEN** 用户请求 `/spec-opt` 新增或修改文档规范
- **THEN** 系统 MUST 更新对应 `rules/*.md` 或 `docs/**/*.md`
- **AND** 若影响入口、读取路由或目录边界，系统 MUST 同步 `AGENTS.md`
- **AND** 若新增或调整 docs 索引，系统 MUST 同步 `docs/README.md`

#### Scenario: 修改治理脚本
- **WHEN** 用户请求 `/spec-opt` 新增或修改治理脚本
- **THEN** 系统 MUST 更新 `scripts/` 下对应脚本或校验工具
- **AND** 系统 SHOULD 更新脚本帮助文本、相关规则文档和对应 Skill 引用
- **AND** 系统 SHOULD 补充或运行脚本级测试

#### Scenario: 禁止修改业务代码
- **WHEN** `/spec-opt` 执行治理规范优化
- **THEN** 系统 MUST NOT 修改 `src/` 下业务运行时代码
- **AND** 系统 MUST NOT 修改后端 API、数据库 schema、Web、小程序或管理端业务实现
- **AND** 若用户请求包含业务实现，系统 MUST 引导其改用 REQ/BUG/OpenSpec 业务流程

#### Scenario: 规范优化后的同步校验
- **WHEN** `/spec-opt` 完成规范、技能、文档或脚本修改
- **THEN** 系统 MUST 运行 `python scripts/validate-agent-context-budget.py`
- **AND** 系统 MUST 运行 `python scripts/validate-openspec-language.py`
- **AND** 系统 MUST 运行 `python scripts/validate-directory-structure.py`
- **AND** 系统 MUST 运行 `openspec validate <change-id>`

#### Scenario: 输出下一步与待处理点
- **WHEN** `/spec-opt` 完成执行
- **THEN** 最终输出 MUST 包含去重后的 `下一步` 与 `待用户决策/处理`
- **AND** 已在 `下一步` 中给出的命令或动作 MUST NOT 重复写入 `待用户决策/处理`
