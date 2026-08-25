---
requirement_id: REQ-0120-webp-derived-image-variants
title: 图片上传生成 WebP 展示图和缩略图 - 原型策略
created_at: 2026-08-22 21:45:57
updated_at: 2026-08-22 21:45:57
---

# 原型策略

## UI 类型判断

本需求主要是媒体上传和端侧图片消费策略增强，不新增独立页面。命中 UI 横切标签 `media-upload`，但首期不要求新增高保真 HTML 原型。

## 复用入口

| 端 | 复用入口 | UI 关注点 |
|---|---|---|
| Web 管理端 | 既有头像、品牌 Logo、Banner、SKU 图片、证书图片上传组件 | 上传状态机、即时回显、错误态、WebP 派生图可见 |
| 店主 Web | 既有商品列表、详情、品牌和证书展示组件 | 列表优先缩略图，详情优先展示图，预览保留原图 |
| 小程序 | 商品卡片、商品详情、品牌、证书图片组件 | `thumbnail_url` / `display_url` / `original_url` 场景匹配、lazy-load、fallback |

## 后续 OpenSpec UI Contract 要点

- 不新增营销页或独立媒体处理页。
- 如管理端展示维护任务结果，应使用紧凑统计摘要、状态标识和失败分类。
- 不在 UI 中展示未脱敏 object key、内部路径、异常堆栈或对象存储配置。
- Web 端样式变更必须使用 Design System semantic token，不新增裸 Hex。
- 小程序验收需覆盖关键页面实际渲染和 Network evidence。

## PNG / HTML 原型状态

- HTML 原型：暂不生成，原因是本需求不新增独立页面或复杂新交互。
- PNG 视觉稿：暂不导出，后续若 OpenSpec 阶段新增维护任务 UI 或设置项，再按 UI Contract 补充。
