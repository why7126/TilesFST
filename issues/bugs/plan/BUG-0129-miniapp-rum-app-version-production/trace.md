---
bug_id: BUG-0129-miniapp-rum-app-version-production
status: draft
severity: medium
created_at: 2026-08-12 09:21:24
updated_at: 2026-08-12 09:42:46
lifecycle_stage: plan
lifecycle:
  captured: 2026-08-12 09:21:24
  generated: 2026-08-12 09:42:46
  completed: null
  reviewed: null
  approved: null
iteration: null
openspec_changes: []
related_requirement: null
related_bug: null
---

# BUG Trace

```yaml
bug_id: BUG-0129-miniapp-rum-app-version-production
status: draft
severity: medium
created_at: 2026-08-12 09:21:24
updated_at: 2026-08-12 09:42:46
lifecycle_stage: plan
lifecycle:
  captured: 2026-08-12 09:21:24
  generated: 2026-08-12 09:42:46
  completed: null
  reviewed: null
  approved: null
iteration: null
openspec_changes: []
related_requirement: null
related_bug: null
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-12 09:42:46 | `/bug-generate` | 生成 `bug.md`，将小程序版本号、request_id、指标标签、性能观测空态和聚合隐藏分组维度统一纳入 BUG-0129 正式缺陷范围。 |
| 2026-08-12 09:21:24 | `/bug-capture` | 记录小程序 RUM 将 `production` 环境名作为 `app_version` 上报，导致管理后台性能观测表版本号显示异常；用户补充小程序与 Web 管理后台应使用统一版本号。 |
