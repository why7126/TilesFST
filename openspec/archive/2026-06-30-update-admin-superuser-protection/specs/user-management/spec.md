---
change_id: update-admin-superuser-protection
capability: user-management
created_at: 2026-06-30 18:26:13
updated_at: 2026-06-30 18:26:13
---

## MODIFIED Requirements

### Requirement: 管理端用户列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/users`，仅 `role=admin` 的用户可调用。接口 MUST 支持分页（默认 `page_size=10`，可选 10/20/50）、关键词模糊搜索（username、display_name、email、phone）、角色筛选、状态筛选（`active`/`disabled`/`deleted`）与登录情况筛选（从未登录、最近 7 天登录、超过 30 天未登录）。响应 MUST 包含用户列表与 summary（用户总数、当前筛选数、正常用户数、已冻结用户数）。每条用户记录 MUST 同时返回 `avatar_object_key` 与可访问的 `avatar_url`（当 `avatar_object_key` 非空时，`avatar_url` MUST 为 `/media/{object_key}` 形式且浏览器可加载）。

系统 MUST 以 `settings.admin_username` / `ADMIN_USERNAME` 作为唯一事实源识别受保护系统账号。用户列表中每条用户记录 MUST 返回 `is_protected` 与 `protected_reason` 字段；受保护账号 MUST 返回 `is_protected=true` 与明确中文原因，普通用户 MUST 返回 `is_protected=false` 且 `protected_reason=null`。

#### Scenario: 管理员查询用户列表

- **WHEN** `admin` 携带有效 token 请求 `GET /api/v1/admin/users`
- **THEN** 系统返回 HTTP 200，`data` 包含 `items`、`pagination` 与 `summary`
- **AND** 每条用户记录 MUST 包含 id、username、display_name、role、status、avatar_object_key、avatar_url、email、phone、last_login_at、created_at、is_protected、protected_reason
- **AND** 当 `avatar_object_key` 非空时 `avatar_url` MUST 非空且可加载

#### Scenario: 受保护账号在列表中带保护标识

- **GIVEN** `ADMIN_USERNAME=admin`
- **AND** 数据库存在 username 为 `admin` 的用户
- **WHEN** `admin` 请求 `GET /api/v1/admin/users`
- **THEN** 该用户记录 MUST 返回 `is_protected=true`
- **AND** `protected_reason` MUST 为明确中文说明
- **AND** 其他普通 `role=admin` 用户 MUST 返回 `is_protected=false`

#### Scenario: 非管理员被拒绝

- **WHEN** `employee` 或 `store_owner` 请求 `GET /api/v1/admin/users`
- **THEN** 系统 MUST 返回 HTTP 403

#### Scenario: 分页默认值

- **WHEN** 请求未指定 `page_size`
- **THEN** 系统 MUST 默认每页 10 条

### Requirement: 管理端用户更新 API

系统 MUST 提供 `GET /api/v1/admin/users/{id}` 与 `PATCH /api/v1/admin/users/{id}`，仅 `admin` 可调用。GET 返回的用户对象 MUST 包含 `is_protected` 与 `protected_reason`。PATCH MUST 允许更新 display_name、role、avatar_object_key；username MUST NOT 可修改。当目标用户为受保护账号时，PATCH MUST 返回 HTTP 403 与已登记错误码，且 MUST NOT 修改 display_name、role、avatar_object_key 或其他用户资料字段。

#### Scenario: 更新昵称与角色

- **WHEN** `admin` PATCH 合法 display_name（可为空，最多 32 字符）与 role
- **THEN** 系统返回 HTTP 200 与更新后用户对象

#### Scenario: 详情返回受保护标识

- **GIVEN** 目标用户 username 等于 `ADMIN_USERNAME`
- **WHEN** `admin` 请求 `GET /api/v1/admin/users/{id}`
- **THEN** 响应用户对象 MUST 包含 `is_protected=true`
- **AND** `protected_reason` MUST 为明确中文说明

#### Scenario: 禁止修改用户名

- **WHEN** 请求体包含 username 字段试图修改
- **THEN** 系统 MUST 忽略或返回 HTTP 400

#### Scenario: 受保护账号禁止编辑

- **GIVEN** 目标用户 username 等于 `ADMIN_USERNAME`
- **WHEN** `admin` 请求 `PATCH /api/v1/admin/users/{id}` 修改 display_name、role 或 avatar_object_key
- **THEN** 系统 MUST 返回 HTTP 403
- **AND** 错误响应 `code` MUST 为已登记的受保护账号错误码
- **AND** 数据库中的 display_name、role、avatar_object_key MUST 保持不变

### Requirement: 管理端重置密码 API

