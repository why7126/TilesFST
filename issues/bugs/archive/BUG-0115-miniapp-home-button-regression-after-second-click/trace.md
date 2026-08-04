---
bug_id: BUG-0115-miniapp-home-button-regression-after-second-click
status: done
lifecycle_stage: archive
severity: high
priority: P1
created_at: 2026-08-04 08:44:39
updated_at: 2026-08-04 09:29:17
lifecycle:
  captured: 2026-08-04 08:44:39
  generated: 2026-08-04 08:52:50
  completed: 2026-08-04 08:55:33
  reviewed: 2026-08-04 09:01:04
  approved: 2026-08-04 09:01:04
iteration: sprint-019
openspec_changes:
  - change_id: fix-miniapp-home-button-repeat-click-regression
    type: fix
    status: archived
related_requirement: null
related_bug: BUG-0109-miniapp-home-button-one-time-failure
related_change: null
---

# Trace

## 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-08-04 09:28:51 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-home-button-repeat-click-regression） |
| 2026-08-04 09:28:21 | /opsx-archive | Change `fix-miniapp-home-button-repeat-click-regression` 已归档，状态同步完成。 |
| 2026-08-04 09:13:47 | /opsx-apply | Change `fix-miniapp-home-button-repeat-click-regression` apply 完成，已 archive。 |
| 2026-08-04 09:07:53 | sprint.propose | 纳入 Sprint 019 正式范围，关联 Change `fix-miniapp-home-button-repeat-click-regression`。 |
| 2026-08-04 09:08:00 | bug.opsx | 创建 OpenSpec Change `fix-miniapp-home-button-repeat-click-regression`，状态 archived。 |
| 2026-08-04 09:01:38 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-04 09:01:04 | bug.review | 评审通过，确认修复；允许后续 bug-opsx 与 Sprint 规划。 |
| 2026-08-04 08:55:33 | bug.complete | 补齐 root-cause、workaround、acceptance，状态曾推进为 review_ready，现已闭环。 |
| 2026-08-04 08:52:50 | bug.generate | 生成正式缺陷稿 bug.md，完成初稿生成，现已闭环。 |
| 2026-08-04 08:44:39 | bug.capture | 通过 /capture 记录小程序返回首页按钮第二次点击失效回归问题。 |

- 2026-08-04 09:28:21 workflow-sync：状态同步为 done（Change archived）
