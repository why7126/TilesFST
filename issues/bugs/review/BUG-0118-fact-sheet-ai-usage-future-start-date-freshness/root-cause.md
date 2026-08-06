---
bug_id: BUG-0118-fact-sheet-ai-usage-future-start-date-freshness
classification: code
created_at: 2026-08-06 08:41:59
updated_at: 2026-08-06 08:42:36
---

# 根因分析

## 直接原因

`scripts/generate-sprint-fact-sheet.py` 在计算 `ai_usage_freshness_baseline.min_generated_at` 时，将 `sprint.yaml:start_date` 作为候选时间加入 baseline，且默认允许未来时间参与比较。

当 `sprint-020` 的 `start_date: 2026-08-19 09:00:00` 晚于当前 snapshot 的 `generated_at: 2026-08-06T00:34:43.070618Z` 时，Fact Sheet 将未来计划开始时间选为 `min_generated_at`。随后 `scripts/ai_usage.py` 的 snapshot 检查逻辑把 `generated_at < min_generated_at` 判为 `snapshot-stale`，导致 summary 降级为 `snapshot_status: stale`、`ai_usage_mode: estimated_fallback`。

## 根本原因

Freshness baseline 混用了“计划时间”和“文档/数据更新时间”两类语义：

- `updated_at` 可作为 snapshot 是否覆盖最新文档事实的下限。
- 已发生的 Sprint 周期时间可辅助判断 snapshot 是否覆盖 Sprint 生命周期。
- 未来计划 `start_date` / `end_date` 不代表当前已有事实已经发生，不应阻塞当前已生成且完整的 snapshot。

现有逻辑已对 `sprint.yaml:end_date` 设置 `allow_future=False`，但 `sprint.yaml:start_date` 仍沿用默认 `allow_future=True`，造成相同性质的未来计划时间处理不一致。

## 触发条件

同时满足以下条件时触发：

1. Sprint 的 `sprint.yaml:start_date` 是未来时间。
2. AI usage snapshot 已在当前时间生成，且早于该未来 `start_date`。
3. `python scripts/generate-sprint-fact-sheet.py --sprint <sprint> --summary` 通过 Fact Sheet baseline 调用 snapshot 检查。
4. snapshot 本身为 `actual` / `present`，且 `totals`、`coverage`、`usage_matrices` 完整。

## 分类

- 分类：`code`
- 模块：Sprint Fact Sheet / AI usage snapshot freshness gate
- 影响脚本：`scripts/generate-sprint-fact-sheet.py`、`scripts/ai_usage.py`

## 证据

- `scripts/generate-sprint-fact-sheet.py` 中 `start_date` 进入候选 baseline 时未禁用未来时间。
- `scripts/generate-sprint-fact-sheet.py` 中 `end_date` 已使用 `allow_future=False`。
- `scripts/ai_usage.py` 中当 `generated_at < min_generated_at` 时追加 `snapshot-stale` warning。
- `docs/knowledge-base/retrospectives/sprint-020-retrospective.md` 记录独立 snapshot check 为 `present` / `actual` / fresh gate pass，但 Fact Sheet summary 因未来 `start_date` 误判 stale。
