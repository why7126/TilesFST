---
change_id: fix-miniapp-sku-detail-carousel-original-image-height
status: implemented
created_at: 2026-08-21 13:43:10
updated_at: 2026-08-21 13:52:48
---

# 测试计划

## 后端

- 聚焦测试 SKU 详情接口图片媒体展示 URL 使用原图或详情级高清展示图。
- 聚焦测试 SKU 详情接口图片 `preview_url` 保持原图或等价高清 URL。
- 聚焦测试商品列表、商品卡片、推荐位和 Banner 仍返回 `.thumb` 或等价轻量图片 URL。
- 若 API schema 或 OpenAPI 输出变化，运行 OpenAPI/Orval 生成并复核相关 generated 片段。

## 小程序

- 静态测试商品详情页首屏图片绑定展示源，点击预览绑定 `preview_url` 或等价高清 URL。
- 静态或样式测试商品详情页轮播高度约束，覆盖 320、375、430px 逻辑宽度。
- 静态测试首屏商品名称或关键商品信息不被媒体区完全挤出。
- 回归视频媒体播放 URL、视频封面和图片 fallback，避免图片修复影响视频链路。

## 媒体验收

- 记录 SKU 图片 key/object/URL/render 四联状态。
- 小程序 DevTools、真机或体验版至少提供一种 render evidence；缺少体验版时记录 blocked 或发布前补证项。

## 文档

- 更新 `docs/03-api-index.md` 中 SKU 详情媒体字段语义；若无 schema 变化，说明无需 Orval。
- 若产生可复用事故经验，更新 `docs/knowledge-base/incidents/` 或说明无需沉淀。
