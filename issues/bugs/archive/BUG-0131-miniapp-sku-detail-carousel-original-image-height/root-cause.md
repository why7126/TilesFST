---
bug_id: BUG-0131-miniapp-sku-detail-carousel-original-image-height
root_cause_status: probable
created_at: 2026-08-21 13:08:22
updated_at: 2026-08-21 13:08:22
category: design
evidence_level: code-and-screenshot
---

# 根因分析

## 根因状态

`probable`

当前已有代码定位、规格约束和用户截图证据，可以解释商品详情页轮播首屏清晰度不足与高度偏小的现象；但尚缺具体 SKU 原图与 `.thumb` 的像素、体积、加载耗时对比，以及修复后的真机/开发者工具闭环截图，因此暂不标记为 `confirmed`。

## 直接原因

小程序商品详情页首屏图片 `<image>` 使用 `item.url || imageFallback` 渲染，而 SKU 详情接口当前将图片媒体 `url` 优先返回同目录 `.thumb` 缩略图。`.thumb` 缩略图在详情页顶部大图区域中被放大展示，导致瓷砖纹理、边缘和背景文字细节不够清晰。

同时，详情页轮播容器、图片和视频层高度固定为 `680rpx`，无法根据主流小程序视口和瓷砖详情展示场景进行更合适的比例调整。

## 根本原因

`BUG-0125-miniapp-sku-detail-media-original-load` 修复时，为了解决商品详情页直接加载原图导致首屏媒体慢的问题，将 SKU 详情图片展示 URL 调整为 `.thumb`，并保留 `preview_url` 指向原图。该策略适合列表、卡片和推荐位等小图场景，但没有为商品详情页“大图查看细节”的场景保留独立的高清展示图语义。

现行正式规格也写明“详情页首屏图片使用缩略图”，导致实现和测试都锁定了 `.thumb` 作为详情首屏展示 URL。当用户在详情页查看瓷砖花色和纹理时，性能优先策略与清晰度优先诉求发生冲突。

## 触发条件

- SKU 存在图片媒体。
- 后端 SKU 详情接口返回图片媒体 `url` 为 `.thumb`，`preview_url` 为原图或高清 URL。
- 小程序商品详情页首屏轮播渲染 `item.url`。
- 设备 DPR 或图片内容细节使 `.thumb` 在大图区域中被明显放大。
- 用户需要查看瓷砖纹理、花色、表面质感或展板文字等细节。

## 证据链

| 证据入口 | 类型 | 结论 |
|---|---|---|
| `src/miniapp/pages/tile-detail/index.wxml` | 代码定位 | 首屏 `<image>` 绑定 `src="{{item.url || imageFallback}}"`，预览才绑定 `data-url="{{item.preview_url || item.url}}"`。 |
| `src/backend/app/services/miniapp_home_service.py` | 代码定位 | `_media_items()` 对图片媒体调用 `_card_media_url(..., prefer_thumbnail=True)`，将展示 URL 指向 `.thumb`。 |
| `src/backend/app/modules/media/storage.py` | 代码定位 | 缩略图生成默认最大宽高为 `480x480`，属于小图性能优化尺寸。 |
| `src/miniapp/pages/tile-detail/index.wxss` | 代码定位 | `.media-wrap`、`.gallery`、`.gallery-image`、`.video-layer` 高度固定为 `680rpx`。 |
| `tests/test_miniapp_home.py` | 测试定位 | 现有测试断言 SKU 详情图片 `media[0].url` 为 `.thumb`，`preview_url` 为原图。 |
| `openspec/specs/miniapp-sku-detail-page/spec.md` | 规格定位 | 当前正式规格要求详情首屏图片使用缩略图，与本次用户反馈的高清详情诉求冲突。 |
| 用户补充截图 | 小程序视觉证据 | SKU `M612X07` 商品详情页首屏图片纹理和背景文字明显发糊，商品名称和价格仍在首屏露出。 |

## 影响范围

- 微信小程序商品详情页顶部轮播图片展示。
- SKU 图片媒体字段 `url` / `preview_url` 的详情页展示语义。
- 小程序详情页轮播高度、商品信息首屏露出和底部操作栏遮挡风险。
- 相关测试和正式规格中关于“详情首屏展示图”的断言。

不应扩大到商品列表、商品卡片、推荐位、Banner 的 `.thumb` 使用策略；这些位置仍应保留缩略图以避免加载性能回退。

## 验证方式

修复前验证：

1. 请求任一含图片 SKU 的详情接口，确认图片媒体 `url` 为 `.thumb`，`preview_url` 为原图。
2. 在小程序商品详情页查看该 SKU 首屏轮播图，记录纹理和文字清晰度。
3. 点击图片进入预览，对比预览图与首屏展示图清晰度。
4. 记录 320 到 430px 逻辑宽度下轮播高度和商品名称露出情况。

修复后验证：

1. 详情页首屏展示应使用原图或详情级展示图，点击预览仍使用原图或高清 URL。
2. 商品列表、商品卡片和推荐位仍使用 `.thumb`。
3. 轮播高度调整后，首屏仍能露出商品名称或关键商品信息。
4. 小程序 DevTools、真机或体验版补充 Network/render evidence。

## 人工补证步骤

1. 选择用户反馈 SKU `M612X07` 或其他可复现 SKU。
2. 记录该 SKU 第一张图片的 `.thumb` 与原图像素尺寸、bytes 和 MIME 摘要，不记录真实对象存储密钥或未脱敏 object key。
3. 在微信开发者工具或真机打开商品详情页，截取修复前首屏图片、点击预览图和页面首屏信息露出状态。
4. 修复后重复以上步骤，补充截图或人工验收摘要到 `acceptance.md` 的四联验收 `render` 维度。
5. 若发现原图加载耗时明显影响体验，需在 Change 设计中评估详情级展示图或懒加载策略，而不是回退到小尺寸 `.thumb`。
