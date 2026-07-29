---
bug_id: BUG-0089-admin-certificate-edit-image-filename-noise
status: done
lifecycle_stage: archive
severity: low
created_at: 2026-07-29 08:08:23
updated_at: 2026-07-29 09:21:55
related_requirement: REQ-0078-certificate-multiple-images-main-image
related_bug:
iteration: sprint-013
openspec_changes:
  - change_id: fix-admin-certificate-image-filename-noise
    type: fix
    status: archived
---

# 缺陷追踪

## 基本信息

```yaml
bug_id: BUG-0089-admin-certificate-edit-image-filename-noise
bug_name: admin-certificate-edit-image-filename-noise
status: done
severity: low
environment: local
related_requirement: REQ-0078-certificate-multiple-images-main-image
related_bug: null
iteration: sprint-013
openspec_changes:
  - change_id: fix-admin-certificate-image-filename-noise
    type: fix
    status: archived
lifecycle:
  captured: 2026-07-29 08:08:23
  generated: 2026-07-29 08:24:21
  completed: 2026-07-29 08:31:34
  reviewed: 2026-07-29 08:36:14
  approved: 2026-07-29 08:36:14
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-29 09:08:00 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-admin-certificate-image-filename-noise） |
| 2026-07-29 09:07:43 | /opsx-archive | Change `fix-admin-certificate-image-filename-noise` 已归档，状态同步完成。 |
| 2026-07-29 08:57:12 | /opsx-apply | Change `fix-admin-certificate-image-filename-noise` apply 完成，待 archive。 |
| 2026-07-29 08:56:47 | /opsx-apply | Change `fix-admin-certificate-image-filename-noise` apply 进行中，待补齐剩余验收。 |
| 2026-07-29 08:44:45 | `/bug-opsx` | 创建 OpenSpec Change `fix-admin-certificate-image-filename-noise`。 |
| 2026-07-29 08:38:46 | `/sprint-propose` | 纳入 sprint-013 正式范围，待创建修复 Change。 |
| 2026-07-29 08:36:38 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-29 08:36:14 | `/bug-review --approve` | 缺陷评审通过，确认修复。 |
| 2026-07-29 08:31:34 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，状态更新为 pending_review。 |
| 2026-07-29 08:24:21 | `/bug-generate` | 生成 bug.md，状态更新为 draft。 |
| 2026-07-29 08:08:23 | `/bug-capture` | 记录管理端证书编辑弹窗图片下方显示无意义文件名缺陷。 |

- 2026-07-29 09:07:43 workflow-sync：状态同步为 done（Change archived）
