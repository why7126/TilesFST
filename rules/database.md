---
purpose: 数据库规范
content: SQLite表设计、迁移、索引、媒体元数据、软删除、审计字段规则
source: AI自动生成初稿，项目团队确认
update_method: 新增表、字段、索引、迁移或媒体元数据存储规则时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-26 20:26:00
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
- 涉及数据库结构、迁移或 MySQL 查询兼容性的发布，MUST 在 `/release-prepare` 记录目标 MySQL 兼容性证据；推荐运行 `python scripts/check-mysql-schema-drift.py --database-url <mysql-url>`，或记录等价目标 MySQL smoke / `information_schema` 校验结果。
- 发布门禁证据不得包含明文 `DATABASE_URL`、密码或生产敏感信息。

## 6. AI更新规则

AI修改数据库结构时必须同步：

```text
docs/04-database-design.md
openspec/changes/<change-id>/implementation/db.md
tests/integration/
data/README.md
```

若变更会影响生产 MySQL，AI 还必须同步 release gate 证据要求，并补充 SQLite/MySQL 差异测试或目标 MySQL 校验证据。

## 7. 版本升级数据库证据

版本升级治理 MUST 区分“存在幂等 migration 代码”和“某条升级路径已验证”。当升级计划的数据库影响不是 `none`、`na`、`不涉及` 或等价无影响状态时，升级计划 MUST 要求：

- SQLite schema 与 migration 输入摘要。
- MySQL `schema.mysql.sql` 与 MySQL migration 输入摘要。
- `schema_migrations` 或等价版本记录。
- 目标 MySQL schema drift、目标 MySQL smoke 或等价生产目标路径验证。
- DB 备份、恢复责任或回滚边界。
- 升级后关键业务读写 smoke。

不得仅凭本地 SQLite 测试通过宣称生产 DB 升级安全。DB 回滚默认只能依赖升级前备份恢复或已验证的反向迁移策略；缺少 DB 备份或恢复责任时，升级计划 MUST 标记为 blocked 或 requires manual review。

## 8. 产品数据采集与链路观测门禁

数据库变更若涉及 `usage_events`、`request_logs`、`task_traces`、`task_trace_spans`、索引、迁移、保留周期、脱敏字段或链路查询路径，MUST 读取 `docs/standards/product-data-collection-observability.md`。

触发范围内的 Change MUST 在设计、任务或验收材料中声明 `product_data_collection_observability` 适用层级，并同步 SQLite / MySQL schema、迁移、数据库设计文档和测试；若某项不适用，MUST 记录具体 N/A 原因。
