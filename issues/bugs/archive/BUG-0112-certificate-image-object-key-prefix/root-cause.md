---
bug_id: BUG-0112-certificate-image-object-key-prefix
title: 证书图片对象 key 未归入 images 前缀根因分析
root_cause_status: drafted
category: design
created_at: 2026-08-04 08:20:26
updated_at: 2026-08-04 08:20:26
---

# BUG-0112 根因分析

## 直接原因

品牌证书上传链路把“证书”按业务对象或附件语义归入 `files/default/brand-certificates/`，没有在图片类证书与 PDF/文档类证书之间强制区分对象前缀。JPG、PNG、WebP 等图片类证书因此可能与 PDF 证书附件共用 `files/` 前缀。

## 根本原因

对象存储前缀规范、媒体上传规范、证书上传实现和回填脚本之间存在口径漂移：

- `rules/object-storage.md` 已把 `images/` 定义为图片类上传标准前缀，并将 `original/` 标记为 deprecated。
- `rules/media.md` 与 `docs/standards/file-upload.md` 仍可能保留或描述旧的 `original/` / `files/default/brand-certificates/` 图片存储口径。
- 品牌证书能力同时承载图片和 PDF 文档，缺少“图片证书走 `images/`，PDF/文档证书走 `files/`”的类型分流门禁。
- 缩略图回填、对象审计和 Skill 验收没有把证书图片前缀作为强制检查项，导致偏差可被后续脚本继续放大。

## 触发条件

- 上传或保存 JPG、PNG、WebP 类型的品牌证书图片。
- 生成或回填证书图片缩略图。
- 运行历史证书图片补齐脚本或媒体对象迁移脚本时沿用旧前缀。
- 依据旧文档或 Skill 说明实现证书图片相关 Change。

## 缺陷分类

| 维度 | 分类 | 说明 |
|---|---|---|
| 主要分类 | design | 资源类型与对象前缀边界设计未在证书混合媒体场景中收敛。 |
| 次要分类 | code | 上传、缩略图和回填实现需要按 MIME/资源类型分流。 |
| 次要分类 | docs | 媒体规范与文件上传标准存在旧前缀残留。 |
| 次要分类 | workflow | Skill 与验收模板缺少证书图片 key 前缀检查。 |

## 修复方向

后续 OpenSpec Change 应同时收敛规范、实现、脚本、Skill 与测试，避免只把单个上传接口改成 `images/` 后仍被历史回填或文档口径带回 `files/`。
