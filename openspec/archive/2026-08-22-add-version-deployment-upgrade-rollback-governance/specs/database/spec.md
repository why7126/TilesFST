## ADDED Requirements

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
