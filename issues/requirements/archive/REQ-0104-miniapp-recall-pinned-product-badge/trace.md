---
requirement_id: REQ-0104-miniapp-recall-pinned-product-badge
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-08-08 09:16:44
updated_at: 2026-08-11 23:20:31
lifecycle:
  captured: 2026-08-08 09:16:44
  generated: 2026-08-08 09:21:37
  completed: 2026-08-08 09:25:35
  reviewed: 2026-08-08 09:28:24
  approved: 2026-08-08 09:28:24
iteration: sprint-022
openspec_changes:
  - change_id: update-miniapp-recall-pinned-product-badge
    type: update
    status: archived
related_requirements:
  - REQ-0103-product-recall-list-pin-priority
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-product-list-sorting.md
  - docs/knowledge-base/retrospectives/sprint-021-retrospective.md
cross_cutting_tags: []
domain_tags:
  - miniapp-product-list-sorting
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0104-miniapp-recall-pinned-product-badge
requirement_name: miniapp-recall-pinned-product-badge
requirement_type: 小程序商品展示 / 置顶标识
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 不涉及
  web_catalog: 不涉及
  wechat_miniapp: 本期候选
related_requirements:
  - REQ-0103-product-recall-list-pin-priority
related_changes:
  - update-miniapp-recall-pinned-product-badge
lifecycle:
  captured: 2026-08-08 09:16:44
  generated: 2026-08-08 09:21:37
  completed: 2026-08-08 09:25:35
  reviewed: 2026-08-08 09:28:24
  approved: 2026-08-08 09:28:24
iteration: sprint-022
openspec_changes:
  - change_id: update-miniapp-recall-pinned-product-badge
    type: update
    status: archived
readiness: Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance、trace 与小程序 prototype 策略；固定横切标签无命中，领域排序回归 AC 已写入。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/miniapp/context.md
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-product-list-sorting.md
  - docs/knowledge-base/retrospectives/sprint-021-retrospective.md
cross_cutting_tags: []
domain_tags:
  - miniapp-product-list-sorting
kb_cross_cutting_report:
  - tag: none
    ref: N/A
    ac_count: 0
domain_knowledge_report:
  - tag: miniapp-product-list-sorting
    ref: docs/knowledge-base/best-practices/miniapp-product-list-sorting.md
    ac_count: 4
retrospective_notes:
  - sprint-021 提醒后续 UI 需求仍遵守 Design System semantic token；本需求虽为小程序卡片标识，但仍需保持卡片稳定、避免排序与分页回归。
```

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-08-11 23:17:18 | lifecycle-stage-migrate | review → archive（/opsx-archive update-miniapp-recall-pinned-product-badge） |
| 2026-08-11 23:17:08 | /opsx-archive | Change `update-miniapp-recall-pinned-product-badge` 已归档，状态同步完成。 |
| 2026-08-08 09:59:43 | /opsx-apply | Change `update-miniapp-recall-pinned-product-badge` apply 完成，待 archive。 |
| 2026-08-08 09:36:33 | `/req-opsx` | 创建 OpenSpec Change `update-miniapp-recall-pinned-product-badge`，待 Workflow Sync 回填 sprint-022 scope |
| 2026-08-08 09:29:22 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-08-08 09:28:24 | `/req-review --approve` | 需求评审通过，状态更新为 approved，并准备从 plan 迁入 review |
| 2026-08-08 09:25:35 | `/req-complete` | 补齐用户故事、业务流程、验收标准和小程序 prototype 策略；写入小程序商品列表排序领域回归 AC，状态更新为 pending_review |
| 2026-08-08 09:21:37 | `/req-generate` | 生成小程序召回置顶商品展示“置顶”标识 PRD，状态更新为 draft |
| 2026-08-08 09:16:44 | `/req-capture` | 记录小程序召回置顶商品展示“置顶”标识需求 |

- 2026-08-11 23:16:37 workflow-sync：状态同步为 done（Change archived）
