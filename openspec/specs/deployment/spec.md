# 部署规范

## Purpose
定义 VPS 生产 Docker Compose、外部 MySQL、外部 MinIO、环境变量文档、本地 demo 不回归和 Web 层 Swagger 代理要求。
## Requirements
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
`.env.example`、后端环境示例和部署文档 MUST 说明 `DATABASE_URL` 是唯一数据库连接入口。本地/demo 示例 MUST 使用 SQLite DSN；生产示例 MUST 使用 MySQL DSN 占位。生产 `APP_SECRET_KEY`、MySQL 密码、对象存储密钥和管理员初始密码 MUST 通过部署环境注入，MUST NOT 在仓库中提交真实值。系统 MUST NOT 要求或展示 `SQLITE_DATABASE_URL`。当发布涉及数据库 schema 或 migration 时，镜像准备和发布确认 SHALL 将 schema、migration、数据库文档和回滚说明纳入非敏感证据链。

#### Scenario: 环境示例使用单一 DATABASE_URL
- **WHEN** 开发者检查 `.env.example`
- **THEN** MUST 找到 `DATABASE_URL` 的本地 SQLite 默认值
- **AND** MUST 找到生产使用 MySQL DSN 的说明
- **AND** MUST NOT 找到 `SQLITE_DATABASE_URL`

#### Scenario: 数据库变更进入镜像输入证据
- **WHEN** a release includes database schema or migration changes
- **THEN** `/image-prepare` SHALL include SQLite schema, MySQL schema, migration scripts, database documentation, and rollback evidence requirements in the image build plan
- **AND** `/image-build` SHALL record database-related input hashes in the image manifest
- **AND** release publish SHALL reject stale image evidence when database input hashes have drifted after the manifest was generated.

### Requirement: 本地 Docker Compose 演示部署不得回归

现有本地 Docker Compose 演示部署 MUST 继续可用，默认使用 SQLite + 项目自建 MinIO。引入 `deploy/` 后，系统 MUST 保留根目录默认 `docker compose up` 兼容入口或等价 wrapper，开发者仍可低摩擦启动默认本地环境。环境化部署入口 SHOULD 迁移到 `deploy/local/compose.yml` 与 `deploy/scripts/up.sh`，但该迁移 MUST NOT 迫使本地开发者安装 MySQL。

#### Scenario: 本地默认入口仍可启动 SQLite + MinIO

- **WHEN** 开发者按本地默认入口执行 `docker compose up` 或 `./scripts/docker-up.sh`
- **THEN** backend MUST 使用 SQLite 数据卷
- **AND** 项目自建 MinIO MUST 按单桶策略初始化
- **AND** 开发者 MUST NOT 需要本地 MySQL

#### Scenario: 本地环境化入口支持环境 ID

- **WHEN** 开发者执行 `./deploy/scripts/up.sh local sqlite-minio-managed`
- **THEN** 系统 MUST 使用本地环境对应 env 与 Compose 入口启动 backend、web、minio 和 minio-init
- **AND** 输出 MUST 展示 Web、Backend API 和 MinIO Console 访问地址
- **AND** 输出 MUST NOT 展示真实密钥或完整 `.env` 内容

### Requirement: Web 层 Swagger 代理

The Web deployment layer SHALL proxy Swagger and OpenAPI documentation routes to the backend so Web-origin documentation links work in local development and Docker deployments. Future changes touching Swagger documentation routes, Web proxy configuration, or production deployment documentation MUST explicitly record the dev, Docker, and production-equivalent proxy strategy for `/docs`, `/redoc`, `/openapi.json`, and Swagger UI resource paths.

#### Scenario: Existing backend proxy routes remain intact

- **WHEN** the Swagger proxy configuration is added or production proxy configuration is repaired
- **THEN** `/api/`, `/media/`, and `/openapi.json` SHALL continue to proxy to backend as before
- **AND** existing upload size and media proxy behavior SHALL NOT regress
- **AND** production-equivalent smoke SHALL confirm `/api/v1/health` and `/media/{object_key}` are not handled by the Web SPA fallback.

