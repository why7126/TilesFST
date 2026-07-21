## Why

部分工作流命令在 `force-proceed` 场景下可能为了不断流而自动生成 follow-up Issue，但自动落盘会把未经用户确认的待办混入正式 `issues/` 生命周期。需要将默认行为收紧为“仅输出标准 capture 文案”，只有用户明确授权时才创建 REQ/BUG。

## What Changes

- 禁止 `force-proceed` 默认自动创建 follow-up REQ/BUG。
- 当命令发现后续问题、补充需求或残留风险时，默认输出可直接用于 `/capture` 的标准文案，供用户确认后再进入 Issue 生命周期。
- 允许用户在当前命令中明确授权自动 capture；授权缺失时不得写入 `issues/`、不得更新 registry、不得运行 `req.capture`/`bug.capture` Workflow Sync。
- 为标准 capture 文案定义最低字段：建议命令、类型倾向、标题、背景、影响、建议验收/复现、来源 Change/Sprint/命令。
- 增加测试或校验，覆盖 `force-proceed` 与 follow-up 输出边界。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `agent-workflow-tooling`: 约束工作流命令在 `force-proceed` 场景下处理 follow-up Issue 的默认行为和标准 capture 文案输出。

## Impact

- 影响 `.agents/skills/*` 中支持 `force-proceed`、follow-up 或自动 capture 的命令说明。
- 可能影响 `scripts/validate-agent-context-budget.py` 或新增轻量校验脚本，用于检查技能文件是否保留该门禁。
- 可能影响 workflow-sync/AI usage hook 的文档说明，但不改变业务 API、数据库表、Web、小程序或 MinIO 行为。
