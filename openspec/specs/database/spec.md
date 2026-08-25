# 数据库规范

## Purpose
定义生产 MySQL 与非生产 SQLite 双数据库模式、连接参数、schema 初始化、baseline 覆盖和默认管理员 seed 要求，确保本地演示与生产部署路径清晰分离。
## Requirements
### Requirement: 系统必须支持生产 MySQL 与非生产 SQLite 双数据库模式

系统 MUST 通过单一环境变量 `DATABASE_URL` 选择数据库后端。非生产环境默认 `DATABASE_URL` MUST 指向本地 SQLite 数据库，开发者可显式覆盖为其他 SQLite 或兼容测试数据库。`APP_ENV=production` 时系统 MUST 使用 MySQL，且 MUST 配置有效的 MySQL `DATABASE_URL`。生产环境缺失 `DATABASE_URL`、`DATABASE_URL` 指向 SQLite、或 MySQL URL 无法解析时，backend MUST fail fast，并输出不含密码明文的可运维错误日志。系统 MUST NOT 依赖 `SQLITE_DATABASE_URL` 作为 fallback。系统 MUST 支持 MySQL 8.0+，字符集 MUST 为 `utf8mb4`，collation SHOULD 为 `utf8mb4_unicode_ci`。

#### Scenario: 生产环境缺失 DATABASE_URL 时启动失败

- **GIVEN** `APP_ENV=production`
- **AND** 未配置 `DATABASE_URL`
- **WHEN** backend 启动或初始化数据库连接
- **THEN** 系统 MUST fail fast
- **AND** 日志 MUST 指出生产环境缺失 MySQL `DATABASE_URL`
- **AND** MUST NOT 回退 SQLite

#### Scenario: 非生产默认使用 DATABASE_URL 中的 SQLite

- **GIVEN** `APP_ENV=development`
- **AND** `DATABASE_URL=sqlite:////app/data/sqlite/tilesfst.db`
- **WHEN** backend 初始化数据库连接
- **THEN** 系统 MUST 使用 `DATABASE_URL`
- **AND** MUST NOT 读取 `SQLITE_DATABASE_URL`

#### Scenario: 生产拒绝 SQLite DATABASE_URL

- **GIVEN** `APP_ENV=production`
- **AND** `DATABASE_URL` 指向 SQLite
- **WHEN** backend 初始化数据库连接
- **THEN** 系统 MUST fail fast
- **AND** 错误信息 MUST NOT 暴露密码或敏感连接串

#### Scenario: 生产使用 MySQL DATABASE_URL

- **GIVEN** `APP_ENV=production`
- **AND** `DATABASE_URL` 为 MySQL DSN
- **WHEN** backend 初始化数据库连接
- **THEN** 系统 MUST 使用 MySQL engine options
- **AND** MUST NOT 添加 SQLite-only connect args

### Requirement: MySQL 连接必须使用独立 engine 参数

系统 MUST 按数据库 dialect 构建 SQLAlchemy engine。MySQL engine MUST 启用连接健康检查策略（如 `pool_pre_ping=True`）和合理连接池参数；MySQL 连接 MUST NOT 使用 SQLite 专有 `connect_args={"check_same_thread": False}`。SQLite engine MAY 继续使用现有 SQLite 专有参数。

#### Scenario: MySQL engine 不包含 SQLite 专有参数

- **GIVEN** `DATABASE_URL` 为 MySQL DSN
- **WHEN** backend 创建数据库 engine
- **THEN** engine MUST NOT 使用 `check_same_thread`
- **AND** engine MUST 启用连接可用性检查或等价策略

### Requirement: MySQL 必须使用独立 schema 初始化路径

系统 MUST 为 MySQL 提供独立初始化入口，例如 `schema.mysql.sql` 及/或 versioned MySQL migration SQL。MySQL 初始化 MUST NOT 执行依赖 `sqlite_master`、`PRAGMA` 或 SQLite-only DDL 的逻辑。MySQL 初始化 MUST 幂等或通过 migration 版本表安全重复执行。针对已存在的生产 MySQL 表，初始化或迁移路径 MUST 能发现并处理关键业务字段缺失；对于会阻断管理端保存的缺列，系统 MUST 在启动、发布前校验或迁移阶段给出可运维的失败信息，而不是让业务 API 在生产请求中暴露原始 SQL 异常。

#### Scenario: 既有 MySQL banners 表补齐品牌详情字段

- **GIVEN** 生产 MySQL 中已存在 `banners` 表
- **AND** 该表缺少保存 `BRAND_DETAIL` 所需的 `brand_id` 字段
- **WHEN** MySQL migration、schema init 或 drift 修复逻辑执行
- **THEN** 系统 SHALL 幂等补齐 `banners.brand_id`
- **AND** 重复执行 SHALL NOT 因字段已存在而失败
- **AND** 修复记录 SHALL 说明执行命令、字段状态、备份或回滚边界。

