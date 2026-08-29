---
created_at: 2026-08-27 00:00:00
updated_at: 2026-08-27 00:00:00
---

# 测试计划

- 运行 `uv run pytest tests/test_workflow_sync_time_drift.py -q`，验证 Workflow Sync 聚焦行为。
- 运行 `python scripts/validate-agent-context-budget.py`、`python scripts/validate-openspec-language.py`、`python scripts/validate-directory-structure.py`。
- 运行 `openspec validate fix-workflow-sync-sprint-propose-iteration`。

业务测试不适用：本次不修改 `src/`、API、DB、Web、小程序或管理端业务实现。

