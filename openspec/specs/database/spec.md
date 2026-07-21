# 数据库规范

## Purpose
定义生产 MySQL 与非生产 SQLite 双数据库模式、连接参数、schema 初始化、baseline 覆盖和默认管理员 seed 要求，确保本地演示与生产部署路径清晰分离。
## Requirements
### Requirement: 系统必须支持生产 MySQL 与非生产 SQLite 双数据库模式

系统 MUST 通过环境变量选择数据库后端。`APP_ENV=production` 时系统 MUST 使用 MySQL，且 MUST 配置有效的 MySQL `DATABASE_URL`。生产环境缺失 `DATABASE_URL`、`DATABASE_URL` 指向 SQLite、或 MySQL URL 无法解析时，backend MUST fail fast，并输出不含密码明文的可运维错误日志。`APP_ENV` 非 `production` 且未设置 `DATABASE_URL` 时，系统 MUST 回退 `SQLITE_DATABASE_URL`，保持本地开发和 Docker demo 的 SQLite 默认行为。系统 MUST 支持 MySQL 8.0+，字符集 MUST 为 `utf8mb4`，collation SHOULD 为 `utf8mb4_unicode_ci`。

#### Scenario: 生产环境缺失 DATABASE_URL 时启动失败

- **GIVEN** `APP_ENV=production`
- **AND** 未配置 `DATABASE_URL`
- **WHEN** backend 启动
- **THEN** 系统 MUST fail fast
- **AND** 日志 MUST 指出生产环境缺失 MySQL `DATABASE_URL`
- **AND** 日志 MUST NOT 输出任何数据库密码明文

#### Scenario: 非生产环境默认回退 SQLite

- **GIVEN** `APP_ENV` 未设置或不等于 `production`
- **AND** 未配置 `DATABASE_URL`
- **WHEN** backend 启动
- **THEN** 系统 MUST 使用 `SQLITE_DATABASE_URL`
- **AND** `./scripts/docker-up.sh` 的本地 demo 行为 MUST 与变更前一致

### Requirement: MySQL 连接必须使用独立 engine 参数

系统 MUST 按数据库 dialect 构建 SQLAlchemy engine。MySQL engine MUST 启用连接健康检查策略（如 `pool_pre_ping=True`）和合理连接池参数；MySQL 连接 MUST NOT 使用 SQLite 专有 `connect_args={"check_same_thread": False}`。SQLite engine MAY 继续使用现有 SQLite 专有参数。

#### Scenario: MySQL engine 不包含 SQLite 专有参数

- **GIVEN** `DATABASE_URL` 为 MySQL DSN
- **WHEN** backend 创建数据库 engine
- **THEN** engine MUST NOT 使用 `check_same_thread`
- **AND** engine MUST 启用连接可用性检查或等价策略

### Requirement: MySQL 必须使用独立 schema 初始化路径

系统 MUST 为 MySQL 提供独立初始化入口，例如 `schema.mysql.sql` 及/或 versioned MySQL migration SQL。MySQL 初始化 MUST NOT 执行依赖 `sqlite_master`、`PRAGMA` 或 SQLite-only DDL 的逻辑。MySQL 初始化 MUST 幂等或通过 migration 版本表安全重复执行。

#### Scenario: 空 MySQL 库执行 baseline 初始化

- **GIVEN** `APP_ENV=production`
- **AND** `DATABASE_URL` 指向空 MySQL 8.0+ 数据库
- **WHEN** backend 启动
- **THEN** 系统 MUST 执行 MySQL schema 初始化
- **AND** MUST NOT 调用 SQLite `PRAGMA` 或查询 `sqlite_master`
- **AND** 二次启动 MUST NOT 因已存在表而致命失败

### Requirement: MySQL baseline 必须覆盖当前 SQLite 最终态

MySQL baseline schema MUST 覆盖当前 SQLite 最终业务表，至少包括 `users`、`brands`、`tile_categories`、`tiles`、`tile_images`、`tile_videos`、`tile_specs`、`topics`、`banners`、`system_settings`、`audit_logs`、`profile_activity_logs`、`password_change_attempts` 等以现有 `schema.sql` 与 `migrations.py` 合并后的实际表为准的表。关键唯一约束、外键语义和索引 MUST 与现有查询路径一致。Banner 展示端、展示位置、索引和迁移删除策略 MUST 在 SQLite 与 MySQL 文档和 schema 中保持一致。实现 MUST 在对应 Change implementation 记录 SQLite 到 MySQL 的类型映射、约束取舍和旧 Banner 数据删除结果。

#### Scenario: MySQL baseline 包含关键表与约束

- **WHEN** 开发者检查 MySQL baseline DDL
- **THEN** MUST 找到当前 SQLite 最终态的全部业务表
- **AND** MUST 找到 `users.username` 与 `tiles.sku_code` 等关键唯一约束
- **AND** MUST 找到审计或查询路径所需关键索引。

#### Scenario: Banner 展示位置约束一致

- **WHEN** 开发者检查 SQLite schema、SQLite migration、MySQL schema 和数据库文档
- **THEN** Banner 展示端/展示位置约束 SHALL 支持小程序首页轮播与小程序品牌列表页轮播
- **AND** SHALL 不再把 Web 首页、专题页或首页中部运营位作为有效业务范围
- **AND** `banners.brand_id` SHALL 作为品牌详情跳转目标字段并在 SQLite/MySQL schema 中保留
- **AND** `banners` 查询路径 SHALL 仍有支持 `display_client`、`position`、`status` 的索引或等价性能策略。

#### Scenario: 旧 Banner 数据删除迁移

- **WHEN** 数据库迁移执行 Banner 投放范围收敛
- **THEN** 迁移 SHALL 删除不在小程序首页轮播与小程序品牌列表页轮播范围内的 Banner 业务记录
- **AND** 迁移 SHALL NOT 删除 MinIO 对象或其他业务表中的媒体引用
- **AND** 实现记录 SHALL 说明删除条件、删除数量和回滚依赖的备份边界。

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

