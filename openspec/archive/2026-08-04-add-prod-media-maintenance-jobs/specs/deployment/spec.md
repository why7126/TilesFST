## MODIFIED Requirements

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
