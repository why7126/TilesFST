---
change_id: fix-miniapp-sku-detail-video-url
type: fix
status: proposed
created_at: 2026-07-20 08:20:58
updated_at: 2026-07-20 22:42:13
source_bug: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
source_requirement: REQ-0044-miniapp-sku-detail-page
---

# Design - fix-miniapp-sku-detail-video-url

## Root Cause

`tile_videos` 的字段语义在小程序详情接口中被错用：

- `object_key`：MinIO / 媒体对象 key，应作为生成 `/media/{object_key}` 或完整安全 URL 的来源。
- `file_name`：原始上传文件名或显示名，不应作为小程序 `<video>` 播放 URL。

当前小程序详情仓储读取 `file_name` 并写入视频媒体 `url`，导致真实上传数据下可能返回 `example.mp4` 一类不可播放值。测试种子曾把 `file_name` 直接写成 `/media/videos/1.mp4`，没有暴露真实字段语义下的问题。

## Proposed Fix

1. 调整 `MiniappHomeRepository.list_product_media()`：
   - 视频查询返回 `object_key`，不再把 `file_name` 当作播放 URL。
   - `MiniappMediaRecord.url` 对视频承载对象 key 或已经安全归一化的媒体地址。
2. 保持 `MiniappHomeService._media_items()` 的安全 URL 归一化边界：
   - 若值已是 `/media/...`、`http://...` 或 `https://...`，保持原值。
   - 若值是对象 key，则返回 `/media/{object_key}`。
3. 补齐图片 URL 与历史数据兼容：
   - 小程序 SKU 详情图片、主图和分享图使用 `tile_images.object_key` 生成 `/media/{object_key}`。
   - `/media/{object_key}` 访问层对历史 `original/default/tiles/.../images/...` 图片 key 做兼容映射，避免旧 `tile_images.url` 残留导致 404。
4. 回归小程序页面：
   - `<video src="{{item.url}}">` 继续消费后端安全 URL。
   - 保持 `bindplay`、`binderror`、`pauseVideo()` 和 `swiper autoplay="{{!mediaPaused}}"` 行为。
   - 视频 `poster` 仅使用视频自身 `cover_url`，不再回落到商品主图或图片兜底图，避免未播放态覆盖主图。
5. 调整 SKU 详情内容顺序：
   - 页面内容顺序为“商品信息 >> 品牌信息 >> 商品参数”。
   - 商品信息仅显示商品名称和商品价格。
   - 商品参数顺序为“SKU 编码 >> 类目 >> 规格 >> 主色系 >> 表面工艺”。

## API Contract

预期不改变 `GET /api/v1/miniapp/skus/{sku_id}` 的响应结构，仅修正视频 `media[].url` 的数据来源，使既有契约稳定满足“安全媒体 URL”。

如果实现中发现必须新增字段或改变响应结构，必须先更新本 Change 的 spec、`docs/03-api-index.md`、OpenAPI、Orval 生成物和相关测试，再继续实现。

## Data And Storage Boundary

不新增数据库字段，不迁移历史数据。修复应按既有字段语义读取：

- 图片使用 `tile_images.object_key` 生成小程序安全媒体 URL；媒体访问层兼容历史 `tile_images.url` 形态的旧图片 key。
- 视频使用 `tile_videos.object_key` 生成安全媒体 URL。

小程序端不得拼接 MinIO 内部地址、不得接收未授权 object key 直连对象存储。

## Tests

- 后端测试新增场景：`object_key=videos/real.mp4`、`file_name=original-name.mp4` 时，SKU 详情接口返回 `/media/videos/real.mp4`。
- 后端测试保留媒体排序与计数断言，确认视频仍排在图片之后，且响应中不返回旧 `original/default` 图片 URL。
- 媒体访问测试覆盖旧图片 key 到当前对象 key 的兼容映射。
- 小程序静态测试确认详情页 WXML 中 `<video>` 使用 `item.url`，并保留播放、错误、暂停相关事件绑定。
- 小程序静态测试确认视频 `poster` 不回落到商品主图或图片兜底图，并确认内容顺序与参数顺序。

## Risks

| 风险 | 缓解 |
|---|---|
| 旧数据中 `object_key` 异常为空或已写入完整 URL | 使用既有 schema 的 NOT NULL 约束；实现前检查测试数据并保持 `_media_url` 兼容完整 URL |
| 修复视频 URL 时影响图片 URL | 后端测试同时覆盖图片 object key、视频 URL、计数和排序；媒体访问层补旧 key 兼容 |
| API 契约误判为无需同步 Orval | 实现收尾时明确检查 OpenAPI diff；若 schema 未变则说明不需要 Orval |
| 小程序视频未播放态仍被主图遮挡 | 静态测试锁定 `poster` 不使用商品主图兜底 |
