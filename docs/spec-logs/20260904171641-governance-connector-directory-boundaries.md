---
purpose: 连接器目录边界治理日志
content: 记录 WorkBuddy 等外部连接器交付包与 MCP 运行时代码目录规范的补充
source: /spec-opt define-connector-directory-boundaries
update_method: 同一治理变更有补充修正时更新本文档
created_at: 2026-09-04 17:16:41
updated_at: 2026-09-04 17:16:41
---

# 连接器目录边界治理日志

## 背景

REQ-0132 需要支持 ProjectTilesFST 作为腾讯 WorkBuddy 自定义连接器。该能力会同时产生 MCP 运行时代码和 WorkBuddy 平台交付包资产。原目录规范未明确二者边界，且 `.agents/skills/` 已被定义为项目内部 Codex 工作流命令入口，不能混入外部平台 Skill。

## 决策

- 新增顶层 `connectors/`，用于外部连接器交付包。
- 约定 `connectors/<connector>/` 存放 manifest、`mcp.json`、外部 Skill、图标、平台 README 和打包说明。
- 约定 `src/mcp/<connector>/` 存放 MCP server、tools、schema adapter、auth/audit adapter 和 runtime entrypoint。
- `.agents/skills/` 继续只承载项目内部 Codex 工作流命令；WorkBuddy 外部 Skill 不得放入该目录。
- 目录校验脚本登记 `connectors/`，并阻断真实 env、依赖目录、构建产物、运行时数据库、日志、包文件和常见敏感内容。

## 更新文件

- `openspec/changes/define-connector-directory-boundaries/`
- `iterations/change/sprint-029/sprint.yaml`
- `rules/directory-structure.md`
- `AGENTS.md`
- `docs/README.md`
- `connectors/README.md`
- `scripts/validate-directory-structure.py`
- `docs/spec-logs/CHANGELOG.md`

## 验证

- OpenSpec strict 校验通过。
- 目录结构、上下文预算、Sprint scope 和 OpenSpec 文档语言校验通过。
- 文档卫生聚焦校验通过并提示 2 条既有 AGENTS.md 启发式 warning。
- `scripts/validate-directory-structure.py` 编译通过。
- Workflow Sync 完成，AI Usage hook 返回 `usage_mode: actual` 并刷新 `sprint-029` snapshot。

## 跨项目落地提示词

`/spec-opt 为外部平台连接器补充目录边界：新增顶层 connectors/<connector>/ 作为连接器交付包目录，存放 manifest、mcp.json、外部 Skill、图标和打包说明；MCP server、tools、schema adapter、auth/audit adapter 和 runtime entrypoint 放入 src/mcp/<connector>/；项目内部 AI 工作流 Skill 仍放 .agents/skills/，不得混入外部平台 Skill；同步目录规范、入口说明、文档索引、目录校验脚本和 OpenSpec Change。`
