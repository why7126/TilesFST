---
bug_id: BUG-0087-miniapp-brand-detail-product-tab-sort-order
status: done
severity: medium
created_at: 2026-07-28 22:29:01
updated_at: 2026-07-29 07:54:16
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-28 22:29:01
  generated: 2026-07-28 22:32:06
  completed: 2026-07-28 22:36:46
  reviewed: 2026-07-28 22:39:18
  approved: 2026-07-28 22:39:18
iteration: sprint-013
openspec_changes:
  - change_id: fix-miniapp-brand-detail-product-sort-order
    type: fix
    status: archived
related_requirement: REQ-0058-brand-detail-home-page
related_bug: null
---

# BUG Trace

```yaml
bug_id: BUG-0087-miniapp-brand-detail-product-tab-sort-order
status: done
severity: medium
created_at: 2026-07-28 22:29:01
updated_at: 2026-07-29 07:54:16
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-28 22:29:01
  generated: 2026-07-28 22:32:06
  completed: 2026-07-28 22:36:46
  reviewed: 2026-07-28 22:39:18
  approved: 2026-07-28 22:39:18
iteration: sprint-013
openspec_changes:
  - change_id: fix-miniapp-brand-detail-product-sort-order
    type: fix
    status: archived
related_requirement: REQ-0058-brand-detail-home-page
related_bug: null
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-29 07:54:14 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-brand-detail-product-sort-order） |
| 2026-07-29 07:53:54 | /opsx-archive | Change `fix-miniapp-brand-detail-product-sort-order` 已归档，状态同步完成。 |
| 2026-07-28 23:08:48 | /opsx-apply | Change `fix-miniapp-brand-detail-product-sort-order` apply 完成，待 archive。 |
| 2026-07-28 22:29:01 | /capture | 记录品牌详情页商品 Tab 排序需按发布时间升序、ID 升序的问题，分类为 BUG。 |
| 2026-07-28 22:32:06 | /bug-generate | 基于 capture.md 生成 bug.md，并将缺陷状态推进为 draft。 |
| 2026-07-28 22:36:46 | /bug-complete | 补齐 root-cause、workaround、acceptance，缺陷进入待评审。 |
| 2026-07-28 22:39:18 | /bug-review --approve | 评审通过，允许进入 bug-opsx 与 Sprint 规划。 |
| 2026-07-28 22:40:13 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-28 22:45:58 | /bug-opsx | 创建 OpenSpec Change `fix-miniapp-brand-detail-product-sort-order`，状态 proposed。 |
| 2026-07-28 22:48:24 | /bug-opsx | 纠正未纳入 Sprint 时的状态漂移，保持 approved。 |
| 2026-07-28 23:02:00 | /sprint-propose | 纳入 `sprint-013`，状态推进为 in_sprint。 |

- 2026-07-29 07:53:54 workflow-sync：状态同步为 done（Change archived）
