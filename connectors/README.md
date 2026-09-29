---
purpose: 外部连接器交付包目录说明
content: WorkBuddy 等外部连接器 manifest、mcp 配置、外部 Skill、图标和打包说明的存放边界
source: /spec-opt define-connector-directory-boundaries
update_method: 新增连接器类型、连接器交付结构或平台打包规范变化时同步更新
created_at: 2026-09-04 00:00:00
updated_at: 2026-09-04 00:00:00
---

# 外部连接器交付包

`connectors/` 用于存放 WorkBuddy 等外部平台连接器的交付包资产。每个连接器使用独立子目录，例如 `connectors/workbuddy/`。

## 边界

- `connectors/<connector>/manifest.*`、`mcp.json`、平台声明文件、图标、外部 Skill、打包说明和部署说明属于本目录。
- MCP server、tool registry、schema adapter、auth/audit adapter 和 runtime entrypoint 等运行时代码放在 `src/mcp/<connector>/`。
- 本项目内部 Codex 工作流命令继续放在 `.agents/skills/`；WorkBuddy 外部 Skill 不得放入 `.agents/skills/`。
- 不得提交真实企业租户配置、密钥、访问令牌、Cookie、真实客户数据、运行时数据库、依赖目录或构建产物。

## 当前连接器

| 连接器 | 交付包 | 运行时代码 | 说明 |
|---|---|---|---|
| WorkBuddy | `connectors/workbuddy/` | `src/mcp/workbuddy/` | 腾讯 WorkBuddy 自定义连接器；第一阶段支持本地 stdio PoC，第二阶段支持 HTTPS MCP 服务与受控管理写操作。 |

## 推荐结构

```text
connectors/
  workbuddy/
    README.md
    manifest.json
    mcp.json
    skills/
    assets/
```
