# 设计说明

## 1. Bug Analysis Report

| 项目 | 内容 |
|---|---|
| BUG | `BUG-0006-object-storage-upload-not-minio` |
| 严重等级 | high |
| 环境 | local / docker |
| 现象 | MinIO 与 `tile-info-platform` 桶已初始化，但业务上传对象不进入 MinIO |
| 直接原因 | 上传接口调用 `save_upload_file()`，该函数写入 `settings.upload_dir` 本地路径 |
| 根因分类 | backend-storage-adapter / object-storage-integration |
| 影响入口 | 头像、品牌 Logo、SKU 图片、SKU 视频，以及后续复用媒体上传的管理端能力 |

## 2. 当前链路

```text
POST /api/v1/admin/uploads...
  -> build_upload_object_key(prefix, resource_type, content_type)
  -> save_upload_file(file, object_key)
  -> resolve_media_path(object_key)
  -> settings.upload_dir / object_key
  -> write_bytes(...)

GET /media/{object_key}
  -> resolve_media_path(object_key)
  -> FileResponse(local_path)
```

MinIO 相关配置已经存在于 `settings`，Docker Compose 也启动了 `minio` 与 `minio-init`，但上传和读取链路没有调用 MinIO client。

## 3. 目标链路

```text
POST /api/v1/admin/uploads...
  -> validate auth / MIME / size
  -> build_upload_object_key(...)
  -> media storage adapter.put_object(bucket=MINIO_BUCKET, object_key, stream, content_type)
  -> return UploadResult(object_key, url=/media/{object_key})

GET /media/{object_key}
  -> validate object_key
  -> media storage adapter.get_object(bucket=MINIO_BUCKET, object_key)
  -> StreamingResponse / Response with content-type
```

默认优先保持 `/media/{object_key}` URL 语义，以降低前端和 Orval 变更面。若实现评估后改为签名 URL，必须同步 OpenAPI、Orval、前端调用方和文档。

## 4. 存储适配层

媒体模块应集中封装对象存储访问，不允许业务路由直接调用 MinIO client。建议结构：

```text
src/backend/app/modules/media/storage.py       # 对外接口：save_upload_file/get_media_file_response
src/backend/app/modules/media/object_keys.py   # 对象 key 生成与前缀
src/backend/app/modules/media/minio_client.py  # 可选：MinIO client 工厂/适配
```

实现要求：

- 使用 `settings.minio_endpoint`、`settings.minio_access_key`、`settings.minio_secret_key`、`settings.minio_secure`、`settings.minio_bucket`。
- 不新增业务 Bucket，除非后续 OpenSpec 明确要求。
- 对象 key 必须继续通过 `build_object_key()` 或等价统一函数生成。
- `save_upload_file()` 必须保留上传文件读取大小和错误处理的可测试性。
- MinIO 连接异常、桶不可用、对象不存在应转换为统一 `AppError`，错误码遵守 `docs/standards/error-codes.md`。

## 5. 读取策略

本 change 默认采用受控 `/media/{object_key}` 后端代理：

- 优点：保持当前 `UploadResult.url` 与品牌/SKU/头像回显 URL 兼容。
- 安全：后端校验 object_key，不暴露真实 MinIO endpoint 或密钥。
- 测试：可通过 TestClient 请求 `/media/{object_key}` 验证内容。

实现时可用 MinIO `get_object()` 后返回 `StreamingResponse` 或读取内容返回 `Response`。必须确保响应后释放对象流资源。

## 6. API 与错误码

默认不改变上传响应 schema：

```json
{
  "object_key": "original/default/...",
  "url": "/media/original/default/..."
}
```

若补充 `mime_type`、`size`、`media_id` 等字段，必须同步 OpenAPI、Orval 和文档。已有错误码可复用：

- `50001`：对象存储不可用
- `50002`：文件类型不允许
- `50003`：文件大小超限

非法 object_key 仍属于参数错误或现有媒体路径错误，必须返回 4xx，不得暴露内部路径。

## 7. 数据与迁移

默认不新增 SQLite 字段。当前业务表保存 `*_object_key` 或图片/视频 `object_key`，可继续作为对象存储引用。

本 change 不自动迁移 `data/uploads/` 既有本地文件。若修复阶段发现演示数据需要保留，应在 implementation notes 中记录：

- 是否需要一次性迁移。
- 迁移来源目录和目标前缀。
- 失败回滚方式。

## 8. 测试策略

| 层级 | 验证 |
|---|---|
| Unit | object_key 校验、前缀生成、MinIO adapter 调用参数 |
| Backend pytest | 上传合法图片/视频后调用 MinIO 写入；非法 MIME 拒绝；MinIO 不可用返回稳定错误 |
| Media read | `/media/{object_key}` 从 MinIO 返回内容；非法 object_key 拒绝 |
| Regression | 品牌 Logo、头像、SKU 图片/视频上传入口不回退 |
| Docker | Compose 环境上传后 MinIO Console 或 `mc ls` 可看到对象 |

测试不得依赖真实客户素材、真实密钥或生产 MinIO。

## 9. 风险与缓解

| 风险 | 影响 | 缓解 |
|---|---|---|
| MinIO 服务未就绪 | 上传失败 | 保持 `depends_on`，错误返回 `STORAGE_UNAVAILABLE`；Docker 验证记录启动顺序 |
| 前端依赖 `/media` URL | 图片/视频无法展示 | 默认保留 `/media/{object_key}` 代理 |
| 本地已有 `data/uploads` 文件失联 | 演示素材不可读 | 明确不自动迁移；如需迁移另建任务 |
| 测试连接真实 MinIO 不稳定 | CI 不稳定 | 使用 adapter mock / fake client，Docker 验证作为集成或手工项 |
| 误新增多 Bucket | 部署复杂 | 使用 `settings.minio_bucket`，测试断言 bucket 参数 |

## 10. Open Questions

1. 本次是否需要把 `docs/06-video-asset-management.md` 中历史多桶示例同步为单桶前缀策略？建议在 apply 阶段同步。
2. 是否需要迁移 `data/uploads/` 已有演示文件？默认不迁移，只修复后续上传。
3. 是否补充统一媒体元数据表 `tile_media`？本 BUG 修复不新增表，后续如需要应另建 Change。
