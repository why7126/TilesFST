---
requirement_id: REQ-0129-miniapp-sku-detail-actionbar-compact-favorite
status: done
lifecycle_stage: archive
priority: P2
created_at: 2026-08-28 12:54:23
updated_at: 2026-08-28 16:21:48
lifecycle:
  captured: 2026-08-28 12:54:23
  generated: 2026-08-28 12:59:13
  completed: 2026-08-28 13:37:34
  reviewed: 2026-08-28 13:49:45
  approved: 2026-08-28 13:49:45
iteration: sprint-026
openspec_changes:
  - change_id: update-miniapp-sku-detail-actionbar-compact-favorite
    type: update
    status: archived
related_changes:
  - update-miniapp-sku-detail-actionbar-compact-favorite
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0129-miniapp-sku-detail-actionbar-compact-favorite
requirement_name: miniapp-sku-detail-actionbar-compact-favorite
requirement_type: 小程序 / 商品详情体验优化
priority: P2
status: done
lifecycle_stage: review
owner: product
source: 用户反馈
target_clients:
  web_admin: 不涉及
  web_catalog: 不涉及
  wechat_miniapp: 本期
parent_requirement: REQ-0044-miniapp-sku-detail-page
related_requirements:
  - REQ-0085-miniapp-global-home-floating-button
related_changes:
  - update-miniapp-sku-detail-actionbar-compact-favorite
lifecycle:
  captured: 2026-08-28 12:54:23
  generated: 2026-08-28 12:59:13
  completed: 2026-08-28 13:37:34
  reviewed: 2026-08-28 13:49:45
  approved: 2026-08-28 13:49:45
iteration: sprint-026
openspec_changes:
  - change_id: update-miniapp-sku-detail-actionbar-compact-favorite
    type: fix
    status: archived
readiness: Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance、trace 与小程序原型策略；管理端横切标签 N/A，小程序导航 best-practice 已写入验收。
cross_cutting_tags:
  - miniapp
  - sku-detail
  - actionbar
  - floating-button
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
  - docs/knowledge-base/retrospectives/sprint-025-retrospective.md
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/miniapp/context.md
  - prototype/miniapp/actionbar-compact.html
expected_openspec_change: update-miniapp-sku-detail-actionbar-compact-favorite
product_data_collection_observability:
  status: not_applicable
  affected_layers: []
  reason: 仅调整小程序商品详情页底部操作栏静态 UI、收藏按钮文案呈现和首页悬浮按钮 offset，不新增或修改 API、DB、请求封装、行为事件、请求日志或 Task Trace 字段。
  validation: 已在实现与归档阶段通过代码 diff、小程序视觉验收和 Change 归档校验确认。
kb_cross_cutting_report:
  matched_tags: []
  refs:
    - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
    - docs/knowledge-base/retrospectives/sprint-025-retrospective.md
  ac_xcut_count: 0
  rationale: 本 REQ 为微信小程序商品详情页底部 UI 优化，不命中 req-complete 定义的管理端列表、表单、弹窗或媒体上传横切标签；引用小程序自定义导航 best-practice 和 sprint-025 小程序验收经验作为导航 offset 与证据约束。
```

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 将写入 acceptance 的 AC 条数 |
|---|---|---:|
| N/A | 未命中 `admin-list`、`admin-form`、`admin-modal`、`media-upload`；引用小程序导航与 sprint-025 复盘作为普通 AC 证据来源 | 0 |

## Readiness Report

| 项 | 结论 |
|---|---|
| Readiness | Ready |
| Knowledge-base gate | N/A |
| Cross-cutting tags | miniapp, sku-detail, actionbar, floating-button |
| Prototype strategy | 已提供 `prototype/miniapp/context.md` 与 `prototype/miniapp/actionbar-compact.html` |
| 后续门禁 | 已通过 `/req-review`；下一步先纳入 Sprint，再 `/req-opsx` 创建 Change |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-28 16:13:17 | lifecycle-stage-migrate | review → archive（/opsx-archive update-miniapp-sku-detail-actionbar-compact-favorite） |
| 2026-08-28 16:13:12 | /opsx-archive | Change `update-miniapp-sku-detail-actionbar-compact-favorite` 已归档，状态同步完成。 |
| 2026-08-28 14:28:39 | /opsx-apply | Change `update-miniapp-sku-detail-actionbar-compact-favorite` apply 完成，后续已归档。 |
| 2026-08-28 13:50:28 | lifecycle-stage-migrate | plan → review（/req-review） |
| 2026-08-28 14:18:04 | `/req-opsx` | 创建 OpenSpec Change `update-miniapp-sku-detail-actionbar-compact-favorite`，后续已完成实现与归档。 |
| 2026-08-28 13:49:45 | `/req-review` | 评审通过小程序商品详情页底部收藏按钮与操作栏紧凑化需求；准备由 plan 迁入 review 阶段 |
| 2026-08-28 13:37:34 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与小程序原型策略；引用小程序导航 best-practice 与 sprint-025 复盘，状态进入 pending_review |
| 2026-08-28 12:59:13 | `/req-generate` | 生成小程序商品详情页底部收藏按钮与操作栏紧凑化 PRD，状态更新为 draft |
| 2026-08-28 12:54:23 | `/capture` | 记录小程序商品详情页底部收藏按钮精简与操作栏高度压缩体验优化需求 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-08-28 16:12:53 workflow-sync：状态同步为 done（Change archived）
