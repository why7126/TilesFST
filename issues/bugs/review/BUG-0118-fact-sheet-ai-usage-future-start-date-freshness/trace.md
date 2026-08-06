---
bug_id: BUG-0118-fact-sheet-ai-usage-future-start-date-freshness
status: in_sprint
severity: medium
created_at: 2026-08-06 08:35:36
updated_at: 2026-08-06 08:54:10
lifecycle_stage: review
lifecycle:
  captured: 2026-08-06 08:35:36
  generated: 2026-08-06 08:41:12
  completed: 2026-08-06 08:41:59
  reviewed: 2026-08-06 08:44:50
  approved: 2026-08-06 08:44:50
related_requirement:
related_bug: BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot
related_changes:
  - fix-fact-sheet-ai-usage-start-date-freshness
openspec_changes:
  - change_id: fix-fact-sheet-ai-usage-start-date-freshness
    type: fix
    status: proposed
iteration:
---

# BUG 追踪

```yaml
bug_id: BUG-0118-fact-sheet-ai-usage-future-start-date-freshness
status: in_sprint
severity: medium
lifecycle_stage: review
related_requirement:
related_bug: BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot
related_changes:
  - fix-fact-sheet-ai-usage-start-date-freshness
openspec_changes:
  - change_id: fix-fact-sheet-ai-usage-start-date-freshness
    type: fix
    status: proposed
iteration:
```

## 基本信息

| 字段 | 值 |
|---|---|
| 标题 | Fact Sheet AI usage fresh gate 将未来 Sprint start_date 当作 snapshot 新鲜度下限 |
| 严重等级 | medium |
| 来源 | `/bug-capture` |
| 相关 Sprint | sprint-020 |
| 相关历史缺陷 | BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-06 08:45:16 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-06 08:35:36 | `/bug-capture` | 记录 Fact Sheet AI usage fresh gate 将未来 Sprint start_date 当作 snapshot 新鲜度下限的问题。 |
| 2026-08-06 08:41:12 | `/bug-generate` | 生成 bug.md，状态推进为 draft。 |
| 2026-08-06 08:41:59 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，状态推进为 pending_review。 |
| 2026-08-06 08:44:50 | `/bug-review --approve` | 评审通过，允许进入 bug-opsx 与 Sprint 规划。 |
| 2026-08-06 08:52:17 | `/bug-opsx BUG-0118` | 创建 Change `fix-fact-sheet-ai-usage-start-date-freshness`，状态为 proposed。 |