### Requirement: 云上对象存储配置不得启动本地 MinIO

本地或生产等价 Docker Compose 在 `OBJECT_STORAGE_PROVIDER` 配置为 `tencent-cos`、`volcengine-tos`、`s3-compatible` 等外部对象存储时，MUST NOT 默认启动 `minio` 或 `minio-init` 服务。自建 MinIO MUST 通过显式 profile、环境 ID 或专用生产 Compose 启动，避免云上对象存储部署同时创建本地 bucket 并误导排障。

#### Scenario: 外部对象存储环境 ID 不启动 MinIO

- **GIVEN** 操作人员选择 `local-sqlite-tencent-cos`、`local-mysql-tencent-cos` 或 `prod-mysql-tencent-cos`
- **WHEN** 部署脚本解析 Compose 和 profile
- **THEN** MUST NOT 启用本地 `minio` 或 `minio-init`
- **AND** validate-env MUST 要求对象存储 endpoint、region、bucket、TLS 和密钥变量满足所选 provider 要求

#### Scenario: 自建对象存储环境 ID 启动 MinIO

- **GIVEN** 操作人员选择 `local-sqlite-minio-managed` 或 `local-mysql-minio-managed`
- **WHEN** 部署脚本解析 Compose 和 profile
- **THEN** MUST 启用项目自建 MinIO 所需 profile 或 Compose 服务
- **AND** MUST 初始化 `OBJECT_STORAGE_BUCKET`

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

### Requirement: Docker Compose 可选启动 Mintlify 文档站
部署能力 SHALL 支持通过 Docker Compose 可选 profile 启动 Mintlify 文档站服务，用于本地预览、演示部署或受控生产部署。

#### Scenario: 默认 Compose 不启动文档站服务
- **GIVEN** 运维未启用文档站 profile
- **WHEN** 运维执行默认 Docker Compose 启动或服务清单检查
- **THEN** Mintlify 文档站服务 SHALL NOT 被无条件启动
- **AND** backend、web、minio 或对象存储服务 SHALL NOT 依赖 Mintlify 文档站服务才能启动。

#### Scenario: docs-site profile 启动文档站
- **GIVEN** `mintlify/` 站点源目录已生成并通过校验
- **WHEN** 运维执行 `docker compose --profile docs-site up -d` 或等价命令
- **THEN** Compose SHALL 启动 Mintlify 文档站服务
- **AND** 服务 SHALL 使用 `mintlify/` 作为工作目录或挂载源
- **AND** 服务 SHALL 使用 `mintlify/mint.json`、`mintlify/docs.json` 或等价 Mintlify 配置启动文档站
- **AND** 服务 SHALL NOT 将 Docker volume 直接挂载到 Mintlify CLI 会重命名的 `/home/node/.mintlify` 路径。

#### Scenario: 文档站服务端口可配置
- **WHEN** Compose 定义 Mintlify 文档站服务端口
- **THEN** 宿主机端口 SHALL 通过 `.env.example` 中的变量配置，例如 `HOST_PORT_MINTLIFY_DOCS`
- **AND** 项目 SHALL 在端口规则和部署文档中说明容器内端口、宿主机端口和端口冲突处理方式
- **AND** 实现 SHALL NOT 在多个文件中硬编码不可覆盖的文档站宿主机端口。

### Requirement: Mintlify 文档站部署说明和发布门禁
部署能力 SHALL 文档化 Mintlify 文档站的本地、演示和生产部署选择，并 SHALL 在发布涉及 Compose 文档站服务时纳入验证证据。

#### Scenario: 部署文档说明文档站承载方式
- **WHEN** 运维阅读部署文档
- **THEN** 文档 SHALL 说明本地或演示环境如何通过 Compose profile 启动 Mintlify 文档站
- **AND** 文档 SHALL 说明生产可选择 Compose 内 Mintlify 服务、外部 Mintlify 托管、静态托管、CDN rewrite 或反向代理
- **AND** 未确认生产承载方式时，发布准备 SHALL 记录 blocker 或待确认项。

