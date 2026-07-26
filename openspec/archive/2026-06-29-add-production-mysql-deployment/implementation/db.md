---
change_id: add-production-mysql-deployment
title: MySQL DDL 与类型映射实现说明
created_at: 2026-06-29 09:55:35
updated_at: 2026-06-29 10:35:38
source_requirement: REQ-0018-production-mysql-deployment
status: proposed
---

# MySQL DDL 与类型映射实现说明

## 目标

实现阶段 MUST 在本文件补齐最终 MySQL baseline DDL 的表清单、字段类型映射、索引、唯一约束、外键语义和已知差异。本文件是 REQ-0018 AC-017 / AC-039 的验收入口。

## 表覆盖清单

实现阶段 MUST 从当前 `src/backend/app/db/schema.sql` 与 `src/backend/app/db/migrations.py` 汇总最终态，至少确认以下表：

| 表 | MySQL baseline 状态 | 备注 |
|---|---|---|
| `schema_migrations` | 已实现 | MySQL baseline 版本记录，记录 `mysql_baseline_v1` |
| `users` | 已实现 | 管理员 seed 与登录依赖 |
| `login_logs` | 已实现 | 登录审计预留，随 SQLite 最终态同步 |
| `brands` | 已实现 | 品牌管理 |
| `tile_categories` | 已实现 | 类目管理 |
| `tiles` | 已实现 | SKU 主体 |
| `tile_images` | 已实现 | SKU 图片 |
| `tile_videos` | 已实现 | SKU 视频 |
| `tile_specs` | 已实现 | 规格管理 |
| `topics` | 已实现 | Banner 专题 |
| `banners` | 已实现 | Banner 管理 |
| `system_settings` | 已实现 | effective settings；MySQL 使用反引号保护 `key` |
| `audit_logs` | 已实现 | 系统设置与审计 |
| `profile_activity_logs` | 已实现 | 个人资料活动记录 |
| `password_change_attempts` | 已实现 | 改密安全记录 |

## 类型映射原则

| SQLite 现状 | MySQL 映射候选 | 实现决策 |
|---|---|---|
| `INTEGER PRIMARY KEY AUTOINCREMENT` | `BIGINT AUTO_INCREMENT PRIMARY KEY` | 已用于 `brands`、`tiles`、`tile_*`、`topics`、`banners` |
| `TEXT`（ISO 时间戳） | `VARCHAR(64)` | 兼容现有 Python `datetime.now(UTC).isoformat()` 写入，避免生产首版改业务层时间格式 |
| `TEXT`（UUID 主键） | `CHAR(36)` | 已用于 `users` 与日志表 |
| `TEXT`（JSON） | `TEXT` | 当前 Repository 按字符串读写，后续如需 JSON 类型另建 Change |
| `REAL` | `DOUBLE` | 已用于厚度、价格、视频时长 |
| `INTEGER` 布尔 | `TINYINT` | 已用于 `tile_images.is_main`、`password_change_attempts.success` |
| `CHECK` 约束 | MySQL 8.0 `CHECK` | 关键枚举和范围约束已保留 |

## 索引与约束验收

- `users.username` MUST 保持唯一。
- `tiles.sku_code` MUST 保持唯一。
- 审计与活动日志的常用查询字段 MUST 有索引，例如 domain / actor / created_at 组合，以实际查询路径为准。
- 外键约束若因 MySQL DDL 或历史数据兼容无法完全等价，MUST 在此记录原因和替代校验。

实现结果：

| 类型 | MySQL baseline |
|---|---|
| 唯一约束 | `users.username`、`brands.name`、`tile_categories.code`、`tiles.sku_code`、`tile_specs(width_mm,length_mm,unit)`、`topics.code`、`banners(display_client,position,title)` |
| 外键 | 类目自引用、SKU 到品牌/类目/规格、图片/视频到 SKU、Banner 到 SKU/专题/SKU 图、设置/审计/活动到用户 |
| 查询索引 | `idx_tiles_brand_status`、`idx_tiles_category_status`、`idx_tiles_updated_at`、`idx_tile_images_tile_sort`、`idx_tile_videos_tile_sort`、`idx_profile_activity_logs_user_created`、`idx_password_change_attempts_user_created`、`idx_audit_logs_domain_created` |
| 差异说明 | `system_settings.key` 在 MySQL 中以反引号转义；Repository 已对 upsert 做 SQLite `ON CONFLICT` 与 MySQL `ON DUPLICATE KEY UPDATE` 分支 |

## 初始化策略

- MySQL 初始化入口：`src/backend/app/db/session.py::_init_mysql_schema()`。
- MySQL DDL 文件：`src/backend/app/db/schema.mysql.sql`。
- MySQL 初始化 MUST NOT 调用 SQLite `PRAGMA` 或 `sqlite_master`；当前分支只执行 MySQL baseline。
- Baseline 使用 `CREATE TABLE IF NOT EXISTS` 并写入 `schema_migrations(version='mysql_baseline_v1')`，重复启动不致命失败。
- SQLite 继续执行 `schema.sql` + `migrations.py`，本地开发和 demo 不要求 MySQL。
