---
bug_id: BUG-0139-admin-avatar-upload-nginx-redirect-cors
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
bug_id: BUG-0139-admin-avatar-upload-nginx-redirect-cors
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
| 2026-08-25 14:36:24 | `/bug-capture` | 记录管理后台头像上传无尾斜杠路径被 Nginx 301 重定向后丢失宿主机端口，导致 CORS 拦截的问题；来源为用户截图与 `/explore` 只读分析。 |
