---
created_at: 2026-08-07 09:06:21
updated_at: 2026-08-07 09:20:34
change_id: add-spec-sync-skill
---

# spec-sync 学习报告

## 学习对象

本次学习对象为用户提供的治理需求描述：创建一个 `spec-sync` 技能，用于学习其他项目的 Harness 工程，并在用户确认后应用到本项目。

## 学习模式

自动学习模式。由于本次目标是新增技能本身，重点提炼用户给出的目标、输入形态、学习范围、确认门禁、应用边界和报告输出要求。

## 学习到的治理能力

- Harness 学习必须支持本地项目路径和 GitHub URL。
- 学习模式必须支持自动学习和指定学习内容；未指定时默认自动学习。
- 学习单项主题时也必须横向检查入口、规范、文档、Agent 目录、脚本、部署与环境示例，避免片面迁移。
- 学习阶段必须先输出候选学习内容，让用户确认是否应用。
- 学习对象必须全程只读，绝不允许改动学习对象代码、文档、配置、依赖锁文件、Git 状态、缓存、生成物或运行时数据。
- 应用阶段只更新治理资产，绝不修改 `src/` 业务运行时代码。
- 应用完成后必须输出学习报告，说明学到了什么、采纳了什么、未采纳什么、更新了哪些文件和验证结果。

## 已采纳内容

- 新增 `.agents/skills/spec-sync/SKILL.md`，承载两阶段 Harness 学习同步流程。
- 同步 `AGENTS.md`，把 `spec-sync` 加入技能入口和命令速查。
- 同步 `rules/agent-context-budget.md`，要求 `spec-sync` 遵守横向学习、确认后应用和禁止修改 `src/` 的预算与边界。
- 补强 `spec-sync` 的学习对象只读红线，要求本地路径、临时克隆目录和 GitHub 快照都只能作为只读输入。
- 将误建的 `sprint-2026-08-07-spec-sync` 调整为 `sprint-022`，并补充无进行中迭代时的自动编号规则。
- 更新 `scripts/validate-agent-context-budget.py`，把 `spec-sync` 纳入命令技能校验范围。
- 新增 OpenSpec delta spec，记录 `agent-workflow-tooling` 对 `/spec-sync` 的能力约束。

## 未采纳内容

- 未创建 `.cursor/`、`.codex/`、`.kiro/`、`.opencode/`、`.claude/` 等入口目录；本项目当前唯一 AI 工具入口仍为 `.agents/skills/`。
- 未新增业务实现、API、数据库、Web、小程序或管理端代码。

## 更新文件

- `.agents/skills/spec-sync/SKILL.md`：新增跨项目 Harness 学习同步技能。
- `rules/agent-context-budget.md`：同步 `spec-sync` 上下文预算要求和学习对象只读保护。
- `rules/iterations-lifecycle.md`：新增 Sprint 自动编号和非规范名称修正规则。
- `.agents/skills/sprint-propose/SKILL.md`：新增 Sprint ID 自动编号规则。
- `scripts/validate-agent-context-budget.py`：纳入 `spec-sync` 命令技能校验。
- `openspec/archive/2026-08-07-add-spec-sync-skill/*`：记录 proposal、design、tasks、delta spec、trace、acceptance、test-plan 和本报告。
- `iterations/archive/sprint-022/*`：记录本次纯治理 Change 的 Sprint scope 与验收。

## 影响范围

- API：不影响。
- 数据库：不影响。
- Web：不影响。
- 小程序：不影响。
- 管理端：不影响。
- Orval：不需要。
- Docker Compose：不需要验证。
- 测试：业务测试不适用；执行治理校验。

## 验证结果

- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `openspec validate add-spec-sync-skill`：通过。
