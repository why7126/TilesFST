---
change_id: add-miniapp-sku-video-fullscreen-actions
status: applied_local
created_at: 2026-07-23 23:58:12
updated_at: 2026-07-24 13:30:37
source_requirement: REQ-0068-miniapp-sku-video-fullscreen-actions
iteration: sprint-011
---

# Implementation Record

## 平台能力结论

- 微信小程序 `video` 原生全屏层不适合承载页面自定义长按菜单；为贴近图片全屏长按体验，当前右上角全屏入口改为调用 `wx.previewMedia({ showmenu: true })` 打开微信原生媒体预览层。真实调试发现混合传入商品图片与视频列表可能导致视频预览层持续加载，现已收窄为仅传当前视频文件。
- 当前实现隐藏 `video` 控件内置全屏按钮，仅保留右上角 `cover-view` 图标全屏入口，避免用户进入无法承载页面自定义菜单的 `VideoContext.requestFullScreen` 路径。
- 视频文件转发和保存交给微信原生媒体预览菜单处理，不再使用商品详情页 `open-type="share"`，也不再用页面自定义 `wx.downloadFile` + `wx.saveVideoToPhotosAlbum` 保存流程。
- 客户端不再上报 `sku_video_fullscreen_click` 等新增事件，避免生产后端未部署白名单时继续返回 `400 / 40001`；全屏入口点击临时复用已上线白名单事件 `sku_video_play`，附加 `action=fullscreen_preview`。
- 本实现未新增签名下载 URL、媒体字段、数据库字段、Orval 类型或对象存储权限；`/api/v1/usage-events` 请求/响应 Schema 不变。

## 实现摘要

- `src/miniapp/pages/tile-detail/index.wxml`：视频媒体分支隐藏控件内置全屏按钮，保留右上角图标全屏入口；移除页面内“转发给朋友 / 保存视频 / 取消”自定义浮层。
- `src/miniapp/pages/tile-detail/index.ts` / `index.js`：同步实现 `wx.previewMedia({ sources: [当前视频], current: 0, showmenu: true })`，由微信原生媒体预览层提供长按菜单；全屏入口点击复用 `sku_video_play` 埋点，失败复用 `sku_load_error` 并记录 URL 协议、后缀和微信错误摘要。
- `src/miniapp/pages/tile-detail/index.wxss`：保留全屏图标入口样式；移除视频操作浮层样式。
- `src/backend/app/main.py` / `src/backend/app/modules/media/storage.py`：为 `/media/{object_key}` 补充 `HEAD` 响应，返回视频 `Content-Type`、`Content-Length` 与 `Accept-Ranges`，避免微信原生预览层在资源探测阶段遇到 `405 Method Not Allowed` 后持续加载。
- `src/backend/app/services/log_service.py`：注册 SKU 视频全屏、长按菜单、保存成功 / 失败等 usage-events，避免小程序点击全屏时被后端按未知事件拒绝为 `400 / 40001`。
- `docs/03-api-index.md` / `docs/07-object-storage-strategy.md`：同步 usage-events 白名单、小程序事件表与媒体 `HEAD` / 视频 Range 读取说明；本次不需要 Orval。
- `tests/test_miniapp_static.py`：补充小程序静态测试，覆盖全屏入口属性、操作入口、分享路径、保存视频 API、失败提示、埋点和 `.ts` / `.js` 关键逻辑同步。
- `tests/test_media_storage.py`：补充视频媒体 `HEAD` 元信息响应测试。

## Evidence

| 类型 | 状态 | 证据 | 说明 |
|---|---|---|---|
| static_test | passed | `uv run pytest tests/test_miniapp_static.py` → 30 passed | 覆盖 WXML、TS、JS、WXSS 静态契约 |
| media_storage_test | passed | `uv run pytest tests/test_media_storage.py tests/test_miniapp_static.py` → 41 passed | 覆盖视频 Range、HEAD 元信息函数与 HEAD 路由响应、小程序静态契约 |
| openspec | passed | `openspec validate add-miniapp-sku-video-fullscreen-actions --strict` | Change 结构与规格片段有效 |
| prod_media_probe | observed | `GET Range: bytes=0-1 https://tilesfst.wjoyhappy.site/media/videos/default/tiles/3/3f0a88ac-64cb-43ef-b0fc-4c76d24ca708.mp4` → `206 video/mp4`; `HEAD` → `405` | 生产当前已支持 Range GET，但尚未部署本次 HEAD 修复 |
| backend_usage_events | passed | `uv run pytest tests/test_miniapp_home.py -k usage_events` → 9 passed | 后端已兼容视频全屏 / 保存事件白名单；客户端当前不依赖这些新事件，避免生产未部署时 400 |
| devtools_320pt | follow_up | 待补 `screenshots/REQ-0068/devtools-320pt-*` | 当前命令行环境未连接微信开发者工具 |
| devtools_375pt | follow_up | 待补 `screenshots/REQ-0068/devtools-375pt-*` | 当前命令行环境未连接微信开发者工具 |
| devtools_430pt | follow_up | 待补 `screenshots/REQ-0068/devtools-430pt-*` | 当前命令行环境未连接微信开发者工具 |
| real_device | follow_up | 待补真机录屏或人工摘要 | 当前命令行环境无法执行真机全屏、长按、分享和相册保存 |

## 剩余风险

- `wx.previewMedia` 原生菜单在 DevTools 与真机的“发送给朋友 / 保存视频”具体文案和能力仍需真机确认；当前不宣称页面可完全自定义原生预览菜单。
- 视频保存仍依赖微信下载/预览域名、视频格式、文件大小和系统能力；当前不再使用页面自定义下载保存流程，减少“网络错误”暴露面。若仅传当前视频后仍持续加载，下一步应抓取 `sku_load_error.err_msg` 与视频 URL 响应头，重点检查域名白名单、`Content-Type`、`Accept-Ranges`、`Content-Range` 与视频编码。
- DevTools 与真机 evidence 尚待补齐，Sprint 验收不得把静态测试结果写成真机通过。
