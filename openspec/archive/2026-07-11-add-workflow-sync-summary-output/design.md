## Context

当前 `scripts/workflow_sync/engine.py` 的 `SyncReport.format_text()` 会在报告中逐条列出所有 `updated` 和 `skipped` 文件。Workflow Sync 的 `skipped` 在成功路径通常表示“无变化”，不是错误；但当 sprint 或 issue scope 较大时，这个列表会变长，导致 source-command 输出噪音增加。

项目已有 `rules/agent-context-budget.md` 要求 Workflow Sync 成功时只报告摘要，失败时再按报告定位具体 marker 或文件片段。因此本变更将脚本报告能力和规则约束对齐。

## Goals / Non-Goals

**Goals:**

- 提供 summary 输出模式，显示事件、focus 对象、sprint 解析状态、updated/skipped/error 计数和必要提示。
- 成功路径默认减少 `Skipped (no delta)` 明细，只展示聚合计数。
- 保留 verbose/detail 输出，便于人工调试和兼容需要逐文件明细的场景。
- 失败输出仍然包含 errors；必要时可以同时展开 updated/skipped 明细帮助定位。
- 不改变 Workflow Sync 的同步算法、文件写入、`--check` drift 判断和退出码语义。

**Non-Goals:**

- 不重写 Workflow Sync 的 patch/derive/collect 逻辑。
- 不改变 sprint 自动解析规则。
- 不调整 REQ/BUG/Sprint/OpenSpec 生命周期状态机。
- 不引入外部依赖。

## Decisions

1. 在 CLI 层增加输出格式参数。

   `scripts/sync-workflow-status.py` 通过 `workflow_sync.engine.build_parser()` 增加 `--output summary|detail`，默认使用 `summary`。`detail` 输出保持现有逐文件风格，降低迁移风险。

2. 在 `SyncReport` 内部保留结构化结果，新增格式化方法而不是改变数据结构。

   `SyncReport.updated`、`SyncReport.skipped`、`SyncReport.errors` 继续保存完整数据；新增 `format_summary()` 或让 `format_text(mode=...)` 按模式输出。这样测试和未来自动化仍可访问完整结果。

3. summary 报告只压缩成功噪音，不隐藏失败。

   summary 输出 MUST 包含 `Updated: <n>`、`Skipped: <n>`、`Errors: <n>` 这类计数。若存在错误，报告 MUST 展开 `Errors` 列表；若需要排查无变化文件，可提示使用 `--output detail`。

4. source-command 技能文档改为打印 summary report。

   `.agents/skills/workflow-sync/SKILL.md` 和相关 source-command 约定应表达“成功路径 summary，失败路径 detail/错误线索”。命令仍必须检查退出码为 0。

## Risks / Trade-offs

- [Risk] 调用方或人工习惯依赖旧的 skipped 明细。
  Mitigation: 保留 `--output detail`，并在 summary 中提示可用 detail 查看逐文件列表。

- [Risk] `--check` 场景需要知道 drift 文件。
  Mitigation: `--check` 有 drift 时属于失败路径，summary MUST 展开 errors；实现时可让失败或 `--output detail` 展示 updated 文件明细，确保定位能力不丢失。

- [Risk] 技能文档仍要求打印完整 Workflow Sync Report。
  Mitigation: 更新 Workflow Sync 技能与相关 source-command 文档措辞，明确 summary report 属于 Workflow Sync Report 的有效形式。
