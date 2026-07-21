---
bug_id: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
status: done
created_at: 2026-07-20 00:09:10
updated_at: 2026-07-20 22:47:36
classification: code/api/db-contract/test
related_requirement: REQ-0044-miniapp-sku-detail-page
related_change: fix-miniapp-sku-detail-video-url
---

# Root Cause - BUG-0069 SKU 商品详情页轮播图视频不能显示和播放

## 直接原因

小程序 SKU 详情接口在组装视频媒体时疑似读取了 `tile_videos.file_name` 作为视频播放 URL，而不是使用 `tile_videos.object_key` 生成 `/media/{object_key}` 或其他后端授权 / 公开安全 URL。

当前链路如下：

1. `src/backend/app/repositories/miniapp_home_repository.py` 的 `list_product_media()` 查询 `tile_videos.file_name`。
2. 同方法把 `file_name` 写入 `MiniappMediaRecord.url`。
3. `src/backend/app/services/miniapp_home_service.py` 的 `_media_items()` 将该值归一化后写入 SKU 详情响应 `media[].url`。
4. `src/miniapp/pages/tile-detail/index.wxml` 的 `<video src="{{item.url}}">` 直接使用接口返回值播放视频。

如果真实数据中 `file_name` 是原始上传文件名，而不是 `/media/...` URL 或完整 URL，小程序 `<video>` 就无法加载视频。

## 根本原因

根本原因是视频元数据字段语义在管理端保存、数据库文档、小程序详情接口和测试数据之间没有保持一致：

- 数据库文档中 `tile_videos.object_key` 表示 MinIO 对象键，`file_name` 表示原始文件名。
- 管理端 SKU 详情展示视频时使用 `object_key` 生成 `/media/{object_key}`。
- 小程序 SKU 详情接口却从 `file_name` 取视频 URL。
- 后端测试种子把 `file_name` 写成 `/media/videos/1.mp4`，使测试通过了理想 URL 形态，却没有覆盖管理端真实保存语义。

因此，接口契约层暴露了错误的视频地址，前端播放组件拿到无效 `src` 后表现为视频不可见、加载失败或无法播放。

## 触发条件

满足以下条件时可稳定触发：

1. SKU 处于公开 / 已发布状态。
2. SKU 至少有 1 个视频记录。
3. `tile_videos.object_key` 为对象存储 key，例如 `videos/example.mp4`。
4. `tile_videos.file_name` 为原始文件名或显示名，例如 `example-upload.mp4`，而不是 `/media/videos/example.mp4`。
5. 小程序请求 `GET /api/v1/miniapp/skus/{sku_id}` 并用返回的 `media[].url` 渲染 `<video>`。

## 分类

| 分类 | 判断 |
|---|---|
| code | 是。小程序详情接口读取了不适合作为播放 URL 的字段 |
| api | 是。`GET /api/v1/miniapp/skus/{sku_id}` 的视频媒体 URL 契约不稳定 |
| db-contract | 是。实现未遵循 `object_key` / `file_name` 的字段语义 |
| test | 是。现有测试种子绕过了真实字段语义，未覆盖回归场景 |
| frontend | 间接受影响。小程序 `<video>` 直接消费错误 URL，但前端不是主要根因 |
| security | 暂无证据显示敏感信息泄露；修复时仍必须保证媒体 URL 来自后端授权或公开安全 URL |

## 影响判断

该问题影响已交付的 SKU 详情页混合媒体能力，尤其是商品视频展示与播放。它不阻断 SKU 详情页整体加载，也不影响图片轮播和文本信息展示，但会导致视频素材不可用，违反 `REQ-0044-miniapp-sku-detail-page` 中关于图片与视频混合轮播、视频播放控制和安全媒体 URL 的验收要求。
