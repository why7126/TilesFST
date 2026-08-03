---
bug_id: BUG-0112-certificate-image-object-key-prefix
status: captured
severity: high
priority: P1
created_at: 2026-08-04 00:21:47
updated_at: 2026-08-04 00:21:47
lifecycle:
  captured: 2026-08-04 00:21:47
  generated: null
  completed: null
  reviewed: null
  approved: null
  in_sprint: null
  done: null
iteration: null
openspec_changes: []
related_requirement: REQ-0012-object-storage-key-layout
related_bug: null
lifecycle_stage: plan
---

# BUG-0112 证书图片对象 key 未归入 images 前缀

```yaml
bug_id: BUG-0112-certificate-image-object-key-prefix
status: captured
severity: high
priority: P1
created_at: 2026-08-04 00:21:47
updated_at: 2026-08-04 00:21:47
lifecycle:
  captured: 2026-08-04 00:21:47
  generated: null
  completed: null
  reviewed: null
  approved: null
  in_sprint: null
  done: null
iteration: null
openspec_changes: []
related_requirement: REQ-0012-object-storage-key-layout
related_bug: null
lifecycle_stage: plan
```

## 摘要

品牌证书图片当前可能使用 `files/default/brand-certificates/` 或其他非 `images/` 对象前缀，未满足对象存储规范中“图片类上传归入 `images/`”的要求。该偏差会影响证书图片上传、缩略图生成、历史对象回填、媒体四联验收和后续技能执行口径。

## 影响范围

- 后端品牌证书上传与多图保存。
- `brand_certificates`、`brand_certificate_images` 中图片类 `file_key` / `thumbnail_key` 引用。
- 证书图片缩略图生成和历史补齐脚本。
- `rules/object-storage.md`、`rules/media.md`、`docs/standards/file-upload.md` 等媒体存储规范。
- 媒体类 BUG 验收模板与相关 Skill 的对象 key 检查口径。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-04 00:21:47 | /capture | 记录证书图片对象 key 未归入 images 前缀的媒体存储缺陷。 |
