## MODIFIED Requirements

### Requirement: 角色权限前端拦截

前端 MUST 根据用户角色限制管理端访问。用户管理路由 `/admin/users` 与 SYSTEM 分组「用户管理」菜单 MUST 仅对 `role=admin` 可见且可访问。系统设置路由 `/admin/settings` 及其子路径与 SYSTEM 分组「系统设置」菜单 MUST 仅对 `role=admin` 可见且可访问。`employee` MUST 可访问其他管理端页面（如 `/admin/dashboard`）但 MUST NOT 访问用户管理与系统设置。

#### Scenario: 店主角色拒绝管理端

- **WHEN** 角色为 `store_owner` 的用户登录成功
- **THEN** 前端 MUST NOT 进入管理端受保护页面
- **AND** MUST 展示无权限提示或跳转无权限页

#### Scenario: 运营人员不可访问用户管理

- **WHEN** 角色为 `employee` 的用户已登录
- **THEN** Sidebar MUST NOT 展示「用户管理」菜单项
- **AND** 直接访问 `/admin/users` MUST 展示无权限提示或重定向至 `/admin/dashboard`

#### Scenario: 运营人员不可访问系统设置

- **WHEN** 角色为 `employee` 的用户已登录
- **THEN** Sidebar MUST NOT 展示「系统设置」菜单项
- **AND** 直接访问 `/admin/settings/basic` MUST 展示无权限提示或重定向 forbidden

#### Scenario: 管理员可访问用户管理

- **WHEN** 角色为 `admin` 的用户已登录
- **THEN** Sidebar MUST 展示「用户管理」且可导航至 `/admin/users`
- **AND** 页面 MUST 正常加载用户列表

#### Scenario: 管理员可访问系统设置

- **WHEN** 角色为 `admin` 的用户已登录
- **THEN** Sidebar MUST 展示「系统设置」且可导航至 `/admin/settings`
- **AND** 页面 MUST 正常加载系统设置 Shell

#### Scenario: 非管理员访问管理员专属页面（通用）

- **WHEN** 角色为 `employee` 的用户访问其他管理员专属页面（若存在）
- **THEN** 前端 MUST 展示无权限提示
