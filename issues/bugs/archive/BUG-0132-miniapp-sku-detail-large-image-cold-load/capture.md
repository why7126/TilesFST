---
bug_id: BUG-0132-miniapp-sku-detail-large-image-cold-load
status: done
created_at: 2026-08-22 10:40:11
updated_at: 2026-08-22 19:59:31
severity_hint: high
environment: wechat-miniapp
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug: BUG-0125-miniapp-sku-detail-media-original-load
lifecycle_stage: plan
captured_via: capture
classification_rationale: 商品详情页是已交付的小程序能力，用户补充的 Network 证据显示详情页冷加载时存在 1MB 以上图片、PNG 大图和多图并发，导致图片下载阶段耗时 5s-11s，属于既有页面体验与媒体性能预期偏差，因此分类为 BUG。媒体多规格生成、API 字段和 CDN/对象存储直出属于新增能力，已拆分为 REQ-0115。
---

# 现象

小程序商品详情页冷加载时会请求过大的商品图片资源，包含 1.1MB JPEG、1.5MB PNG、3.6MB PNG 等图片，部分请求耗时达到 5s-11s，导致详情页图片展示和页面可用体验明显变慢。

# 复现步骤

1. 在微信小程序开发者工具中打开商品详情页。
2. 打开 Network 面板并禁用缓存，进行冷加载测试。
3. 观察商品详情页图片请求的数量、类型、Size、Time 和 Waterfall。
4. 对比首屏关键图片、普通详情图和高清原图是否在进入页面时全部加载。
5. 记录是否存在大于 1MB 的原图或 PNG 大图阻塞详情页基础浏览。

# 期望 vs 实际

- 期望：商品详情页默认加载适合小程序展示的图片资源，首屏关键图片优先控制在 100-300KB，普通详情展示图控制在 150-500KB；高清原图仅在用户点击预览时加载。
- 实际：详情页冷加载样本中存在 1.1MB JPEG 用时约 6.04s、1.5MB PNG 用时约 5.24s、3.6MB PNG 用时约 11.10s 等请求，说明页面默认加载了不适合冷启动的过大资源。

# 影响范围

- 微信小程序商品详情页冷启动体验。
- 商品图片、详情图、铺贴效果图等媒体展示。
- 弱网或首次访问用户的详情页浏览效率。
- 对象存储或后端 `/media` 图片读取链路的流量和并发压力。

# 初步线索

- 多张 Network 截图显示慢请求主要集中在图片下载阶段，而非 XHR 商品详情接口。
- PNG 大图是高风险资源，非透明图应优先转为 JPG 或 WebP 展示版。
- 部分详情页存在 24-54 个请求，总资源量达到 3.9MB-4.7MB，冷加载压力较大。
- 可能存在进入详情页后首屏外图片立即请求、高清原图直接用于普通展示、或没有使用展示版图片 URL 的问题。

# 建议验收或复现要点

- [ ] 商品详情页冷加载默认不请求大于 1MB 的原图作为普通展示图。
- [ ] 3.6MB PNG、1.5MB PNG 等大图资源有展示版替代；非透明 PNG 可转为 JPG 或 WebP 展示图。
- [ ] 首屏关键图片优先控制在 100-300KB，普通详情展示图控制在 150-500KB。
- [ ] 高清原图只在点击预览或明确查看高清时加载。
- [ ] 首屏外详情图片启用 lazy-load，不在进入详情页时全部请求。
- [ ] 使用微信小程序开发者工具 Network 记录冷加载证据，覆盖 Size、Time、Waterfall、URL 和是否命中缓存。
- [ ] 按媒体类 BUG 四联验收记录 key、object、URL、render 证据。

# 附件

- 用户补充的微信小程序开发者工具 Network 截图：商品详情页图片请求样本，包含 1.1MB JPEG、1.5MB PNG、3.6MB PNG 及多张详情图冷加载耗时。
