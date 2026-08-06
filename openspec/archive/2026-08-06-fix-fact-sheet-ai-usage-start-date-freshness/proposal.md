---
change_id: fix-fact-sheet-ai-usage-start-date-freshness
type: fix
status: proposed
created_at: 2026-08-06 08:52:17
updated_at: 2026-08-06 08:52:17
source_bug: BUG-0118-fact-sheet-ai-usage-future-start-date-freshness
---

# 修复 Fact Sheet AI usage start_date 新鲜度误判

## 背景

`BUG-0118-fact-sheet-ai-usage-future-start-date-freshness` 记录了 Sprint Fact Sheet 的 AI usage fresh gate 误判：当 `sprint.yaml:start_date` 是未来计划时间时，Fact Sheet 将该时间选为 `ai_usage_freshness_baseline.min_generated_at`，导致当前已生成且完整的 snapshot 被判定为 stale。

`sprint-020` 已出现该问题：独立 snapshot check 显示 `present` / `actual` / fresh gate pass，但 Fact Sheet summary 仍因未来 `start_date: 2026-08-19 09:00:00` 显示 `snapshot_status: stale` 与 `ai_usage_mode: estimated_fallback`。

## 变更范围

- 修正 Sprint Fact Sheet 计算 AI usage freshness baseline 的候选时间策略。
- 未来计划 `sprint.yaml:start_date` 与 `sprint.yaml:end_date` 均不得作为 `min_generated_at` 候选。
- 保留非未来周期时间、四件套 `updated_at` 等真实事实更新时间对 stale snapshot 的保护。
- 补充聚焦回归测试，覆盖 future `start_date`、future `end_date`、stale `updated_at` 和 `sprint-020` 类场景。

## 不在范围

- 不调整 AI usage snapshot 文件结构。
- 不修改 `/sprint-exps` 的矩阵展示格式。
- 不改动 `sprint-020` 的事实源日期。
- 不涉及 API、数据库、前端 Orval、小程序或 Docker 配置。

## 回滚计划

若修复导致 Fact Sheet stale 判定误放宽，可回滚本 Change 中对 baseline 候选策略和相关测试的改动，恢复现有 `sprint.yaml:start_date` 候选行为；回滚后继续使用 `scripts/extract-ai-usage.py --check-snapshot --sprint <sprint> --json` 作为临时独立校验手段，并在复盘中显式标注 Fact Sheet summary 可能误报。
