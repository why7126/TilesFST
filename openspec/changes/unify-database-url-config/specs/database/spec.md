## MODIFIED Requirements

### Requirement: 数据库后端必须通过单一 DATABASE_URL 选择

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
