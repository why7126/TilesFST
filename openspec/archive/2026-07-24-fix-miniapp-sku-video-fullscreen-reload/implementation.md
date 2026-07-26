---
change_id: fix-miniapp-sku-video-fullscreen-reload
status: applied_local
created_at: 2026-07-24 20:51:17
updated_at: 2026-07-24 20:51:17
source_bug: BUG-0084-miniapp-sku-video-fullscreen-reloads-slow
iteration: sprint-011
---

# Implementation Record

## 平台能力结论

- BUG-0084 的核心问题来自全屏入口使用独立 `wx.previewMedia` 预览链路：内嵌 `<video>` 已经能播放时，预览层仍可能重新探测和拉流，导致全屏后长时间加载。
- 本修复将 SKU 详情页右上角全屏入口改为优先复用当前 `wx.createVideoContext(...).requestFullScreen()`，以当前 video 组件上下文进入微信支持的视频全屏态。
- 当前实现保留微信 `video` 控件内置全屏按钮隐藏状态，继续使用页面右上角 `cover-view` 作为清晰入口，但入口主路径不再打开独立媒体预览器。
- 本修复未新增 API、数据库字段、OpenAPI / Orval、Docker Compose、对象存储权限或小程序直连对象存储路径。

## 实现摘要

- `src/miniapp/pages/tile-detail/index.wxml`：为视频组件补充 `bindfullscreenchange="onVideoFullscreenChange"` 与 `bindwaiting="onVideoWaiting"`，继续保持 `autoplay="{{false}}"` 和 `show-fullscreen-btn="{{false}}"`。
- `src/miniapp/pages/tile-detail/index.ts` / `index.js`：`openVideoFullscreen` 改为创建当前视频 `VideoContext` 并调用 `requestFullScreen({ direction: 0 })`；全屏失败时展示明确 toast，并复用 `sku_load_error` 记录 `video_fullscreen_failed`、URL 协议、后缀和微信错误摘要。
- `src/miniapp/pages/tile-detail/index.ts` / `index.js`：新增 `fullscreenVideoId`、`fullscreenSwitching`、`onVideoFullscreenChange`、`onVideoWaiting`，为全屏切换等待和失败提供可见反馈；媒体切换、页面隐藏、卸载仍暂停当前视频。
- `tests/test_miniapp_static.py`：更新小程序静态测试，确认全屏主路径使用 `requestFullScreen`，不再依赖 `wx.previewMedia`；同时覆盖 `.ts` / `.js` 运行入口同步、全屏事件绑定和失败反馈。

## Evidence

| 类型 | 状态 | 证据 | 说明 |
|---|---|---|---|
| static_test | passed | `uv run pytest tests/test_miniapp_static.py` → 30 passed | 覆盖 WXML、TS、JS、WXSS 静态契约和全屏主路径 |
| openspec | passed | `openspec validate fix-miniapp-sku-video-fullscreen-reload --strict --json` | Change 结构与规格片段有效 |
| devtools | follow_up | 待补微信开发者工具 evidence | 当前命令行环境未连接微信开发者工具 |
| real_device | follow_up | 待补实际 SKU 真机录屏或人工摘要 | 当前命令行环境无法执行真机视频全屏、首帧耗时和退出全屏验收 |

## 真机 Evidence 待补字段

| 字段 | 状态 | 说明 |
|---|---|---|
| SKU ID | follow_up | 待选择实际反馈 SKU |
| 视频 URL 类型 | follow_up | 应记录为后端安全媒体 URL 或等价受控路径，不记录密钥或真实客户敏感数据 |
| 视频大小 / 格式 / 编码 / 时长 | follow_up | 用于区分全屏路径问题和素材性能问题 |
| 机型 / 系统 / 微信版本 / 基础库版本 | follow_up | 用于确认微信 video 全屏 API 兼容性 |
| 网络类型 | follow_up | 建议记录 Wi-Fi / 5G / 4G 与大致网络质量 |
| 内嵌首帧耗时 | follow_up | 从点击内嵌播放到首帧可见 |
| 全屏切换首帧或恢复播放耗时 | follow_up | 从点击右上角全屏入口到全屏态首帧或恢复播放 |
| 退出全屏上下文 | follow_up | 确认回到当前 SKU 和当前媒体上下文 |

## 知识沉淀评估

本次不新增 `docs/knowledge-base/incidents/`：问题范围集中在单个小程序页面的全屏入口路径选择，已在 BUG-0084 root-cause、Change design 与本 implementation 中记录“避免将已播放视频主全屏入口实现为独立预览链路”的经验。若后续再出现同类媒体预览/全屏上下文混用问题，再沉淀为可复用 best-practice 更合适。
