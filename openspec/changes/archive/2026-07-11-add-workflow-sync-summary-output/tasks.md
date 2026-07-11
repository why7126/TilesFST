## 1. Workflow Sync 报告实现

- [x] 1.1 为 `SyncReport` 增加 summary/detail 两种格式化路径，summary 输出聚合计数和关键上下文。
- [x] 1.2 为 `scripts/sync-workflow-status.py` 增加 `--output summary|detail` 参数，并将默认输出设为 summary。
- [x] 1.3 确保存在 errors 或 `--check` drift 时保留错误明细和可定位的文件线索。
- [x] 1.4 确保 detail 模式保持现有 updated/skipped 逐文件明细和退出码语义。

## 2. 工作流文档与技能约定

- [x] 2.1 更新 `.agents/skills/workflow-sync/SKILL.md`，说明成功路径打印 summary Workflow Sync Report。
- [x] 2.2 更新相关 source-command 技能的 Workflow Sync 输出约定，将成功输出从完整报告调整为摘要报告。
- [x] 2.3 如需补充长期治理规则，更新 `rules/agent-context-budget.md` 或 `rules/document-governance.md` 的对应说明。

## 3. 测试覆盖

- [x] 3.1 新增或扩展 Workflow Sync 单元测试，覆盖 summary 模式不输出长 skipped 列表。
- [x] 3.2 覆盖 detail 模式仍输出 updated/skipped 逐文件明细。
- [x] 3.3 覆盖 errors 或 `--check` drift 场景仍输出诊断信息并返回非零退出码。

## 4. 验证

- [x] 4.1 运行 Workflow Sync 相关 pytest。
- [x] 4.2 运行 `python scripts/sync-workflow-status.py --event opsx.propose --change add-workflow-sync-summary-output --sprint auto` 确认 summary 输出。
- [x] 4.3 运行 OpenSpec 校验并确认 change apply-ready。

## 归档验证摘要

- 验证命令与结果：`uv run pytest tests/test_workflow_sync_time_drift.py` 通过（11 passed）；`openspec validate add-workflow-sync-summary-output --strict` 通过；`python scripts/sync-workflow-status.py --event opsx.apply --change add-workflow-sync-summary-output --sprint auto` 通过且 `Errors: 0`。
- 验收结论：Workflow Sync 默认 summary 输出已实现，detail 输出与失败诊断保留，tasks 全部完成。
- 关联 Issue 或 Sprint 状态：无关联 REQ/BUG；纯技术治理 Change 未纳入 sprint，Workflow Sync 报告 sprint skipped 不阻塞归档。
- 归档路径或归档时间：待 `/opsx-archive add-workflow-sync-summary-output` 生成 `openspec/changes/archive/2026-07-11-add-workflow-sync-summary-output/`。