#### Scenario: Compose 文档站服务进入发布范围
- **WHEN** 发布范围包含 Mintlify Compose service、Dockerfile、Compose 配置或相关 `.env.example` 变量变更
- **THEN** 发布流程 SHALL 要求 Docker Compose 验证证据
- **AND** 发布流程 SHALL 按发布规范判断是否需要 `/image-prepare` 与 `/image-build` 证据
- **AND** 验证证据 SHALL NOT 包含真实生产域名、外部托管账号、访问 token、真实 `.env` 或不可公开运维信息。

#### Scenario: Compose 注释和环境变量同步
- **WHEN** 新增或修改 Mintlify 文档站 service、ports、volumes、profiles、environment 或 command
- **THEN** Compose 文件 SHALL 包含邻近注释说明用途、默认值、安全边界和持久化影响
- **AND** `.env.example`、`rules/environment.md`、`rules/port-management.md` 和 `docs/02-deployment.md` SHALL 同步说明相关变量和端口
- **AND** 若文档站预览缓存不持久化，部署文档 SHALL 明确该缓存不是业务数据且不写宿主机 `~/.mintlify*`。

### Requirement: 系统必须提供部署环境矩阵

系统 MUST 在 `deploy/` 下提供部署环境矩阵，用稳定环境 ID 描述本地与生产部署组合。每个环境 ID MUST 映射到 env 示例、Compose 文件、profile 策略、必填变量、安全边界和启动命令。部署矩阵 MUST 遵守“一拓扑一 Compose + 一环境一 env 示例”原则。生产部署矩阵涉及媒体历史维护时，MUST 支持受控的一次性维护作业入口，并 SHOULD 以 `deploy/prod/compose.tencent-cos.yml` 作为当前生产主路径。

#### Scenario: 本地部署矩阵覆盖六种组合

- **WHEN** 开发者阅读 `deploy/local/README.md` 或 `docs/02-deployment.md`
- **THEN** MUST 找到 `local-sqlite-minio-managed`
- **AND** MUST 找到 `local-sqlite-minio-external`
- **AND** MUST 找到 `local-sqlite-tencent-cos`
- **AND** MUST 找到 `local-mysql-minio-managed`
- **AND** MUST 找到 `local-mysql-minio-external`
- **AND** MUST 找到 `local-mysql-tencent-cos`
- **AND** 每个环境 MUST 标注数据库、对象存储、Compose 文件、profile 和 env 示例路径

#### Scenario: 生产部署矩阵覆盖腾讯云 COS

- **WHEN** 运维阅读 `deploy/prod/README.md` 或 `docs/02-deployment.md`
- **THEN** MUST 找到 `prod-mysql-tencent-cos`
- **AND** MUST 说明生产使用外部 MySQL 与腾讯云 COS
- **AND** MUST 说明 `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false`
- **AND** MUST 说明 bucket、权限、region、endpoint 和密钥由运维前置准备

#### Scenario: Compose 按拓扑复用

- **WHEN** 团队新增或检查本地部署环境
- **THEN** 环境变量差异 MUST 通过 `.env.example` 表达
- **AND** 服务拓扑差异 MUST 通过 Compose 或 profile 表达
- **AND** 不得为本地六种环境复制六份完整 Compose

#### Scenario: 生产维护作业入口属于部署矩阵

- **WHEN** 运维阅读生产部署矩阵或生产维护任务文档
- **THEN** MUST 找到媒体历史维护作业的 Compose 执行入口
- **AND** SHOULD 找到 `tilesfst-maintenance` service 或等价受控维护入口
- **AND** MUST 说明根目录 `docker-compose.prod.external.yml` 若保留，仅作为兼容入口
- **AND** MUST 说明维护作业不得要求下载生产 `.env` 到开发机。

