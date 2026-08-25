---
requirement_id: REQ-0120-webp-derived-image-variants
title: 图片上传生成 WebP 展示图和缩略图 - 用户故事
created_at: 2026-08-22 21:45:57
updated_at: 2026-08-22 21:45:57
---

# 用户故事

## US-001 小程序用户快速浏览图片密集页面

作为微信小程序用户，我希望商品列表、详情普通展示、品牌和证书图片优先加载体积更小的 WebP 派生图，以便弱网或冷启动时也能尽快看到核心内容。

验收要点：

- 列表和卡片优先使用 WebP `thumbnail_url`。
- 详情普通展示优先使用 WebP `display_url`。
- 预览和下载仍使用 `original_url` 或等价高清原图。
- 派生图缺失时有明确 fallback，不出现图片空白或无限重试。

## US-002 店主 Web 访客获得更轻量的图片展示

作为店主 Web 访客，我希望浏览 SKU、品牌、Banner 和证书图片时加载的是适合展示的 WebP 图片，以便页面打开更快且不牺牲基本清晰度。

验收要点：

- 列表或卡片使用 WebP 缩略图。
- 详情图册普通浏览使用 WebP 展示图。
- 高清查看仍保留原图入口。
- 加载失败时可回退到原图或占位图。

## US-003 管理端用户上传后自动获得 WebP 派生图

作为企业管理端用户，我希望上传 JPEG、PNG 或 WebP 图片后系统自动生成 WebP 展示图和缩略图，以便不需要手工转码即可获得更好的端侧加载性能。

验收要点：

- 原图对象保留上传格式和 MIME。
- 生成 `.thumb.webp` 与 `.display.webp` 或等价标准 WebP 派生 key。
- 上传控件具备 `idle -> uploading -> done / failed` 状态。
- 同一会话上传成功后可立即看到派生图或可用 fallback。

## US-004 后端维护者安全补齐历史 WebP 派生图

作为后端或运维维护者，我希望能以 dry-run / apply 方式为历史 JPEG、PNG、WebP 图片补生成 WebP 派生图，以便安全提升既有数据的展示性能。

验收要点：

- dry-run 输出待处理数量、已存在数量、跳过原因、失败分类和预计写入数量。
- apply 显式触发，并要求生产执行前确认数据库与对象存储备份。
- 维护任务幂等，重复运行不会重复写入无变化对象。
- 输出只包含脱敏 key hash、资源类型、统计摘要和失败原因枚举。

## US-005 测试人员验证 WebP 派生收益

作为测试人员，我希望验收材料同时覆盖 key、object、URL、render 和资源体积收益，以便证明端侧实际使用了 WebP 派生图，而不是只生成了对象。

验收要点：

- WebP 派生对象的 key、MIME、扩展名和对象大小一致。
- 小程序记录 DevTools、真机或体验版 Network evidence。
- Web 管理端通过 Docker Web `http://localhost:3000` 入口验证上传和回显。
- 若缺少端侧证据，验收记录标记 `blocked` 或 `follow_up`，不得写作已通过。
