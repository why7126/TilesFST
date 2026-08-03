---
change_id: fix-admin-certificate-list-main-image-name-only
status: applied
type: fix
source_bug: BUG-0107-admin-certificate-list-main-image-name-only
created_at: 2026-08-03 12:01:13
updated_at: 2026-08-03 12:01:13
owner: product
iteration: sprint-018
---

# Change Trace

## 来源

- BUG: `issues/bugs/archive/BUG-0107-admin-certificate-list-main-image-name-only/`

## 影响范围

```yaml
backend: false
web: true
miniapp: false
admin: true
database: false
storage: false
api: false
capabilities:
  new: []
  modified:
    - brand-certificate-management
```

## 文档同步

| 项 | 结论 | 说明 |
|---|---|---|
| 长期 docs | 不适用 | 本修复仅收敛管理端列表展示噪音，不改变产品模块边界、API、DB、部署、环境变量或公开使用说明。 |
| Knowledge Base | 已复用 | 复用 `docs/knowledge-base/best-practices/admin-list-page-consistency.md` 与 `docs/knowledge-base/best-practices/admin-media-upload-chain.md`，未发现新的事故模式。 |
| API / Orval | 不适用 | 未新增或修改后端接口、OpenAPI Schema 或 Orval 生成物。 |
| DB / Docker | 不适用 | 未修改 SQLite/MySQL 表结构、迁移、Dockerfile、Compose 或环境变量。 |

## 实现证据

| 项 | 结论 | 证据 |
|---|---|---|
| 列表展示 | 完成 | `CertificateListIdentity` 使用主图缩略图或原图作为预览，不再向列表缩略图传入文件名；`CertificateSummary` 不再以证书编号或文件名作为副标题回退。 |
| 无主图占位 | 完成 | 无主图时保留 PDF/FILE 稳定占位，证书名称仍独立展示。 |
| 噪音隐藏 | 完成 | 目标测试覆盖文件名、图片名、对象 key、原始 URL 不出现在列表证书字段。 |

## 验证证据

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-08-03 09:01:49 | `pnpm --dir src/web exec vitest run src/features/admin/components/BrandCertificateComponents.test.tsx src/pages/admin/BrandCertificateManagementPage.test.tsx` | 2 files / 13 tests passed。 |
| 2026-08-03 09:01:49 | `openspec validate fix-admin-certificate-list-main-image-name-only --strict` | passed。 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-03 12:01:13 | `/opsx-archive BUG-0107` | 归档前补齐验收通过结论、文档同步说明与归档证据。 |
| 2026-08-03 09:01:49 | `/opsx-apply BUG-0107` | 完成管理后台品牌证书列表证书字段修复，待归档。 |
