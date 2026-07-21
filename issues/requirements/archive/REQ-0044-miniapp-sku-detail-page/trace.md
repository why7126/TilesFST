---
requirement_id: REQ-0044-miniapp-sku-detail-page
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-18 18:48:34
updated_at: 2026-07-21 08:14:55
lifecycle:
  captured: 2026-07-18 18:48:34
  generated: 2026-07-18 18:55:47
  completed: 2026-07-18 18:55:47
  reviewed: 2026-07-18 19:00:01
  approved: 2026-07-18 19:00:01
iteration: sprint-008
openspec_changes:
  - change_id: add-miniapp-sku-detail-page
    type: add
    status: proposed
related_requirements:
  - REQ-0006-tile-sku-management
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
cross_cutting_tags: []
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0044-miniapp-sku-detail-page
requirement_name: miniapp-sku-detail-page
requirement_type: 小程序 / SKU 详情
priority: P1
status: done
lifecycle_stage: review
owner: product
source: 用户输入
target_clients:
  web_admin: 默认不涉及
  web_catalog: 不涉及
  wechat_miniapp: 本期
parent_requirement: REQ-0006-tile-sku-management
related_requirements:
  - REQ-0006-tile-sku-management
related_changes:
  - add-miniapp-sku-detail-page
lifecycle:
  captured: 2026-07-18 18:48:34
  generated: 2026-07-18 18:55:47
  completed: 2026-07-18 18:55:47
  reviewed: 2026-07-18 19:00:01
  approved: 2026-07-18 19:00:01
iteration: sprint-008
openspec_changes:
  - change_id: add-miniapp-sku-detail-page
    type: add
    status: proposed
readiness: Ready
readiness_notes: 五件套已补齐，且小程序 UI 原型策略已存在；本 REQ 不命中管理端横切 best-practice 标签，knowledge-base gate 为 N/A。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/miniapp/prototype-context.md
  - prototype/miniapp/interaction.md
  - prototype/miniapp/sku-detail.html
  - prototype/miniapp/sku-detail-main.png
  - prototype/miniapp/sku-detail-preview.png
  - prototype/miniapp/sku-detail-favorite.png
  - prototype/miniapp/sku-detail-share.png
expected_openspec_change: add-miniapp-sku-detail-page
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
cross_cutting_tags: []
knowledge_base_gate: N/A
scope:
  backend_api: 可能涉及；若新增或调整小程序 SKU 详情、收藏或分享接口 contract，必须同步 OpenAPI、Orval、docs 和测试。
  database: 默认不直接变更；若后续新增 SKU 详情字段、媒体关系或公开状态字段，必须同步 SQLite/MySQL 文档、schema / migration 和测试。
  web_admin: 默认不涉及；若详情字段依赖管理端维护能力补充，需要另行评估并补充对应 REQ/Change。
  web_storefront: 不涉及。
  wechat_miniapp: 本期；新增 SKU 详情页与首页、分类、搜索、品牌、收藏、分享入口跳转。
  object_storage: 涉及图片、视频和分享图展示；必须使用后端鉴权或公开安全 URL，不得直连未授权对象存储。
prototype:
  status: available
  paths:
    - prototype/miniapp/prototype-context.md
    - prototype/miniapp/interaction.md
    - prototype/miniapp/sku-detail.html
    - prototype/miniapp/sku-detail-main.png
    - prototype/miniapp/sku-detail-preview.png
    - prototype/miniapp/sku-detail-favorite.png
    - prototype/miniapp/sku-detail-share.png
kb_cross_cutting_report:
  matched_tags: []
  refs:
    - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
  ac_xcut_count: 0
  rationale: 微信小程序 SKU 详情页不属于当前 req-complete 定义的管理端列表、表单、弹窗或媒体上传横切标签；Sprint 007 复盘用于提示 XL 业务能力需分层验收与 compact 输出。
```

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 将写入 acceptance 的 AC 条数 |
|---|---|---:|
| N/A | 无匹配管理端横切 best-practice；参考 `docs/knowledge-base/retrospectives/sprint-007-retrospective.md` 的分层验收经验 | 0 |

## Readiness Report

| 项 | 结论 |
|---|---|
| Readiness | Ready |
| Knowledge-base gate | N/A |
| Cross-cutting tags | 无 |
| Prototype strategy | 已提供 `prototype/miniapp/` HTML、context、interaction 与多状态 PNG |
| 后续门禁 | 已通过 `/req-review --approve`；可 `/req-opsx`，纳入 Sprint 仍需通过 `/sprint-propose` |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-18 21:23:45 | lifecycle-stage-migrate | review → archive（/opsx-archive add-miniapp-sku-detail-page） |
| 2026-07-18 21:22:44 | /opsx-archive | Change `add-miniapp-sku-detail-page` 已归档，状态同步完成。 |
| 2026-07-18 20:00:29 | /opsx-apply | Change `add-miniapp-sku-detail-page` apply 完成，待 archive。 |
| 2026-07-18 19:20:46 | /req-opsx | 创建 OpenSpec Change `add-miniapp-sku-detail-page`，状态 proposed |
| 2026-07-18 19:06:05 | /sprint-propose | 纳入 sprint-008 正式范围，状态更新为 in_sprint |
| 2026-07-18 19:01:11 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-18 19:00:01 | /req-review --approve | 评审通过，状态更新为 approved；准备由 plan 迁入 review 阶段 |
| 2026-07-18 18:55:47 | /req-complete | 补齐 user-stories、business-flow、acceptance，修正 REQ 编号与 requirement frontmatter；小程序 UI 原型策略已存在；knowledge-base 横切标签 N/A |
| 2026-07-18 18:48:34 | /req-capture | 记录微信小程序新增瓷砖 SKU 详情页需求 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0069-miniapp-sku-detail-carousel-video-not-playable | high | done | fix-miniapp-sku-detail-video-url | SKU 商品详情页轮播图视频不能显示和播放 |
| BUG-0070-miniapp-sku-detail-duplicate-brand-button | medium | draft | — | 小程序商品详情页底部品牌按钮与内容区查看品牌主页重复 |
