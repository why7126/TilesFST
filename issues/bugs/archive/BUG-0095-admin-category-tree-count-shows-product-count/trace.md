---
bug_id: BUG-0095-admin-category-tree-count-shows-product-count
status: done
severity: medium
created_at: 2026-07-31 14:16:27
updated_at: 2026-07-31 17:36:00
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-31 14:16:27
  generated: 2026-07-31 14:52:35
  completed: 2026-07-31 14:57:01
  reviewed: 2026-07-31 15:06:02
  approved: 2026-07-31 15:06:02
iteration: sprint-015
openspec_changes:
  - change_id: fix-admin-category-tree-count
    type: fix
    status: archived
related_requirement: REQ-0005-tile-category-management
related_bug: null
---

# BUG Trace

```yaml
bug_id: BUG-0095-admin-category-tree-count-shows-product-count
status: done
severity: medium
created_at: 2026-07-31 14:16:27
updated_at: 2026-07-31 17:36:00
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-31 14:16:27
  generated: 2026-07-31 14:52:35
  completed: 2026-07-31 14:57:01
  reviewed: 2026-07-31 15:06:02
  approved: 2026-07-31 15:06:02
iteration: sprint-015
openspec_changes:
  - change_id: fix-admin-category-tree-count
    type: fix
    status: archived
related_requirement: REQ-0005-tile-category-management
related_bug: null
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 17:35:06 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-admin-category-tree-count） |
| 2026-07-31 17:34:43 | /opsx-archive | Change `fix-admin-category-tree-count` 已归档，状态同步完成。 |
| 2026-07-31 17:20:41 | /opsx-modify | Change `fix-admin-category-tree-count` 验收返修已同步，待复验或 archive。 |
| 2026-07-31 15:31:48 | /opsx-apply | Change `fix-admin-category-tree-count` apply 完成，待 archive。 |
| 2026-07-31 15:20:06 | `/sprint-propose sprint-015` | 纳入 Sprint 015 正式范围，关联 Change `fix-admin-category-tree-count`。 |
| 2026-07-31 15:13:20 | `/bug-opsx` | 创建 OpenSpec Change `fix-admin-category-tree-count`，状态为 proposed。 |
| 2026-07-31 15:06:37 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-31 15:06:02 | `/bug-review --approve` | 评审通过，确认该缺陷需要修复；可进入 /bug-opsx 或 Sprint 正式范围。 |
| 2026-07-31 15:02:48 | `/bug-complete` | 根据补充验证点更新 root-cause 与 acceptance：确认后端返回直接子类目数量字段，全部类目入口应显示顶层类目数量，问题收敛到前端计数字段绑定错误。 |
| 2026-07-31 14:57:01 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，状态推进为 pending_review，等待评审确认是否修复。 |
| 2026-07-31 14:52:35 | `/bug-generate` | 基于 capture 生成正式缺陷稿 bug.md，状态推进为 draft；明确类目树右侧数字应显示下一层级类目数量而不是商品数量。 |
| 2026-07-31 14:16:27 | `/capture` | 记录管理端类目树节点右侧计数口径错误：应显示下一层级类目数量，当前显示商品数量；分类为 BUG，关联类目管理需求 REQ-0005。 |
