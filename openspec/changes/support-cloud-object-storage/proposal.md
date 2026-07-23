## Why

当前生产部署文档和 Compose 已支持外部 MinIO/S3 兼容对象存储，但规格、环境变量命名和验收口径仍强绑定 MinIO，导致腾讯云 COS、火山云 TOS 等云上对象存储接入时缺少明确的配置边界、前置检查和兼容性验收。

本变更将云上 S3 兼容对象存储纳入正式部署能力，保持现有后端授权上传、单桶前缀和 `/media/{object_key}` 受控读取不变。

## What Changes

- 将对象存储提供方抽象为 `minio`、`s3-compatible` 等可配置类型，现有 MinIO 配置继续兼容。
- 为腾讯云 COS、火山云 TOS 等 S3 兼容服务补充 endpoint、region、bucket、path-style/virtual-host 风格、TLS 和权限前置检查。
- 更新生产外部对象存储部署说明、`.env.example` 注释和 Docker Compose 环境变量传递。
- 更新后端对象存储适配层，使 bucket 初始化策略可按部署类型控制：本地/自建 MinIO 可自动创建，云上对象存储必须运维预创建并最小授权。
- 补充对象存储连接、上传、读取和非法配置的测试与部署 smoke 清单。
- 不改变前端上传接口、管理端/店主端媒体 URL 语义、数据库媒体 object_key 结构。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `object-storage`: 扩展对象存储规格，从 MinIO 单一实现改为支持 MinIO 与 S3 兼容云上对象存储，同时保持单桶、标准前缀、后端授权上传和受控读取。
- `deployment`: 扩展生产部署规格，明确外部云上对象存储的配置、前置检查、Compose 环境变量和 smoke 验收。

## Impact

- 后端：`src/backend/app/core/config.py`、`src/backend/app/modules/media/storage.py` 及相关对象存储测试。
- 部署：`.env.example`、`docker-compose.prod.external.yml`、必要时 `docker-compose.prod.yml` 注释与变量传递。
- 文档：`docs/02-deployment.md`、`docs/07-object-storage-strategy.md`、`rules/object-storage.md`。
- API：上传与媒体读取接口路径、请求和响应不变；错误码沿用对象存储不可用、媒体不存在、非法 object_key 等既有语义。
- 数据库：不新增表，不修改 SQLite/MySQL schema；继续只保存 `object_key` 等媒体元数据。
- Web/小程序/管理端：不改变调用方式；仍通过后端 API 上传和 `/media/{object_key}` 读取。
