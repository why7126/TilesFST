---
bug_id: BUG-0116-prod-media-historical-object-drift
status: done
severity: high
created_at: 2026-08-04 10:25:13
updated_at: 2026-08-04 23:12:32
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-04 10:25:13
  generated: 2026-08-04 10:39:56
  completed: 2026-08-04 10:43:35
  reviewed: 2026-08-04 10:46:13
  approved: 2026-08-04 10:46:13
iteration: sprint-019
openspec_changes:
  - change_id: fix-prod-media-historical-object-drift
    type: fix
    status: archived
related_requirement: REQ-0012-object-storage-key-layout
related_bug: BUG-0099-public-sku-main-image-key-staging-path
---

# BUG Trace

```yaml
bug_id: BUG-0116-prod-media-historical-object-drift
status: done
severity: high
created_at: 2026-08-04 10:25:13
updated_at: 2026-08-04 10:46:13
lifecycle_stage: review
lifecycle:
  captured: 2026-08-04 10:25:13
  generated: 2026-08-04 10:39:56
  completed: 2026-08-04 10:43:35
  reviewed: 2026-08-04 10:46:13
  approved: 2026-08-04 10:46:13
iteration: sprint-019
openspec_changes:
  - change_id: fix-prod-media-historical-object-drift
    type: fix
    status: archived
related_requirement: REQ-0012-object-storage-key-layout
related_bug: BUG-0099-public-sku-main-image-key-staging-path
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-04 22:59:48 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-prod-media-historical-object-drift） |
| 2026-08-04 22:59:22 | /opsx-archive | Change `fix-prod-media-historical-object-drift` 已归档，状态同步完成。 |
| 2026-08-04 20:02:51 | /opsx-modify | Change `fix-prod-media-historical-object-drift` 验收返修已同步，待复验或 archive。 |
| 2026-08-04 11:14:44 | /opsx-apply | Change `fix-prod-media-historical-object-drift` apply 完成，已 archive。 |
| 2026-08-04 10:46:45 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-04 10:25:13 | `/capture` | 记录生产历史媒体对象与缩略图存在规范漂移的问题，分类为媒体类 BUG。 |
| 2026-08-04 10:39:56 | `/bug-generate` | 生成 bug.md，明确 SKU、品牌 Logo、证书图片三类历史媒体对象与缩略图规范漂移。 |
| 2026-08-04 10:43:35 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，进入待评审状态。 |
| 2026-08-04 10:46:13 | `/bug-review --approve` | 评审通过，确认进入后续 bug-opsx 与 Sprint 规划流程。 |
| 2026-08-04 10:54:57 | `/bug-opsx` | 创建 OpenSpec Change `fix-prod-media-historical-object-drift`。 |
| 2026-08-04 11:00:43 | `/sprint-propose` | 纳入 `sprint-019` 正式范围，状态已闭环。 |

- 2026-08-04 22:59:06 workflow-sync：状态同步为 done（Change archived）
