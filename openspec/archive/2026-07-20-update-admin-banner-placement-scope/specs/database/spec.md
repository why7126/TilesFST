## MODIFIED Requirements

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
