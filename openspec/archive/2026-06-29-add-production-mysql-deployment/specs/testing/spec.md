---
change_id: add-production-mysql-deployment
capability: testing
created_at: 2026-06-29 09:55:35
updated_at: 2026-06-29 09:55:35
---

## ADDED Requirements

### Requirement: 生产 MySQL 路径必须有集成验证

项目 MUST 提供至少一种 MySQL 集成验证路径，用于验证 MySQL schema 初始化、默认管理员 seed 和至少一条读写 API。该验证 MAY 作为 CI MySQL 8 service container job，也 MAY 作为 `@pytest.mark.mysql` optional pytest 与 documented manual smoke 组合。默认 SQLite pytest MUST 保持可从本地运行，不要求开发者本机安装 MySQL。

#### Scenario: MySQL 集成验证覆盖启动关键路径

- **WHEN** MySQL 集成验证运行
- **THEN** MUST 覆盖 MySQL schema 初始化
- **AND** MUST 覆盖默认管理员 seed
- **AND** MUST 覆盖至少一条 API 读写路径，如登录或 health + 简单 CRUD

#### Scenario: SQLite 默认 pytest 仍可运行

- **WHEN** 开发者在未安装 MySQL 的本地环境运行默认 pytest
- **THEN** 测试 MUST 使用 SQLite 默认路径
- **AND** MUST NOT 因缺少 MySQL 服务而失败
