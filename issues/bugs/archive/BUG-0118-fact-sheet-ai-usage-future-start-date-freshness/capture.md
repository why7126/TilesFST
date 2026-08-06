---
bug_id: BUG-0118-fact-sheet-ai-usage-future-start-date-freshness
status: done
created_at: 2026-08-06 08:35:36
updated_at: 2026-08-06 12:04:01
severity_hint: medium
environment: local
related_requirement:
related_bug: BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot
---

# 现象

Fact Sheet AI usage fresh gate 将未来 Sprint `start_date` 当作 snapshot 新鲜度下限，导致 `/sprint-exps` 在 snapshot 文件本身为 `actual` / `present` 且覆盖完整时，仍显示 `snapshot_status: stale`、`ai_usage_mode: estimated_fallback`，从而无法输出真实 token 成本矩阵。

# 复现步骤

1. 使用已归档的 `sprint-020`。
2. 确认 `iterations/archive/sprint-020/sprint.yaml` 中 `start_date: 2026-08-19 09:00:00`，而当前执行日期为 2026-08-06。
3. 执行 `/sprint-archive` 或 `/sprint-exps` post-command hook 刷新 AI usage snapshot。
4. 运行 `python scripts/generate-sprint-fact-sheet.py --sprint sprint-020 --summary`。
5. 观察 Fact Sheet summary 中 `ai_usage_snapshot.fresh_gate.status`、`snapshot_status` 与 `ai_usage_mode`。

# 期望 vs 实际

期望：

- 未来计划 `start_date` / `end_date` 不应作为当前 snapshot 的 freshness blocker。
- 当 snapshot 文件为 actual/present，且 totals、coverage、usage_matrices 均完整时，fresh gate 应允许输出 `--ai-usage-markdown` 真实成本矩阵。

实际：

- Fact Sheet summary 将未来 `sprint.yaml:start_date` 选为 `min_generated_at`。
- 当前时间生成的 snapshot 被判定早于该下限，返回 `snapshot_status: stale`、`ai_usage_mode: estimated_fallback`。
- `/sprint-exps` 因 fresh gate blocker 没有输出真实 token 成本矩阵。

# 附件

- 相关 Sprint：`iterations/archive/sprint-020/`
- 相关命令：`python scripts/generate-sprint-fact-sheet.py --sprint sprint-020 --summary`
- 相关历史缺陷：`BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot`
