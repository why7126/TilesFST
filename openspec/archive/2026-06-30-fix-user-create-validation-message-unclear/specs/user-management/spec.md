---
change_id: fix-user-create-validation-message-unclear
capability: user-management
created_at: 2026-06-30 18:35:35
updated_at: 2026-06-30 18:35:35
---

## MODIFIED Requirements

### Requirement: 管理端用户创建 API

系统 MUST 提供 `POST /api/v1/admin/users`，仅 `admin` 可调用。请求 MUST 接受 username、可选 display_name、role、可选 avatar_object_key。新用户 status MUST 默认为 `active`。系统 MUST 生成随机初始密码并在响应 `data.initial_password` 中一次性返回明文；数据库 MUST 仅存 bcrypt 哈希。

用户名校验失败时，系统 MUST 返回项目统一错误结构 `{ code, message, data }`，MUST NOT 将 FastAPI 默认 422 `detail` 列表作为面向前端用户的唯一错误体。`message` MUST 明确指出用户名字段与具体原因，至少覆盖长度、首字符、字符集、连续特殊符号与保留字。用户名长度不足或超长 SHOULD 返回 HTTP 400 与 `USER_INVALID_USERNAME`；若实现保留 HTTP 422，响应体仍 MUST 符合统一错误结构且包含明确中文 `message`。

#### Scenario: 创建用户成功

- **WHEN** `admin` 提交合法 username（4–32 位及格式规则）、role 与可选字段
- **THEN** 系统返回 HTTP 200，包含用户对象与 `initial_password`
- **AND** 用户 status MUST 为 `active`

#### Scenario: 用户名重复

- **WHEN** username 已存在
- **THEN** 系统 MUST 返回 HTTP 409，错误码 `USER_USERNAME_TAKEN`
- **AND** 错误响应 MUST 保持统一 `{ code, message, data }` 结构

#### Scenario: 用户名长度不足

- **WHEN** `admin` 提交 `username="abc"` 创建用户
- **THEN** 系统 MUST 返回 HTTP 400 或统一 envelope 的 HTTP 422
- **AND** 响应体 MUST 包含 `code`、`message`、`data`
- **AND** 响应体 MUST NOT 仅包含 FastAPI 默认 `detail` 列表
- **AND** `message` MUST 明确说明用户名长度须为 4-32 位或等价中文原因

#### Scenario: 用户名格式非法

- **WHEN** username 不满足 4–32 位、字符集、保留字或连续特殊符号规则
- **THEN** 系统 MUST 返回 HTTP 400 或统一 envelope 的 HTTP 422
- **AND** 错误码 MUST 表示 `USER_INVALID_USERNAME` 或等价已登记用户校验错误
- **AND** `message` MUST 明确指出对应用户名规则

#### Scenario: 创建用户校验不影响重复用户名

- **GIVEN** 数据库已存在 username 为 `store_user_01` 的用户
- **WHEN** `admin` 再次提交同名用户
- **THEN** 系统 MUST 返回 HTTP 409
- **AND** 错误码与文案 MUST 仍明确表示用户名已存在
