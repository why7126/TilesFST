---
bug_id: BUG-0107-admin-certificate-list-main-image-name-only
status: done
severity: low
created_at: 2026-08-03 08:13:39
updated_at: 2026-08-03 12:02:41
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-03 08:13:39
  generated: 2026-08-03 08:20:11
  completed: 2026-08-03 08:22:37
  reviewed: 2026-08-03 08:26:56
  approved: 2026-08-03 08:26:56
iteration: sprint-018
openspec_changes:
  - change_id: fix-admin-certificate-list-main-image-name-only
    type: fix
    status: archived
related_requirement: null
related_bug: BUG-0089-admin-certificate-edit-image-filename-noise
---

# BUG Trace

```yaml
bug_id: BUG-0107-admin-certificate-list-main-image-name-only
status: done
severity: low
created_at: 2026-08-03 08:13:39
updated_at: 2026-08-03 12:02:41
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-03 08:13:39
  generated: 2026-08-03 08:20:11
  completed: 2026-08-03 08:22:37
  reviewed: 2026-08-03 08:26:56
  approved: 2026-08-03 08:26:56
iteration: sprint-018
openspec_changes:
  - change_id: fix-admin-certificate-list-main-image-name-only
    type: fix
    status: archived
related_requirement: null
related_bug: BUG-0089-admin-certificate-edit-image-filename-noise
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-03 12:02:41 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-admin-certificate-list-main-image-name-only） |
| 2026-08-03 12:02:24 | /opsx-archive | Change `fix-admin-certificate-list-main-image-name-only` 已归档，状态同步完成。 |
| 2026-08-03 09:01:49 | /opsx-apply | Change `fix-admin-certificate-list-main-image-name-only` apply 完成；后续已完成归档。 |
| 2026-08-03 08:41:10 | `/sprint-propose` | 纳入 sprint-018 正式范围，与 Change `fix-admin-certificate-list-main-image-name-only` 共同进入迭代规划。 |
| 2026-08-03 08:33:06 | `/bug-opsx` | 创建 OpenSpec Change `fix-admin-certificate-list-main-image-name-only`；后续已纳入 sprint-018 并归档。 |
| 2026-08-03 08:27:21 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-03 08:26:56 | `/bug-review --approve` | 评审通过，确认需要修复，状态更新为 approved。 |
| 2026-08-03 08:22:37 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，状态更新为 pending_review。 |
| 2026-08-03 08:20:11 | `/bug-generate` | 生成 bug.md，状态更新为 draft。 |
| 2026-08-03 08:13:39 | `/capture` | 记录管理后台证书列表证书字段显示图片或文件名称的问题，分类为 BUG。 |

- 2026-08-03 12:02:24 workflow-sync：状态同步为 done（Change archived）
