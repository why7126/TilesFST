---
bug_id: BUG-0140-admin-current-user-avatar-missing-object
status: captured
severity: high
created_at: 2026-08-25 14:36:24
updated_at: 2026-08-25 14:36:24
lifecycle_stage: plan
lifecycle:
  captured: 2026-08-25 14:36:24
  generated: null
  completed: null
  reviewed: null
  approved: null
iteration: null
openspec_changes: []
related_requirement: null
related_bug: null
related_change: null
---

# BUG Trace

```yaml
bug_id: BUG-0140-admin-current-user-avatar-missing-object
status: captured
severity: high
created_at: 2026-08-25 14:36:24
updated_at: 2026-08-25 14:36:24
lifecycle_stage: plan
lifecycle:
  captured: 2026-08-25 14:36:24
  generated: null
  completed: null
  reviewed: null
  approved: null
iteration: null
openspec_changes: []
related_requirement: null
related_bug: null
related_change: null
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-25 14:36:24 | `/bug-capture` | 记录当前登录用户 `avatar_object_key` 指向缺失对象，导致 `/media/images/default/user/avatars/*.png` 返回 404 的问题；来源为用户描述。 |
