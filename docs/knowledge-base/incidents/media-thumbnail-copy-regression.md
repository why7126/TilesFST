---
title: 缩略图对象复制原图导致性能优化失效
purpose: 沉淀 BUG-0100 中“对象存在不等于真实轻量缩略图”的媒体链路经验
content: SKU 图片缩略图生成、历史审计与验收要点
source: BUG-0100 / fix-media-thumbnail-generation
created_at: 2026-08-01 08:05:25
updated_at: 2026-08-01 08:05:25
status: draft
---

# 缩略图对象复制原图导致性能优化失效

## 现象

SKU 图片上传后会生成同目录 `.thumb` 对象，小程序商品卡片也优先返回 `.thumb` URL，但缩略图对象可能只是原图 bytes 的复制品。此时对象存在、URL 可访问、小程序图片可显示都成立，实际移动端加载体积没有下降。

## 根因

媒体链路把“生成缩略图 key 并写入对象”误当作“生成真实缩略图”。上传链路和历史回填脚本都直接复制原图 bytes，测试也只覆盖对象存在性和 URL 可访问性，缺少像素尺寸、文件体积和 bytes 差异断言。

## 预防

- 媒体性能类验收必须同时检查对象存在、URL 可访问、像素尺寸、bytes 差异和文件体积。
- 大图生成 `.thumb` 后，宽高应不超过目标最大宽高，bytes 不得与原图完全一致。
- 历史审计脚本需要统计缺失缩略图、同 size、同 bytes、需要重生成、跳过和失败原因。
- dry-run 不写对象存储；apply/execute 必须幂等，已合格缩略图不得重复破坏。
- 透明 PNG/WebP、小图和异常图片要有明确策略，避免为了压缩破坏图片显示。

## 关联

- `issues/bugs/archive/BUG-0100-thumbnail-size-equals-original/`
- `openspec/changes/fix-media-thumbnail-generation/`
- `scripts/audit-miniapp-card-images.py`
