---
requirement_id: REQ-0115-media-multi-variant-images
title: 媒体图片多规格展示图能力 - 原型策略
status: pending_review
created_at: 2026-08-22 11:00:33
updated_at: 2026-08-22 11:00:33
---

# 原型策略

## 1. 原型判断

本需求不是新增独立页面，而是上传链路、媒体字段和多端展示策略的能力增强。当前阶段不绘制完整页面 HTML 原型，后续 OpenSpec Change 若涉及管理端上传控件、生成状态面板、历史媒体维护入口或小程序展示改造，必须补齐对应 UI Contract 与截图证据。

## 2. 管理端 UI 策略

- 上传控件应复用既有媒体上传组件或抽取共享 hook，覆盖 `idle -> uploading -> done / failed` 状态。
- 成功后应即时回显缩略图、展示图或文件卡片，不能只显示全局 toast。
- 如果展示派生生成状态，应使用紧凑表格或行内状态，不暴露对象 key 全量值、内部路径或异常堆栈。
- 批量 dry-run / apply 若提供页面入口，应采用明确的范围、风险提示、确认动作和结果统计。

## 3. 小程序 UI 策略

- 列表图片优先快速可见，使用 `thumbnail_url`。
- 详情普通展示使用 `display_url`，首屏外图片延迟加载。
- 图片预览使用 `original_url`，不能因性能优化丢失高清查看能力。
- 图片加载失败时展示稳定 fallback，不应出现空白、无限 loading 或重复请求。

## 4. 后续原型验收要求

- 若创建管理端页面或弹窗，必须遵守 `rules/ui-design.md` 和 Design System semantic token。
- 若创建小程序展示原型，需覆盖列表、详情、预览、失败态和 lazy-load 证据。
- 若出现 `prototype/web/*.html`，后续 `/opsx-apply` 需完成 1440px 视觉证据和关键交互验收。
- PNG 截图当前标记为待导出；待 UI 方案进入 OpenSpec Change 后再补。
