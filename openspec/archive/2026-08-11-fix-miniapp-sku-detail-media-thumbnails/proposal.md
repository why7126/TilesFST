---
change_id: fix-miniapp-sku-detail-media-thumbnails
status: proposed
created_at: 2026-08-07 22:55:00
updated_at: 2026-08-07 22:55:00
source_bug: BUG-0125-miniapp-sku-detail-media-original-load
related_sprint: sprint-022
---

# 修复小程序 SKU 详情媒体缩略图加载

## 背景

`BUG-0125-miniapp-sku-detail-media-original-load` 已确认微信小程序商品详情页顶部媒体轮播仍加载 SKU 原图。商品列表、首页推荐和 Banner 已使用同目录 `.thumb` 缩略图，但 SKU 详情接口的图片媒体 `url` 与 `preview_url` 都指向原图，小程序详情页 `<image>` 又直接绑定 `item.url`，导致首屏详情页在弱网、多图和大图 SKU 场景下加载慢。

## 变更内容

- 调整 `GET /api/v1/miniapp/skus/{sku_id}` 的图片媒体语义，使首屏展示 URL 优先使用同目录 `.thumb` 缩略图，预览 URL 保留原图。
- 调整视频媒体封面语义，使 `cover_url` 优先使用主图缩略图，视频 `url` 仍保持原视频受控 URL。
- 调整微信小程序详情页首屏图片渲染，使用缩略图字段展示，点击预览时继续使用原图。
- 同步后端测试、小程序静态测试、API 文档、媒体四联验收证据和回归测试。

## 不做范围

- 不新增对象存储 Bucket。
- 不引入小程序直连对象存储。
- 不实现视频转码、多清晰度或 CDN 策略。
- 不批量迁移历史媒体对象；若发现缺失或无收益缩略图，只记录审计/回填建议。

## 回滚方案

- 若详情页缩略图 URL 在生产环境出现不可访问问题，可回退到原图展示 URL，同时保留 `/media/{object_key}` 缺失缩略图回退能力。
- 若小程序预览清晰度回退，可恢复预览列表使用原图 URL。
- 回滚后必须保留 BUG-0125 验收阻塞记录，并重新评估缩略图对象存在性和同目录 `.thumb` 生成链路。
