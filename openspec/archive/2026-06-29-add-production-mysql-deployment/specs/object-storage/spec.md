---
change_id: add-production-mysql-deployment
capability: object-storage
created_at: 2026-06-29 09:55:35
updated_at: 2026-06-29 11:18:14
---

## ADDED Requirements

### Requirement: 生产 MinIO 必须持久化并保持单桶策略

生产 Docker Compose MUST 继续使用 MinIO 存储媒体对象，MUST 为 MinIO 配置持久化 volume，MUST 通过 `minio-init` 或等价初始化流程创建单桶 `MINIO_BUCKET`，并 MUST 将桶权限设置为最小权限。生产环境 `MINIO_ACCESS_KEY` 与 `MINIO_SECRET_KEY` MUST 使用非默认值。生产环境上传、媒体 URL、`object_key` 前缀和受控读取规则 MUST 与既有 object-storage capability 保持兼容。

#### Scenario: 生产 Compose 初始化单桶

- **WHEN** 运维启动生产 Compose
- **THEN** `minio-init` 或等价流程 MUST 创建 `MINIO_BUCKET`
- **AND** MUST NOT 创建额外业务 Bucket
- **AND** MinIO 数据 MUST 写入持久化 volume

#### Scenario: 生产媒体上传和读取可用

- **GIVEN** 生产 backend 已连接外部 MySQL 和 MinIO
- **WHEN** `admin` 完成一次图片上传
- **THEN** 对象 MUST 写入 `MINIO_BUCKET`
- **AND** 上传响应中的 `/media/{object_key}` 或等价 URL MUST 可读取该对象
- **AND** 重启 backend、web、minio 后对象 MUST 仍可访问

### Requirement: 外部 MinIO 生产部署必须保持单桶和受控读取策略

当生产环境使用客户已提供的外部 MinIO/S3 兼容对象存储时，系统 MUST 仍使用单桶 `MINIO_BUCKET` 与既有对象 Key 前缀策略。外部 bucket MUST 由运维提前创建，并设置最小权限；backend MUST 通过授权凭据读写对象，Web MUST 继续通过 backend `/media/{object_key}` 反代受控读取，不得要求前端直连对象存储写入。

#### Scenario: 外部 MinIO 上传和读取可用

- **GIVEN** backend 已通过 `MINIO_ENDPOINT` 连接外部 MinIO
- **AND** `MINIO_BUCKET` 已存在且凭据具备读写权限
- **WHEN** `admin` 完成一次图片上传
- **THEN** 对象 MUST 写入外部 `MINIO_BUCKET`
- **AND** 上传响应中的 `/media/{object_key}` MUST 可通过 backend 读取
