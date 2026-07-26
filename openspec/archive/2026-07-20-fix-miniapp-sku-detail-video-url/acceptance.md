---
change_id: fix-miniapp-sku-detail-video-url
type: fix
status: proposed
created_at: 2026-07-20 08:20:58
updated_at: 2026-07-20 22:42:13
source_bug: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
source_requirement: REQ-0044-miniapp-sku-detail-page
---

# Acceptance - fix-miniapp-sku-detail-video-url

## 验收标准

- [ ] AC-001 `GET /api/v1/miniapp/skus/{sku_id}` 在视频记录 `object_key=videos/example.mp4`、`file_name=原始上传文件名.mp4` 时，返回视频 `media[].url=/media/videos/example.mp4` 或完整公开安全 URL。
- [ ] AC-002 SKU 详情响应不把原始上传文件名作为视频播放 URL 返回。
- [ ] AC-003 SKU 详情响应不暴露 MinIO 内部地址、真实密钥、未授权对象存储路径或本地临时路径。
- [ ] AC-004 图片和视频混合轮播保持主图第一、其余图片按排序、视频接在图片后按排序展示。
- [ ] AC-005 图片数和视频数统计准确，图片预览能力不受视频修复影响。
- [ ] AC-006 小程序视频项显示封面或播放器，用户主动点击后可播放和暂停。
- [ ] AC-007 视频默认不自动播放；播放期间轮播不自动切换。
- [ ] AC-008 页面隐藏、返回、跳转或进入新 SKU 时暂停当前视频。
- [ ] AC-009 单个视频加载失败时展示失败提示或占位，不阻断其他媒体和详情信息。
- [ ] AC-010 后端测试覆盖真实 `object_key` / `file_name` 字段语义，小程序静态测试覆盖视频节点和事件绑定。
- [ ] AC-011 不新增交易、下单、支付、库存、询价、视频转码、多清晰度或封面自动生成能力。
- [ ] AC-012 若 API schema 未变化，修复输出明确不需要 Orval；若 schema 变化，必须同步 OpenAPI、Orval、API 文档和测试。
- [ ] AC-013 SKU 详情响应中的图片、主图和分享图使用 `tile_images.object_key` 生成安全媒体 URL，不返回历史 `original/default/...` 图片 URL。
- [ ] AC-014 `/media/{object_key}` 访问层对历史 `original/default/tiles/.../images/...` 图片 key 可兼容映射到当前对象 key，避免旧数据残留导致 404。
- [ ] AC-015 视频未开始播放时不得用商品主图或图片兜底图作为覆盖 poster；仅当视频自身有 `cover_url` 时展示视频封面。
- [ ] AC-016 SKU 详情页内容顺序为“商品信息 >> 品牌信息 >> 商品参数”；商品信息仅显示商品名称和商品价格。
- [ ] AC-017 商品参数展示顺序为“SKU 编码 >> 类目 >> 规格 >> 主色系 >> 表面工艺”。

## 验收证据

| 类型 | 要求 |
|---|---|
| 接口响应 | 包含视频 SKU 的详情响应展示安全可播放视频 URL |
| 自动化测试 | 后端目标测试、媒体访问测试和小程序静态测试通过 |
| 小程序人工验收 | 微信开发者工具或真机确认视频显示、播放、暂停和失败提示 |
| 追溯 | BUG-0069、REQ-0044、本 Change 和 Sprint 状态一致 |
