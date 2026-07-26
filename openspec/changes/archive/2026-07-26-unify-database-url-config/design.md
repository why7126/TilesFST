## Context

现有生产规则已要求 `APP_ENV=production` 时 `DATABASE_URL` 必须是 MySQL。非生产环境则允许 `DATABASE_URL` 为空并 fallback 到 `SQLITE_DATABASE_URL`。这给本地开发提供了便利，但增加了一套重复环境变量。

## Goals / Non-Goals

**Goals:**

- 数据库连接只使用 `DATABASE_URL` 一个入口。
- 本地/demo 默认值直接为 SQLite DSN。
- 生产仍必须显式覆盖为 MySQL，且拒绝 SQLite。

**Non-Goals:**

- 不修改数据库 schema、迁移脚本或数据文件路径。
- 不引入 `MYSQL_*`、`DB_*` 等新的拆分变量。

## Decisions

1. `DATABASE_URL` 默认使用当前 SQLite 路径。

   这样复制 `.env.example` 后本地仍可直接启动；生产 Compose 仍用 `${DATABASE_URL:?Set production MySQL DATABASE_URL}` 强制覆盖。

2. 移除 `sqlite_database_url` 设置项。

   所有运行路径都从 `settings.database_url` 读取。生产校验继续通过 SQLAlchemy URL backend 判断 MySQL dialect。

## Risks / Trade-offs

- 本地旧 `.env` 只配置了 `SQLITE_DATABASE_URL` 且 `DATABASE_URL` 为空时会失效 -> `.env.example` 和部署文档必须明确迁移到 `DATABASE_URL`。
