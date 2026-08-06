---
requirement_id: REQ-0098-admin-media-list-thumbnails
status: pending_review
created_at: 2026-08-05 09:20:54
updated_at: 2026-08-05 09:20:54
---

# 原型上下文

## 目的

本原型用于表达管理端图片密集列表的资源选择策略，不作为最终视觉稿。后续实现应沿用现有 SKU、品牌、证书与 Banner 列表布局，只调整图片 URL 优先级、fallback 和必要测试。

## 覆盖页面

- SKU 列表：主图缩略图优先，原图兜底。
- Banner 列表：Banner 图片缩略图优先，原图兜底。
- 品牌列表：复核已有 `logo_thumbnail_url` 优先。
- 证书列表：复核已有 `thumbnail_url` 优先。

## 交互说明

- 列表单元格仍为固定尺寸图片容器。
- 缩略图加载失败时，前端应尝试原图或展示既有占位。
- 点击详情、编辑或预览仍进入原图 / 原文件查看语义。
- 不新增分页、筛选、状态操作或弹窗。

## 待导出

- PNG Golden Reference：待后续 OpenSpec Change 或设计确认后导出。
