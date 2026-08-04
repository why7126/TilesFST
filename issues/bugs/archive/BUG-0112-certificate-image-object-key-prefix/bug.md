---
bug_id: BUG-0112-certificate-image-object-key-prefix
title: 证书图片对象 key 未归入 images 前缀
severity: high
status: done
owner: null
discovered_at: 2026-08-04 00:21:47
environment: "本地开发 / 对象存储治理检查；涉及 MinIO、S3 兼容对象存储或腾讯 COS 的品牌证书图片链路"
related_requirement: REQ-0012-object-storage-key-layout
related_change: fix-certificate-image-object-key-prefix
created_at: 2026-08-04 08:17:39
updated_at: 2026-08-04 09:24:42
---

# BUG-0112 证书图片对象 key 未归入 images 前缀

## 现象

品牌证书的图片类对象没有稳定存放在 `images/` 标准前缀下，可能继续使用 `files/default/brand-certificates/` 或其他非图片前缀。该行为不满足当前对象存储规范中“图片类上传归入 `images/`，文档类归入 `files/`”的前缀边界。

## 复现步骤

1. 在管理端上传或维护图片类品牌证书，文件类型使用 JPG、PNG 或 WebP。
2. 检查后端保存的证书图片记录，重点查看 `brand_certificate_images.file_key`、主图引用和缩略图 key。
3. 检查对象存储中实际 object key 与数据库引用是否一致。
4. 对比 `rules/object-storage.md` 中标准对象前缀与 `{prefix}/{tenant}/{resource_type}/{uuid}.{ext}` 形态。
5. 如存在历史回填或缩略图补齐脚本，执行 dry-run 并观察图片类证书对象是否仍生成或保留在 `files/` 前缀下。

## 实际结果

图片类品牌证书对象 key 可能位于非 `images/` 前缀，例如 `files/default/brand-certificates/<name>.<ext>` 或同目录缩略图 key。这样会让证书图片与 PDF 等文档类证书附件混用同一前缀，削弱图片资源治理、缩略图生成、对象审计和媒体验收的一致性。

## 期望结果

图片类品牌证书必须使用 `images/` 标准前缀，例如 `images/default/brand-certificates/<uuid>.<ext>` 或规范确认后的等价形态。PDF 等文档类证书附件继续使用 `files/` 前缀。缩略图、回填脚本、对象审计脚本、文档规范和相关 Skill 均应按同一前缀边界执行。

## 影响范围

- 后端品牌证书上传、证书多图保存和主图引用。
- `brand_certificate_images.file_key`、`thumbnail_key` 及相关公开读取 URL。
- 证书图片缩略图生成、历史补齐和对象迁移脚本。
- `rules/media.md`、`docs/standards/file-upload.md`、媒体类 BUG 验收模板和相关 Skill 的执行口径。
- 管理端、店主 Web、小程序证书图片展示与媒体四联验收证据。

## 严重等级说明

严重等级为 `high`。该问题不会直接导致所有证书不可用，但它触及对象存储 key 规范、历史对象迁移、缩略图派生和跨端媒体展示证据链，若继续扩散会让后续修复成本和数据治理风险上升。修复应覆盖规范、脚本、技能、实现和测试，避免只修单点上传路径。
