---
bug_id: BUG-0091-miniapp-product-list-sort-consistency
status: done
severity: medium
created_at: 2026-07-30 22:53:04
updated_at: 2026-07-31 00:24:38
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-30 22:53:04
  generated: 2026-07-30 23:05:08
  completed: 2026-07-30 23:09:40
  reviewed: 2026-07-30 23:19:10
  approved: 2026-07-30 23:19:10
iteration: sprint-014
openspec_changes:
  - change_id: fix-miniapp-product-list-sort-consistency
    type: fix
    status: archived
related_requirement: REQ-0047-product-list-common-component-application
related_bug: BUG-0087-miniapp-brand-detail-product-tab-sort-order
---

# BUG Trace

```yaml
bug_id: BUG-0091-miniapp-product-list-sort-consistency
status: done
severity: medium
created_at: 2026-07-30 22:53:04
updated_at: 2026-07-31 00:24:38
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-30 22:53:04
  generated: 2026-07-30 23:05:08
  completed: 2026-07-30 23:09:40
  reviewed: 2026-07-30 23:19:10
  approved: 2026-07-30 23:19:10
iteration: sprint-014
openspec_changes:
  - change_id: fix-miniapp-product-list-sort-consistency
    type: fix
    status: archived
related_requirement: REQ-0047-product-list-common-component-application
related_bug: BUG-0087-miniapp-brand-detail-product-tab-sort-order
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 00:23:56 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-product-list-sort-consistency） |
| 2026-07-31 00:22:58 | /opsx-archive | Change `fix-miniapp-product-list-sort-consistency` 已归档，状态同步完成。 |
| 2026-07-30 23:57:48 | /opsx-apply | Change `fix-miniapp-product-list-sort-consistency` apply 完成，待 archive。 |
| 2026-07-30 23:41:56 | `/sprint-propose` | 纳入 `sprint-014` 正式范围。 |
| 2026-07-30 23:26:22 | `/bug-opsx` | 创建 OpenSpec Change：`fix-miniapp-product-list-sort-consistency`。 |
| 2026-07-30 23:19:48 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-30 23:19:10 | `/bug-review --approve` | 评审通过，确认进入修复流程。 |
| 2026-07-30 23:09:40 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，状态进入 `pending_review`。 |
| 2026-07-30 23:05:08 | `/bug-generate` | 生成 `bug.md`，状态从 `captured` 推进为 `draft`。 |
| 2026-07-30 22:53:04 | `/capture` | 记录小程序搜索商品结果页和分类商品列表页排序需与品牌详情页一致的问题，分类为 BUG；首页全部产品列表不纳入本次范围。 |
