## Why

当前项目规则、技能、脚本和历史 Change 主要使用 `openspec/changes/archive/`，但 `openspec/config.yaml` 与用户期望指向 `openspec/archive/`。Change archive 作为已完成 OpenSpec 变更的长期事实源，应从 active change 根目录中独立出来，降低“开发中变更”和“已归档变更”混在同一树下带来的语义混淆。

## What Changes

- **BREAKING**：将 OpenSpec Change 的 canonical archive root 从 `openspec/changes/archive/` 迁移为 `openspec/archive/`。
- 更新 OpenSpec 配置、项目规则、命令技能、Workflow Sync、readiness、release、fact sheet、AI usage、测试 helper 等所有 Change archive 路径解析逻辑。
- 迁移既有历史归档目录，并提供旧路径残留检查，确保文档和脚本不再继续写入 `openspec/changes/archive/`。
- 保留只读兼容解析期：工具在迁移期可读取旧路径，但新增归档和生成事实源 MUST 写入 `openspec/archive/`。
- 清理或约束 `openspec/changes/archive/`，防止它继续承载新归档 Change。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `agent-workflow-tooling`：修改 OpenSpec Change 归档根目录契约、路径残留检查和命令输出要求。
- `testing`：修改测试读取 Change 文件的 archive 路径兼容契约。

## Impact

- 影响规则文档：`AGENTS.md`、`rules/directory-structure.md`、`rules/document-governance.md`、`rules/issues-lifecycle.md`、`rules/iterations-lifecycle.md`、`rules/agent-context-budget.md` 等涉及 Change archive 路径的说明。
- 影响命令技能：`.agents/skills/opsx-archive/`、`.agents/skills/openspec-archive-change/`、`.agents/skills/sprint-archive/`、`.agents/skills/sprint-exps/`、release 相关技能以及默认搜索排除规则。
- 影响脚本与测试：Workflow Sync 收集、issue promote、Sprint archive readiness、archived path residual、AI usage、Fact Sheet、release 生成、测试 helper 与对应 pytest。
- 不影响业务 API、数据库表结构、Web/小程序运行时功能、Orval 生成物或 Docker Compose 服务拓扑。
