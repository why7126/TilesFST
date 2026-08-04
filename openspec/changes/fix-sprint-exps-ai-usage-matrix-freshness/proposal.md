---
created_at: 2026-08-04 23:30:00
updated_at: 2026-08-04 23:30:00
---

# 提案：修复 sprint-exps AI usage 矩阵新鲜度误判

## 背景

`/sprint-exps sprint-019` 复盘文档未输出 AI usage 四张矩阵。排查发现 `data/ai-usage/sprints/sprint-019.json` 已由 post-command hook 刷新为真实 `actual` snapshot，包含 totals 与 usage matrices；但 `scripts/generate-sprint-fact-sheet.py --summary` 仍将其标记为 `snapshot_status: stale` 与 `ai_usage_mode: estimated_fallback`。

根因是 Fact Sheet 使用 `sprint.yaml.end_date` 作为 snapshot `min_generated_at`。归档后的 `sprint-019` 计划结束时间为 `2026-08-18 18:00:00`，晚于当前归档和复盘时间，因此任何当前真实 snapshot 都会被误判为早于关键时间。

## 目标

- Sprint 已归档且计划结束日在未来时，不得使用未来 `end_date` 作为 AI usage snapshot 新鲜度下限。
- Fact Sheet 应从 Sprint 四件套 frontmatter 的 `updated_at`、`start_date`、非未来 `end_date` 中计算可解释的新鲜度下限。
- `/sprint-exps` 在 fresh gate pass 后必须按需读取完整 `usage_matrices` 并输出四张矩阵。
- 同步更新规范、技能和测试，避免后续复盘再次漏出矩阵。

## 非目标

- 不改变 AI usage command-run 聚合口径。
- 不改变真实 session JSONL 的采集和脱敏规则。
- 不直接修改 `openspec/specs/` 正式规格；本 Change 只提供 delta spec。
