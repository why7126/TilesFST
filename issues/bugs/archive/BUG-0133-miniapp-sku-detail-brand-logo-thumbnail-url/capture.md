---
bug_id: BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url
status: done
created_at: 2026-08-22 20:38:13
updated_at: 2026-08-22 21:52:34
severity_hint: high
environment: wechat-miniapp
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0126-miniapp-brand-media-slow-load
lifecycle_stage: plan
captured_via: capture
classification_rationale: 商品详情页品牌卡与品牌 Logo 展示已属于既有小程序详情能力；用户反馈缺少 `brand_logo_thumbnail_url` 导致品牌卡加载原图，是已交付媒体缩略图消费策略在具体接口或页面字段上的偏差，因此分类为 BUG。
---

# 现象

小程序商品详情页品牌卡展示品牌 Logo 时缺少 `brand_logo_thumbnail_url`，页面可能直接使用品牌 Logo 原图，导致商品详情页额外加载大图资源。

# 复现步骤

1. 打开包含品牌 Logo 的小程序商品详情页。
2. 查看商品详情接口返回的品牌字段。
3. 检查品牌卡 Logo 使用的 URL 字段。
4. 在 Network 面板观察品牌 Logo 请求是否命中缩略图或展示图资源。

# 期望 vs 实际

- 期望：商品详情接口返回 `brand_logo_thumbnail_url`，商品详情页品牌卡优先使用该缩略图字段展示 Logo。
- 实际：商品详情页品牌卡缺少 `brand_logo_thumbnail_url`，存在直接加载品牌 Logo 原图的风险。

# 影响范围

- 微信小程序商品详情页品牌卡。
- 商品详情接口的品牌信息返回结构。
- 品牌 Logo 缩略图生成、存储与消费链路。
- 移动端详情页冷加载性能与对象存储流量。

# 初步线索

- 需复核商品详情接口是否只返回品牌 Logo 原图 URL，未补充缩略图 URL。
- 需确认前端品牌卡是否存在缩略图字段优先级，例如 `brand_logo_thumbnail_url` > 展示图 > 占位图。
- 需与 `REQ-0115-media-multi-variant-images` 的图片多规格消费策略保持一致。

# 建议验收或复现要点

- [ ] 商品详情接口为品牌信息返回 `brand_logo_thumbnail_url`。
- [ ] 品牌 Logo 缩略图为空时，品牌卡不直接回退到过大的原图资源。
- [ ] 小程序商品详情页品牌卡优先渲染缩略图 URL。
- [ ] Network 证据显示品牌卡普通展示不请求 Logo 原图大文件。
- [ ] 回归已有品牌详情、品牌列表和商品详情媒体加载策略。

# 附件

- 暂无。
