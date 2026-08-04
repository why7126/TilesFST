---
bug_id: BUG-0112-certificate-image-object-key-prefix
status: done
severity: high
priority: P1
created_at: 2026-08-04 00:21:47
updated_at: 2026-08-04 09:28:29
lifecycle:
  captured: 2026-08-04 00:21:47
  generated: 2026-08-04 08:17:39
  completed: 2026-08-04 08:20:26
  reviewed: 2026-08-04 08:24:14
  approved: 2026-08-04 08:24:14
  sprint_joined: 2026-08-04 08:38:42
  done: 2026-08-04 09:24:42
iteration: sprint-019
openspec_changes:
  - change_id: fix-certificate-image-object-key-prefix
    type: fix
    status: archived
related_requirement: REQ-0012-object-storage-key-layout
related_bug: null
lifecycle_stage: archive
---

# BUG-0112 证书图片对象 key 未归入 images 前缀

```yaml
bug_id: BUG-0112-certificate-image-object-key-prefix
status: done
severity: high
priority: P1
created_at: 2026-08-04 00:21:47
updated_at: 2026-08-04 09:25:04
lifecycle:
  captured: 2026-08-04 00:21:47
  generated: 2026-08-04 08:17:39
  completed: 2026-08-04 08:20:26
  reviewed: 2026-08-04 08:24:14
  approved: 2026-08-04 08:24:14
  sprint_joined: 2026-08-04 08:38:42
  done: 2026-08-04 09:24:42
iteration: sprint-019
openspec_changes:
  - change_id: fix-certificate-image-object-key-prefix
    type: fix
    status: archived
related_requirement: REQ-0012-object-storage-key-layout
related_bug: null
lifecycle_stage: archive
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
| 2026-08-04 09:25:04 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-certificate-image-object-key-prefix） |
| 2026-08-04 09:24:42 | /opsx-archive | Change `fix-certificate-image-object-key-prefix` 已归档，状态同步完成。 |
| 2026-08-04 08:55:11 | /opsx-apply | Change `fix-certificate-image-object-key-prefix` apply 完成，已 archive。 |
| 2026-08-04 08:38:42 | /sprint-propose | 纳入 sprint-019，关联 Change fix-certificate-image-object-key-prefix。 |
| 2026-08-04 08:28:57 | /bug-opsx | 创建 Change fix-certificate-image-object-key-prefix。 |
| 2026-08-04 08:24:48 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-04 08:24:14 | /bug-review --approve | 评审通过，状态推进为 approved，阶段迁移 plan → review。 |
| 2026-08-04 08:20:26 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态曾推进为 review_ready，现已闭环。 |
| 2026-08-04 08:17:39 | /bug-generate | 生成 bug.md，完成初稿生成，现已闭环。 |
| 2026-08-04 00:21:47 | /capture | 记录证书图片对象 key 未归入 images 前缀的媒体存储缺陷。 |

- 2026-08-04 09:24:42 workflow-sync：状态同步为 done（Change archived）
