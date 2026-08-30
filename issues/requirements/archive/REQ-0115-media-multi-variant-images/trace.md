---
requirement_id: REQ-0115-media-multi-variant-images
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-08-22 10:40:11
updated_at: 2026-08-30 11:49:33
lifecycle:
  captured: 2026-08-22 10:40:11
  generated: 2026-08-22 10:52:29
  completed: 2026-08-22 11:00:33
  reviewed: 2026-08-22 13:39:52
  approved: 2026-08-22 13:39:52
iteration: sprint-025
openspec_changes:
  - change_id: add-media-multi-variant-images
    type: add
    status: proposed
related_requirements:
  - REQ-0012-object-storage-key-layout
  - REQ-0099-global-thumbnail-size-limit
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md
  - docs/knowledge-base/retrospectives/sprint-022-retrospective.md
cross_cutting_tags:
  - media-upload
related_bugs:
  - BUG-0132-miniapp-sku-detail-large-image-cold-load
  - BUG-0125-miniapp-sku-detail-media-original-load
  - BUG-0110-miniapp-card-banner-thumbnail-usage
related_changes:
  - add-media-multi-variant-images
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0115-media-multi-variant-images
requirement_name: media-multi-variant-images
requirement_type: 媒体能力 / 性能优化
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 后续确认
  wechat_miniapp: 本期
related_requirements:
  - REQ-0012-object-storage-key-layout
  - REQ-0099-global-thumbnail-size-limit
related_changes:
  - add-media-multi-variant-images
lifecycle:
  captured: 2026-08-22 10:40:11
  generated: 2026-08-22 10:52:29
  completed: 2026-08-22 11:00:33
  reviewed: 2026-08-22 13:39:52
  approved: 2026-08-22 13:39:52
iteration: sprint-025
openspec_changes:
  - change_id: add-media-multi-variant-images
    type: add
    status: proposed
readiness: Partially Ready
readiness_notes: 已评审通过；命中的 best-practices 为 draft，且 UI PNG 待后续 Change 阶段导出，因此保持 Partially Ready。
expected_openspec_change: add-media-multi-variant-images
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md
  - docs/knowledge-base/retrospectives/sprint-022-retrospective.md
cross_cutting_tags:
  - media-upload
knowledge_base_cross_cutting_report:
  - tag: media-upload
    ref: docs/knowledge-base/best-practices/admin-media-upload-chain.md
    ac_count: 5
  - tag: miniapp-media
    ref: docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md
    ac_count: 2
retrospective_summary: sprint-022 复盘指出小程序媒体性能不能只验证缩略图对象存在，必须同时覆盖 key、object、URL、render 与 Network evidence。
review_decisions:
  - 存量图片批量生成多规格资源纳入本期。
  - 对象存储直出纳入本期。
  - CDN 正式接入不作为本期必达项，仅保留 URL 适配层和缓存策略预留。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-22 18:25:13 | lifecycle-stage-migrate | review → archive（/opsx-archive add-media-multi-variant-images） |
| 2026-08-22 18:25:07 | /opsx-archive | Change `add-media-multi-variant-images` 已归档，状态同步完成。 |
| 2026-08-22 17:23:46 | /opsx-modify | Change `add-media-multi-variant-images` 验收返修已同步，待复验或 archive。 |
| 2026-08-22 14:41:37 | /opsx-apply | Change `add-media-multi-variant-images` apply 进行中，待补齐剩余验收。 |
| 2026-08-22 13:41:03 | lifecycle-stage-migrate | plan → review（/req-review） |
| 2026-08-22 10:40:11 | `/capture` | 记录媒体图片多规格展示图能力需求；与 `BUG-0132-miniapp-sku-detail-large-image-cold-load` 拆分处理。 |
| 2026-08-22 10:52:29 | `/req-generate` | 生成 `requirement.md`，需求状态更新为 `draft`。 |
| 2026-08-22 11:00:33 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 prototype 策略；读取 media-upload 与小程序媒体四联知识库，需求状态更新为 `pending_review`。 |
| 2026-08-22 13:39:52 | `/req-review` | 默认评审通过；确认存量图片批量生成与对象存储直出纳入本期，CDN 正式接入仅预留。 |
| 2026-08-22 14:02:31 | `/sprint-propose` | 纳入 `sprint-025` 正式范围，完成迭代范围登记。 |
| 2026-08-22 14:11:17 | `/req-opsx` | 创建 OpenSpec Change `add-media-multi-variant-images` 并纳入 `sprint-025` Change 范围。 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url | high | done | fix-miniapp-sku-detail-brand-logo-thumbnail-url | 小程序商品详情页品牌卡缺少 brand_logo_thumbnail_url 导致加载原图 |
| BUG-0134-miniapp-certificate-detail-display-url | high | done | fix-miniapp-certificate-detail-display-url | 小程序证书详情页顶部展示缺少 display_url 导致退回原图 |
| BUG-0135-miniapp-certificate-card-file-url-fallback | high | done | fix-miniapp-certificate-card-file-url-fallback | 小程序证书卡缺缩略图时不应 fallback 到 file_url 原文件 |
| BUG-0137-miniapp-lightweight-image-variant-consumption | high | done | fix-miniapp-lightweight-image-variant-consumption | 小程序 Banner、品牌 Logo、分享图普通展示未统一消费轻量图字段 |
| BUG-0146-batch-media-maintenance-banner-variants | high | done | fix-media-maintenance-banner-variants | 批量媒体维护命令未覆盖 Banner 自定义上传图 |
| BUG-0147-miniapp-certificate-list-images-missing | high | done | fix-miniapp-certificate-media-urls | 小程序证书列表页图片不显示 |
