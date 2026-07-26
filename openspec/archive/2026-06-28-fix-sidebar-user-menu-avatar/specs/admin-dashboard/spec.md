## MODIFIED Requirements

### Requirement: 管理端 Sidebar 用户菜单

Sidebar 底部 MUST 固定用户菜单（`margin-top: auto`）。**expanded** 态 MUST 展示用户头像区（有 `avatar_url` 时 MUST 为头像图片，否则 MUST 为首字母缩写 fallback）、用户名、邮箱与展开箭头；**collapsed** 态（桌面 >1023px）MUST 仅展示用户头像区（同上规则），点击 MUST 仍可展开下拉框（个人资料、密码修改、退出登录）。用户菜单按钮下方 MUST NOT 直接展示「退出登录」按钮。头像区 MUST 为 34×34px，使用 semantic token（`--admin-gold-bg`、`--admin-avatar-border` 等），MUST NOT 硬编码裸 Hex。

#### Scenario: 用户菜单展示 expanded

- **WHEN** 用户查看 expanded Sidebar 底部（桌面端 >1023px）
- **THEN** MUST 展示用户触发按钮（头像区、用户名、邮箱、箭头）
- **AND** MUST NOT 在按钮下方直接展示「退出登录」按钮

#### Scenario: 用户菜单展示 collapsed

- **WHEN** 用户查看 collapsed Sidebar 底部（桌面端 >1023px）
- **THEN** MUST 仅展示头像区按钮
- **AND** 点击 MUST 打开与 expanded 相同的下拉菜单

#### Scenario: 侧栏头像图片展示

- **WHEN** `AdminLayout` 从 `GET /api/v1/profile/me` 获得非空 `avatar_url`
- **THEN** 侧栏 `.avatar` MUST 渲染 `<img src={avatar_url}>` 且图片可见
- **AND** 图片 MUST 填充 34×34px 容器（`object-fit: cover`）

#### Scenario: 侧栏头像 initials fallback

- **WHEN** `avatar_url` 为空、null 或图片加载失败（`onError`）
- **THEN** 侧栏 `.avatar` MUST 回退显示 `getUserInitials(display_name, username)` 文本占位
- **AND** MUST NOT 展示破损图片占满容器

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
