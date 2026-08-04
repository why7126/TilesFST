---
change_id: fix-certificate-image-object-key-prefix
type: fix
status: proposed
related_bug: BUG-0112-certificate-image-object-key-prefix
created_at: 2026-08-04 08:28:57
updated_at: 2026-08-04 08:28:57
---

# 修复证书图片对象 key 前缀

## 背景

`BUG-0112-certificate-image-object-key-prefix` 已确认：品牌证书的图片类对象可能落在 `files/default/brand-certificates/` 或其他非 `images/` 前缀下，不满足对象存储标准前缀规范。

当前对象存储能力已经要求图片类上传使用 `images/`，文档类资源使用 `files/`。品牌证书同时承载图片和 PDF 文档，若不按 MIME/媒体类型分流，会让证书图片、PDF 附件、缩略图和历史回填脚本混用同一前缀，影响对象审计、缩略图治理和媒体四联验收。

## 变更范围

- 明确品牌证书图片使用 `images/default/brand-certificates/` 或等价标准图片前缀，PDF/文档类证书继续使用 `files/`。
- 修复证书图片上传、证书多图保存、缩略图生成和历史补齐/审计脚本的对象 key 前缀分流。
- 同步更新对象存储、媒体、文件上传、Skill 和测试口径，防止后续 Change 再次沿用旧前缀。
- 补充历史非 `images/` 证书图片 key 的 dry-run/apply 迁移能力或等价审计修复路径。

## 不在本次范围

- 不新增对象存储 bucket。
- 不引入前端直传对象存储。
- 不改变证书 PDF 等文档类附件的 `files/` 归属。
- 不引入视频转码、图片多清晰度或新的公开 CDN 策略。

## 回滚计划

- 若上传路径修复导致证书图片无法展示，回滚后端 key 分流实现并保留数据库引用不变。
- 历史迁移脚本必须先 dry-run，apply 前输出待迁移计数；若 apply 后发现异常，使用迁移日志中的旧 key、新 key 映射回滚数据库引用，并保留对象存储新旧对象直到验证完成。
- 文档和 Skill 变更可随实现回滚，但不得重新允许图片类证书长期使用 `files/` 作为规范目标；回滚说明必须标注临时兼容期限。

## 追溯

- BUG：`BUG-0112-certificate-image-object-key-prefix`
- 父需求：`REQ-0012-object-storage-key-layout`
- 相关能力：`object-storage`、`brand-certificate-management`、`media-acceptance-template`
