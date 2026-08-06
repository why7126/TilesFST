---
change_id: fix-fact-sheet-ai-usage-start-date-freshness
created_at: 2026-08-06 08:52:17
updated_at: 2026-08-06 08:52:17
---

# 测试计划

## 聚焦测试

- `python3 -m pytest tests/test_generate_sprint_fact_sheet.py`

## 覆盖点

- future `sprint.yaml:start_date` 被跳过。
- future `sprint.yaml:end_date` 继续被跳过。
- stale `updated_at` baseline 仍生效。
- `ai_usage_snapshot` 在 snapshot 完整时保持 `actual` / `present`。

## 非适用测试

- 不涉及 API，不需要 Orval。
- 不涉及数据库迁移。
- 不涉及 Web、小程序或 Docker Compose。
