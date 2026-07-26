## Why

Workflow Sync 在成功路径中会输出较长的 `Skipped (no delta)` 列表，尤其是 `opsx.propose`、`req-*`、`bug-*` 等只更新少量目标文件时，长 skipped 清单会挤占上下文并降低人工确认效率。

需要为 Workflow Sync 增加摘要输出模式，让成功路径默认展示关键结果、计数和必要提示；仅在失败、调试或显式请求详细输出时展开逐文件列表。

## What Changes

- 为 `scripts/sync-workflow-status.py` 增加 summary 输出模式，报告 updated / skipped / errors 的聚合计数、focus 对象、sprint 解析状态和关键警告。
- 在成功路径中减少长 `Skipped (no delta)` 列表输出；默认或推荐输出只保留摘要，不逐条打印无变化文件。
- 保留详细模式，用于失败排查、`--check` drift 定位、人工调试或兼容旧输出需求。
- 更新 Workflow Sync 技能说明，要求成功时打印 summary report，失败时展开错误和必要文件线索。
- 补充测试覆盖 summary 输出、详细输出和错误输出，确保不改变实际同步写入行为。

## Capabilities

### New Capabilities

### Modified Capabilities
- `agent-workflow-tooling`: Workflow Sync 输出契约新增 summary 模式，并约束成功路径不得默认输出长 skipped 列表。

## Impact

- 影响脚本：`scripts/sync-workflow-status.py`、`scripts/workflow_sync/engine.py`。
- 影响技能文档：`.agents/skills/workflow-sync/SKILL.md` 以及调用该报告的 source-command 技能输出约定。
- 影响测试：新增或扩展 Workflow Sync 报告格式测试。
- 不影响 API、数据库、Web、小程序、管理端和 Orval 生成物。
