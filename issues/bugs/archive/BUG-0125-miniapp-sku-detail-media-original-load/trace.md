---
bug_id: BUG-0125-miniapp-sku-detail-media-original-load
title: 微信小程序商品详情页媒体加载慢
status: done
lifecycle_stage: archive
severity: high
created_at: 2026-08-07 22:24:59
updated_at: 2026-08-11 23:22:34
related_requirement:
related_bug: BUG-0110-miniapp-card-banner-thumbnail-usage
iteration: sprint-022
openspec_changes:
  - change_id: fix-miniapp-sku-detail-media-thumbnails
    type: fix
    status: archived
---

```yaml
bug_id: BUG-0125-miniapp-sku-detail-media-original-load
title: 微信小程序商品详情页媒体加载慢
status: done
lifecycle_stage: archive
severity: high
related_requirement:
related_bug: BUG-0110-miniapp-card-banner-thumbnail-usage
iteration: sprint-022
openspec_changes:
  - change_id: fix-miniapp-sku-detail-media-thumbnails
    type: fix
    status: archived
```

# Trace

## 背景

用户反馈微信小程序商品详情页媒体加载速度很慢。探索阶段定位到详情页媒体链路未使用缩略图：后端 SKU 详情聚合数据仍返回原图 URL，小程序详情页首屏轮播直接以 `item.url` 渲染图片。

## 初始影响范围

- 微信小程序商品详情页 `pages/tile-detail/index.*`
- 后端小程序 SKU 详情接口 `GET /api/v1/miniapp/skus/{sku_id}`
- SKU 图片、视频封面、媒体预览和分享图片 URL 语义
- 媒体四联验收中的 `key`、`object`、`URL`、`render` 维度

## 完善状态

- root-cause.md：已补齐直接原因、根本原因、触发条件和分类。
- workaround.md：已补齐正式修复前的素材与验收规避方案，并说明局限。
- acceptance.md：已引用媒体类 BUG 四联验收模板，覆盖 key、object、URL、render 和小程序 evidence。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-11 23:22:18 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-sku-detail-media-thumbnails） |
| 2026-08-11 23:22:12 | /opsx-archive | Change `fix-miniapp-sku-detail-media-thumbnails` 已归档，状态同步完成。 |
| 2026-08-07 23:18:15 | /opsx-apply | Change `fix-miniapp-sku-detail-media-thumbnails` apply 完成，待 archive。 |
| 2026-08-07 22:42:04 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-07 22:24:59 | /bug-capture | 记录小程序商品详情页媒体加载慢缺陷，待进入复现与根因分析。 |
| 2026-08-07 22:30:34 | /bug-generate | 生成 bug.md，状态推进为 draft。 |
| 2026-08-07 22:35:02 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态推进为 pending_review。 |
| 2026-08-07 22:41:40 | /bug-review --approve | 评审通过，确认修复。 |
| 2026-08-07 22:55:00 | /bug-opsx | 创建修复 Change `fix-miniapp-sku-detail-media-thumbnails`。 |

- 2026-08-11 23:22:12 workflow-sync：状态同步为 done（Change archived）
