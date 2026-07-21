---
requirement_id: REQ-0055-brand-certificate-common-component
title: 品牌证书通用组件原型上下文
status: pending_review
created_at: 2026-07-19 17:46:26
updated_at: 2026-07-19 17:46:26
source: requirement.md
---

# Prototype Context

## 目标

本原型用于表达品牌证书通用组件的状态矩阵，不是完整品牌证书管理页。实现时优先参考 `acceptance.md`，再参考 HTML 中的组件布局和状态组合。

## 组件状态

| 组件 | 状态 |
|---|---|
| CertificateThumb | 图片缩略图、PDF、文件 fallback、图片加载失败 |
| CertificateSummary | 证书名称、证书编号、文件名 fallback、所属品牌可选 |
| CertificateValidityBadge | 长期有效、有效、即将到期、已过期、未设置 |
| CertificateVisibilityBadge | 前台展示、前台隐藏 |
| CertificatePreviewAction | URL 存在、URL 缺失、预览失败提示 |
| CertificateFileCard | idle、uploading、done、failed |

## 视觉说明

- 使用管理端暗色语义，品牌金只用于强调和主状态，不新增裸 Hex。
- 缩略图固定 52px，文件卡片固定最小高度，避免表格行和弹窗内容跳动。
- 文件卡片在窄视口下允许操作按钮换行。
- PNG Golden Reference 待后续设计验收导出；当前 HTML 为首轮组件状态参考。

## 非目标

- 不展示完整筛选、分页、权限和保存流程。
- 不定义新 API 或上传链路。
- 不承诺店主 Web 或小程序复用样式。
