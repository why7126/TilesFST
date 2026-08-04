---
change_id: fix-certificate-image-object-key-prefix
type: fix
status: proposed
related_bug: BUG-0112-certificate-image-object-key-prefix
created_at: 2026-08-04 08:28:57
updated_at: 2026-08-04 08:28:57
---

# 设计说明

## 根因

品牌证书能力同时处理图片类证书和 PDF/文档类证书，但上传实现、文档规范、缩略图脚本和 Skill 验收没有统一按媒体类型分流对象 key。结果是 JPG、PNG、WebP 证书图片可能沿用 `files/default/brand-certificates/`，与 PDF 等文件类资源混在一起。

## 修复方案

1. 在后端媒体 key 生成层明确证书图片资源类型，图片类证书生成 `images/default/brand-certificates/{uuid}.{ext}` 或等价标准图片 key。
2. 保留 PDF/文档类证书的 `files/` 前缀，避免把文档附件错误迁入图片前缀。
3. 证书图片缩略图与原图保持同一图片资源归属，避免继续生成 `files/default/brand-certificates/*.thumb.*`。
4. 增加历史对象审计/迁移脚本能力：dry-run 汇总非 `images/` 证书图片，apply 迁移对象和数据库引用，重复执行幂等。
5. 更新 `rules/media.md`、`docs/standards/file-upload.md` 和相关 Skill，让未来媒体 BUG 和对象存储 Change 都检查证书图片前缀。

## 数据与兼容

- 数据库表结构预计不变；修复重点是 `brand_certificate_images.file_key`、缩略图 key 和相关 URL 的值。
- 历史记录通过迁移脚本更新对象 key 引用；迁移必须保留旧 key 到新 key 的脱敏映射摘要，便于回滚和验收。
- 公开读取仍通过 `/media/{object_key}` 或等价后端受控 URL；不暴露对象存储 raw URL。

## 测试策略

- 后端测试覆盖 JPG、PNG、WebP 证书图片上传后进入 `images/`。
- 后端测试覆盖 PDF 证书文件继续进入 `files/`。
- 缩略图测试覆盖图片类证书缩略图同目录或等价可追溯图片路径。
- 脚本测试覆盖 dry-run、apply、重复 apply 幂等，以及敏感信息不输出。
- 前端或小程序现有展示测试保持不暴露 object key、原始文件名或未授权对象存储直连。

## 风险

- 历史迁移若只更新数据库不复制对象，会导致媒体读取 404；脚本必须先确认对象存在再更新引用。
- 若只修上传不修回填脚本，后续缩略图补齐仍可能生成旧前缀。
- 若文档和 Skill 不同步，后续同类任务可能继续按 `files/` 实现图片证书。
