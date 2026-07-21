---
bug_id: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
status: done
created_at: 2026-07-20 00:09:10
updated_at: 2026-07-20 22:47:36
related_requirement: REQ-0044-miniapp-sku-detail-page
related_change: fix-miniapp-sku-detail-video-url
---

# Acceptance - BUG-0069 SKU 商品详情页轮播图视频不能显示和播放

## 回归验收标准

- [ ] AC-BUG-001 当 `tile_videos.object_key = videos/example.mp4` 且 `tile_videos.file_name = 原始上传文件名.mp4` 时，`GET /api/v1/miniapp/skus/{sku_id}` 返回的视频 `media[].url` MUST 为 `/media/videos/example.mp4` 或完整公开安全 URL，不得返回原始文件名。
- [ ] AC-BUG-002 SKU 详情响应中的图片、视频和分享图 URL MUST 来自后端授权、公开安全 URL 或对象存储适配层生成结果，不允许小程序端直连未授权对象存储。
- [ ] AC-BUG-003 包含至少 1 张图片和 1 个视频的 SKU 详情页，顶部轮播图 MUST 正确展示图片项和视频项，媒体计数准确显示图片数和视频数。
- [ ] AC-BUG-004 视频项 MUST 能在微信开发者工具或真机中显示封面或播放器；用户主动点击后可正常播放、暂停。
- [ ] AC-BUG-005 视频默认不自动播放；视频播放期间轮播不自动切换。
- [ ] AC-BUG-006 页面隐藏、锁屏、返回、跳转或进入新 SKU 详情时，当前视频 MUST 暂停，不得继续后台播放。
- [ ] AC-BUG-007 单个视频加载失败时，页面 MUST 展示明确失败提示或占位，不阻断其他图片媒体和 SKU 文本信息浏览。
- [ ] AC-BUG-008 图片项回归正常：主图仍为第一项，图片可展示、切换和预览，图片失败提示不被视频修复逻辑破坏。
- [ ] AC-BUG-009 后端测试 MUST 覆盖管理端真实视频保存语义，即 `object_key` 为媒体对象 key、`file_name` 为原始文件名时，小程序详情接口仍返回安全可播放 URL。
- [ ] AC-BUG-010 小程序静态或运行验收 MUST 覆盖 `<video src="{{item.url}}">` 消费详情接口视频 URL、播放埋点 `sku_video_play`、媒体切换埋点 `sku_media_swipe` 和失败提示。
- [ ] AC-BUG-011 修复不得新增或暴露购物车、购买、下单、支付、库存、优惠券、促销倒计时或询价承诺等 `REQ-0044` 范围外能力。
- [ ] AC-BUG-012 若调整 API 契约、数据库字段语义或媒体 URL 生成策略，MUST 同步 OpenAPI、Orval、`docs/03-api-index.md`、`docs/04-database-design.md` 和相关测试；若仅修正既有响应字段来源且契约不变，应在修复输出中明确说明不需要 Orval。
- [ ] AC-BUG-013 SKU 详情响应中的图片、主图和分享图 MUST 使用 `tile_images.object_key` 生成安全媒体 URL，不得把历史 `original/default/...` 图片 URL 返回给小程序。
- [ ] AC-BUG-014 `/media/{object_key}` MUST 兼容历史 `original/default/tiles/.../images/...` 图片 key 映射，避免旧数据残留导致图片 404。
- [ ] AC-BUG-015 视频未播放态不得使用商品主图或图片兜底图作为覆盖 poster；仅视频自身 `cover_url` 可作为视频封面。
- [ ] AC-BUG-016 SKU 详情页内容顺序 MUST 为“商品信息 >> 品牌信息 >> 商品参数”；商品信息仅展示商品名称和商品价格。
- [ ] AC-BUG-017 商品参数展示顺序 MUST 为“SKU 编码 >> 类目 >> 规格 >> 主色系 >> 表面工艺”。

## 验收证据要求

| 类型 | 要求 |
|---|---|
| 接口证据 | `GET /api/v1/miniapp/skus/{sku_id}` 响应中视频 `media[].url` 为安全可访问 URL |
| 数据证据 | 测试或样例数据体现 `object_key` 与 `file_name` 的真实语义差异 |
| 小程序证据 | 微信开发者工具或真机截图 / 录屏覆盖视频显示、播放、暂停和失败提示 |
| 自动化测试 | 后端测试覆盖视频 URL、图片 URL 与参数顺序；媒体访问测试覆盖旧 key 兼容；小程序静态测试覆盖视频节点、poster、内容顺序和事件绑定 |
| 追溯证据 | BUG、REQ-0044、修复 Change 和 Sprint 状态同步一致 |

## 非目标

- 本 BUG 不要求新增视频转码、压缩、多清晰度或封面自动生成能力。
- 本 BUG 不要求新增管理端媒体上传流程。
- 本 BUG 不要求改变 SKU 详情页的交易范围边界。
- 本 BUG 不要求修复非 SKU 详情页的视频展示问题；若其他页面也存在独立视频播放缺陷，应另行 capture。
