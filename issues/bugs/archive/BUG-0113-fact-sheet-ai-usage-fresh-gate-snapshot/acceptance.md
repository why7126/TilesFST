---
bug_id: BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot
acceptance_status: passed
created_at: 2026-08-04 08:22:00
updated_at: 2026-08-04 23:12:32
---

# Acceptance Criteria

## 回归验收

| ID | 验收项 | 通过标准 |
|---|---|---|
| AC-001 | 已刷新 snapshot 通过 fresh gate | 构造或生成一个当前有效的 Fact Sheet AI usage snapshot 后，fresh gate 输出 fresh/pass，不再误报 stale。 |
| AC-002 | 过期 snapshot 仍被拦截 | 构造过期 timestamp 或明确 stale 状态的 snapshot 后，fresh gate 输出 stale/fail，并说明过期原因。 |
| AC-003 | usage mode 映射一致 | refreshed / actual / skipped / unavailable / stale 等状态映射到预期 mode，不出现已刷新状态被映射为 unavailable、skipped 或 stale。 |
| AC-004 | 路径与缓存一致 | fresh gate 读取的 snapshot 与刷新流程写入的 snapshot 为同一事实源，不读取旧路径、旧缓存或旧 payload。 |
| AC-005 | 回归测试覆盖 | 新增或更新测试覆盖 fresh snapshot、stale snapshot、缺失 snapshot、mode fallback 的核心分支。 |
| AC-006 | 报告输出可解释 | gate 输出包含足够的 snapshot status / timestamp / mode 摘要，便于判断 fresh/stale 结论来源。 |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-04 23:12:32
accepted_by: workflow-sync
source_change: fix-fact-sheet-ai-usage-fresh-gate-snapshot
source_sprint: sprint-019
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

## /opsx-apply 实现证据

| AC | 证据 | 结论 |
|---|---|---|
| AC-001 | `tests/test_ai_usage.py::test_check_sprint_snapshot_status_present_missing_stale_failed`、`tests/test_generate_sprint_fact_sheet.py::test_fact_sheet_reads_ai_usage_snapshot` | 已覆盖有效 snapshot fresh gate pass。 |
| AC-002 | `tests/test_ai_usage.py::test_check_sprint_snapshot_status_present_missing_stale_failed`、`tests/test_generate_sprint_fact_sheet.py::test_fact_sheet_does_not_treat_stale_snapshot_as_actual` | 已覆盖过期 snapshot stale blocker。 |
| AC-003 | `tests/test_ai_usage.py::test_sprint_snapshot_fresh_gate_blocks_coverage_and_matrix_gaps` | 已覆盖 coverage / matrix 缺口时 snapshot 可保持 present，但 `ai_usage_mode` 降级为 `estimated_fallback` 且 fresh gate blocker。 |
| AC-004 | `scripts/ai_usage.py::check_sprint_snapshot` | fresh gate 统一基于同一 snapshot payload 的 `generated_at`、coverage、totals 与 `usage_matrices` 计算。 |
| AC-005 | `pytest tests/test_ai_usage.py tests/test_generate_sprint_fact_sheet.py` | 53 passed。 |
| AC-006 | `scripts/ai_usage.py::sprint_snapshot_fresh_gate`、`tests/test_generate_sprint_fact_sheet.py::test_fact_sheet_summary_exposes_ai_usage_fresh_gate_without_evidence_hints` | fresh gate compact 输出包含 snapshot status、usage mode、generated_at、coverage、矩阵 presence、warning_count 和 recommended_action。 |
