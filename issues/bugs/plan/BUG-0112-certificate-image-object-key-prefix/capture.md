---
bug_id: BUG-0112-certificate-image-object-key-prefix
title: 证书图片对象 key 未归入 images 前缀
status: captured
severity: high
priority: P1
source: "/capture"
captured_via: capture
classification_rationale: "对象存储规范已要求图片类上传使用 images/ 标准前缀，但品牌证书图片仍可能落在 files/default/brand-certificates/ 或其他非 images 前缀下，属于既有媒体存储规范与实现/脚本/技能约束不一致导致的缺陷。"
created_at: 2026-08-04 00:21:47
updated_at: 2026-08-04 00:21:47
related_requirement: REQ-0012-object-storage-key-layout
related_bug: null
iteration: null
openspec_changes: []
---

# BUG-0112 证书图片对象 key 未归入 images 前缀

## 原始描述

存储对象中，证书的图片没有存在 images 下方，不满足规范。需要修复并优化规范、脚本和技能。

## 分类分析

| 字段 | 内容 |
|---|---|
| 类型倾向 | BUG |
| 判断依据 | `rules/object-storage.md` 已定义 `images/` 为图片类上传标准前缀，且 `original/` 已标记为 deprecated；证书图片属于图片类媒体，落在非 `images/` 前缀是已有规范下的偏差。 |
| 影响范围 | 品牌证书图片上传、证书多图与主图记录、缩略图补齐/回填脚本、对象 key 校验、媒体验收模板、后续技能执行口径。 |
| 严重程度 | high |
| 优先级 | P1 |

## 复现或验证要点

- 上传或回填图片类品牌证书，检查 `brand_certificate_images.file_key`、主图 `file_key` 与缩略图 key。
- 确认证书图片 key 使用 `images/default/brand-certificates/<uuid>.<ext>` 或经规范确认的 `images/{tenant}/brand-certificates/{uuid}.{ext}` 形态。
- 确认 PDF 等文档类证书仍使用 `files/` 前缀，图片类证书不得混入 `files/`。
- 确认缩略图与原图保持同一图片资源归属，不再生成 `files/default/brand-certificates/*.thumb.*` 这类图片缩略图 key。
- 确认审计/回填脚本能 dry-run 报告历史非 `images/` 证书图片对象，并在 apply 后幂等迁移对象 key 与数据库引用。
- 确认 `rules/media.md`、`docs/standards/file-upload.md`、相关 Skill 和校验脚本不再鼓励证书图片使用 `files/` 或 `original/` 前缀。

## 建议修复方向

- 收敛规范：明确证书图片属于 `images/`，证书 PDF/文档附件属于 `files/`。
- 收敛实现：后端证书图片上传、证书多图保存、缩略图生成与公开读取统一使用图片前缀生成器。
- 收敛脚本：补充历史证书图片对象 key 审计/迁移或现有缩略图回填脚本前缀校验，默认 dry-run，`--apply` 后更新对象与数据库引用。
- 收敛技能：在媒体、对象存储、BUG 验收相关技能中加入证书图片 key 前缀检查，避免后续 Change 再次遗漏。
- 补充测试：覆盖 JPG/PNG/WebP 证书图片 key、PDF 证书文件 key、缩略图 key、历史非 `images/` key 的 dry-run/apply 幂等性。
