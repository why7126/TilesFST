## MODIFIED Requirements

### Requirement: 管理端 Sidebar 用户菜单

Sidebar 底部 MUST 固定用户菜单（`margin-top: auto`）。**expanded** 态 MUST 展示头像缩写、用户名、邮箱与展开箭头；**collapsed** 态（桌面 >1023px）MUST 仅展示头像缩写，点击 MUST 仍可展开下拉框（个人资料、密码修改、退出登录）。用户菜单按钮下方 MUST NOT 直接展示「退出登录」按钮。

#### Scenario: 用户菜单展示 expanded

- **WHEN** 用户查看 expanded Sidebar 底部（桌面端 >1023px）
- **THEN** MUST 展示用户触发按钮（头像缩写、用户名、邮箱、箭头）
- **AND** MUST NOT 在按钮下方直接展示「退出登录」按钮

#### Scenario: 用户菜单展示 collapsed

- **WHEN** 用户查看 collapsed Sidebar 底部（桌面端 >1023px）
- **THEN** MUST 仅展示头像缩写按钮
- **AND** 点击 MUST 打开与 expanded 相同的下拉菜单

#### Scenario: 用户菜单下拉内容

- **WHEN** 用户点击 Sidebar 底部用户菜单
- **THEN** MUST 在用户按钮上方展开下拉框
- **AND** 下拉框 MUST 包含「个人资料」「密码修改」、分隔线与「退出登录」
- **AND** 「退出登录」MUST 使用风险色弱强调

#### Scenario: 用户菜单可访问性

- **WHEN** 辅助技术访问用户菜单
- **THEN** 触发按钮 MUST 设置 `aria-expanded` 与 `aria-haspopup="menu"`
- **AND** 下拉框 MUST 使用 `role="menu"`，菜单项 MUST 使用 `role="menuitem"`

#### Scenario: 密码修改打开弹窗

- **WHEN** 用户点击「密码修改」
- **THEN** 系统 MUST 打开 `ChangePasswordModal`
- **AND** MUST NOT 展示「功能建设中」占位 toast

#### Scenario: 个人资料入口（至 REQ-0014 apply 前）

- **WHEN** `add-admin-profile-page` 尚未 apply
- **THEN** 「个人资料」MAY 仍为 placeholder
- **WHEN** `add-admin-profile-page` 已 apply
- **THEN** 「个人资料」MUST 导航至 `/admin/profile`