#### Scenario: 既有 MySQL banners 表补齐创建接口写入字段

- **GIVEN** 生产 MySQL 中已存在旧版 `banners` 表
- **AND** 该表缺少当前 `POST /api/v1/admin/banners` 或 `PUT /api/v1/admin/banners/{id}` 会写入的字段
- **WHEN** MySQL migration、schema init 或 drift 修复逻辑执行
- **THEN** 系统 SHALL 幂等补齐缺失字段，至少覆盖 `image_source`、`sku_gallery_asset_id`、`topic_id`、`brand_id`、`valid_from`、`valid_to`、`remark`
- **AND** 字段类型、可空性和默认值 SHALL 与 `schema.mysql.sql` 保持兼容
- **AND** 重复执行 SHALL NOT 因字段、索引或可安全添加的外键已存在而失败
- **AND** 若历史脏数据导致外键暂不能添加，系统 SHALL 记录跳过原因和脏数据计数，并确保 Banner 创建保存不因可空字段缺失而失败。

### Requirement: MySQL baseline 必须覆盖当前 SQLite 最终态

MySQL baseline schema MUST 覆盖当前 SQLite 最终业务表，至少包括 `users`、`brands`、`tile_categories`、`tiles`、`tile_images`、`tile_videos`、`tile_specs`、`topics`、`banners`、`system_settings`、`audit_logs`、`profile_activity_logs`、`password_change_attempts` 等以现有 `schema.sql` 与 `migrations.py` 合并后的实际表为准的表。关键唯一约束、外键语义和索引 MUST 与现有查询路径一致。Banner 展示端、展示位置、索引和迁移删除策略 MUST 在 SQLite 与 MySQL 文档和 schema 中保持一致。实现 MUST 在对应 Change implementation 记录 SQLite 到 MySQL 的类型映射、约束取舍和旧 Banner 数据删除结果。`banners` 的品牌详情跳转字段与创建接口写入字段 SHALL 在 SQLite schema、SQLite migration、MySQL baseline、MySQL 既有表迁移路径和数据库文档中保持一致。

#### Scenario: Banner 品牌跳转字段跨数据库一致

- **WHEN** 开发者检查 SQLite schema、SQLite migration、MySQL baseline、MySQL migration/drift 修复逻辑和数据库文档
- **THEN** 均 SHALL 支持 `banners.brand_id` 作为品牌详情跳转目标字段
- **AND** `brand_id` 对非品牌跳转类型 SHALL 可为空
- **AND** 保存品牌详情 Banner 的 repository/service 路径 SHALL 不因数据库 dialect 差异而失败。

#### Scenario: Banner 创建字段跨数据库一致

- **WHEN** 开发者检查 SQLite schema、SQLite migration、MySQL baseline、MySQL migration/drift 修复逻辑和数据库文档
- **THEN** 均 SHALL 支持 Banner 创建/编辑接口写入字段
- **AND** `image_source`、`sku_gallery_asset_id`、`topic_id`、`brand_id`、`valid_from`、`valid_to`、`remark` 的语义 SHALL 在 SQLite 与 MySQL 路径保持一致
- **AND** 旧 MySQL 表升级路径 SHALL 通过自动化测试覆盖缺列补齐。

### Requirement: 生产空库首次启动必须 seed 默认管理员

生产 MySQL 空库首次启动完成 schema 初始化后，系统 MUST 按现有 `ADMIN_USERNAME`、`ADMIN_INITIAL_PASSWORD` 和 `ADMIN_RESET_PASSWORD_ON_STARTUP` 规则创建或重置默认管理员。密码 MUST 使用 bcrypt 哈希存储。系统 MUST NOT 提供 SQLite 业务数据自动导入 MySQL 的工具作为本 change 交付物。

#### Scenario: 空 MySQL 库可创建默认管理员并登录

- **GIVEN** 空 MySQL 数据库已完成 schema 初始化
- **AND** 已配置 `ADMIN_USERNAME` 与 `ADMIN_INITIAL_PASSWORD`
- **WHEN** backend 启动完成
- **THEN** 系统 MUST 创建默认管理员账号
- **AND** `POST /api/v1/auth/login` MUST 可使用该账号登录
- **AND** 数据库 MUST NOT 保存明文密码

### Requirement: 用户主题偏好持久化

The database capability MUST persist account-level user theme preference for Web theme switching. SQLite and MySQL schemas MUST remain aligned, and new users MUST default to `system`.

#### Scenario: 用户表包含主题偏好字段

- **WHEN** the application schema is initialized or migrated
- **THEN** the `users` table SHALL include a theme preference field equivalent to `theme_mode`
- **AND** the field SHALL default to `system`
- **AND** supported stored values SHALL be `system`, `dark_flagship`, `comfort_dark`, and `light`.

#### Scenario: SQLite 与 MySQL 保持一致

