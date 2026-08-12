---
requirement_id: REQ-0106-admin-banner-title-hidden
surface: miniapp
status: pending_review
created_at: 2026-08-10 22:40:54
updated_at: 2026-08-10 22:40:54
---

# Miniapp Prototype Context

## 页面

- 首页：顶部 Banner 轮播。
- 品牌列表页：顶部 Banner 轮播。

## 展示策略

- 有 Banner 图片时，轮播以图片为主视觉。
- 不渲染 Banner `title` 作为前台主标题。
- 与标题绑定的副标题、按钮或空文案容器需在实现阶段一并确认是否移除或保留。
- 无 Banner 时继续使用原有兜底 Hero 文案。

## 验证重点

- 轮播图片比例、裁切和指示器不回归。
- 点击跳转不回归。
- 标题隐藏后不留下空遮罩、空容器或异常点击区域。
