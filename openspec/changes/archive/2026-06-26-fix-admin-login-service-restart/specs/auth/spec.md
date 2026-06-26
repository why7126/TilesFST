## MODIFIED Requirements

### Requirement: 管理员账号初始化

系统 MUST 提供默认管理员初始化机制，通过环境变量配置首批管理员账号密码。系统 MUST 在空数据库或缺少默认管理员时创建默认管理员；对于已存在的默认管理员，系统 MUST NOT 在普通服务重启时静默覆盖其密码。若需要恢复默认管理员密码，系统 MUST 提供显式、可审计的恢复触发策略，并 MUST 保持密码哈希存储、统一凭证错误语义和管理端权限边界。

#### Scenario: 种子管理员创建

- **WHEN** 部署环境设置 `ADMIN_INITIAL_PASSWORD` 且数据库无 admin 用户
- **THEN** 系统 MUST 创建 role 为 `admin` 的默认用户
- **AND** 该用户 MUST 可以使用配置的初始密码登录管理端
- **AND** 数据库中 MUST 仅存储密码哈希，不得存储明文密码

#### Scenario: 已存在管理员时重启不覆盖密码

- **GIVEN** `users` 表中已存在 `username = admin` 且 status 为 `active` 的用户
- **WHEN** 服务重启或默认管理员 seed 逻辑再次执行
- **THEN** 系统 MUST NOT 静默覆盖该用户的 `password_hash`
- **AND** 该用户已有正确密码 MUST 仍可登录

#### Scenario: 初始密码变化时必须有明确策略

- **GIVEN** `users` 表中已存在默认管理员
- **AND** 当前环境中的 `ADMIN_INITIAL_PASSWORD` 与该用户现有密码不同
- **WHEN** 服务启动但未启用显式恢复策略
- **THEN** 系统 MUST NOT 将现有管理员密码自动改为新的初始密码
- **AND** 系统 SHOULD 通过文档或安全日志提示初始密码只在首次创建或显式恢复时生效

#### Scenario: 显式恢复默认管理员密码

- **GIVEN** `users` 表中已存在默认管理员
- **AND** 运维或开发环境显式启用默认管理员密码恢复策略
- **WHEN** 服务启动或恢复流程执行
- **THEN** 系统 MUST 使用 `ADMIN_INITIAL_PASSWORD` 的哈希值更新默认管理员密码
- **AND** 新密码 MUST 可以登录
- **AND** 旧密码 MUST 不再可登录
- **AND** 日志和 API 响应 MUST NOT 输出明文密码

#### Scenario: 登录错误语义保持统一

- **WHEN** 用户使用不存在的账号、错误密码或未恢复成功的默认管理员密码登录
- **THEN** 系统 MUST 返回 HTTP 401，错误码 `AUTH_INVALID_CREDENTIALS`，消息为「账号或密码错误」
- **AND** 响应不得区分「用户不存在」「密码错误」与「恢复策略未触发」

#### Scenario: 认证能力不回退

- **WHEN** 修复默认管理员初始化与恢复策略后
- **THEN** `POST /api/v1/auth/login`、`GET /api/v1/auth/me`、`POST /api/v1/auth/logout` MUST 保持统一响应结构
- **AND** `admin`、`employee`、`store_owner` 的管理端权限边界 MUST 保持不变
- **AND** status 为 `disabled` 或 `deleted` 的用户仍 MUST 被拒绝登录
