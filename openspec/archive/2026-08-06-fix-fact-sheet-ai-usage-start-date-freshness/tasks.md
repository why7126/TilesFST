---
change_id: fix-fact-sheet-ai-usage-start-date-freshness
created_at: 2026-08-06 08:52:17
updated_at: 2026-08-06 08:52:17
---

# 任务清单

- [x] 修改 `scripts/generate-sprint-fact-sheet.py` 的 AI usage freshness baseline 候选策略，使未来 `sprint.yaml:start_date` 进入 skipped 而非 candidates。
- [x] 保持未来 `sprint.yaml:end_date` 的跳过行为，并统一 skipped reason 为 `future-planned-time`。
- [x] 补充 `tests/test_generate_sprint_fact_sheet.py` 回归测试：未来 `start_date` 不阻塞完整 snapshot。
- [x] 补充回归测试：未来计划时间进入 `ai_usage_freshness_baseline.skipped[]`，不得成为 `min_generated_at` source。
- [x] 补充负向回归测试：四件套 `updated_at` 晚于 snapshot `generated_at` 时仍判定 stale。
- [x] 针对 `sprint-020` 类场景复核 Fact Sheet summary 可得到 `ai_usage_mode: actual`、`snapshot_status: present`。
- [x] 运行聚焦测试：`python3 -m pytest tests/test_generate_sprint_fact_sheet.py`。
- [x] 运行 OpenSpec 语言校验：`python3 scripts/validate-openspec-language.py`。
- [x] 归档前评估是否需要在 `docs/knowledge-base/incidents/` 沉淀 Fact Sheet freshness baseline 经验；如不需要，在验收记录中说明原因。
