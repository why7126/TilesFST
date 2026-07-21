---
change_id: fix-miniapp-sku-detail-video-url
type: fix
status: proposed
created_at: 2026-07-20 08:20:58
updated_at: 2026-07-20 08:20:58
source_bug: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
source_requirement: REQ-0044-miniapp-sku-detail-page
source_change: add-miniapp-sku-detail-page
iteration: null
affected_capabilities:
  - miniapp-sku-detail-page
impact:
  backend: true
  web: false
  miniapp: true
  admin: false
  database: false
  storage: true
  api: true
---

# Proposal - fix-miniapp-sku-detail-video-url

## Why

`BUG-0069-miniapp-sku-detail-carousel-video-not-playable` 已确认微信小程序 SKU 商品详情页轮播图中的视频不能显示和播放。

该缺陷影响 `REQ-0044-miniapp-sku-detail-page` 已交付的图片与视频混合轮播能力。探索与完善阶段发现，小程序 SKU 详情接口疑似把 `tile_videos.file_name` 当作视频播放 URL 返回，而数据库文档和管理端展示逻辑中，`tile_videos.object_key` 才是对象存储 key，`file_name` 是原始文件名。真实管理端保存数据若满足 `object_key=videos/example.mp4`、`file_name=原始上传文件名.mp4`，小程序 `<video src="{{item.url}}">` 会拿到不可播放地址。

## What Changes

- 修复小程序 SKU 详情接口的视频媒体 URL 组装逻辑，确保视频项返回 `/media/{object_key}` 或完整公开安全 URL。
- 保持图片媒体、分享图、媒体排序、媒体计数和视频播放控制行为不退化。
- 补充后端回归测试，覆盖 `object_key` 与 `file_name` 语义不同的真实保存场景。
- 补充或更新小程序静态测试，确认详情页 `<video>` 节点、播放事件、媒体切换和失败提示仍存在。
- 若 API 响应结构不变，仅修正既有字段来源，不要求 Orval；若修复中调整 API 契约，必须同步 OpenAPI、Orval 和 API 文档。

## Capabilities

### Modified Capabilities

- `miniapp-sku-detail-page`: 修复 SKU 详情页视频媒体 URL 来源，保证混合轮播中的视频可以显示和播放。

## Impact

- **Backend/API:** 影响 `GET /api/v1/miniapp/skus/{sku_id}` 的视频 `media[].url` 字段来源；预期响应 schema 不变。
- **Miniapp:** 影响 SKU 详情页视频播放体验；小程序端应继续直接消费接口返回的安全 URL。
- **Storage/Media:** 涉及对象存储媒体 URL 生成策略；不得让小程序端直连未授权 object key。
- **Database:** 不新增或变更表结构；仅按既有 `object_key` / `file_name` 语义读取正确字段。
- **Web/Admin:** 默认不影响 Web 展示端或企业管理端。
- **Testing:** 必须补充后端测试覆盖真实视频字段语义，并回归小程序静态结构。

## Rollback Plan

- 若修复导致 SKU 详情接口视频或图片媒体异常，可回退本 Change 对小程序详情媒体组装逻辑的修改，恢复原有响应行为。
- 回退后保留新增测试作为问题证据，并在 BUG trace 中记录回退原因和后续处理。
- 回退不得修改已归档的 `add-miniapp-sku-detail-page`；后续状态必须通过 Workflow Sync 同步。
