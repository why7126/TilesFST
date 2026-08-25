---
bug_id: BUG-0136-workflow-sync-bug-generate-captured-draft
status: done
severity: medium
created_at: 2026-08-22 21:13:43
updated_at: 2026-08-22 21:56:07
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-22 21:13:43
  generated: 2026-08-22 21:19:40
  completed: 2026-08-22 21:24:15
  reviewed: 2026-08-22 21:29:14
  approved: 2026-08-22 21:29:14
iteration: sprint-025
openspec_changes:
  - change_id: fix-workflow-sync-bug-generate-status-transition
    type: update
    status: archived
related_requirement: null
related_bug: null
related_change: fix-workflow-sync-bug-generate-status-transition
---

# BUG Trace

```yaml
bug_id: BUG-0136-workflow-sync-bug-generate-captured-draft
status: done
severity: medium
created_at: 2026-08-22 21:13:43
updated_at: 2026-08-22 21:34:27
lifecycle_stage: review
lifecycle:
  captured: 2026-08-22 21:13:43
  generated: 2026-08-22 21:19:40
  completed: 2026-08-22 21:24:15
  reviewed: 2026-08-22 21:29:14
  approved: 2026-08-22 21:29:14
iteration: sprint-025
openspec_changes:
  - change_id: fix-workflow-sync-bug-generate-status-transition
    type: update
    status: archived
related_requirement: null
related_bug: null
related_change: fix-workflow-sync-bug-generate-status-transition
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-22 21:55:31 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-workflow-sync-bug-generate-status-transition） |
| 2026-08-22 21:55:26 | /opsx-archive | Change `fix-workflow-sync-bug-generate-status-transition` 已归档，状态同步完成。 |
| 2026-08-22 21:48:55 | /opsx-apply | Change `fix-workflow-sync-bug-generate-status-transition` apply 完成，待 archive。 |
| 2026-08-22 21:34:27 | `/sprint-propose` | 纳入 sprint-025，修正 trace fenced YAML 与 registry 当前态同步漂移。 |
| 2026-08-22 21:29:47 | lifecycle-stage-migrate | plan → review（/bug-review） |
| 2026-08-22 21:29:14 | `/bug-review` | 默认评审通过，确认进入 approved，后续需先纳入 Sprint。 |
| 2026-08-22 21:24:15 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，状态进入 pending_review。 |
| 2026-08-22 21:19:40 | `/bug-generate` | 根据 capture 生成正式 `bug.md`，状态更新为 draft；Workflow Sync detail 显示 `bug.generate` 对 trace 与 registry 为 no delta，已作为本 BUG 的复现证据。 |
| 2026-08-22 21:13:43 | `/capture` | 记录 Workflow Sync 对 `bug.generate` 未主动从 captured 推进 draft 的问题。 |

- 2026-08-22 21:55:26 workflow-sync：状态同步为 done（Change archived）
