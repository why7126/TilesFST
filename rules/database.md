---
purpose: 数据库规范
content: SQLite表设计、迁移、索引、媒体元数据、软删除、审计字段规则
source: AI自动生成初稿，项目团队确认
update_method: 新增表、字段、索引、迁移或媒体元数据存储规则时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-06-29 10:35:38
note: 当前项目本地/演示默认 SQLite，生产支持 MySQL 8.0+
---

# 数据库规范

## 1. 数据库定位

当前项目本地开发与 Docker demo 默认使用 SQLite，适合单体部署、演示环境、小规模门店信息管理场景。

生产环境使用 MySQL 8.0+，必须通过 `APP_ENV=production` + MySQL `DATABASE_URL` 显式启用。生产环境不得静默回退 SQLite。

## 2. 表设计要求

核心表建议包括：

- tiles：瓷砖主表
- tile_categories：分类
- tile_series：系列
- tile_media：图片/视频/文档媒体资产
- admin_users：企业内部员工
- audit_logs：操作日志

## 3. 通用字段

业务表建议包含：

```text
id
created_at
updated_at
deleted_at
created_by
updated_by
```

## 4. 媒体元数据

媒体表必须记录：

```text
media_type
object_key
bucket_name
mime_type
file_size
width
height
duration
cover_object_key
sort_order
```

## 5. SQLite规则

- 必须使用参数化查询。
- 需要为常用筛选条件建立索引。
- 不允许在业务代码中拼接SQL字符串。
- 迁移脚本必须可重复执行或有版本记录。

## 5.1 MySQL生产规则

- `APP_ENV=production` 时 `DATABASE_URL` MUST 使用 `mysql` / `mysql+pymysql` dialect。
- MySQL schema MUST 使用独立 `src/backend/app/db/schema.mysql.sql` 或 versioned migration，不得执行 `sqlite_master`、`PRAGMA` 或 SQLite-only DDL。
- MySQL 字符集 MUST 为 `utf8mb4`，collation SHOULD 为 `utf8mb4_unicode_ci`。
- MySQL 初始化 MUST 幂等，或通过 `schema_migrations` 记录版本。
- 生产 Compose MUST NOT 内嵌 mysql 服务；应连接客户已有 MySQL。

## 6. AI更新规则

AI修改数据库结构时必须同步：

```text
docs/04-database-design.md
openspec/changes/<change-id>/implementation/db.md
tests/integration/
data/README.md
```
