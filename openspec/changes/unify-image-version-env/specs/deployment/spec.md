## MODIFIED Requirements

### Requirement: 系统必须提供 VPS 生产 Docker Compose 部署

系统 MUST 提供生产向 Docker Compose 文件（如 `docker-compose.prod.yml`）及部署说明，用于在 VPS 上启动 backend、web、minio、minio-init。生产 Compose MUST 连接客户已有 MySQL 实例，MUST NOT 包含 mysql 服务，backend MUST NOT 挂载 `./data/sqlite` 作为生产数据库。生产 Compose MUST 保留宿主机端口可通过 `.env` 覆盖的策略。生产 Compose MUST 支持通过单个 `TILESFST_IMAGE_TAG` 为 backend 与 web 生成默认镜像 tag，并 SHOULD 允许通过独立 repository 变量覆盖镜像仓库名。

#### Scenario: 生产 Compose 不包含 mysql 服务

- **WHEN** 运维检查生产 Compose 文件
- **THEN** MUST 找到 backend、web、minio、minio-init 服务
- **AND** MUST NOT 找到 mysql 服务
- **AND** backend MUST 通过环境变量访问外部 MySQL

#### Scenario: 生产 backend 不挂载 SQLite 数据库卷

- **WHEN** 运维检查生产 Compose 的 backend 服务
- **THEN** backend MUST NOT 将 `./data/sqlite` 挂载为生产数据库
- **AND** backend MUST 使用生产 `DATABASE_URL`

#### Scenario: 生产 Compose 共用镜像版本 tag

- **WHEN** 运维在 `.env` 中设置 `TILESFST_IMAGE_TAG=vX.Y.Z`
- **THEN** 生产 Compose MUST 默认生成 `tilesfst-backend:vX.Y.Z`
- **AND** 生产 Compose MUST 默认生成 `tilesfst-web:vX.Y.Z`
- **AND** 运维不需要分别填写 backend 与 web 的完整镜像版本号

### Requirement: 系统必须支持外部 MySQL 与外部 MinIO 的生产部署

系统 MUST 提供外部服务型生产 Compose 变体（如 `docker-compose.prod.external.yml`）及部署说明，用于客户已提供 MySQL 与外部 MinIO、自建 S3 兼容服务或云上对象存储（如腾讯云 COS、火山云 TOS）的场景。该 Compose MUST 仅启动 backend 与 web，MUST NOT 启动 mysql、minio 或 minio-init 服务。backend MUST 通过 `DATABASE_URL` 连接外部 MySQL，并通过 `OBJECT_STORAGE_*` 环境变量连接外部对象存储；该变量组 MUST 支持 provider、endpoint、region、bucket、TLS、path-style/virtual-host 风格和自动创建 bucket 策略。该场景下 bucket 初始化与权限配置 MUST 作为外部对象存储前置条件，而不是由本项目 Compose 自动创建。外部服务型生产 Compose MUST 同样支持通过单个 `TILESFST_IMAGE_TAG` 为 backend 与 web 生成默认镜像 tag，并 SHOULD 允许通过独立 repository 变量覆盖镜像仓库名。

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

#### Scenario: 外部服务型生产 Compose 共用镜像版本 tag

- **WHEN** 运维在 `.env` 中设置 `TILESFST_IMAGE_TAG=vX.Y.Z`
- **THEN** 外部服务型生产 Compose MUST 默认生成 `tilesfst-backend:vX.Y.Z`
- **AND** 外部服务型生产 Compose MUST 默认生成 `tilesfst-web:vX.Y.Z`
- **AND** 运维不需要分别填写 backend 与 web 的完整镜像版本号
