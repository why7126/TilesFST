---
bug_id: BUG-0097-admin-sku-material-main-image-tag-redundant
status: done
severity: low
created_at: 2026-07-31 14:19:22
updated_at: 2026-07-31 20:55:56
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-31 14:19:22
  generated: 2026-07-31 14:53:38
  completed: 2026-07-31 14:56:58
  reviewed: 2026-07-31 15:06:59
  approved: 2026-07-31 15:06:59
iteration: sprint-015
openspec_changes:
  - change_id: fix-admin-sku-material-main-image-tag
    type: fix
    status: archived
related_requirement: REQ-0006-tile-sku-management
related_bug: null
---

# BUG Trace

```yaml
bug_id: BUG-0097-admin-sku-material-main-image-tag-redundant
status: done
severity: low
created_at: 2026-07-31 14:19:22
updated_at: 2026-07-31 15:40:28
lifecycle_stage: review
lifecycle:
  captured: 2026-07-31 14:19:22
  generated: 2026-07-31 14:53:38
  completed: 2026-07-31 14:56:58
  reviewed: 2026-07-31 15:06:59
  approved: 2026-07-31 15:06:59
iteration: sprint-015
openspec_changes:
  - change_id: fix-admin-sku-material-main-image-tag
    type: fix
    status: archived
related_requirement: REQ-0006-tile-sku-management
related_bug: null
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 20:54:58 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-admin-sku-material-main-image-tag） |
| 2026-07-31 20:54:29 | /opsx-archive | Change `fix-admin-sku-material-main-image-tag` 已归档，状态同步完成。 |
| 2026-07-31 15:36:22 | `/opsx-modify BUG-0097` | 验收返修：删除素材完整度条件筛选，列表请求不再提交 `material_completeness`；同步测试与文档。 |
| 2026-07-31 15:31:58 | /opsx-modify | Change `fix-admin-sku-material-main-image-tag` 验收返修已同步，待复验或 archive。 |
| 2026-07-31 15:28:34 | `/opsx-modify BUG-0097` | 验收返修：素材列只显示图片/视频数量，其他素材状态标签全部移除。 |
| 2026-07-31 15:22:52 | /opsx-apply | Change `fix-admin-sku-material-main-image-tag` apply 完成，待 archive。 |
| 2026-07-31 15:16:00 | `/bug-opsx BUG-0097` | 创建 OpenSpec Change `fix-admin-sku-material-main-image-tag`。 |
| 2026-07-31 15:17:00 | `/sprint-propose sprint-015` | 纳入 sprint-015 正式范围。 |
| 2026-07-31 15:07:36 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-31 15:06:59 | `/bug-review --approve` | 评审通过，确认修复。 |
| 2026-07-31 14:56:58 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，状态同步为 pending_review。 |
| 2026-07-31 14:53:38 | `/bug-generate` | 生成 bug.md，状态同步为 draft。 |
| 2026-07-31 14:19:22 | `/capture` | 记录管理后台瓷砖 SKU 页素材列不需要展示「主图已设」冗余标签的问题，分类为 BUG。 |

- 2026-07-31 20:54:29 workflow-sync：状态同步为 done（Change archived）
