---
bug_id: BUG-0057-api-governance-tags-known-debt
status: in_sprint
lifecycle_stage: review
created_at: 2026-07-04 15:25:45
updated_at: 2026-07-05 07:52:26
---

```yaml
status: in_sprint
lifecycle:
  captured: 2026-07-04 15:25:45
  generated: 2026-07-04 22:21:01
  completed: 2026-07-04 22:27:55
  reviewed: 2026-07-04 22:32:37
openspec_changes:
  - change_id: fix-api-governance-route-tags-known-debt
    type: fix
    status: proposed
related_requirement:
related_change: fix-api-governance-route-tags-known-debt
iteration: sprint-005
```

# Trace

## 变更记录

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-07-05 07:52:26 | bug-opsx | 创建 OpenSpec Change `fix-api-governance-route-tags-known-debt`，进入 proposed |
| 2026-07-04 22:42:09 | sprint-propose | 纳入 `sprint-005` 正式范围；OpenSpec Change 待 `/bug-opsx` 创建 |
| 2026-07-04 22:33:13 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-04 22:32:37 | bug-review | Approved，确认需要修复，可进入 bug-opsx |
| 2026-07-04 22:27:55 | bug-complete | 补齐 root-cause、workaround、acceptance，状态推进为 pending_review |
| 2026-07-04 22:21:01 | bug-generate | 生成 `bug.md`，状态推进为 draft |
| 2026-07-04 15:25:45 | bug-capture | 记录 API governance route tags `known-debt` 清理失败缺陷 |
