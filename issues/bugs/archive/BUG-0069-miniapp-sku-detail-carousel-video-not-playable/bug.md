---
bug_id: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
title: SKU 商品详情页轮播图视频不能显示和播放
severity: high
status: done
owner:
discovered_at: 2026-07-19 23:36:55
created_at: 2026-07-19 23:55:50
updated_at: 2026-07-20 22:47:36
environment: 微信小程序 / SKU 商品详情页
related_requirement: REQ-0044-miniapp-sku-detail-page
related_change: fix-miniapp-sku-detail-video-url
---

# 现象

微信小程序 SKU 商品详情页顶部轮播图中，视频媒体项不能正常显示和播放。用户进入包含视频素材的 SKU 详情页后，轮播区域应同时承载商品图片与视频，但当前视频项不可用，导致商品视频素材无法被浏览。

# 复现步骤

1. 在管理端为某个已发布 SKU 配置至少 1 张图片和 1 个视频素材。
2. 使用微信开发者工具或真机打开小程序。
3. 进入该 SKU 商品详情页。
4. 在顶部轮播图中切换到视频媒体项。
5. 点击或尝试播放视频。

# 期望结果

- 轮播图正确展示视频封面或视频播放器。
- 用户主动点击视频项后，视频可以正常播放、暂停。
- 视频播放期间轮播不自动切换，页面隐藏、锁屏或跳转时暂停当前视频。
- 同一轮播图内图片项仍可正常展示、切换和预览。

# 实际结果

- 视频媒体项不能正常显示或无法播放。
- 页面可能只展示视频加载失败状态，或视频区域为空白 / 无响应。
- 图片媒体项仍可能正常展示，问题集中在视频 URL 或视频播放承载链路。

# 影响范围

- 影响端：微信小程序。
- 影响页面：SKU 商品详情页 `pages/tile-detail/index`。
- 影响模块：顶部图片与视频混合轮播。
- 影响用户：装修客户、设计师、门店导购、品牌访客无法查看 SKU 视频素材。
- 关联能力：`REQ-0044-miniapp-sku-detail-page` 已要求 SKU 详情页支持图片和视频混合轮播、视频播放控制、单项媒体失败兜底，以及安全媒体 URL。

# 严重等级说明

严重等级为 `high`。该问题不阻断整个小程序访问，也不影响图片浏览和 SKU 文本信息展示，但会使已交付的 SKU 详情页视频展示能力不可用，削弱商品详情页关键媒体表达，并违反已归档规格中“图片与视频混合媒体浏览”和“安全媒体 URL”的验收要求。

# 初步分析

探索阶段发现，后端小程序详情接口组装视频媒体时疑似使用了错误字段：

- `src/backend/app/repositories/miniapp_home_repository.py` 的 `list_product_media()` 查询 `tile_videos.file_name`，并把 `file_name` 写入视频媒体 `url`。
- `docs/04-database-design.md` 中 `tile_videos.object_key` 是 MinIO 对象键，`file_name` 是原始文件名。
- 管理端 SKU 服务展示视频时使用 `object_key` 生成 `/media/{object_key}`，而小程序详情页当前链路读取 `file_name`。
- 小程序 WXML 中 `<video src="{{item.url}}">` 直接消费详情接口返回的 `item.url`，如果该值是原始文件名而非 `/media/...` 或完整 URL，微信小程序无法加载播放。

因此，真实管理端保存数据若形如：

```text
object_key = videos/example.mp4
file_name = 原始上传文件名.mp4
```

小程序详情接口可能返回：

```text
url = 原始上传文件名.mp4
```

而不是期望的：

```text
url = /media/videos/example.mp4
```

现有后端测试种子将 `tile_videos.file_name` 直接写成 `/media/videos/1.mp4`，覆盖的是理想 URL 形态，未覆盖管理端真实保存语义，因此当前测试可能无法暴露该缺陷。

# 建议后续验证

1. 构造或选取真实管理端保存的视频数据，确认 `tile_videos.object_key` 与 `tile_videos.file_name` 的实际值。
2. 请求 `GET /api/v1/miniapp/skus/{sku_id}`，检查 `data.media[]` 中视频项的 `url` 是否为 `/media/...` 或完整安全 URL。
3. 在微信开发者工具或真机打开该 SKU 详情页，确认视频项是否可见、可播放。
4. 回归图片项展示、图片预览、媒体计数、视频播放埋点和页面隐藏时暂停逻辑。
