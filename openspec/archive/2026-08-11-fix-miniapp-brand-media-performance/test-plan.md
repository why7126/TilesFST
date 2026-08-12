---
change_id: fix-miniapp-brand-media-performance
status: proposed
created_at: 2026-08-10 23:31:00
updated_at: 2026-08-10 23:31:00
---

# 测试计划

## 后端

- 覆盖品牌列表接口返回品牌轮播、品牌 Logo 和品牌卡片图片缩略图优先。
- 覆盖品牌详情接口返回品牌 Logo、商品 Tab、证书 Tab 图片展示 URL 与预览 URL 语义。
- 覆盖商品列表接口在 `brandId + categoryId` 场景下继续返回商品卡片轻量主图。
- 覆盖 `.thumb` 缺失回退原图时的可观测记录，不把回退原图计作性能通过。

## 小程序

- 静态测试覆盖 `pages/brand-list` 图片绑定、非首屏懒加载和失败占位。
- 静态测试覆盖 `pages/brand-detail` Logo、商品 Tab、证书 Tab 图片绑定和预览入口。
- 静态测试覆盖 `pages/product-list` 品牌分类入口商品卡片图片字段。
- 静态测试覆盖 `components/product-card` 缩略图优先与原图/占位降级顺序。

## 媒体与生产证据

- 媒体对象 dry-run 审计覆盖品牌 Logo、Banner、SKU 主图和图片类品牌证书。
- 抽样记录原图与 `.thumb` 的 MIME、bytes、像素或等价体积收益证据。
- 记录 `/media` 图片响应缓存头、网关缓存或 CDN 策略。
- 记录微信 DevTools、真机或体验版 Network evidence。
