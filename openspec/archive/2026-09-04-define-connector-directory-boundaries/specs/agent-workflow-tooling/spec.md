## ADDED Requirements

### Requirement: 外部连接器目录边界

系统 SHALL 为 WorkBuddy 等外部连接器维护清晰的仓库目录边界：`src/mcp/<connector>/` 承载 MCP 运行时代码，`connectors/<connector>/` 承载连接器交付包资产，`.agents/skills/` 仅承载本项目内部 Codex 工作流命令。

#### Scenario: 新增 MCP 运行时代码
- **WHEN** 变更为 WorkBuddy 或其他外部连接器新增 MCP server、tool registry、schema adapter、auth/audit adapter 或 runtime entrypoint
- **THEN** 运行时代码 SHALL 位于 `src/mcp/<connector>/`
- **AND** 不得将业务运行时代码直接放在仓库根目录或 `connectors/` 交付包目录中。

#### Scenario: 新增外部连接器交付包
- **WHEN** 变更新增 WorkBuddy manifest、`mcp.json`、外部 Skill、图标、打包说明或平台适配 README
- **THEN** 交付包资产 SHALL 位于 `connectors/<connector>/`
- **AND** 外部 Skill SHALL NOT 放入 `.agents/skills/`。

#### Scenario: 更新内部 Codex 工作流 Skill
- **WHEN** 变更新增或修改本项目 `/req-*`、`/opsx-*`、`/sprint-*`、`/spec-*` 等 AI 工作流命令入口
- **THEN** 这些内部 Skill SHALL 继续位于 `.agents/skills/`
- **AND** 不得以 WorkBuddy 连接器交付为理由恢复 `.codex/`、`.cursor/`、`.claude/`、`.opencode/` 或 `.kiro/` 工具入口目录。
