---
requirement_id: REQ-0103-product-recall-list-pin-priority
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-08-07 22:19:41
updated_at: 2026-08-11 23:16:37
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0103-product-recall-list-pin-priority
requirement_name: product-recall-list-pin-priority
requirement_type: 商品排序 / 运营配置
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 本期
related_requirements:
  - REQ-0006-tile-sku-management
related_changes:
  - add-product-recall-list-pin-priority
lifecycle:
  captured: 2026-08-07 22:19:41
  generated: 2026-08-07 22:29:45
  completed: 2026-08-07 22:35:04
  reviewed: 2026-08-07 22:41:24
  approved: 2026-08-07 22:41:24
iteration: sprint-022
openspec_changes:
  - change_id: add-product-recall-list-pin-priority
    type: add
    status: archived
readiness: Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance、trace 与 prototype 策略；管理端配置与小程序排序横切 AC 已写入。
cross_cutting_tags:
  - admin-list
  - admin-modal
  - miniapp-product-list-sorting
domain_tags:
  - sku-list
  - product-ranking
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/miniapp-product-list-sorting.md
  - docs/knowledge-base/retrospectives/sprint-020-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-021-retrospective.md
kb_cross_cutting_report:
  - tag: admin-list
    ref: docs/knowledge-base/best-practices/admin-list-page-consistency.md
    ac_count: 4
  - tag: admin-modal
    ref: docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
    ac_count: 2
  - tag: miniapp-product-list-sorting
    ref: docs/knowledge-base/best-practices/miniapp-product-list-sorting.md
    ac_count: 3
retrospective_notes:
  - sprint-020 提醒 Web 管理端列表仍需复用 admin-list/admin-form best practices，并强调 API/Orval/DB 影响说明要清晰。
  - sprint-021 未涉及运行时 UI 代码，但提醒后续 UI 需求仍遵守 Design System semantic token。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - prototype/web/context.md
  - review.md
expected_openspec_change: add-product-recall-list-pin-priority
```

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-08-11 23:14:26 | lifecycle-stage-migrate | review → archive（/opsx-archive add-product-recall-list-pin-priority） |
| 2026-08-11 23:14:18 | /opsx-archive | Change `add-product-recall-list-pin-priority` 已归档，状态同步完成。 |
| 2026-08-08 07:01:34 | /opsx-modify | Change `add-product-recall-list-pin-priority` 验收返修已同步，待复验或 archive。 |
| 2026-08-07 23:48:12 | /opsx-apply | Change `add-product-recall-list-pin-priority` apply 完成，待 archive。 |
| 2026-08-07 23:16:00 | `/req-opsx` | 创建 OpenSpec Change `add-product-recall-list-pin-priority`，并纳入 sprint-022 scope |
| 2026-08-07 22:55:18 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-08-07 22:41:24 | `/req-review --approve` | 需求评审通过，状态更新为 approved，并准备从 plan 迁入 review |
| 2026-08-07 22:35:04 | `/req-complete` | 补齐用户故事、业务流程、验收标准和原型策略；写入管理端配置与小程序排序横切 AC，状态更新为 pending_review |
| 2026-08-07 22:29:45 | `/req-generate` | 生成商品召回列表排序置顶 PRD，状态更新为 draft |
| 2026-08-07 22:19:41 | `/capture` | 记录商品召回列表排序置顶需求 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-08-11 23:14:05 workflow-sync：状态同步为 done（Change archived）
