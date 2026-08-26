---
bug_id: BUG-0139-admin-avatar-upload-nginx-redirect-cors
status: done
severity: high
created_at: 2026-08-25 14:36:24
updated_at: 2026-08-25 18:21:51
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-25 14:36:24
  generated: null
  completed: 2026-08-25 15:35:15
  reviewed: 2026-08-25 15:47:17
  approved: 2026-08-25 15:47:17
iteration: sprint-026
openspec_changes:
  - change_id: fix-admin-avatar-upload-nginx-redirect-cors
    type: update
    status: archived
related_requirement: null
related_bug: null
related_change: fix-admin-avatar-upload-nginx-redirect-cors
---

# BUG Trace

```yaml
bug_id: BUG-0139-admin-avatar-upload-nginx-redirect-cors
status: done
severity: high
created_at: 2026-08-25 14:36:24
updated_at: 2026-08-25 17:06:20
lifecycle_stage: review
lifecycle:
  captured: 2026-08-25 14:36:24
  generated: null
  completed: 2026-08-25 15:35:15
  reviewed: 2026-08-25 15:47:17
  approved: 2026-08-25 15:47:17
iteration: sprint-026
openspec_changes:
  - change_id: fix-admin-avatar-upload-nginx-redirect-cors
    type: update
    status: archived
related_requirement: null
related_bug: null
related_change: fix-admin-avatar-upload-nginx-redirect-cors
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-25 17:43:49 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-admin-avatar-upload-nginx-redirect-cors） |
| 2026-08-25 17:43:45 | /opsx-archive | Change `fix-admin-avatar-upload-nginx-redirect-cors` 已归档，状态同步完成。 |
| 2026-08-25 17:19:13 | /opsx-apply | Change `fix-admin-avatar-upload-nginx-redirect-cors` apply 完成，待 archive。 |
| 2026-08-25 17:04:09 | `/sprint-propose` | 纳入 sprint-026 正式范围，待创建 OpenSpec 修复 Change。 |
| 2026-08-25 15:47:17 | `/bug-review` | 根因 confirmed 门禁通过，评审通过，建议纳入 Sprint 后创建修复 Change。 |
| 2026-08-25 15:47:38 | lifecycle-stage-migrate | plan → review（/bug-review） |
| 2026-08-25 15:35:15 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；根因状态为 confirmed，待评审。 |
| 2026-08-25 14:36:24 | `/bug-capture` | 记录管理后台头像上传无尾斜杠路径被 Nginx 301 重定向后丢失宿主机端口，导致 CORS 拦截的问题；来源为用户截图与 `/explore` 只读分析。 |

- 2026-08-25 17:43:45 workflow-sync：状态同步为 done（Change archived）
