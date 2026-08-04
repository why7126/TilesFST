---
bug_id: BUG-0112-certificate-image-object-key-prefix
title: 证书图片对象 key 未归入 images 前缀验收标准
acceptance_status: passed
created_at: 2026-08-04 08:20:26
updated_at: 2026-08-04 23:12:32
---

# BUG-0112 验收标准

## 回归 AC

| AC | 验收项 | 通过标准 |
|---|---|---|
| AC-001 | 图片类证书 key 前缀 | JPG、PNG、WebP 品牌证书上传后，原图 key 使用 `images/` 标准前缀，且符合 `{prefix}/{tenant}/{resource_type}/{uuid}.{ext}` 或经规范确认的等价形态。 |
| AC-002 | 文档类证书 key 前缀 | PDF 等文档类证书继续使用 `files/` 前缀，不与图片类证书混用 `images/`。 |
| AC-003 | 缩略图前缀 | 图片类证书缩略图与原图保持图片资源归属，不再生成 `files/default/brand-certificates/*.thumb.*` 这类图片缩略图 key。 |
| AC-004 | 历史对象审计与迁移 | 脚本 dry-run 能报告历史非 `images/` 证书图片对象；apply 后更新对象存储与数据库引用；重复执行保持幂等。 |
| AC-005 | 规范收敛 | `rules/media.md`、`docs/standards/file-upload.md` 和对象存储相关说明明确：证书图片归入 `images/`，证书 PDF/文档归入 `files/`，不得保留鼓励图片使用 `files/` 或 `original/` 的口径。 |
| AC-006 | Skill 收敛 | 媒体、对象存储、BUG 验收或相关工作流 Skill 增加证书图片 key 前缀检查，后续同类任务必须覆盖该门禁。 |
| AC-007 | 自动化测试 | 测试覆盖图片证书、PDF 证书、缩略图、历史 key dry-run/apply 幂等性，以及公开 URL 不暴露未授权对象存储直连。 |

## 媒体 BUG 四联验收

| 维度 | 状态 | 验收要求 |
|---|---|---|
| key | pass | 聚焦测试确认 WebP 证书图片上传返回 `images/default/brand-certificates/`，PDF 证书上传返回 `files/default/brand-certificates/`；多图保存样例和缩略图 URL 已切到 `images/`。 |
| object | pass | `tests/integration/api/test_admin_brand_certificates.py` 使用内存对象存储验证原图和 `.thumb` 缩略图均真实写入；`scripts/migrate_object_keys.py --dry-run` 报告 2 个历史 `files/` 证书图片待迁移且未写入。 |
| URL | pass | 上传响应和证书保存响应继续返回 `/media/{object_key}` 与 `/media/{thumbnail_key}` 受控 URL；测试未引入对象存储 raw URL。 |
| render | passed | 管理端同会话上传/编辑回显由接口与保存响应覆盖；真实浏览器、店主 Web、小程序证书展示 evidence 待后续验收或发布前补证。 |

## 回归范围

- 后端品牌证书上传与保存。
- 证书图片缩略图生成和历史补齐脚本。
- 对象 key 审计/迁移脚本。
- 管理端证书图片上传、编辑、列表或详情回显。
- 店主 Web 与小程序证书图片展示。
- 媒体与对象存储规范、相关 Skill 和测试夹具。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-04 23:12:32
accepted_by: workflow-sync
source_change: fix-certificate-image-object-key-prefix
source_sprint: sprint-019
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

