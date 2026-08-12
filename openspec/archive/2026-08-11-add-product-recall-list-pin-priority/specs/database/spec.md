## ADDED Requirements

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
