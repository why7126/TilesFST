---
bug_id: BUG-0146-batch-media-maintenance-banner-variants
status: done
severity: high
created_at: 2026-08-29 19:02:43
updated_at: 2026-08-30 08:36:15
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-29 19:02:43
  generated: 2026-08-29 19:08:27
  completed: 2026-08-29 19:10:08
  reviewed: 2026-08-29 19:13:50
  approved: 2026-08-29 19:13:50
iteration: sprint-027
openspec_changes:
  - change_id: fix-media-maintenance-banner-variants
    type: fix
    status: archived
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0137-miniapp-lightweight-image-variant-consumption
related_change: fix-media-maintenance-banner-variants
---

# BUG Trace

```yaml
bug_id: BUG-0146-batch-media-maintenance-banner-variants
status: done
severity: high
created_at: 2026-08-29 19:02:43
updated_at: 2026-08-29 19:33:31
lifecycle_stage: review
lifecycle:
  captured: 2026-08-29 19:02:43
  generated: 2026-08-29 19:08:27
  completed: 2026-08-29 19:10:08
  reviewed: 2026-08-29 19:13:50
  approved: 2026-08-29 19:13:50
iteration: sprint-027
openspec_changes:
  - change_id: fix-media-maintenance-banner-variants
    type: fix
    status: archived
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0137-miniapp-lightweight-image-variant-consumption
related_change: fix-media-maintenance-banner-variants
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-30 08:36:15 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-media-maintenance-banner-variants） |
| 2026-08-30 08:36:05 | /opsx-archive | Change `fix-media-maintenance-banner-variants` 已归档，状态同步完成。 |
| 2026-08-29 21:14:40 | /opsx-modify | Change `fix-media-maintenance-banner-variants` 验收返修已同步，待复验或 archive。 |
| 2026-08-29 19:46:01 | /opsx-apply | Change `fix-media-maintenance-banner-variants` apply 进行中，待补齐剩余验收。 |
| 2026-08-29 19:31:20 | `/bug-opsx` | 创建 OpenSpec Change `fix-media-maintenance-banner-variants`，等待 Workflow Sync 回填 Sprint scope。 |
| 2026-08-29 19:18:06 | `/sprint-propose` | 纳入 sprint-027 正式范围；后续已创建并归档修复 Change `fix-media-maintenance-banner-variants`。 |
| 2026-08-29 19:14:26 | lifecycle-stage-migrate | plan → review（/bug-review） |
| 2026-08-29 19:13:50 | `/bug-review` | confirmed 根因门禁通过，评审结果 approved，等待纳入 Sprint。 |
| 2026-08-29 19:10:08 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，根因状态为 confirmed，BUG 进入待评审。 |
| 2026-08-29 19:02:43 | `/bug-capture` | 记录批量媒体维护命令未覆盖 Banner 自定义上传图，导致生产 Banner 缺少 WebP 派生图并 fallback 到原图的问题。 |

- 2026-08-30 08:36:05 workflow-sync：状态同步为 done（Change archived）
