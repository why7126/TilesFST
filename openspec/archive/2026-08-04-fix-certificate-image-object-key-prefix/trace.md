---
change_id: fix-certificate-image-object-key-prefix
type: fix
status: archived
created_at: 2026-08-04 08:28:57
updated_at: 2026-08-04 09:23:49
related_bug: BUG-0112-certificate-image-object-key-prefix
related_requirement: REQ-0012-object-storage-key-layout
sprint: sprint-019
---

# 变更追踪

## 基本信息

```yaml
change_id: fix-certificate-image-object-key-prefix
type: fix
status: archived
related_bug: BUG-0112-certificate-image-object-key-prefix
related_requirement: REQ-0012-object-storage-key-layout
sprint: sprint-019
created_at: 2026-08-04 08:28:57
updated_at: 2026-08-04 09:23:49
```

## 缺陷分析报告

| 字段 | 内容 |
|---|---|
| 现象 | 品牌证书图片类对象可能位于 `files/default/brand-certificates/` 或其他非 `images/` 前缀。 |
| 复现 | 上传 JPG、PNG、WebP 证书图片后检查 `brand_certificate_images.file_key`、主图 key 与缩略图 key。 |
| 影响 | 对象 key 规范、证书图片缩略图、历史迁移、媒体四联验收、管理端/店主端/小程序证书展示。 |
| 根因分类 | design / code / docs / workflow |
| 严重等级 | high |
| 关联需求 | REQ-0012-object-storage-key-layout |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-04 09:23:49 | /opsx-archive | 归档到 `openspec/archive/2026-08-04-fix-certificate-image-object-key-prefix/`。 |
| 2026-08-04 08:55:11 | /opsx-apply | apply 完成，待 archive。 |
| 2026-08-04 08:38:42 | /sprint-propose | 纳入 sprint-019 正式范围。 |
| 2026-08-04 08:28:57 | /bug-opsx | 由 BUG-0112 创建修复 Change。 |
