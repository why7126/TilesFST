---
bug_id: BUG-0132-miniapp-sku-detail-large-image-cold-load
title: 小程序商品详情页冷加载存在大图资源导致图片加载耗时过长
severity: high
status: done
owner:
discovered_at: 2026-08-22 10:40:11
environment: wechat-miniapp
related_requirement: REQ-0044-miniapp-sku-detail-page
related_change: fix-miniapp-sku-detail-large-image-cold-load
created_at: 2026-08-22 10:40:11
updated_at: 2026-08-25 14:53:29
---

# 现象

微信小程序商品详情页冷加载时仍会请求过大的商品图片资源。用户补充的多组微信开发者工具 Network 证据显示，详情页图片请求中存在 1MB 以上 JPEG、1.5MB PNG、3.6MB PNG 等大图资源，部分请求耗时达到 5s-11s，导致详情页图片展示和基础浏览体验明显变慢。

# 复现步骤

1. 在微信小程序开发者工具中打开商品详情页。
2. 打开 Network 面板，勾选 Disable cache，保持 Online 网络状态。
3. 刷新或重新进入商品详情页，触发冷加载。
4. 观察图片请求的 Type、Size、Time 和 Waterfall。
5. 记录是否存在大于 1MB 的原图或 PNG 大图，以及首屏外详情图片是否在进入页面后立即请求。

# 期望结果

- 商品详情页默认加载适合小程序展示的图片资源，不应把 1MB 以上原图作为普通展示图冷加载。
- 首屏关键图片优先控制在 100-300KB。
- 普通详情展示图优先控制在 150-500KB。
- 非透明 PNG 大图应有 JPG 或 WebP 展示版替代。
- 高清原图只在用户点击预览或明确查看高清时加载。
- 首屏外详情图片应 lazy-load，不应在进入页面时全部请求并抢占网络。

# 实际结果

- 多个详情页冷加载样本中出现大图请求，例如：
  - 1.1MB JPEG，用时约 6.04s。
  - 1.5MB PNG，用时约 5.24s。
  - 3.6MB PNG，用时约 11.10s。
  - 826KB JPEG，用时约 5.68s。
- 部分详情页请求数量达到 24-54 个，总资源量达到 3.9MB-4.7MB。
- 慢请求主要集中在图片下载阶段，XHR 商品详情接口不是主要瓶颈。
- 小图样本通常在 150ms-800ms 范围，说明问题集中在大图资源和详情页加载策略，而不是所有媒体请求都不可用。

# 影响范围

- 微信小程序商品详情页冷启动和弱网浏览体验。
- 商品主图、详情图、铺贴效果图等商品媒体展示。
- 依赖 `/media` 或对象存储图片 URL 的端侧渲染链路。
- 媒体四联验收中的 `key`、`object`、`URL`、`render` 维度。
- 后续媒体多规格能力 `REQ-0115-media-multi-variant-images` 的范围判断和验收基线。

# 严重等级说明

严重等级建议为 `high`。该问题影响用户进入商品详情页后的核心浏览体验，并且已有多组 Network 证据显示大图下载耗时达到秒级到十秒级。问题虽不阻断页面接口返回，但会显著拖慢商品图片展示，尤其影响首次访问、弱网和多图商品场景。
openspec_changes:
  - change_id: fix-miniapp-sku-detail-large-image-cold-load
    type: update
    status: archived
