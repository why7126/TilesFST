---
bug_id: BUG-0006-object-storage-upload-not-minio
status: in_sprint
updated_at: 2026-06-26 11:44:07
root_cause_type: backend-storage-adapter/object-storage-integration
---

# 根因分析

## 1. 直接原因

### 1.1 上传接口调用本地文件系统保存逻辑

后端上传接口统一调用 `save_upload_file(file, object_key)` 保存头像、品牌 Logo、SKU 图片和 SKU 视频。该函数当前通过 `resolve_media_path(object_key)` 将对象 Key 映射到 `settings.upload_dir` 下的本地路径，并执行 `media_path.write_bytes(await file.read())`。

因此，业务上传成功后文件落在后端容器的本地挂载目录 `UPLOAD_DIR`，而不是写入 MinIO 的 `MINIO_BUCKET`。

关键证据：

- `src/backend/app/api/v1/uploads.py`：头像、品牌 Logo、SKU 图片、SKU 视频上传均调用 `save_upload_file()`。
- `src/backend/app/modules/media/storage.py`：`resolve_media_path()` 使用 `settings.upload_dir` 解析文件路径。
- `src/backend/app/modules/media/storage.py`：`save_upload_file()` 使用 `write_bytes()` 写入本地文件系统。

### 1.2 媒体读取接口也依赖本地文件系统

`get_media_file_response(object_key)` 通过同一套 `resolve_media_path()` 从本地路径返回 `FileResponse`。这说明当前 `/media/{object_key}` 的受控读取策略绑定在本地 `UPLOAD_DIR`，尚未接入 MinIO 的 `get_object`、签名 URL 或后端代理读取能力。

### 1.3 MinIO 配置存在但未被上传链路使用

项目配置中已经存在 MinIO 相关环境变量和标准前缀：

- `MINIO_ENDPOINT`
- `MINIO_ACCESS_KEY`
- `MINIO_SECRET_KEY`
- `MINIO_SECURE`
- `MINIO_BUCKET`
- `MINIO_PREFIX_*`

Docker Compose 也启动了 `minio` 和 `minio-init`，并由 `minio-init` 创建 `tile-info-platform` 桶。但上传保存路径没有使用 MinIO client，因此桶初始化成功不等于业务对象被写入对象存储。

## 2. 根本原因

### 2.1 媒体存储适配层仍停留在本地开发实现

`src/backend/app/modules/media/storage.py` 文件说明为本地媒体存储与受控媒体文件访问，实际实现也是本地文件系统适配。该实现适合早期快速验证上传和回显，但没有演进为 MinIO 对象存储适配层。

缺失能力包括：

- MinIO client 初始化与健康检查。
- 桶存在性确认或启动期校验。
- 基于 `MINIO_BUCKET` 的 `put_object` 写入。
- 基于标准对象前缀的对象 Key 生成约束。
- 对象读取策略，例如后端代理读取或签名 URL。
- 上传失败时面向 API 的稳定错误码和错误消息。

### 2.2 对象存储规范与实现之间缺少回归门禁

`rules/object-storage.md` 要求“一个项目一个 Bucket，桶内按对象前缀区分资源类型”，并复用 `.env.example` 中的 `MINIO_BUCKET`。当前代码虽然生成了 `original/`、`videos/` 等前缀形式的对象 Key，但对象实际存储位置仍是本地目录。

现有测试主要验证：

- 上传接口返回 `object_key` 和 `/media/{object_key}`。
- 本地 `/media` 读取可访问。
- 路径穿越被拒绝。

测试没有验证对象是否写入 MinIO bucket，因此本地文件系统实现通过了回归，而对象存储集成缺陷没有被拦截。

### 2.3 Docker 环境挂载掩盖了对象存储未接入问题

Docker Compose 同时挂载了：

- `./data/uploads:/app/data/uploads`
- `./data/minio:/data`

业务上传写入 `data/uploads` 时，上传和本地 `/media` 回显可能仍然可用；但 MinIO Console 只展示 `data/minio` 中的桶内容。因此用户会看到“上传接口成功，但对象存储桶内无业务对象”的割裂状态。

## 3. 触发条件

满足以下条件时可稳定触发：

1. 使用本地或 Docker Compose 环境启动后端、Web 和 MinIO。
2. `minio-init` 成功创建 `tile-info-platform` 桶。
3. 管理端执行头像、品牌 Logo、SKU 图片或 SKU 视频上传。
4. 上传接口返回成功，前端拿到 `object_key` 和 `/media/{object_key}`。
5. 打开 MinIO Console 查看 `tile-info-platform` 桶。
6. 桶内没有对应业务对象。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | backend-storage-adapter / object-storage-integration |
| 直接原因 | 上传保存函数写入 `UPLOAD_DIR` 本地路径，未调用 MinIO client |
| 根本原因 | 媒体存储适配层未从本地文件系统实现演进为 MinIO 对象存储实现 |
| 是否接口缺陷 | 是；上传接口的实际持久化位置不符合对象存储规范 |
| 是否数据库缺陷 | 待确认；当前元数据字段可能仍只保存 `object_key`，但需确认是否记录本地路径语义 |
| 是否权限缺陷 | 不是直接权限缺陷；修复时必须保持后端鉴权与受控读取 |
| 是否对象存储缺陷 | 是 |
| 是否 Docker 缺陷 | 不是主要根因；Docker 已启动 MinIO 并创建桶，但业务代码未写入 |
| 主要修复面 | 后端媒体存储适配、MinIO 写入、媒体读取策略、错误码、集成测试 |

## 5. 后续修复建议

1. 在媒体模块中引入 MinIO 存储适配层，封装 `put_object`、`get_object` 或签名 URL 能力。
2. `save_upload_file()` 应写入 `settings.minio_bucket`，并继续使用标准对象前缀。
3. `/media/{object_key}` 应改为受控读取 MinIO 对象，或返回符合安全策略的签名 URL。
4. 上传失败时应返回统一 API 错误结构与稳定错误码，不暴露内部路径或 MinIO 密钥。
5. 保留并强化对象 Key 校验，继续拒绝绝对路径、`..`、反斜杠和空路径。
6. 补充集成测试，验证上传后 MinIO bucket 中存在对象，而不是只验证本地 `/media` 能读。
7. 评估已有 `data/uploads` 中本地文件是否需要迁移；若需要，必须在修复 Change 中明确迁移策略。
