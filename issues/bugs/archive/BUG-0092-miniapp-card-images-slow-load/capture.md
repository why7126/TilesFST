---
bug_id: BUG-0092-miniapp-card-images-slow-load
status: done
created_at: 2026-07-30 22:58:23
updated_at: 2026-07-31 08:09:43
severity_hint: high
environment: miniapp_experience
related_requirement: REQ-0049-miniapp-product-card-component
related_bug:
lifecycle_stage: plan
captured_via: bug-capture
classification_rationale: 小程序体验版商品卡片图片加载很慢，属于已交付商品卡片与媒体读取链路的性能和稳定性偏差；现象集中在卡片图片加载，不拆分为多个缺陷。
---

# 现象

微信小程序体验版页面加载速度较慢，商品卡片文字内容出现后，需要等待较久才能把所有卡片图片加载出来；部分卡片图片可能加载失败并触发兜底图。

# 复现步骤

1. 打开微信小程序体验版，进入首页。
2. 观察 Banner、新品推荐、热销推荐和全部产品卡片图片加载过程。
3. 下拉到“全部产品”区域或进入商品列表页，继续观察卡片图片加载速度。
4. 在微信开发者工具或真机调试网络面板中筛选 `/media/` 请求，记录请求数量、单张大小、耗时和失败状态。

# 期望 vs 实际

- 期望：首屏核心卡片图片应在可接受时间内完成加载，滚动列表图片应按需加载；缺失对象或对象存储慢响应应可被后端观测定位。
- 实际：首屏会同时渲染多组商品卡片并触发多张 `/media/` 图片请求；卡片组件未启用图片懒加载，后端返回原始媒体地址且缺少缩略图链路，用户体感为图片长时间逐步补齐。

# 影响范围

- 微信小程序体验版首页。
- 微信小程序商品列表页、品牌商品列表页、搜索结果中复用的商品卡片。
- 后端 `/api/v1/miniapp/home`、`/api/v1/miniapp/products` 返回的 `cover_image` 字段。
- 后端 `/media/{object_key}` 受控媒体读取链路。
- 对象存储中 SKU 主图对象与数据库 `tile_images.object_key` 引用一致性。

# 初步线索

- 首页同时请求首页聚合数据和“全部产品”第一页，首屏可能渲染 Banner + 新品 6 张 + 热销 6 张 + 全部产品 12 张。
- `product-card` 的 `<image>` 当前未设置 `lazy-load`，拿到数据后会直接加载 `cover_image`。
- 后端 `cover_image` 使用 `/media/{object_key}`，`/media` GET 会从对象存储完整读取对象后返回，未见列表缩略图、图片缓存头或媒体读取耗时日志。
- 本地 `usage_events` 里存在较多 `product_card_image_failed` 记录，集中在 `new_products`、`hot_products`、`all_products`。
- 本地 SQLite 中存在公开 SKU 主图对象缺失或无主图记录的情况；体验版需进一步核对生产对象存储。

# 建议验收或复现要点

- [ ] 体验版网络面板可记录首页首屏 `/media/` 请求数量、单张大小、P50/P95 耗时、失败状态。
- [ ] 数据库公开 SKU 主图引用均能在对象存储中找到，不存在 404 或迁移残留 key。
- [ ] 商品卡片图片采用列表缩略图或等价轻量 URL，详情页仍可查看原图。
- [ ] 首页和商品列表滚动场景启用按需加载策略，首屏不一次性拉取过多非可见图片。
- [ ] `/media` 图片读取具备必要缓存头和可排障的耗时观测，不记录 raw object key 或敏感信息。
- [ ] 优化后体验版首页卡片图片加载体感明显改善，图片失败事件显著下降。

# 附件

暂无；建议后续补充微信开发者工具网络面板截图或真机抓包摘要。
