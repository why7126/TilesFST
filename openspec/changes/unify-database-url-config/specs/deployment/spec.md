## MODIFIED Requirements

### Requirement: 生产环境变量文档必须说明 DATABASE_URL 与环境关系

`.env.example`、后端环境示例和部署文档 MUST 说明 `DATABASE_URL` 是唯一数据库连接入口。本地/demo 示例 MUST 使用 SQLite DSN；生产示例 MUST 使用 MySQL DSN 占位。生产 `APP_SECRET_KEY`、MySQL 密码、对象存储密钥和管理员初始密码 MUST 通过部署环境注入，MUST NOT 在仓库中提交真实值。系统 MUST NOT 要求或展示 `SQLITE_DATABASE_URL`。

#### Scenario: 环境示例使用单一 DATABASE_URL

- **WHEN** 开发者检查 `.env.example`
- **THEN** MUST 找到 `DATABASE_URL` 的本地 SQLite 默认值
- **AND** MUST 找到生产使用 MySQL DSN 的说明
- **AND** MUST NOT 找到 `SQLITE_DATABASE_URL`
