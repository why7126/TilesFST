---
bug_id: BUG-0125-miniapp-sku-detail-media-original-load
acceptance_status: passed
created_at: 2026-08-07 22:35:02
updated_at: 2026-08-12 00:15:15
source_change: fix-miniapp-sku-detail-media-thumbnails
source_sprint: sprint-022
---

# 验收标准

## 回归 AC

| 编号 | 验收项 | 验收方式 |
|---|---|---|
| AC-001 | SKU 详情接口为图片媒体区分首屏展示用缩略图和预览用原图 | 接口测试断言图片展示 URL 使用同目录 `.thumb`，预览 URL 保留原图 |
| AC-002 | 小程序商品详情页首屏图片渲染使用缩略图字段 | 静态测试或小程序 DevTools Network 证据确认 `<image>` 请求 `.thumb` |
| AC-003 | 点击图片预览仍使用原图，保证清晰度 | 小程序 DevTools 或真机预览证据确认 preview URL 为原图 |
| AC-004 | 视频封面优先使用主图缩略图，视频播放 URL 不被替换 | 接口测试和小程序页面证据确认 `cover_url` 为缩略图，视频 `url` 仍为视频资源 |
| AC-005 | 缩略图缺失时页面不破图，并通过 `/media/{object_key}` 受控读取保持可回退 | 后端媒体 URL 测试或人工证据确认 200/回退行为，记录性能风险 |
| AC-006 | 现有首页、商品列表、搜索结果、Banner 和推荐卡片缩略图契约不回退 | 运行相关小程序接口与静态测试 |

## 媒体类 BUG 四联验收

引用模板：`docs/standards/media-bug-four-point-acceptance-template.md`

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0125-miniapp-sku-detail-media-original-load |
| 标题 | 微信小程序商品详情页媒体加载慢 |
| 严重等级 | high |
| 影响范围 | 小程序 / 后端接口 / 对象存储受控 URL |
| 复现入口 | 微信小程序商品列表、首页推荐或搜索结果 → 商品详情页 |
| 受影响端 | miniapp / backend / storage |
| 环境 | miniapp-devtools / miniapp-device / local |
| 媒体类型 | image / video / thumbnail / cover |
| 业务资源 | 已发布 SKU 的脱敏图片与视频资源 |
| 修复前实际结果 | 详情页首屏图片和视频封面使用原图 URL，加载较慢 |
| 修复后期望结果 | 详情页首屏图片和视频封面优先使用真实轻量 `.thumb` 缩略图，预览和播放仍使用原始资源 |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | pass | 后端测试使用 `tiles/1.webp` 派生 `/media/tiles/1.thumb.webp`，未返回 `object_key` 或 `original/default` 内部路径 | 若仍引用非标准主图或非标准前缀，需先纳入修复范围或记录历史对象维护项 |
| object | pass | 自动化测试覆盖缩略图 URL 语义，验收回填确认原图、缩略图、视频 object 存在且 MIME/大小符合预期 | 若缩略图缺失或无收益，需记录回填/重生成策略和统计摘要 |
| URL | pass | `tests/test_miniapp_home.py::test_miniapp_sku_detail_returns_public_media_recommendations_and_share` 断言图片 `url` 为 `.thumb`、`preview_url` 为原图、视频 `url` 保持 `.mp4`、`cover_url` 为 `.thumb` | 若出现 403、404、直连未授权对象存储或 URL 语义混淆，必须返修 |
| render | pass | `tests/test_miniapp_static.py::test_miniapp_sku_detail_page_covers_media_favorite_share_and_empty_states` 断言 `<image src="{{item.url || imageFallback}}">`、预览 `data-url="{{item.preview_url || item.url}}"`、视频 poster 兜底链路；验收回填确认小程序 Network/render evidence 已完成 | 若缺少小程序 evidence，发布前必须补证 |

### 横切检查

| Gate | 状态 | 说明 |
|---|---|---|
| 上传状态机 | n/a | 本 BUG 不涉及上传入口状态机变更 |
| 同会话即时回显 | n/a | 本 BUG 不涉及 Web 管理端上传或编辑即时回显 |
| Docker Web 边界 | n/a | 本 BUG 不涉及文件大小、Nginx 或 Docker Web 上传边界 |
| 媒体代理一致性 | pass | 接口断言覆盖 `/media/{object_key}` URL 语义，响应未暴露 raw object key |
| 历史对象与审计 | pass | 测试与验收回填已覆盖缩略图语义；若生产数据后续发现缺失/无收益缩略图，需记录 dry-run、apply 或幂等摘要 |
| 小程序 evidence | pass | DevTools、真机或体验版 Network 和页面 evidence 已在验收回填中确认 |

## 验收结论

当前状态：`passed`。实现修复、接口测试、小程序静态测试和小程序 DevTools/真机或体验版 Network/render evidence 均已完成。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-12 00:15:15
accepted_by: workflow-sync
source_change: fix-miniapp-sku-detail-media-thumbnails
source_sprint: sprint-022
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

