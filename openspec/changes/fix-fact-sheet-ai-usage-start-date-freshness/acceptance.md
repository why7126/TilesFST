---
change_id: fix-fact-sheet-ai-usage-start-date-freshness
acceptance_status: pending
created_at: 2026-08-06 08:52:17
updated_at: 2026-08-06 08:52:17
source_bug: BUG-0118-fact-sheet-ai-usage-future-start-date-freshness
---

# 验收计划

## 验收项

| AC | 验收标准 | 证据 |
|---|---|---|
| AC-001 | 未来 `sprint.yaml:start_date` 不导致完整 AI usage snapshot 被判定 stale | 聚焦 pytest 与 Fact Sheet summary |
| AC-002 | 未来计划时间进入 `ai_usage_freshness_baseline.skipped[]`，不成为 `min_generated_at` source | 聚焦 pytest |
| AC-003 | 非未来 `updated_at` baseline 仍可阻止陈旧 snapshot | 聚焦 pytest |
| AC-004 | `sprint-020` 类场景 summary 可得到 `actual` / `present` | 聚焦 pytest 或手工 summary 输出 |

## 验收结果回填

| 时间 | 结论 | 证据 | 备注 |
|---|---|---|---|
| 待回填 | pending | 待 `/opsx-apply` 后补充 | 需与 BUG-0118 acceptance 同步闭环 |
