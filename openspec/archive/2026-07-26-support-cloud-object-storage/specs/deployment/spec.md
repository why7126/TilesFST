## MODIFIED Requirements

### Requirement: 系统必须支持外部 MySQL 与外部 MinIO 的生产部署

系统 MUST 提供外部服务型生产 Compose 变体（如 `docker-compose.prod.external.yml`）及部署说明，用于客户已提供 MySQL 与外部 MinIO、自建 S3 兼容服务或云上对象存储（如腾讯云 COS、火山云 TOS）的场景。该 Compose MUST 仅启动 backend 与 web，MUST NOT 启动 mysql、minio 或 minio-init 服务。backend MUST 通过 `DATABASE_URL` 连接外部 MySQL，并通过 `OBJECT_STORAGE_*` 环境变量连接外部对象存储；该变量组 MUST 支持 provider、endpoint、region、bucket、TLS、path-style/virtual-host 风格和自动创建 bucket 策略。该场景下 bucket 初始化与权限配置 MUST 作为外部对象存储前置条件，而不是由本项目 Compose 自动创建。

#### Scenario: 外部服务型生产 Compose 只包含应用服务

- **WHEN** 运维检查 `docker-compose.prod.external.yml`
- **THEN** MUST 找到 backend 与 web 服务
- **AND** MUST NOT 找到 mysql、minio、minio-init 服务
- **AND** backend MUST 通过环境变量访问外部 MySQL 与外部对象存储

#### Scenario: 外部对象存储前置条件由运维准备

- **WHEN** 运维阅读生产部署文档
- **THEN** MUST 找到外部对象存储 provider、endpoint、region、bucket、access key、secret key、TLS 开关、path-style/virtual-host 风格与网络可达性检查项
- **AND** MUST 找到 bucket 已存在且权限最小化的说明
- **AND** MUST 找到腾讯云 COS、火山云 TOS 等 S3 兼容对象存储的配置示例边界

#### Scenario: 云上对象存储部署 smoke

- **GIVEN** 运维已配置外部 MySQL 与云上对象存储
- **WHEN** 运维执行生产等价 smoke
- **THEN** `docker compose -f docker-compose.prod.external.yml config --services` MUST 仅输出 `backend` 和 `web`
- **AND** 管理员完成一次品牌 Logo 或 SKU 图片上传后，对象 MUST 写入云上 bucket
- **AND** 访问上传响应中的 `/media/{object_key}` MUST 由 backend 受控读取成功

### Requirement: 生产部署文档必须包含外部 MySQL 前置检查

生产部署文档 MUST 包含客户 MySQL 前置条件检查清单，至少覆盖 MySQL 版本 8.0+、字符集 `utf8mb4`、collation `utf8mb4_unicode_ci`、账号具备 DDL + DML 权限、VPS 到 MySQL 主机和端口网络可达、生产密钥不得使用 `.env.example` 默认值。若采用外部对象存储场景，文档 MUST 同时包含外部 MinIO、自建 S3 兼容服务、腾讯云 COS、火山云 TOS 等对象存储前置检查，并明确 bucket 预创建、最小权限、TLS、region、endpoint、path-style/virtual-host 风格和网络白名单要求。

#### Scenario: 运维按文档检查 MySQL 前置条件

- **WHEN** 运维阅读 `docs/02-deployment.md` 的生产部署章节
- **THEN** MUST 找到 MySQL 8.0+、`utf8mb4`、权限、网络可达和密钥注入检查项
- **AND** MUST 找到禁止使用示例密钥的说明

#### Scenario: 运维按文档检查云上对象存储前置条件

- **WHEN** 运维阅读 `docs/02-deployment.md` 的外部服务型生产部署章节
- **THEN** MUST 找到 MinIO、COS、TOS 等对象存储的配置差异说明
- **AND** MUST 找到 bucket 预创建、最小读写权限、endpoint 可达性、region 匹配、TLS 与 path-style/virtual-host 风格的检查项

## ADDED Requirements

### Requirement: 云上对象存储配置不得启动本地 MinIO

本地或生产等价 Docker Compose 在 `OBJECT_STORAGE_PROVIDER` 配置为 `tencent-cos`、`volcengine-tos`、`s3-compatible` 等外部对象存储时，MUST NOT 默认启动 `minio` 或 `minio-init` 服务。自建 MinIO MUST 通过显式 profile 或专用生产 Compose 启动，避免云上对象存储部署同时创建本地 bucket 并误导排障。

#### Scenario: 默认 Compose 不启动 MinIO

- **GIVEN** Compose 未启用自建对象存储 profile
- **WHEN** 运维执行 `docker compose config --services`
- **THEN** MUST 仅包含应用服务和网络所需服务
- **AND** MUST NOT 包含 `minio` 或 `minio-init`

#### Scenario: 自建对象存储 profile 启动 MinIO

- **GIVEN** 运维明确启用 `self-hosted-storage` profile
- **WHEN** 运维执行 `docker compose --profile self-hosted-storage config --services`
- **THEN** MUST 包含 `minio` 和 `minio-init`
