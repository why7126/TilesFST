## MODIFIED Requirements

### Requirement: 管理端个人资料路由

Web 客户端 MUST 注册 `/admin/profile` 路由，受管理端路由守卫保护。`admin` 与 `employee` MUST 可访问；`store_owner` MUST 跳转 forbidden。`AdminLayout` MUST 通过 `GET /api/v1/profile/me` 预取当前用户 profile 摘要，并将 `avatar_url`（非空时）传递给侧栏 `AdminUserMenu`；MUST NOT 依赖 auth login `/me` 的 `UserProfile` 获取头像 URL。用户邮箱 SHALL 作为真实联系邮箱字段处理，允许为空；Web 客户端 MUST NOT 在任何管理端身份展示区域通过用户名拼接邮箱样式占位。

#### Scenario: 路由注册与守卫

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/profile`
- **THEN** MUST 渲染 `ProfilePage`
- **AND** MUST NOT 要求 `requireAdmin`

#### Scenario: 店主拒绝

- **WHEN** `store_owner` 访问 `/admin/profile`
- **THEN** MUST 跳转 `/admin/forbidden`

#### Scenario: 侧栏用户菜单身份展示

- **WHEN** 用户查看管理端 Sidebar 底部用户菜单触发区
- **THEN** Sidebar 用户区 MUST 只展示当前用户昵称
- **AND** 昵称为空时 MUST 展示用户名
- **AND** MUST NOT 展示邮箱、副标题、`{username}@tilesfst.com` 或 `admin@tilesfst.com`

#### Scenario: 个人资料页顶部身份栏邮箱展示

- **WHEN** 用户访问 `/admin/profile`
- **AND** 当前用户 `profile.email` 非空
- **THEN** 个人资料页顶部身份栏 MAY 展示该真实邮箱
- **AND** 展示内容 MUST 来自 `profile.email`

- **WHEN** 用户访问 `/admin/profile`
- **AND** 当前用户 `profile.email` 为空
- **THEN** 个人资料页顶部身份栏 MUST NOT 展示 `{username}@tilesfst.com`
- **AND** MUST NOT 展示 `admin@tilesfst.com`
- **AND** MUST 省略邮箱片段或使用不暗示真实邮箱存在的展示

#### Scenario: 个人资料联系邮箱编辑入口

- **WHEN** 用户查看个人资料基础资料表单
- **THEN** 表单 MUST 保留“联系邮箱”输入框
- **AND** 邮箱为空时输入框 MUST 保持为空
- **AND** MUST NOT 自动填入 `{username}@tilesfst.com` 或 `admin@tilesfst.com`

#### Scenario: 用户管理页邮箱能力边界

- **WHEN** 本 BUG 修复实施
- **THEN** MUST NOT 要求用户管理列表新增邮箱列
- **AND** MUST NOT 要求用户创建或编辑弹窗新增联系邮箱输入框
- **AND** 管理员维护用户联系邮箱能力 MUST 由独立需求定义

#### Scenario: 侧栏头像数据 plumbing

- **WHEN** `AdminLayout` 挂载且用户为 `admin` 或 `employee`
- **THEN** MUST 调用 `GET /api/v1/profile/me`（或等价 `fetchProfileMe`）
- **AND** 响应中的 `avatar_url` MUST 传递给 `AdminUserMenu`
- **AND** MUST NOT 扩展 auth `UserProfile` schema 作为唯一数据源
