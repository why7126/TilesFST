## MODIFIED Requirements

### Requirement: 管理端个人资料路由

Web 客户端 MUST 注册 `/admin/profile` 路由，受管理端路由守卫保护。`admin` 与 `employee` MUST 可访问；`store_owner` MUST 跳转 forbidden。`AdminLayout` MUST 通过 `GET /api/v1/profile/me` 预取当前用户 profile 摘要，并将 `email` 与 `avatar_url`（非空时）传递给侧栏 `AdminUserMenu`；MUST NOT 依赖 auth login `/me` 的 `UserProfile` 获取头像 URL。

#### Scenario: 路由注册与守卫

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/profile`
- **THEN** MUST 渲染 `ProfilePage`
- **AND** MUST NOT 要求 `requireAdmin`

#### Scenario: 店主拒绝

- **WHEN** `store_owner` 访问 `/admin/profile`
- **THEN** MUST 跳转 `/admin/forbidden`

#### Scenario: 侧栏邮箱展示

- **WHEN** 用户 profile 含 email
- **THEN** Sidebar 用户区 MUST 展示该 email
- **WHEN** email 为空
- **THEN** MAY fallback `{username}@tilesfst.com`

#### Scenario: 侧栏头像数据 plumbing

- **WHEN** `AdminLayout` 挂载且用户为 `admin` 或 `employee`
- **THEN** MUST 调用 `GET /api/v1/profile/me`（或等价 `fetchProfileMe`）
- **AND** 响应中的 `avatar_url` MUST 传递给 `AdminUserMenu`
- **AND** MUST NOT 扩展 auth `UserProfile` schema 作为唯一数据源

#### Scenario: Profile 上传后侧栏刷新

- **WHEN** 用户在 `/admin/profile` 成功上传并持久化新头像
- **THEN** 导航至其他 `/admin/*` 页时侧栏 MUST 展示新头像图片
- **AND** MUST NOT 要求整页硬刷新浏览器