- **WHEN** database documentation or schema checks compare SQLite and MySQL support
- **THEN** both backends SHALL document and support the same theme preference field semantics
- **AND** implementation notes SHALL record any type or constraint differences.

#### Scenario: 主题偏好不影响认证安全字段

- **WHEN** a user updates theme preference
- **THEN** the system SHALL NOT modify password hash, token version, role, status, or protected account semantics
- **AND** theme preference SHALL NOT be treated as sensitive credential data.

### Requirement: 数据库发布必须验证 MySQL 目标路径
Database-impacting releases MUST validate MySQL compatibility before publish confirmation.

#### Scenario: MySQL schema drift check blocks release
- **GIVEN** a release has `impact_scope.database` marked as database-impacting
- **WHEN** release preparation validates the database gate
- **THEN** the release MUST include evidence from a MySQL schema drift check or equivalent target MySQL schema verification.
- **AND** missing target tables or columns MUST block release confirmation.

#### Scenario: MySQL compatibility evidence is explicit
- **WHEN** database migration evidence is recorded in `release.json`
- **THEN** the evidence SHALL name the MySQL check that was run and the schema source used.
- **AND** the evidence SHALL include rollback or backup evidence for the database change.

### Requirement: 真实用户性能事件数据库支持
数据库 SHALL 支持真实用户性能事件在 SQLite demo 与生产 MySQL 中的兼容存储、索引和保留策略。

#### Scenario: 性能事件表兼容 SQLite 与 MySQL
- **WHEN** 系统新增性能事件存储
- **THEN** SQLite schema、SQLite migration、MySQL baseline 和 MySQL migration SHALL 均包含兼容字段
- **AND** 字段 SHALL 至少支持端类型、页面 key、版本、网络类型、设备类别、指标名、耗时、采样率、客户端事件时间和服务端接收时间
- **AND** MySQL DDL SHALL NOT 使用 SQLite-only 语法。

#### Scenario: 性能聚合索引
- **WHEN** 系统按时间范围、端类型、页面 key、版本、网络类型或设备类别查询性能事件
- **THEN** 数据库 SHALL 提供索引或等价查询优化
- **AND** 后端 SHALL NOT 在过滤前将全部性能事件加载到内存。

#### Scenario: 性能事件保留周期
- **WHEN** 性能事件进入生产存储
- **THEN** 系统 SHALL 明确保留周期、清理策略或后续运维任务边界
- **AND** 数据库文档 SHALL 说明性能事件与审计日志、请求日志、行为事件的保留差异。

### Requirement: SKU 召回置顶字段持久化

数据库能力 MUST 在 SQLite 与 MySQL 中一致持久化 SKU 召回置顶配置。`tiles` 表 MUST 新增或等价支持 `recall_pin_sort_order`、`recall_pin_starts_at`、`recall_pin_ends_at` 字段。`recall_pin_sort_order` MUST 默认为 `9999`，并通过数据库约束、应用校验或等价组合保证持久化值为正整数。`recall_pin_starts_at` 为空表示立即可生效，`recall_pin_ends_at` 为空表示长期有效。

#### Scenario: SQLite 与 MySQL 字段一致

- **WHEN** 开发者初始化或迁移 SQLite 与 MySQL schema
- **THEN** 两种数据库的 `tiles` 表 MUST 支持召回排序值、生效开始时间和生效结束时间
- **AND** 默认值和可空语义 MUST 保持一致。

#### Scenario: 历史 SKU 默认不置顶

- **WHEN** 迁移历史 SKU 数据
- **THEN** 既有 SKU 的 `recall_pin_sort_order` MUST 回填或默认视为 `9999`
- **AND** 历史 SKU MUST NOT 因迁移自动进入召回置顶区。

#### Scenario: 数据库文档同步

- **WHEN** 本 Change 实现完成
- **THEN** 数据库设计文档 MUST 记录新增字段、默认值、有效期空值语义、SQLite / MySQL 类型映射和索引策略
- **AND** 发布前数据库校验 MUST 覆盖 MySQL 目标路径。

### Requirement: 数据库升级路径必须可验证和可回滚
数据库能力 SHALL 为部署升级计划提供生产 MySQL 目标路径验证、备份和回滚证据要求。

#### Scenario: 数据库升级计划要求目标 MySQL 证据
- **WHEN** 版本升级影响 schema、migration、数据修复或数据库文档
- **THEN** 升级计划 SHALL 要求 MySQL schema drift check、目标 MySQL smoke 或等价生产目标路径验证
- **AND** 升级计划 SHALL 记录 SQLite schema、MySQL schema、migration、`schema_migrations` 或等价版本记录、DB 备份和关键业务读写 smoke。

#### Scenario: 数据库回滚边界明确
- **WHEN** 升级计划包含数据库影响
- **THEN** 回滚计划 SHALL 明确 DB 回滚基于备份恢复、已验证反向迁移或人工方案
- **AND** 缺少 DB 备份或恢复责任 SHALL 使升级计划 blocked 或 requires manual review。

