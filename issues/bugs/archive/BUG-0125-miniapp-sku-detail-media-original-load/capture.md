---
bug_id: BUG-0125-miniapp-sku-detail-media-original-load
status: done
created_at: 2026-08-07 22:24:59
updated_at: 2026-08-11 23:22:18
severity_hint: high
environment: miniapp
related_requirement:
related_bug: BUG-0110-miniapp-card-banner-thumbnail-usage
---

# 现象

微信小程序商品详情页媒体加载速度慢。初步探索发现详情页未使用已生成的缩略图策略，首屏图库仍加载原图，导致进入详情页时图片请求体积偏大、首屏等待时间变长。

# 复现步骤

1. 打开微信小程序商品列表、首页推荐或搜索结果。
2. 点击任一有多张 SKU 图片或视频的商品，进入商品详情页。
3. 观察详情页顶部媒体轮播区的图片加载速度和 Network 请求路径。
4. 对比商品列表卡片图片请求路径是否使用 `.thumb` 缩略图。

# 期望 vs 实际

- 期望：商品详情页首屏展示图优先使用轻量缩略图；点击预览或播放时再使用原图/视频资源；视频封面也应复用轻量图片，避免首屏拉取原始大图。
- 实际：详情接口当前返回的媒体 `url` 与 `preview_url` 均指向原图，详情页 `<image>` 直接使用 `item.url`；首屏媒体轮播加载原图，未复用列表页已有的缩略图优化策略。

# 附件

- 待补充：微信 DevTools 或真机 Network 截图，需包含详情页图片请求 URL、响应体积和首屏加载耗时。
