---
bug_id: BUG-0090-admin-sku-list-publish-sort-order
status: done
severity: medium
created_at: 2026-07-30 22:53:04
updated_at: 2026-07-31 00:19:26
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-30 22:53:04
  generated: 2026-07-30 23:05:16
  completed: 2026-07-30 23:11:20
  reviewed: 2026-07-30 23:19:33
  approved: 2026-07-30 23:19:33
iteration: sprint-014
openspec_changes:
  - change_id: fix-admin-sku-list-publish-sort-order
    type: fix
    status: archived
related_requirement: REQ-0006-tile-sku-management
related_bug: null
---

# BUG Trace

```yaml
bug_id: BUG-0090-admin-sku-list-publish-sort-order
status: done
severity: medium
created_at: 2026-07-30 22:53:04
updated_at: 2026-07-31 00:19:26
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-30 22:53:04
  generated: 2026-07-30 23:05:16
  completed: 2026-07-30 23:11:20
  reviewed: 2026-07-30 23:19:33
  approved: 2026-07-30 23:19:33
iteration: sprint-014
openspec_changes:
  - change_id: fix-admin-sku-list-publish-sort-order
    type: fix
    status: archived
related_requirement: REQ-0006-tile-sku-management
related_bug: null
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 00:18:31 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-admin-sku-list-publish-sort-order） |
| 2026-07-31 00:17:51 | /opsx-archive | Change `fix-admin-sku-list-publish-sort-order` 已归档，状态同步完成。 |
| 2026-07-31 00:13:18 | /opsx-apply | Change `fix-admin-sku-list-publish-sort-order` apply 完成，待 archive。 |
| 2026-07-30 23:20:28 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-30 22:53:04 | `/capture` | 记录 Web 端瓷砖 SKU 列表排序应按发布时间降序、未发布按创建时间降序的问题，分类为 BUG。 |
| 2026-07-30 23:05:16 | `/bug-generate` | 基于 capture.md 生成 bug.md，状态推进为 draft。 |
| 2026-07-30 23:11:20 | `/bug-complete` | 补齐 root-cause.md、workaround.md、acceptance.md，状态推进为 pending_review。 |
| 2026-07-30 23:19:33 | `/bug-review --approve` | 评审确认修复，状态推进为 approved。 |
| 2026-07-30 23:28:00 | `/bug-opsx` | 创建 OpenSpec Change `fix-admin-sku-list-publish-sort-order`，状态为 proposed。 |
| 2026-07-30 23:38:50 | `/sprint-propose sprint-014` | 纳入 sprint-014 正式范围，关联 Change `fix-admin-sku-list-publish-sort-order`。 |

- 2026-07-31 00:17:51 workflow-sync：状态同步为 done（Change archived）
