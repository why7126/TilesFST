---
change_id: fix-object-storage-upload-not-minio
status: proposed
created_at: 2026-06-26 13:47:54
---

# 实现备注

## 1. 实现边界

本 change 在 `/opsx-apply` 阶段才允许修改 `src/`。当前 `/bug-opsx` 阶段仅创建 OpenSpec artifacts 与追溯。

## 2. 默认技术决策

- 默认使用 MinIO 单桶 `settings.minio_bucket`。
- 默认保留 `/media/{object_key}` URL 语义，后端代理读取 MinIO。
- 默认不新增数据库字段。
- 默认不自动迁移 `data/uploads` 历史文件。
- 默认不改变上传响应 schema；若实现时必须改变，需同步 OpenAPI 与 Orval。

## 3. 文档待同步

Apply 阶段需检查并同步：

- `.env.example`
- `docs/03-api-index.md`
- `docs/06-video-asset-management.md`
- `docs/07-object-storage-strategy.md`
- `data/README.md`
- `docs/standards/file-upload.md`
- `docs/standards/error-codes.md`（仅当新增错误码时）
