---
bug_id: BUG-0118-fact-sheet-ai-usage-future-start-date-freshness
acceptance_status: not_started
created_at: 2026-08-06 08:41:59
updated_at: 2026-08-06 08:55:15
---

# 验收标准

## 回归 AC

### AC-001 未来 start_date 不阻塞完整 snapshot

给定一个 Sprint 的 `sprint.yaml:start_date` 晚于当前 snapshot `generated_at`，且 snapshot 为 `actual` / `present`，并包含完整 `totals`、`coverage`、`usage_matrices`：

- 当运行 `python3 scripts/generate-sprint-fact-sheet.py --sprint <sprint> --summary`；
- 则 Fact Sheet summary 不应仅因未来 `start_date` 返回 `snapshot_status: stale`；
- 且 `ai_usage_snapshot.fresh_gate.status` 应保持 `pass`。

### AC-002 future planned time 应进入 skipped 而非 candidates

给定 `sprint.yaml:start_date` 或 `sprint.yaml:end_date` 是未来计划时间：

- 当计算 `ai_usage_freshness_baseline`；
- 则该未来计划时间应被记录到 `skipped`，reason 为 `future-planned-time` 或等价说明；
- 且不得成为 `min_generated_at` 的候选来源。

### AC-003 非未来时间 baseline 仍生效

给定 Sprint 四件套存在 `updated_at`，且 snapshot `generated_at` 早于该更新时间：

- 当运行 Fact Sheet summary；
- 则 freshness gate 仍应判定 snapshot stale；
- 防止修复未来计划时间误判时放宽真实陈旧 snapshot 的保护。

### AC-004 sprint-020 回归

针对 `sprint-020`：

- `iterations/archive/sprint-020/sprint.yaml:start_date` 保持 `2026-08-19 09:00:00`；
- 运行 Fact Sheet summary 后，`ai_usage_freshness_baseline.source` 不应为 `sprint.yaml:start_date`；
- `ai_usage_snapshot.snapshot_status` 应为 `present`；
- `ai_usage_snapshot.ai_usage_mode` 应为 `actual`；
- 满足输出真实 token 成本矩阵的条件。

## 建议测试

- 补充或更新 `tests/test_generate_sprint_fact_sheet.py`，覆盖未来 `start_date` 被跳过。
- 保留已有未来 `end_date` 被跳过的回归语义。
- 增加一个陈旧 `updated_at` baseline 的负向用例，确保 fresh gate 未被整体绕过。

## 验收结果回填

```yaml
acceptance_status: not_started
accepted_at: null
accepted_by: null
source_change: fix-fact-sheet-ai-usage-start-date-freshness
source_sprint: null
evidence: []
failed_items: []
source_event: bug.opsx
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

