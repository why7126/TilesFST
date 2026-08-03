---
bug_id: BUG-0096-admin-sku-category-filter-only-top-level
status: done
severity: medium
created_at: 2026-07-31 14:17:30
updated_at: 2026-07-31 21:40:00
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-31 14:17:30
  generated: 2026-07-31 14:52:50
  completed: 2026-07-31 14:56:38
  reviewed: 2026-07-31 15:13:05
  approved: 2026-07-31 15:13:05
iteration: sprint-015
openspec_changes:
  - change_id: fix-admin-sku-category-cascade-filter
    type: fix
    status: archived
related_requirement: REQ-0006-tile-sku-management
related_bug: null
---

# BUG Trace

```yaml
bug_id: BUG-0096-admin-sku-category-filter-only-top-level
status: done
severity: medium
created_at: 2026-07-31 14:17:30
updated_at: 2026-07-31 15:19:43
lifecycle_stage: review
lifecycle:
  captured: 2026-07-31 14:17:30
  generated: 2026-07-31 14:52:50
  completed: 2026-07-31 14:56:38
  reviewed: 2026-07-31 15:13:05
  approved: 2026-07-31 15:13:05
iteration: sprint-015
openspec_changes:
  - change_id: fix-admin-sku-category-cascade-filter
    type: fix
    status: archived
related_requirement: REQ-0006-tile-sku-management
related_bug: null
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 21:39:51 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-admin-sku-category-cascade-filter） |
| 2026-07-31 21:38:31 | /opsx-archive | Change `fix-admin-sku-category-cascade-filter` 已归档，状态同步完成。 |
| 2026-07-31 20:55:56 | /opsx-modify | Change `fix-admin-sku-category-cascade-filter` 验收返修已同步，待复验或 archive。 |
| 2026-07-31 15:53:11 | /opsx-apply | Change `fix-admin-sku-category-cascade-filter` apply 进行中，待补齐剩余验收。 |
| 2026-07-31 15:36:25 | `/sprint-propose sprint-015` | 纳入 sprint-015 正式范围，关联 Change `fix-admin-sku-category-cascade-filter`。 |
| 2026-07-31 15:18:53 | `/bug-opsx BUG-0096` | 创建 OpenSpec Change `fix-admin-sku-category-cascade-filter`。 |
| 2026-07-31 15:14:01 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-31 15:13:05 | `/bug-review --approve` | 评审通过，确认修复；可进入 /bug-opsx 或纳入 Sprint 正式范围。 |
| 2026-07-31 15:11:15 | `/bug-complete` | 补充产品确认口径：父类目筛选包含所有子孙类目 SKU，SKU 页类目筛选 UI 采用级联选择控件。 |
| 2026-07-31 15:07:23 | `/bug-complete` | 复核待验证点：代码确认 SKU 列表筛选只取一级类目、SKU 表单已有全层级选项、后端 category_id 为精确匹配；父类目是否包含子孙类目需产品评审确认。 |
| 2026-07-31 14:56:38 | `/bug-complete` | 补齐 root-cause.md、workaround.md、acceptance.md，状态推进为 pending_review，等待评审确认是否修复。 |
| 2026-07-31 14:52:50 | `/bug-generate` | 基于 capture 生成正式缺陷稿 bug.md，状态推进为 draft；明确管理后台 SKU 页类目筛选需支持各层级类目。 |
| 2026-07-31 14:17:30 | `/capture` | 记录管理后台瓷砖 SKU 页类目筛选只能选择一级类目、无法筛选各层级类目的问题，分类为 BUG。 |

- 2026-07-31 21:38:31 workflow-sync：状态同步为 done（Change archived）
