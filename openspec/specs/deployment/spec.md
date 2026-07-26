# 部署规范

## Purpose
定义 VPS 生产 Docker Compose、外部 MySQL、外部 MinIO、环境变量文档、本地 demo 不回归和 Web 层 Swagger 代理要求。
## Requirements
### Requirement: 系统必须提供 VPS 生产 Docker Compose 部署

系统 MUST 提供生产向 Docker Compose 文件（如 `docker-compose.prod.yml`）及部署说明，用于在 VPS 上启动 backend、web、minio、minio-init。生产 Compose MUST 连接客户已有 MySQL 实例，MUST NOT 包含 mysql 服务，backend MUST NOT 挂载 `./data/sqlite` 作为生产数据库。生产 Compose MUST 保留宿主机端口可通过 `.env` 覆盖的策略。

#### Scenario: 生产 Compose 不包含 mysql 服务

- **WHEN** 运维检查生产 Compose 文件
- **THEN** MUST 找到 backend、web、minio、minio-init 服务
- **AND** MUST NOT 找到 mysql 服务
- **AND** backend MUST 通过环境变量访问外部 MySQL

#### Scenario: 生产 backend 不挂载 SQLite 数据库卷

- **WHEN** 运维检查生产 Compose 的 backend 服务
- **THEN** backend MUST NOT 将 `./data/sqlite` 挂载为生产数据库
- **AND** backend MUST 使用生产 `DATABASE_URL`

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

### Requirement: 生产环境变量文档必须说明 DATABASE_URL 与 SQLite 的关系

`.env.example`、后端环境示例和部署文档 MUST 说明 `DATABASE_URL` 是唯一数据库连接入口。本地/demo 示例 MUST 使用 SQLite DSN；生产示例 MUST 使用 MySQL DSN 占位。生产 `APP_SECRET_KEY`、MySQL 密码、对象存储密钥和管理员初始密码 MUST 通过部署环境注入，MUST NOT 在仓库中提交真实值。系统 MUST NOT 要求或展示 `SQLITE_DATABASE_URL`。

#### Scenario: 环境示例使用单一 DATABASE_URL

- **WHEN** 开发者检查 `.env.example`
- **THEN** MUST 找到 `DATABASE_URL` 的本地 SQLite 默认值
- **AND** MUST 找到生产使用 MySQL DSN 的说明
- **AND** MUST NOT 找到 `SQLITE_DATABASE_URL`

### Requirement: 本地 Docker Compose 演示部署不得回归

现有 `docker-compose.yml` 和 `./scripts/docker-up.sh` MUST 继续支持本地开发与演示部署，默认使用 SQLite + MinIO。生产 Compose 的新增 MUST NOT 迫使本地开发者安装 MySQL。

#### Scenario: 本地 docker-up 仍使用 SQLite

- **WHEN** 开发者按现有本地文档执行 `./scripts/docker-up.sh`
- **THEN** backend MUST 使用 SQLite 数据卷
- **AND** MinIO MUST 继续按单桶初始化
- **AND** 开发者 MUST NOT 需要本地 MySQL

#### Scenario: 生产入口 smoke 不返回 Nginx 502

- **WHEN** 团队修复生产运行时、外层 Nginx upstream、Docker Web Nginx 或 Backend 启动配置
- **THEN** `https://tilesfst.wjoyhappy.site/` MUST NOT 返回 Nginx 502
- **AND** `https://tilesfst.wjoyhappy.site/api/v1/health` MUST 返回 200 与健康响应
- **AND** 生产 smoke 记录 MUST 包含根路径、健康检查、实际小程序 SKU 接口和实际 `/media/{object_key}` 视频 URL 的响应状态
- **AND** 若生产验证不可执行，Change 验收 MUST 记录具体 N/A 原因和替代生产等价验证。

### Requirement: Web 层 Swagger 代理

The Web deployment layer SHALL proxy Swagger and OpenAPI documentation routes to the backend so Web-origin documentation links work in local development and Docker deployments. Future changes touching Swagger documentation routes, Web proxy configuration, or production deployment documentation MUST explicitly record the dev, Docker, and production-equivalent proxy strategy for `/docs`, `/redoc`, `/openapi.json`, and Swagger UI resource paths.

#### Scenario: Existing backend proxy routes remain intact

- **WHEN** the Swagger proxy configuration is added or production proxy configuration is repaired
- **THEN** `/api/`, `/media/`, and `/openapi.json` SHALL continue to proxy to backend as before
- **AND** existing upload size and media proxy behavior SHALL NOT regress
- **AND** production-equivalent smoke SHALL confirm `/api/v1/health` and `/media/{object_key}` are not handled by the Web SPA fallback.

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

### Requirement: 生产环境上传路径代理配置

生产部署 MUST 对管理端上传路径 `/api/v1/admin/uploads/` 提供与业务上传上限匹配的代理配置。外层 HTTPS Nginx、容器内 Web Nginx、CDN、网关或等价反代 MUST 避免使用默认 60 秒级 upstream 超时截断大文件上传响应链路。上传路径的请求体大小、客户端 body timeout、upstream send/read timeout 和请求缓冲策略 MUST 可被部署验证。

#### Scenario: 容器内 Web Nginx 上传路径配置生效

- **WHEN** Web 容器使用生产镜像或生产等价镜像启动
- **THEN** 运行中的 Nginx 配置 MUST 包含 `/api/v1/admin/uploads/` 专用 location
- **AND** 该 location MUST 配置不低于业务上传上限的 `client_max_body_size`
- **AND** 该 location MUST 配置上传专用 `proxy_send_timeout`、`proxy_read_timeout`、`client_body_timeout` 与 `send_timeout`
- **AND** 验收记录 MUST 说明 `proxy_request_buffering` 策略是否为 `off` 或等价可接受配置。

#### Scenario: 外层 HTTPS 反代上传路径配置生效

- **WHEN** 生产流量经外层 HTTPS Nginx、CDN 或网关进入 Web / backend
- **THEN** 外层代理 MUST 对 `/api/v1/admin/uploads/` 配置上传专用超时
- **AND** 上传合法视频时 MUST NOT 因默认 60 秒 upstream 超时返回 504 或记录 499
- **AND** 若外层代理不由本仓库管理，部署验收记录 MUST 记录配置摘要、验证时间和负责人确认。

#### Scenario: 生产上传 smoke 覆盖 99% 问题

- **WHEN** 发布或修复涉及上传代理、Web 镜像、对象存储或 SKU 视频上传体验
- **THEN** 团队 MUST 执行一次生产或生产等价视频上传 smoke
- **AND** smoke MUST 记录浏览器 Network 状态码、请求总耗时、对象 key、对象存储存在性、`/media/{object_key}` 读取结果
- **AND** smoke MUST 确认管理端 SKU 表单能将上传视频加入列表并保存闭环
- **AND** smoke MUST 记录外层与容器内 Nginx/backend 日志中无同类 60 秒 499/504。

