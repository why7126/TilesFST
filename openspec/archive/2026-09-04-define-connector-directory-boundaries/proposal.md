---
created_at: 2026-09-04 00:00:00
updated_at: 2026-09-04 00:00:00
---

# 提案：定义连接器目录边界

## 背景

ProjectTilesFST 后续需要支持作为腾讯 WorkBuddy 自定义连接器。该能力会同时产生 MCP 运行时代码、WorkBuddy 连接器 manifest、外部 Skill、图标和打包说明。现有目录规范只定义了 `.agents/skills/` 作为项目内部 AI 工作流入口，未明确外部连接器资产应存放在哪里，容易把 WorkBuddy Skill 误放入 `.agents/skills/`，或把 MCP 运行时代码散落到仓库根目录。

## 变更内容

- 新增顶层 `connectors/` 目录边界，用于存放 WorkBuddy 等外部连接器交付包资产。
- 明确 `src/mcp/<connector>/` 承载 MCP server、tool registry、schema adapter、auth/audit adapter 和 runtime entrypoint 等运行时代码。
- 明确 `.agents/skills/` 仍仅承载本项目 Codex 工作流命令，不承载 WorkBuddy 外部 Skill。
- 同步 `AGENTS.md`、`rules/directory-structure.md`、`docs/README.md`、目录结构校验脚本和治理日志。

## 非目标

- 不实现 WorkBuddy MCP server、WorkBuddy Skill 或管理端写操作。
- 不修改业务 API、数据库、Web、小程序或管理端功能。
- 不引入真实 WorkBuddy 凭据、企业租户配置或生产部署文件。
