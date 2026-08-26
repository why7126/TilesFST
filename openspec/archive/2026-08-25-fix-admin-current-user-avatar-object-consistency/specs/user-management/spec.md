## MODIFIED Requirements

### Requirement: 管理端用户列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/users`，仅 `role=admin` 的用户可调用。接口 MUST 支持分页（默认 `page_size=10`，可选 10/20/50）、关键词模糊搜索（username、display_name、email、phone）、角色筛选、状态筛选（`active`/`disabled`/`deleted`）与登录情况筛选（从未登录、最近 7 天登录、超过 30 天未登录）。响应 MUST 包含用户列表与 summary（用户总数、当前筛选数、正常用户数、已冻结用户数）。每条用户记录 MUST 同时返回 `avatar_object_key` 与可访问的 `avatar_url`。当 `avatar_object_key` 非空时，`avatar_url` MUST 为 `/media/{object_key}` 或等价受控媒体 URL，且 SHOULD 对应可加载对象；若历史数据漂移导致对象缺失，系统 MUST 通过数据修复或安全 fallback 避免用户可见破损头像。

系统 MUST 以 `settings.admin_username` / `ADMIN_USERNAME` 作为唯一事实源识别受保护系统账号。用户列表中每条用户记录 MUST 返回 `is_protected` 与 `protected_reason` 字段；受保护账号 MUST 返回 `is_protected=true` 与明确中文原因，普通用户 MUST 返回 `is_protected=false` 且 `protected_reason=null`。

#### Scenario: 管理员查询用户列表

- **WHEN** `admin` 携带有效 token 请求 `GET /api/v1/admin/users`
- **THEN** 系统返回 HTTP 200，`data` 包含 `items`、`pagination` 与 `summary`
- **AND** 每条用户记录 MUST 包含 id、username、display_name、role、status、avatar_object_key、avatar_url、email、phone、last_login_at、created_at、is_protected、protected_reason
- **AND** 当 `avatar_object_key` 非空时 `avatar_url` MUST 非空且使用受控媒体 URL

### Requirement: 管理端用户更新 API

系统 MUST 提供 `GET /api/v1/admin/users/{id}` 与 `PATCH /api/v1/admin/users/{id}`，仅 `admin` 可调用。GET 返回的用户对象 MUST 包含 `is_protected`、`protected_reason`、`email`、`phone`。PATCH MUST 允许更新 display_name、role、avatar_object_key、email、phone；username MUST NOT 可修改。当目标用户为受保护账号时，PATCH MUST 返回 HTTP 403 与已登记错误码，且 MUST NOT 修改 display_name、role、avatar_object_key、email、phone 或其他用户资料字段。写入非空 `avatar_object_key` 时 SHOULD 与 profile self-service API 保持一致的对象存在性校验；若本次实现范围不修改管理员代改接口，MUST 在验收记录中说明差异和后续处理方式。

`email` 与 `phone` 字段缺省时 MUST 保持原值；显式传入 `null` 或空白字符串时 MUST 清空对应字段。

#### Scenario: 更新昵称、角色与联系信息

- **WHEN** `admin` PATCH 合法 display_name、role、email、phone
- **THEN** 系统返回 HTTP 200 与更新后用户对象
- **AND** 响应用户对象 MUST 包含更新后的 `email` 与 `phone`

### Requirement: 管理端用户管理页面

Web 客户端 MUST 提供 `/admin/users` 页面，视觉 MUST 高保真对齐 `user-management-list.html` / `user-management-list.png` 的 CSS Port 策略。页面 MUST 继承 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容宽度跟随全局 Admin Shell `content-inner` 策略，MUST NOT 重新锁定为 1080px）。当前路由为用户管理时 SYSTEM「用户管理」导航 MUST 为 active。用户列表「用户」列 MUST 在有 `avatar_url` 时展示头像图片，无头像时 MUST 展示 initials 占位；图片加载失败 MUST 稳定回退 initials 且不引起布局跳动。

#### Scenario: 用户列表头像加载失败兜底

- **GIVEN** 用户列表记录包含非空 `avatar_url`
- **WHEN** 头像图片加载失败
- **THEN** 用户列表 MUST 显示 initials fallback
- **AND** MUST NOT 展示破损图片
- **AND** 表格行高与布局 MUST 保持稳定
