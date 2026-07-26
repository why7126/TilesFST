## MODIFIED Requirements

### Requirement: 退出登录

Web 客户端 MUST 提供退出登录能力。退出入口 MUST 位于管理端 Sidebar 底部用户菜单的下拉框内，MUST NOT 在 Sidebar 用户按钮下方或管理端顶栏直接展示独立的「退出登录」按钮。

#### Scenario: 退出操作

- **WHEN** 用户在管理端 Sidebar 用户菜单下拉框中点击「退出登录」
- **THEN** 前端 MUST 调用 logout API（可选）、清除本地 token 与用户态
- **AND** MUST 跳转至 `/admin/login`

#### Scenario: 退出后再访问

- **WHEN** 用户退出后访问管理端受保护页面
- **THEN** 前端 MUST 跳转至 `/admin/login`

#### Scenario: 无顶栏退出按钮

- **WHEN** 用户查看管理端 Shell（`/admin/dashboard` 及后续 AdminLayout 包裹页）
- **THEN** 页面 MUST NOT 在顶栏 header 展示独立「退出登录」按钮
- **AND** MUST NOT 在用户菜单触发按钮正下方直接展示「退出登录」
