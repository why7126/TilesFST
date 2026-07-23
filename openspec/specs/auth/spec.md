# 认证与权限规范

## Purpose
定义账号密码登录、密码安全存储、当前用户查询、退出登录、用户数据模型、管理端访问控制、登录日志和管理员初始化要求。
## Requirements
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

系统 MUST 使用 bcrypt 算法哈希存储用户密码，数据库中 MUST NOT 存在明文密码。用户设置新密码或管理员重置/创建用户密码时，系统 MUST 使用统一基础密码策略校验：长度 5-32 位，至少包含 1 个 ASCII 英文字符（`A-Z` / `a-z`），至少包含 1 个 ASCII 数字（`0-9`）。符号等其他字符 MAY 与英文/数字共同出现；非 ASCII 字母或数字 MUST NOT 被计入英文字符或数字满足项，除非后续规范明确扩展字符集。

校验失败 MUST 返回 400 及统一业务错误码，并 SHOULD 提供可被客户端展示的具体失败项。失败项至少 MUST 能区分 `min_length`、`max_length`、`missing_letter`、`missing_digit`。具体失败项 MUST NOT 包含明文密码。

#### Scenario: 密码哈希验证

- **WHEN** 系统创建或验证用户密码
- **THEN** 系统 MUST 使用 passlib bcrypt 进行哈希与校验
- **AND** 日志与 API 响应 MUST NOT 包含明文密码

#### Scenario: 密码长度不足

- **WHEN** 用户或管理员提交少于 5 位的新密码
- **THEN** MUST 返回 400 及密码策略错误码
- **AND** MUST 提供可识别的 `min_length` 失败项
- **AND** MUST NOT 更新 `password_hash`

#### Scenario: 密码长度超限

- **WHEN** 用户或管理员提交超过 32 位的新密码
- **THEN** MUST 返回 400 及密码策略错误码
- **AND** MUST 提供可识别的 `max_length` 失败项
- **AND** MUST NOT 更新 `password_hash`

#### Scenario: 密码缺少英文字符

- **WHEN** 用户或管理员提交长度合规但不含 ASCII 英文字符的新密码
- **THEN** MUST 返回 400 及密码策略错误码
- **AND** MUST 提供可识别的 `missing_letter` 失败项
- **AND** MUST NOT 更新 `password_hash`

#### Scenario: 密码缺少数字

- **WHEN** 用户或管理员提交长度合规但不含 ASCII 数字的新密码
- **THEN** MUST 返回 400 及密码策略错误码
- **AND** MUST 提供可识别的 `missing_digit` 失败项
- **AND** MUST NOT 更新 `password_hash`

#### Scenario: 密码满足基础策略

- **WHEN** 用户或管理员提交 5-32 位且同时包含 ASCII 英文字符和 ASCII 数字的新密码
- **THEN** 基础密码策略校验 MUST 通过
- **AND** 后续业务规则 MAY 继续校验弱密码、新旧密码相同、受保护账号或限流

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

### Requirement: 退出登录

系统 MUST 提供 `POST /api/v1/auth/logout` 接口，允许已认证用户退出。

#### Scenario: 退出成功

- **WHEN** 已认证用户调用 logout 接口
- **THEN** 系统返回 HTTP 200，`data.success` 为 true
- **AND** 客户端 MUST 清除本地 token

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

### Requirement: 管理端角色访问控制

系统 MUST 在后端依赖注入层校验用户角色，仅允许 `admin` 和 `employee` 访问管理端 API。

#### Scenario: 员工访问管理端 API

- **WHEN** 角色为 `employee` 或 `admin` 的用户携带有效 token 访问受保护管理端 API
- **THEN** 系统 MUST 允许访问

#### Scenario: 店主访问管理端 API

- **WHEN** 角色为 `store_owner` 的用户携带有效 token 访问管理端 API
- **THEN** 系统 MUST 返回 HTTP 403，拒绝访问

### Requirement: 登录日志表预留

系统 MUST 创建 `login_logs` 表结构，包含 id、user_id、login_identifier、result、failure_reason、ip、user_agent、created_at 字段，本期不要求写入业务数据。

#### Scenario: 表结构存在

- **WHEN** 数据库 migration 执行完成
- **THEN** `login_logs` 表 MUST 存在于 schema 中

### Requirement: API 响应格式

认证相关 API MUST 遵循项目统一响应结构 `{ code, message, data }`。

#### Scenario: 成功响应格式

- **WHEN** 认证 API 调用成功
- **THEN** 响应 MUST 包含 `code: 0`、`message: "success"` 和 `data` 字段

#### Scenario: 错误响应格式

- **WHEN** 认证 API 调用失败
- **THEN** 响应 MUST 包含非零 `code`、可读 `message` 和 `data: null`

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

### Requirement: 管理端用户管理 API 访问控制

系统 MUST 将 `/api/v1/admin/users` 及其子路径设为 **仅 `admin` 角色** 可访问的受保护管理端 API。`employee` 角色 MUST NOT 调用上述接口，即使其可访问其他管理端 API。

#### Scenario: 管理员调用用户管理 API

- **WHEN** `role=admin` 的用户携带有效 token 访问 `/api/v1/admin/users` 或子资源
- **THEN** 系统 MUST 允许访问（subject to 业务校验）

#### Scenario: 运营人员被拒绝

- **WHEN** `role=employee` 的用户访问 `/api/v1/admin/users` 或子资源
- **THEN** 系统 MUST 返回 HTTP 403

#### Scenario: 前台用户被拒绝

- **WHEN** `role=store_owner` 的用户访问上述路径
- **THEN** 系统 MUST 返回 HTTP 403

### Requirement: 当前用户主题偏好 API

The authentication capability MUST expose the current user's theme preference and allow authenticated users to update their own theme preference. Supported values are `system`, `dark_flagship`, `comfort_dark`, and `light`. Production and local deployments MUST keep this API route, persistence field, authentication behavior, and unified response envelope consistent so Web clients can distinguish successful account preference persistence from recoverable client-side fallback.

#### Scenario: 当前用户信息包含主题偏好

- **WHEN** an authenticated user calls `GET /api/v1/auth/me`
- **THEN** the response `data` SHALL include `theme_mode`
- **AND** `theme_mode` SHALL be one of `system`, `dark_flagship`, `comfort_dark`, or `light`.

#### Scenario: 当前用户更新主题偏好

- **WHEN** an authenticated user submits a valid theme mode to the current-user theme preference endpoint
- **THEN** the system SHALL persist the value for that user
- **AND** the response SHALL use the unified `ApiResponse` envelope
- **AND** the response `data.theme_mode` SHALL equal the persisted value
- **AND** a later `GET /api/v1/auth/me` SHALL return the updated `theme_mode`.

#### Scenario: 主题偏好生产链路可用

- **WHEN** a production or production-equivalent deployment serves the Web admin client and backend together
- **THEN** `PATCH /api/v1/auth/me/theme` SHALL be reachable through the configured `/api/` route
- **AND** authenticated requests with valid Bearer tokens SHALL preserve the Authorization context through reverse proxies
- **AND** the deployment database SHALL include the `users.theme_mode` persistence field with the supported values.

#### Scenario: 无效主题偏好被拒绝

- **WHEN** an authenticated user submits a theme mode outside the supported values
- **THEN** the system SHALL return HTTP 400 with the unified error envelope
- **AND** the stored preference SHALL NOT change.

#### Scenario: 未认证用户不能更新主题偏好

- **WHEN** a request without a valid Bearer token attempts to read or update account-level theme preference
- **THEN** the system SHALL return the existing authentication error behavior
- **AND** no user preference SHALL be changed.

