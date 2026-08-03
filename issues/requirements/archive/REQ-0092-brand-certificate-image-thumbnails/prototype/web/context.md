---
requirement_id: REQ-0092-brand-certificate-image-thumbnails
title: 品牌图片与证书图片真实缩略图使用策略 Prototype Context
owner: product
source: requirement.md
created_at: 2026-08-02 17:55:40
updated_at: 2026-08-02 17:55:40
---

# Prototype Context

## 目标

本 prototype 用于说明品牌图片与证书图片缩略图能力对管理端展示和上传回显的影响，不作为最终 UI 设计稿。

## 覆盖场景

- 品牌列表 Logo 优先使用缩略图，失败回退首字母占位。
- 证书列表和卡片优先使用缩略图，PDF 使用文件类型占位。
- 上传弹窗中展示 `idle / uploading / done / failed` 状态机。
- 缩略图生成失败不阻断原图保存，并在控件内展示可定位错误。
- 存量补齐入口展示 dry-run / apply 状态摘要。

## 不覆盖

- 不定义新的品牌或证书业务字段。
- 不定义真实接口字段名。
- 不替代后续 OpenSpec Change 的设计文档。
- PNG Golden Reference 待后续设计导出；当前 HTML 仅作为布局与状态说明。

## 设计约束

- 管理端保持工业石材暗色旗舰风。
- 列表、卡片、弹窗和 toast 不引入新的视觉体系。
- 上传控件错误必须在字段附近出现。
- 原图预览入口与缩略图展示入口语义分离。
