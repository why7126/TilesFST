---
bug_id: BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url
title: 小程序商品详情页品牌卡缺少 brand_logo_thumbnail_url 导致加载原图
severity: high
status: done
owner:
discovered_at: 2026-08-22 20:38:13
environment: wechat-miniapp
related_requirement: REQ-0115-media-multi-variant-images
related_change: fix-miniapp-sku-detail-brand-logo-thumbnail-url
created_at: 2026-08-22 21:02:56
updated_at: 2026-08-25 14:53:29
---

# 现象

小程序商品详情页的品牌卡没有稳定消费 `brand_logo_thumbnail_url`。当前商品详情页品牌信息存在只声明或只使用 `brand_logo_url` 的风险，导致品牌 Logo 在详情页普通展示场景中回退为原图加载。

这与媒体多规格展示策略不一致：详情页的品牌卡属于小尺寸展示位，应优先加载品牌 Logo 缩略图或展示图，原图只应在明确需要高清预览时加载。

# 复现

1. 准备一个已配置品牌 Logo 且存在缩略图派生资源的商品。
2. 打开微信小程序商品详情页。
3. 查看商品详情接口返回的 `brand` 字段，确认是否包含 `brand_logo_thumbnail_url`。
4. 检查商品详情页品牌卡渲染所使用的图片字段。
5. 在微信小程序开发者工具 Network 面板中观察品牌 Logo 请求 URL、资源大小和耗时。

# 期望

- 商品详情接口的 `brand` 数据返回 `brand_logo_thumbnail_url`。
- 商品详情页品牌卡优先使用 `brand_logo_thumbnail_url` 展示品牌 Logo。
- 缩略图缺失时采用受控降级策略，不在普通卡片展示中直接请求大体积原图。
- Network 面板中品牌卡展示请求命中缩略图或展示图资源，而不是原始 Logo 大图。

# 实际

- 商品详情页品牌卡存在只依赖 `brand_logo_url` 的链路。
- 当 `brand_logo_thumbnail_url` 未返回或未被消费时，页面可能直接拉取品牌 Logo 原图。
- 在商品详情页冷加载场景中，品牌卡可能额外引入不必要的大图请求，增加页面可用前的等待时间。

# 影响范围

- 微信小程序商品详情页品牌卡展示。
- 商品详情 API 的品牌信息响应结构。
- 品牌 Logo 的缩略图生成、返回与前端消费链路。
- 移动端冷加载性能、弱网体验和对象存储流量。

# 严重等级说明

严重等级为 high。该问题发生在商品详情页核心浏览链路，且与近期媒体多规格图片能力的验收目标直接相关；一旦品牌 Logo 原图体积较大，会影响详情页冷加载耗时，并造成对象存储流量浪费。

# 初步技术线索

- 品牌列表和品牌详情链路已有 `brand_logo_thumbnail_url` 字段与缩略图优先使用逻辑。
- 商品详情页的 `SkuDetail.brand` 类型附近仍存在只声明 `brand_logo_url` 的风险，需要补齐 `brand_logo_thumbnail_url`。
- 后端商品详情响应需要确认品牌卡数据是否沿用 `MiniappBrandCard` 的缩略图字段，或在详情专用 Schema 中补充同名字段。

# 建议验收

- [ ] 商品详情接口响应中 `brand.brand_logo_thumbnail_url` 可用，且与品牌 Logo 原图 URL 区分。
- [ ] 商品详情页品牌卡优先渲染 `brand_logo_thumbnail_url`。
- [ ] 缩略图缺失时不直接加载过大的原图资源，按约定展示占位或受控展示图。
- [ ] 微信小程序开发者工具 Network 证据覆盖 URL、Size、Time 与是否命中缓存。
- [ ] 回归品牌列表、品牌详情和商品详情三个入口，确认品牌 Logo 缩略图消费策略一致。
openspec_changes:
  - change_id: fix-miniapp-sku-detail-brand-logo-thumbnail-url
    type: update
    status: archived