### Requirement: 系统必须治理 deploy 目录边界

系统 MUST 正式允许并约束一级 `deploy/` 目录。`deploy/` MUST 只存放部署矩阵、环境化 Compose、env 示例、部署 README、部署脚本和部署校验工具。`deploy/` MUST NOT 存放真实 `.env`、真实密钥、真实数据库连接串、对象存储凭据、真实客户数据、运行时数据库文件、MinIO 对象数据或镜像 tar 包。

#### Scenario: 目录结构校验允许合法 deploy 结构

- **WHEN** 团队运行目录结构校验
- **THEN** `deploy/README.md` MUST 被允许
- **AND** `deploy/local/` MUST 被允许
- **AND** `deploy/prod/` MUST 被允许
- **AND** `deploy/scripts/` MUST 被允许

#### Scenario: 目录结构校验阻断敏感或运行时文件

- **WHEN** `deploy/` 下出现真实 `.env`、数据库文件、MinIO 数据目录或镜像 tar 包
- **THEN** 目录结构校验 MUST 报告 blocker
- **AND** 输出 MUST 不展示敏感文件内容

### Requirement: 部署脚本必须集中环境解析与校验

系统 SHOULD 将核心部署 up/down/validate 逻辑集中在 `deploy/scripts/`。`scripts/docker-up.sh` 与 `scripts/docker-down.sh` MAY 保留为兼容 wrapper，但 MUST NOT 重复维护复杂环境解析逻辑。

#### Scenario: up 脚本按环境 ID 启动

- **WHEN** 操作人员执行 `./deploy/scripts/up.sh local mysql-tencent-cos`
- **THEN** 脚本 MUST 解析 domain 为 `local`
- **AND** MUST 解析 environment 为 `mysql-tencent-cos`
- **AND** MUST 定位对应 env 示例或真实 env 路径
- **AND** MUST 定位对应 Compose 文件
- **AND** MUST 在启动前执行环境校验

#### Scenario: down 脚本按部署域停止

- **WHEN** 操作人员执行 `./deploy/scripts/down.sh local`
- **THEN** 脚本 MUST 使用本地域 Compose 停止服务
- **AND** MUST 输出是否保留 SQLite、MinIO 或其他数据卷的说明

#### Scenario: 兼容 wrapper 转调新入口

- **WHEN** 开发者执行 `./scripts/docker-up.sh`
- **THEN** wrapper SHOULD 转调 `./deploy/scripts/up.sh local sqlite-minio-managed`
- **AND** wrapper MUST NOT 复制完整环境矩阵逻辑

### Requirement: 部署环境示例必须安全可审查

系统 MUST 为每个部署环境提供独立 `.env.example`。每个 env 示例 MUST 使用示例值，并按环境标识、应用安全、数据库、镜像、对象存储、端口等适用主题分组。每个变量上一行 MUST 说明用途、候选值或候选格式、默认值含义或安全边界。生产 env 示例 MUST 要求 MySQL、腾讯云 COS、`APP_ENV=production`、`APP_DEBUG=false`、非示例密钥和 `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false`。若生产维护作业新增环境变量、service、profile 或 command，相关 env 示例和 Compose 注释 MUST 同步说明用途、安全边界和禁止提交真实值。

#### Scenario: 本地 env 示例可复制

- **WHEN** 开发者检查 `deploy/local/*.env.example`
- **THEN** 每个文件 MUST 说明对应环境 ID
- **AND** MUST 使用清晰分组组织变量
- **AND** MUST 为布尔、枚举、provider、region、端口和连接串变量说明候选值或候选格式
- **AND** MUST 说明复制为真实 env 的目标路径或命令入口
- **AND** MUST 不包含真实密钥、真实连接串或真实客户数据

#### Scenario: 生产 env 示例阻止本地配置泄露到生产

