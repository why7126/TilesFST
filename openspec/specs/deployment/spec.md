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

系统 MUST 提供外部服务型生产 Compose 变体（如 `docker-compose.prod.external.yml`）及部署说明，用于客户已提供 MySQL 与 MinIO/S3 兼容对象存储的场景。该 Compose MUST 仅启动 backend 与 web，MUST NOT 启动 mysql、minio 或 minio-init 服务。backend MUST 通过 `DATABASE_URL` 连接外部 MySQL，并通过 `MINIO_ENDPOINT`、`MINIO_ACCESS_KEY`、`MINIO_SECRET_KEY`、`MINIO_BUCKET`、`MINIO_SECURE` 连接外部 MinIO。该场景下 bucket 初始化与权限配置 MUST 作为外部对象存储前置条件，而不是由本项目 Compose 自动创建。

#### Scenario: 外部服务型生产 Compose 只包含应用服务

- **WHEN** 运维检查 `docker-compose.prod.external.yml`
- **THEN** MUST 找到 backend 与 web 服务
- **AND** MUST NOT 找到 mysql、minio、minio-init 服务
- **AND** backend MUST 通过环境变量访问外部 MySQL 与外部 MinIO

#### Scenario: 外部 MinIO 前置条件由运维准备

- **WHEN** 运维阅读生产部署文档
- **THEN** MUST 找到外部 MinIO endpoint、bucket、access key、secret key、TLS 开关与网络可达性检查项
- **AND** MUST 找到 bucket 已存在且权限最小化的说明

### Requirement: 生产部署文档必须包含外部 MySQL 前置检查

生产部署文档 MUST 包含客户 MySQL 前置条件检查清单，至少覆盖 MySQL 版本 8.0+、字符集 `utf8mb4`、collation `utf8mb4_unicode_ci`、账号具备 DDL + DML 权限、VPS 到 MySQL 主机和端口网络可达、生产密钥不得使用 `.env.example` 默认值。若采用外部 MinIO 场景，文档 MUST 同时包含外部 MinIO/S3 兼容存储前置检查。

#### Scenario: 运维按文档检查 MySQL 前置条件

- **WHEN** 运维阅读 `docs/02-deployment.md` 的生产部署章节
- **THEN** MUST 找到 MySQL 8.0+、`utf8mb4`、权限、网络可达和密钥注入检查项
- **AND** MUST 找到禁止使用示例密钥的说明

### Requirement: 生产环境变量文档必须说明 DATABASE_URL 与 SQLite 的关系

`.env.example`、后端环境示例和部署文档 MUST 说明 `DATABASE_URL`、`SQLITE_DATABASE_URL` 与 `APP_ENV` 的关系。生产示例 MUST 使用 MySQL DSN 占位，非生产默认 MUST 继续说明 SQLite 路径。生产 `APP_SECRET_KEY`、MySQL 密码、MinIO 密钥和管理员初始密码 MUST 通过部署环境注入，MUST NOT 在仓库中提交真实值。

#### Scenario: 环境示例区分生产 MySQL 和开发 SQLite

- **WHEN** 开发者检查 `.env.example`
- **THEN** MUST 找到 `APP_ENV`、`DATABASE_URL` 与 `SQLITE_DATABASE_URL` 的说明
- **AND** MUST 明确生产使用 MySQL DSN
- **AND** MUST 明确本地开发可继续使用 SQLite

### Requirement: 本地 Docker Compose 演示部署不得回归

现有 `docker-compose.yml` 和 `./scripts/docker-up.sh` MUST 继续支持本地开发与演示部署，默认使用 SQLite + MinIO。生产 Compose 的新增 MUST NOT 迫使本地开发者安装 MySQL。

#### Scenario: 本地 docker-up 仍使用 SQLite

- **WHEN** 开发者按现有本地文档执行 `./scripts/docker-up.sh`
- **THEN** backend MUST 使用 SQLite 数据卷
- **AND** MinIO MUST 继续按单桶初始化
- **AND** 开发者 MUST NOT 需要本地 MySQL

### Requirement: Web 层 Swagger 代理

The Web deployment layer SHALL proxy Swagger and OpenAPI documentation routes to the backend so Web-origin documentation links work in local development and Docker deployments.

#### Scenario: Vite 开发代理转发 Swagger 路由

- **WHEN** the Web development server receives a request for `/docs`, `/redoc`, or their required nested paths
- **THEN** the request SHALL be proxied to the backend service
- **AND** the response SHALL NOT be the Web SPA `index.html`.

#### Scenario: Docker Nginx 在 SPA fallback 前转发 Swagger 路由

- **WHEN** the Docker Web container receives a request for `/docs`, `/redoc`, or their required nested paths
- **THEN** Nginx SHALL proxy the request to backend
- **AND** the request SHALL be matched before the SPA fallback route.

#### Scenario: 既有代理保持可用

- **WHEN** the Swagger proxy configuration is added
- **THEN** `/api/`, `/media/`, and `/openapi.json` SHALL continue to proxy to backend as before
- **AND** `/admin/api-docs` SHALL continue to be served by the Web SPA.

#### Scenario: 生产 Try It Out 策略保持不变

- **WHEN** production or production-equivalent configuration serves Swagger through the Web proxy
- **THEN** backend Swagger Try It Out SHALL remain hidden or disabled according to the existing environment policy.
