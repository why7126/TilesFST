## MODIFIED Requirements

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

## ADDED Requirements

### Requirement: 系统必须提供部署环境矩阵

系统 MUST 在 `deploy/` 下提供部署环境矩阵，用稳定环境 ID 描述本地与生产部署组合。每个环境 ID MUST 映射到 env 示例、Compose 文件、profile 策略、必填变量、安全边界和启动命令。部署矩阵 MUST 遵守“一拓扑一 Compose + 一环境一 env 示例”原则。

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

系统 MUST 为每个部署环境提供独立 `.env.example`。每个 env 示例 MUST 使用示例值，并按环境标识、应用安全、数据库、镜像、对象存储、端口等适用主题分组。每个变量上一行 MUST 说明用途、候选值或候选格式、默认值含义或安全边界。生产 env 示例 MUST 要求 MySQL、腾讯云 COS、`APP_ENV=production`、`APP_DEBUG=false`、非示例密钥和 `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false`。

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
