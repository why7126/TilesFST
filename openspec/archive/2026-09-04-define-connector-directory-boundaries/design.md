---
created_at: 2026-09-04 17:30:00
updated_at: 2026-09-04 17:30:00
---

# 设计说明：连接器目录边界

## 目录分层

本 Change 只定义目录边界，不实现连接器运行时。

- `src/mcp/<connector>/`：MCP 运行时代码目录，承载 server、tools、schema adapter、auth/audit adapter 和 runtime entrypoint。
- `connectors/<connector>/`：外部平台连接器交付包目录，承载 manifest、`mcp.json`、外部 Skill、图标和打包说明。
- `.agents/skills/`：本项目内部 Codex 工作流命令目录，不承载 WorkBuddy 外部 Skill。

## 校验策略

目录结构校验脚本登记顶层 `connectors/`，并对该目录执行安全边界检查：

- 阻断真实 env、依赖目录、构建产物、运行时数据库、日志和包文件。
- 对 Markdown、JSON、YAML 与常见图片配置文件做敏感内容启发式扫描。
- `src/mcp/` 作为 `src/` 下的源码归属，不需要新增顶层目录。

## 不适用项

- API、DB、Web、小程序、管理端业务实现：不适用。
- OpenAPI / Orval：不适用。
- Docker Compose：不适用。
- 产品数据采集与链路观测：本 Change 不新增运行时请求链路；后续连接器实现 Change 需要单独声明适用层级。
