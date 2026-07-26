---
created_at: 2026-07-21 15:28:51
updated_at: 2026-07-21 15:28:51
---

# database Specification Delta

## MODIFIED Requirements

### Requirement: MySQL 必须使用独立 schema 初始化路径

系统 MUST 为 MySQL 提供独立初始化入口，例如 `schema.mysql.sql` 及/或 versioned MySQL migration SQL。MySQL 初始化 MUST NOT 执行依赖 `sqlite_master`、`PRAGMA` 或 SQLite-only DDL 的逻辑。MySQL 初始化 MUST 幂等或通过 migration 版本表安全重复执行。针对已存在的生产 MySQL 表，初始化或迁移路径 MUST 能发现并处理关键业务字段缺失；对于会阻断管理端保存的缺列，系统 MUST 在启动、发布前校验或迁移阶段给出可运维的失败信息，而不是让业务 API 在生产请求中暴露原始 SQL 异常。

#### Scenario: 既有 MySQL banners 表补齐品牌详情字段

- **GIVEN** 生产 MySQL 中已存在 `banners` 表
- **AND** 该表缺少保存 `BRAND_DETAIL` 所需的 `brand_id` 字段
- **WHEN** MySQL migration、schema init 或 drift 修复逻辑执行
- **THEN** 系统 SHALL 幂等补齐 `banners.brand_id`
- **AND** 重复执行 SHALL NOT 因字段已存在而失败
- **AND** 修复记录 SHALL 说明执行命令、字段状态、备份或回滚边界。

### Requirement: MySQL baseline 必须覆盖当前 SQLite 最终态

MySQL baseline schema MUST 覆盖当前 SQLite 最终业务表，至少包括 `users`、`brands`、`tile_categories`、`tiles`、`tile_images`、`tile_videos`、`tile_specs`、`topics`、`banners`、`system_settings`、`audit_logs`、`profile_activity_logs`、`password_change_attempts` 等以现有 `schema.sql` 与 `migrations.py` 合并后的实际表为准的表。关键唯一约束、外键语义和索引 MUST 与现有查询路径一致。Banner 展示端、展示位置、索引和迁移删除策略 MUST 在 SQLite 与 MySQL 文档和 schema 中保持一致。实现 MUST 在对应 Change implementation 记录 SQLite 到 MySQL 的类型映射、约束取舍和旧 Banner 数据删除结果。`banners.brand_id` SHALL 在 SQLite schema、SQLite migration、MySQL baseline、MySQL 既有表迁移路径和数据库文档中保持一致。

#### Scenario: Banner 品牌跳转字段跨数据库一致

- **WHEN** 开发者检查 SQLite schema、SQLite migration、MySQL baseline、MySQL migration/drift 修复逻辑和数据库文档
- **THEN** 均 SHALL 支持 `banners.brand_id` 作为品牌详情跳转目标字段
- **AND** `brand_id` 对非品牌跳转类型 SHALL 可为空
- **AND** 保存品牌详情 Banner 的 repository/service 路径 SHALL 不因数据库 dialect 差异而失败。
