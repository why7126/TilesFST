---
change_id: fix-fact-sheet-ai-usage-start-date-freshness
acceptance_status: passed
created_at: 2026-08-06 08:52:17
updated_at: 2026-08-06 10:58:30
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
| 2026-08-06 10:58:30 | passed | `python3 -m pytest tests/test_generate_sprint_fact_sheet.py`，26 passed | 覆盖 future start_date、future end_date、stale updated_at 和 Fact Sheet summary actual/present 路径；不新增 incidents，原因是 sprint-020 retrospective 与 BUG-0118 文档已承载经验入口 |
