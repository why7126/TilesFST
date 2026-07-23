---
requirement_id: REQ-0016-banner-management
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-06-28 10:55:38
updated_at: 2026-07-22 09:35:32
lifecycle:
  captured: 2026-06-28 10:55:38
  generated: 2026-06-28 11:06:00
  completed: 2026-06-28 11:07:50
  reviewed: 2026-06-28 11:14:51
  approved: 2026-06-28 11:14:51
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0016-banner-management
requirement_name: banner-management
requirement_type: 管理端 / 运营配置
priority: P1
status: done
owner: product
source: 产品
target_clients:
  web_admin: 本期
  web_catalog: 本期不包含消费端
  wechat_miniapp: 本期不包含消费端
related_requirements:
  - REQ-0004-admin-home
  - REQ-0006-tile-sku-management
  - REQ-0005-brand-management
  - REQ-0008-brand-status-confirm
  - REQ-0009-tile-spec-management
related_changes: []
lifecycle:
  captured: 2026-06-28 10:55:38
  exploring: null
  generated: 2026-06-28 11:06:00
  completed: 2026-06-28 11:07:50
  reviewed: 2026-06-28 11:14:51
  approved: 2026-06-28 11:14:51
iteration: sprint-003
openspec_changes:
  - change_id: add-banner-management
    type: add
    status: proposed
readiness: Ready
readiness_notes: 评审通过；五件套 + review + prototype HTML/PNG/context 齐全
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - trace.md
  - prototype/web/banner-management-list.html
  - prototype/web/banner-management-list.png
  - prototype/web/banner-management-list-context.md
  - prototype/web/banner-management-modal-sku-detail.html
  - prototype/web/banner-management-modal-sku-detail.png
  - prototype/web/banner-management-modal-sku-detail-context.md
  - prototype/web/banner-management-modal-external-link.html
  - prototype/web/banner-management-modal-external-link.png
  - prototype/web/banner-management-modal-external-link-context.md
  - prototype/web/banner-management-modal-topic-page.html
  - prototype/web/banner-management-modal-topic-page.png
  - prototype/web/banner-management-modal-topic-page-context.md
  - prototype/web/banner-management-modal-no-jump.html
  - prototype/web/banner-management-modal-no-jump.png
  - prototype/web/banner-management-modal-no-jump-context.md
expected_openspec_change: add-banner-management
```

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-28 19:23:08 | lifecycle-stage-migrate | review → archive（backfill opsx-archive hook (sprint-003)） |
| 2026-06-28 15:40:00 | `/sprint-apply` | add-banner-management 实现完成；openspec status → applied |
| 2026-06-28 11:25:53 | `/req-opsx` | 创建 OpenSpec `add-banner-management`；status proposed |
| 2026-06-28 11:18:03 | `/sprint-propose` | 纳入 sprint-003；status → in_sprint |
| 2026-06-28 11:14:51 | `/req-review --approve` | 评审通过；status → approved；迁入 review/ |
| 2026-06-28 11:15:10 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-06-28 11:07:50 | `/req-complete` | 补齐 user-stories、business-flow、acceptance；更新 prototype context；status → pending_review |
| 2026-06-28 11:06:00 | `/req-generate` | 生成 requirement.md v1；status → draft |
| 2026-06-28 10:55:38 | `/req-capture` | 创建 capture.md 与 trace 壳；prototype 落盘 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0030-banner-list-ui-inconsistency | medium | done | fix-banner-admin-ui | Banner列表分页与用户管理页不一致且表头上方多余标题行 |
| BUG-0031-banner-modal-image-section-label | low | done | fix-banner-admin-ui | Banner弹窗图片模块首行自定义上传/SKU主图文案冗余 |
| BUG-0032-banner-modal-upload-button-label | low | done | fix-banner-admin-ui | Banner弹窗图片上传按钮文案应为选择或更换 |
| BUG-0033-banner-modal-form-layout-overflow | high | done | fix-banner-admin-ui | Banner 弹窗运营备注宽度不足且底部按钮超出弹窗无滚动 |
| BUG-0034-banner-modal-link-selector-combined | medium | done | fix-banner-admin-ui | Banner弹窗关联专题/SKU搜索框与下拉框应合并 |
| BUG-0035-banner-modal-sku-hero-image-no-effect | high | done | fix-banner-admin-ui | Banner弹窗点击使用SKU主图无任何效果 |
| BUG-0036-banner-modal-datetime-picker | medium | done | fix-banner-admin-ui | Banner弹窗有效期DateTime选择器无法选择时分秒 |
| BUG-0039-banner-list-display-position-column | medium | done | fix-banner-list-and-modal-ui | Banner列表第一列标题与展示位置挤在同一列 |
| BUG-0040-banner-modal-width-too-narrow | medium | done | fix-banner-list-and-modal-ui | Banner弹窗宽度偏小未对齐SKU弹窗 |
| BUG-0048-banner-modal-width-css-cascade-overridden | medium | done | fix-banner-list-and-modal-ui | Banner弹窗880px样式被modal-card全局规则层叠覆盖 |
| BUG-0080-admin-banner-image-preview-cropped | medium | done | fix-admin-banner-image-preview-cropped | 管理端 Banner 列表和弹窗中 Banner 图片显示不全 |

## 视觉验收 Trace（PNG 并排）

| 页面 | HTML | PNG | 状态 | 日期 |
|---|---|---|---|---|
| 列表页 | banner-management-list.html | banner-management-list.png | 待 apply 阶段并排验收 | — |
| 弹窗 SKU 详情 | banner-management-modal-sku-detail.html | *.png | 待 apply 阶段并排验收 | — |
| 弹窗 外部链接 | banner-management-modal-external-link.html | *.png | 待 apply 阶段并排验收 | — |
| 弹窗 专题页 | banner-management-modal-topic-page.html | *.png | 待 apply 阶段并排验收 | — |
| 弹窗 无跳转 | banner-management-modal-no-jump.html | *.png | 待 apply 阶段并排验收 | — |
- 2026-06-28 16:54:11 workflow-sync：状态同步为 done（Change archived）
