## Why

`BUG-0006-object-storage-upload-not-minio` 已评审通过并纳入 `sprint-002`。当前 Docker Compose 环境中 MinIO 服务已启动，`minio-init` 也能创建 `tile-info-platform` 桶，但业务上传链路仍把头像、品牌 Logo、SKU 图片、SKU 视频等对象写入本地 `UPLOAD_DIR`，MinIO Console 中看不到业务对象。

根因已在 `issues/bugs/BUG-0006-object-storage-upload-not-minio/root-cause.md` 中确认：后端上传接口统一调用 `save_upload_file()`，当前实现通过 `settings.upload_dir` 将 `object_key` 映射成本地路径并执行 `write_bytes()`；媒体读取接口也依赖本地文件系统 `FileResponse`。这与项目 MinIO 单桶策略、媒体上传安全规范和 Docker 演示部署目标不一致。

## What Changes

- 引入或补齐后端媒体存储适配层：
  - 使用 `settings.minio_bucket` 作为唯一业务 Bucket。
  - 通过 MinIO client 将上传对象写入 `MINIO_BUCKET=tile-info-platform`。
  - 继续使用标准对象前缀，例如 `original/`、`videos/`、`videos/covers/`。
- 修复受控媒体读取链路：
  - `/media/{object_key}` 或等价 URL 必须能从 MinIO 读取对象。
  - 保持 object_key 校验，拒绝路径穿越、绝对路径、反斜杠和空路径。
  - 读取失败返回统一错误结构，不暴露 MinIO 密钥、内部地址或服务器绝对路径。
- 保持上传接口兼容：
  - 默认保留 `object_key` 与 `/media/{object_key}` URL 语义。
  - 若实现需要改变 URL 或错误码语义，必须同步 OpenAPI、Orval、API 文档和前端调用方。
- 补充回归测试：
  - 后端测试覆盖上传后调用 MinIO 适配层写入对象。
  - 覆盖图片/视频前缀、非法 MIME、非法 object_key、MinIO 不可用错误。
  - Docker Compose 验证 MinIO 桶内出现业务对象。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端媒体上传 | `save_upload_file()` 从本地文件写入改为 MinIO 写入或 MinIO-backed adapter |
| 后端媒体读取 | `/media/{object_key}` 或等价 URL 从 MinIO 受控读取对象 |
| Web 管理端 | 头像、品牌 Logo、SKU 图片/视频上传返回 URL 继续可用；若 URL 语义变化需同步调用方 |
| 小程序 | 潜在受益；后续复用媒体 URL 时将读取真实对象存储 |
| API / Orval | 默认不改响应 schema；若 URL、错误码或响应字段变化则必须重新生成 |
| 数据库 | 默认不新增字段；继续保存 object_key；如发现本地路径语义数据需给出迁移策略 |
| Docker Compose | 必须验证 `backend`、`minio`、`minio-init` 上传闭环 |
| 文档 | 需同步 `docs/06-video-asset-management.md`、`docs/07-object-storage-strategy.md`、`docs/03-api-index.md`、`data/README.md`、`.env.example`（若环境变量变化） |
| 测试 | 后端 pytest + 必要集成测试；避免真实密钥和真实客户素材 |

## Rollback Plan

如 MinIO 写入修复导致上传不可用或媒体读取失败：

1. 回滚本 change 对媒体存储适配层、上传保存和媒体读取代码的改动。
2. 保留 object_key 校验和安全错误处理测试中可复用的部分。
3. 临时恢复本地 `UPLOAD_DIR` 读写，仅用于开发环境回显，不作为对象存储验收通过依据。
4. 将 `BUG-0006` 状态回退为 `approved` 或 `in_sprint` 未修复，并保留验收失败记录。
5. 若已写入 MinIO 的测试对象存在，可按对象前缀清理演示/测试数据；不得删除真实客户素材。
