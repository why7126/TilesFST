## MODIFIED Requirements

### Requirement: 用户账号密码登录

系统 MUST 提供 `POST /api/v1/auth/login` 接口，接受 `username`、`password` 和可选 `remember_me` 字段，校验通过后返回 JWT access token 与用户基本信息。

#### Scenario: 登录成功

- **WHEN** 用户提供正确的 username 和 password，且用户 status 为 `active`
- **THEN** 系统返回 HTTP 200，包含 `access_token`、`token_type`（Bearer）、`expires_in` 和用户对象（id、username、display_name、role、status）
- **AND** 系统更新用户 `last_login_at` 字段
- **AND** 签发的 JWT MUST 含 `tv` claim 等于用户当前 `token_version`

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
- **THEN** 系统签发的 token 有效期 MUST 为 2 小时

### Requirement: 当前用户信息查询

系统 MUST 提供 `GET /api/v1/auth/me` 接口，返回当前已认证用户的信息。

#### Scenario: 已登录用户查询

- **WHEN** 请求携带有效 Bearer token，且 JWT `tv` 与 `users.token_version` 一致
- **THEN** 系统返回 HTTP 200，包含用户 id、username、display_name、role、status

#### Scenario: 未登录或 token 无效

- **WHEN** 请求未携带 token 或 token 已过期/无效
- **THEN** 系统返回 HTTP 401

#### Scenario: token_version 不匹配

- **WHEN** JWT `tv` 与数据库 `token_version` 不一致（如改密后旧 token）
- **THEN** 系统 MUST 返回 HTTP 401

#### Scenario: 用户被禁用后 token 仍有效

- **WHEN** 用户 status 变为 `disabled` 后携带旧 token 请求
- **THEN** 系统返回 HTTP 403，错误码 `AUTH_USER_DISABLED`

### Requirement: 用户数据模型

系统 MUST 维护 `users` 表，支持以下角色：`admin`（系统管理员 / 后台管理员）、`employee`（企业内部员工 / 后台运营）、`store_owner`（瓷砖零售店店主 / 前台用户，本期预留）。用户 MUST 支持可选头像引用 `avatar_object_key`；`display_name`（昵称）MAY 为空，展示层回退 username。用户 MUST 含 `token_version`（INTEGER NOT NULL DEFAULT 0），用于 JWT 全端失效。

#### Scenario: 用户角色字段

- **WHEN** 系统存储用户信息
- **THEN** role 字段 MUST 为 `admin`、`employee` 或 `store_owner` 之一
- **AND** status 字段 MUST 为 `active`、`disabled` 或 `deleted` 之一

#### Scenario: 用户名唯一

- **WHEN** 系统创建用户
- **THEN** username MUST 在表中唯一

#### Scenario: 昵称可为空

- **WHEN** 系统创建或更新用户且未提供 display_name
- **THEN** 数据库 MAY 存储 NULL 或空字符串
- **AND** API 响应与前端展示 MUST 回退为 username

#### Scenario: token_version 默认值

- **WHEN** 新建用户
- **THEN** `token_version` MUST 默认为 0