- **WHEN** 运维检查 `deploy/prod/mysql-tencent-cos.env.example`
- **THEN** MUST 找到 `APP_ENV=production`
- **AND** MUST 找到 `APP_DEBUG=false`
- **AND** MUST 找到 MySQL `DATABASE_URL` 占位说明
- **AND** MUST 找到生产变量分组和候选值说明
- **AND** MUST 找到腾讯云 COS provider、region、endpoint、bucket 和 `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false`
- **AND** MUST 找到禁止示例密钥用于生产的说明

#### Scenario: validate-env 阻断危险配置

- **WHEN** 操作人员对生产环境运行 `deploy/scripts/validate-env.py`
- **THEN** SQLite `DATABASE_URL` MUST 被阻断
- **AND** `APP_DEBUG=true` MUST 被阻断
- **AND** 示例密钥 MUST 被阻断
- **AND** 腾讯云 COS 生产环境 `OBJECT_STORAGE_AUTO_CREATE_BUCKET=true` MUST 被阻断

#### Scenario: 维护作业 env 示例脱敏

- **WHEN** 生产维护作业新增或引用 env 变量
- **THEN** `deploy/prod/*.env.example` 或等价示例 MUST 使用占位值
- **AND** MUST 说明变量用途、默认值含义和安全边界
- **AND** MUST NOT 包含真实 `.env` 内容、数据库 URL、对象存储 access key、secret key 或生产私有域名。

### Requirement: 部署文件必须纳入发布镜像输入追踪

当部署 Compose、部署脚本或 env 示例影响镜像构建、生产部署或发布门禁时，镜像准备与发布确认 MUST 将实际使用的 `deploy/` 文件纳入输入追踪。

#### Scenario: image prepare 记录 deploy 输入

- **WHEN** `/image-prepare <version>` 执行并发现发布范围涉及部署目录
- **THEN** image build plan MUST 记录实际使用的 `deploy/**/*.yml`
- **AND** MUST 记录实际使用的 `deploy/**/*.env.example`
- **AND** MUST 记录实际使用的 `deploy/scripts/*`
- **AND** MUST 记录这些输入的 hash 或明确不适用理由

#### Scenario: release publish 识别 deploy 输入漂移

- **WHEN** 部署 Compose、部署脚本或 env 示例在 manifest 生成后发生变化
- **THEN** `/release-publish` MUST 将镜像证据视为过期或记录 blocker
- **AND** MUST 提示重新执行 `/image-prepare` 与必要的 `/image-build`

### Requirement: 部署说明必须覆盖首次部署、升级和回滚
部署能力 SHALL 文档化首次部署、相邻版本升级、跨版本升级和回滚的执行边界。

#### Scenario: 部署文档说明三类部署路径
- **WHEN** 运维阅读部署文档
- **THEN** 文档 SHALL 区分首次部署、相邻版本升级和跨版本升级
- **AND** 文档 SHALL 说明同一目标版本复用同一组 backend / web 镜像，不按部署场景拆分业务镜像。

#### Scenario: 回滚说明包含证据前置
- **WHEN** 运维阅读升级回滚说明
- **THEN** 文档 SHALL 要求旧镜像、旧 env 摘要、DB 备份、对象存储影响确认和回滚后 smoke
- **AND** 文档 SHALL 说明 DB 回滚不能凭空自动完成，必须依赖备份恢复或明确反向迁移策略。

### Requirement: 部署升级输出不得泄露真实环境配置
部署升级计划、部署校验和回滚记录 SHALL 遵守真实 env 与生产敏感信息安全边界。

#### Scenario: 输出脱敏部署摘要
- **WHEN** 系统生成部署升级计划、env diff 或回滚记录
- **THEN** 输出 SHALL NOT 包含真实 `.env` 内容、数据库连接串、对象存储凭据、Authorization header、Cookie、生产私有域名或真实客户数据
- **AND** 输出 SHALL 使用变量名、hash、摘要、负责人确认或占位符表达证据。

