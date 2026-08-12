---
bug_id: BUG-0125-miniapp-sku-detail-media-original-load
title: 微信小程序商品详情页媒体加载慢
severity: high
status: done
owner:
discovered_at: 2026-08-07 22:24:59
environment: miniapp
related_requirement:
related_change: fix-miniapp-sku-detail-media-thumbnails
created_at: 2026-08-07 22:24:59
updated_at: 2026-08-11 23:22:12
---

# 现象

微信小程序商品详情页顶部媒体轮播加载速度慢。商品列表、首页推荐和 Banner 已存在缩略图优先策略，但详情页进入后仍直接加载 SKU 原图，导致首屏媒体区在弱网、真机或多图商品场景下等待明显。

# 复现步骤

1. 打开微信小程序首页、商品列表或搜索结果。
2. 选择一个已发布且有 SKU 图片的商品，进入商品详情页。
3. 在微信 DevTools 或真机 Network 中观察详情页顶部媒体轮播请求。
4. 对比商品列表卡片请求路径，确认列表卡片使用 `.thumb` 缩略图，而详情页图片请求仍为原图路径。

# 期望结果

- 商品详情页首屏展示图优先使用轻量缩略图。
- 点击图片预览时再使用原图 URL，保证预览清晰度。
- 视频封面优先使用主图缩略图，视频播放 URL 保持原视频资源。
- 缩略图缺失时可通过后端受控 `/media/{object_key}` 回退原图，但不应把回退机制当作性能优化完成标准。

# 实际结果

- SKU 详情接口当前对详情卡片主图使用原图 URL。
- 详情页图片媒体项的 `url` 与 `preview_url` 均指向同一个原图 URL。
- 小程序详情页 `<image>` 直接绑定 `item.url`，首屏轮播加载原图而不是 `.thumb` 缩略图。
- 现有自动化测试也固化了详情页返回原图的契约，说明这是当前实现遗漏，而不是单次数据异常。

# 影响范围

- 微信小程序商品详情页 `pages/tile-detail/index.*`。
- 后端小程序 SKU 详情接口 `GET /api/v1/miniapp/skus/{sku_id}`。
- SKU 图片展示 URL、预览 URL、分享图片 URL 和视频封面 URL 语义。
- 媒体四联验收中的 `key`、`object`、`URL`、`render` 维度。

# 严重等级说明

严重等级建议为 `high`。该问题影响用户进入商品详情后的首屏体验，尤其在多图 SKU、弱网真机和大图素材场景中会直接增加等待时间；同时它属于既有缩略图优化未覆盖到详情页的回归/遗漏，修复需要同步后端接口契约、小程序渲染逻辑和测试断言。
