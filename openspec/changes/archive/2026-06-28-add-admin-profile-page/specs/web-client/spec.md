## ADDED Requirements

### Requirement: 管理端个人资料路由

Web 客户端 MUST 注册 `/admin/profile` 路由，受管理端路由守卫保护。`admin` 与 `employee` MUST 可访问；`store_owner` MUST 跳转 forbidden。

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
