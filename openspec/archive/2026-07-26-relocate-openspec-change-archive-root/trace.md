---
change_id: relocate-openspec-change-archive-root
status: archived
created_at: 2026-07-26 16:17:12
updated_at: 2026-07-26 16:28:00
source_requirement: null
source_bug: null
iteration: null
---

```yaml
change_id: relocate-openspec-change-archive-root
status: archived
lifecycle:
  proposed: 2026-07-26 16:17:12
  applied: 2026-07-26 16:17:12
  archived: 2026-07-26 16:28:00
source_requirement: null
source_bug: null
iteration: null
archive_root:
  canonical: openspec/archive/
  legacy: openspec/changes/archive/
  legacy_mode: read_only_fallback
```

# Trace

## 应用摘要

- Change 类型：纯 OpenSpec / 工作流治理 Change，无 REQ/BUG 来源。
- Sprint Inclusion Gate：豁免；`sync-workflow-status.py --event opsx.apply --change relocate-openspec-change-archive-root --sprint auto --dry-run` 返回 Sprint skipped，原因是 Change 未纳入 Sprint scope 且无 REQ/BUG 关联。
- 目录迁移：将 `openspec/changes/archive/<date>-<change-id>/` 历史包迁移到 `openspec/archive/<date>-<change-id>/`；迁移后删除空的 `openspec/changes/archive/` 目录。
- Canonical archive root：`openspec/archive/`。
- Legacy archive root：`openspec/changes/archive/`，仅作为脚本只读 fallback 与残留检查目标。

## 验证记录

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-07-26 16:17:12 | `openspec validate relocate-openspec-change-archive-root` | PASS |
| 2026-07-26 16:17:12 | `python scripts/validate-agent-context-budget.py` | PASS |
| 2026-07-26 16:17:12 | `uv run pytest tests/test_path_helpers.py tests/test_archived_path_residuals.py tests/test_sprint_archive_readiness.py tests/test_workflow_sync_time_drift.py tests/test_generate_sprint_fact_sheet.py` | PASS，53 passed |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-26 16:17:12 | `/opsx-apply relocate-openspec-change-archive-root` | 完成 archive root 迁移、规则/技能/脚本/测试更新和历史路径替换 |
| 2026-07-26 16:28:00 | `/opsx-archive relocate-openspec-change-archive-root` | OpenSpec CLI 完成 spec 合并后先输出到 legacy archive；已迁移归档包到 canonical `openspec/archive/2026-07-26-relocate-openspec-change-archive-root/` |
