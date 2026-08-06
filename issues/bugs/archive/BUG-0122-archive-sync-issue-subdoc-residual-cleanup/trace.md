---
bug_id: BUG-0122-archive-sync-issue-subdoc-residual-cleanup
status: done
lifecycle_stage: archive
created_at: 2026-08-06 11:29:58
updated_at: 2026-08-06 12:02:30
severity: medium
related_requirement:
related_bug:
related_change: fix-archive-sync-issue-subdoc-residual-cleanup
iteration: sprint-021
---

# BUG-0122 追踪记录

## 概要

归档同步阶段未自动清理已确认安全的 Issue 子文档状态残留，导致 `promote-issues-for-archive` 被 `capture.md` 中残留的 `captured` 状态阻断。

## 生命周期

```yaml
status: done
lifecycle_stage: archive
severity: medium
related_requirement:
related_bug:
related_change: fix-archive-sync-issue-subdoc-residual-cleanup
iteration: sprint-021
openspec_changes:
  - change_id: fix-archive-sync-issue-subdoc-residual-cleanup
    type: fix
    status: archived
```

## 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-08-06 12:01:54 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-archive-sync-issue-subdoc-residual-cleanup） |
| 2026-08-06 12:01:48 | /opsx-archive | Change `fix-archive-sync-issue-subdoc-residual-cleanup` 已归档，状态同步完成。 |
| 2026-08-06 11:58:11 | /opsx-apply | Change `fix-archive-sync-issue-subdoc-residual-cleanup` 已完成实现验证，后续归档已闭环。 |
| 2026-08-06 11:47:41 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-06 11:50:37 | sprint.propose | 纳入 sprint-021，后续已交付闭环。 |
| 2026-08-06 11:52:40 | bug.opsx | 创建 Change `fix-archive-sync-issue-subdoc-residual-cleanup`。 |
| 2026-08-06 11:29:58 | bug.capture | 创建缺陷记录。 |
| 2026-08-06 11:32:51 | bug.generate | 生成 bug.md，状态更新为 draft。 |
| 2026-08-06 11:41:58 | bug.complete | 补齐 root-cause、workaround、acceptance，评审前资料完成。 |
| 2026-08-06 11:47:08 | bug.review | 评审通过，状态更新为 approved。 |