系统 MUST 提供 `POST /api/v1/admin/users/{id}/reset-password`，仅 `admin` 可调用。系统 MUST 生成满足 **effective** 密码策略的随机密码（长度与复杂度按 `system_settings` security 分组 merge 默认值）并在响应中一次性返回明文；后续 GET 接口 MUST NOT 再返回该密码。当目标用户为受保护账号时，系统 MUST 返回 HTTP 403 与已登记错误码，MUST NOT 生成新随机明文密码，MUST NOT 更新 `password_hash`。

#### Scenario: 重置密码成功

- **WHEN** `admin` 对存在且非 `deleted` 的用户调用重置密码
- **THEN** 系统返回 HTTP 200，`data.password` 为一次性明文
- **AND** 用户 password_hash MUST 已更新
- **AND** 生成密码 MUST 满足 effective 最小长度与复杂度开关

#### Scenario: 受保护账号禁止重置密码

- **GIVEN** 目标用户 username 等于 `ADMIN_USERNAME`
- **WHEN** `admin` 请求 `POST /api/v1/admin/users/{id}/reset-password`
- **THEN** 系统 MUST 返回 HTTP 403
- **AND** 错误响应 `code` MUST 为已登记的受保护账号错误码
- **AND** 系统 MUST NOT 生成或返回新随机密码
- **AND** 目标用户 `password_hash` MUST 保持不变

### Requirement: 管理端用户状态变更 API

系统 MUST 提供 `PATCH /api/v1/admin/users/{id}/status`，仅 `admin` 可调用，用于冻结（`disabled`）、解冻（`active`）与软删除（`deleted`）。当目标用户为受保护账号时，系统 MUST 对任意状态变更返回 HTTP 403 与已登记错误码，且 MUST NOT 修改 status。

#### Scenario: 冻结与解冻

- **WHEN** `admin` 将 `active` 用户设为 `disabled` 或反向
- **THEN** 系统返回 HTTP 200 且 status 已更新

#### Scenario: 软删除仅从未登录用户

- **WHEN** `admin` 对 `last_login_at` 非空的用户请求 `deleted`
- **THEN** 系统 MUST 返回 HTTP 400，错误码 `USER_CANNOT_DELETE_LOGGED_IN`

#### Scenario: 软删除成功

- **WHEN** `admin` 对从未登录用户请求 `deleted`
- **THEN** 系统返回 HTTP 200 且 status 为 `deleted`

#### Scenario: 受保护账号禁止任意状态变更

- **GIVEN** 目标用户 username 等于 `ADMIN_USERNAME`
- **WHEN** `admin` 请求将该用户状态变更为 `active`、`disabled` 或 `deleted`
- **THEN** 系统 MUST 返回 HTTP 403
- **AND** 错误响应 `code` MUST 为已登记的受保护账号错误码
- **AND** 目标用户 status MUST 保持原值

### Requirement: 管理端用户列表行操作

用户列表操作列 MUST 提供：编辑、重置密码、冻结/解冻、删除。已冻结用户 MUST 显示「解冻」；仅 `last_login_at` 为空的用户 MUST 启用「删除」，否则删除按钮 MUST 置灰。当 `user.is_protected=true` 时，编辑、重置密码、冻结/解冻、删除按钮 MUST 保留但置灰，MUST 使用 `protected_reason` 作为 title、tooltip 或等价原因提示，且 MUST NOT 打开确认弹窗或调用对应 API。前端 MUST NOT 通过硬编码 `admin` 或 role 判断保护状态。

#### Scenario: 重置密码交互

- **WHEN** 用户确认重置密码且 API 成功
- **THEN** MUST 在二次弹窗展示一次性密码与复制按钮
- **AND** 关闭后 MUST NOT 再次展示同一密码

#### Scenario: 冻结解冻 Toast

- **WHEN** 冻结或解冻成功
- **THEN** MUST 分别 Toast「用户已冻结」「用户已恢复正常」

#### Scenario: 删除 Toast

- **WHEN** 软删除成功
- **THEN** MUST Toast「用户已删除」

#### Scenario: 受保护账号行操作置灰

- **GIVEN** 用户列表中存在 `is_protected=true` 的用户
- **WHEN** 管理员查看该用户行
- **THEN** 编辑、重置密码、冻结/解冻、删除按钮 MUST 置灰但仍可见
- **AND** 禁用原因 MUST 来自 `protected_reason`
- **AND** 点击这些禁用操作 MUST NOT 打开 confirm modal 或调用 API

#### Scenario: 普通用户行操作不回归

- **GIVEN** 用户列表中存在 `is_protected=false` 的普通用户
- **WHEN** 管理员点击编辑、重置密码、冻结/解冻或删除
- **THEN** 既有弹窗、confirm、toast、刷新和权限规则 MUST 保持不变
