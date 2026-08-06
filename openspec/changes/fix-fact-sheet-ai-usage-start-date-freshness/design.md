---
change_id: fix-fact-sheet-ai-usage-start-date-freshness
created_at: 2026-08-06 08:52:17
updated_at: 2026-08-06 08:52:17
---

# 设计说明

## 根因

`scripts/generate-sprint-fact-sheet.py` 的 `ai_usage_freshness_baseline` 会从 Sprint 元数据和四件套 frontmatter 中收集候选时间，并选择最大值作为 `min_generated_at`。其中：

- `sprint.yaml:end_date` 已使用 `allow_future=False`，未来计划结束时间会进入 `skipped`。
- `sprint.yaml:start_date` 仍使用默认 `allow_future=True`，未来计划开始时间会进入 `candidates`。

当未来 `start_date` 晚于当前 snapshot `generated_at` 时，`scripts/ai_usage.py` 按 `generated_at < min_generated_at` 追加 `snapshot-stale` warning，进而让 Fact Sheet summary 降级为 `estimated_fallback`。

## 修复策略

1. 将 `sprint.yaml:start_date` 与 `sprint.yaml:end_date` 统一视为计划周期时间。
2. 当计划周期时间晚于当前执行时间时，记录到 `ai_usage_freshness_baseline.skipped[]`，原因使用 `future-planned-time`。
3. `min_generated_at` 只从非未来计划周期时间与文档事实更新时间中选取。
4. 保持 `scripts/ai_usage.py` 的 stale 检查语义不变，避免绕过真正过期的 snapshot。

## 测试方案

- 在 `tests/test_generate_sprint_fact_sheet.py` 中构造未来 `start_date`，确认 summary 不因该值 stale。
- 确认未来 `start_date` 出现在 `skipped`，且不出现在 `candidates`。
- 保留或补充未来 `end_date` 的同类断言。
- 构造四件套 `updated_at` 晚于 snapshot `generated_at` 的负向用例，确认 stale 仍触发。
- 针对 `sprint-020` 类 fixture 确认 baseline source 不再为 `sprint.yaml:start_date`，summary 可输出 `actual` / `present`。

## 风险与兼容

- 风险：如果某些历史 Sprint 依赖未来 `start_date` 作为 stale blocker，修复后会改变其 Fact Sheet summary。
- 缓解：未来计划时间本身不代表事实已经发生，跳过未来值符合已有 `end_date` 语义；真实 stale 仍由 `updated_at` 和非未来候选时间保护。
- 兼容：不改 AI usage snapshot schema，不影响已有 snapshot 文件读取。
