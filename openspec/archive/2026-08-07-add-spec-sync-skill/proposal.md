## 背景

项目需要一个专门的治理技能，用于学习其他项目的 Harness 工程经验，并在用户确认后把可复用的规范、技能、脚本和部署治理资产应用到本项目。当前只能通过通用 `/spec-opt` 临时处理，缺少“先学习报告、再确认应用、最后输出同步报告”的稳定流程。

## 变更内容

- 新增 `/spec-sync` 技能，支持从本地项目或 GitHub 项目 URL 学习 Harness 工程。
- 支持自动学习和指定学习内容两种模式；未指定模式时默认自动学习。
- 规定学习范围必须跨 `AGENTS.md`、`project.yaml`、`DOCUMENT_METADATA_INDEX.md`、`rules/`、`docs/`、多 Agent 目录、`scripts/`、部署与环境示例综合分析。
- 规定应用前必须输出候选学习内容并等待用户确认。
- 规定用户确认后只更新本项目治理资产，绝不修改 `src/` 目录，并输出学习报告。

## 能力

### 新增能力

- 无。

### 修改能力

- `agent-workflow-tooling`：新增 `/spec-sync` Harness 学习与同步技能的流程约束。
- `sprint-planning-governance`：新增 Sprint 自动编号与非规范 Sprint 名称修正规则。

## 影响

- 影响 `.agents/skills/spec-sync/SKILL.md`、`.agents/skills/sprint-propose/SKILL.md`、`AGENTS.md`、`rules/agent-context-budget.md`、`rules/iterations-lifecycle.md` 与本 Change 文档。
- 不影响后端 API、数据库、Web、小程序、管理端业务实现。
- 不需要 Orval。
- 不需要 Docker Compose 验证。
