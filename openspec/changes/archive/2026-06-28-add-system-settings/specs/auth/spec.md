## MODIFIED Requirements

### Requirement: 用户账号密码登录

系统 MUST 提供 `POST /api/v1/auth/login` 接口，接受 `username`、`password` 和可选 `remember_me` 字段，校验通过后返回 JWT access token 与用户基本信息。非 remember_me 路径的 access token 过期时间 MUST 由 **effective** `security.jwt_access_token_expire_minutes`（merge env `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`）决定；remember_me 路径 MUST 仍按 `JWT_REMEMBER_ME_EXPIRE_DAYS` env。修改 effective 会话超时 MUST 仅影响**新签发** token。

#### Scenario: 登录成功

- **WHEN** 用户提供正确的 username 和 password，且用户 status 为 `active`
- **THEN** 系统返回 HTTP 200，包含 `access_token`、`token_type`（Bearer）、`expires_in` 和用户对象（id、username、display_name、role、status）
- **AND** 系统更新用户 `last_login_at` 字段
- **AND** `expires_in` MUST 与 effective access token 分钟数一致（非 remember_me 路径）

#### Scenario: 账号或密码错误

- **WHEN** 用户提供错误的 username 或 password
- **THEN** 系统返回 HTTP 401，错误码 `AUTH_INVALID_CREDENTIALS`，消息为「账号或密码错误」
- **AND** 响应不得区分「用户不存在」与「密码错误」

#### Scenario: 用户被禁用

- **WHEN** 用户提供正确的凭证但用户 status 为 `disabled`
- **THEN** 系统返回 HTTP 403，错误码 `AUTH_USER_DISABLED`，消息为「账号已停用，请联系管理员」

#### Scenario: 用户已软删除

- **WHEN** 用户提供正确的凭证但用户 status 为 `deleted`
- **THEN** 系统 MUST 返回 HTTP 403，错误码 `AUTH_USER_DISABLED` 或 `AUTH_USER_DELETED`
- **AND** 行为 MUST 与禁用用户一致（不允许登录）

#### Scenario: 请求参数无效

- **WHEN** 请求体缺少 username 或 password，或字段为空
- **THEN** 系统返回 HTTP 400，错误码 `AUTH_INVALID_REQUEST`

#### Scenario: remember_me 延长有效期

- **WHEN** 用户设置 `remember_me` 为 true 且登录成功
- **THEN** 系统签发的 token 有效期 MUST 为 7 天

#### Scenario: 默认 token 有效期

- **WHEN** 用户未设置 `remember_me` 或设为 false 且登录成功
- **THEN** 系统签发的 token 有效期 MUST 等于 effective access token 分钟数（默认 merge 自 env，典型 120 分钟）

### Requirement: 密码安全存储

系统 MUST 使用 bcrypt 算法哈希存储用户密码，数据库中 MUST NOT 存在明文密码。用户设置新密码或管理员重置/创建用户密码时，系统 MUST 按 **effective** 安全策略（`system_settings` merge 代码/env 默认值）校验：最小长度、大写/小写/数字/特殊字符复杂度（若对应开关启用）。校验失败 MUST 返回 400 及统一业务错误码。

#### Scenario: 密码哈希验证

- **WHEN** 系统创建或验证用户密码
- **THEN** 系统 MUST 使用 passlib bcrypt 进行哈希与校验
- **AND** 日志与 API 响应 MUST NOT 包含明文密码

#### Scenario: 密码不符合 effective 策略

- **GIVEN** effective 最小长度为 12 且要求数字
- **WHEN** 用户或管理员提交不含数字的 10 位密码
- **THEN** MUST 返回 400 及密码策略错误码
- **AND** MUST NOT 更新 password_hash
