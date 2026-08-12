## MODIFIED Requirements

### Requirement: 管理端主题选择器侧边栏位置

Web admin clients SHALL NOT render the global theme selector as an independent control inside the AdminLayout sidebar. The management-side theme preference control SHALL move into the sidebar bottom `AdminUserMenu` dropdown or equivalent user menu surface, because theme preference is a user/account preference rather than a navigation item.

#### Scenario: 侧边栏不再渲染独立主题选择器

- **WHEN** an authenticated admin user opens any AdminLayout page
- **THEN** the sidebar SHALL NOT render an independent 「界面主题」 selector above the bottom user avatar/account block
- **AND** the sidebar navigation, collapse control, user avatar, username, email, and user menu trigger SHALL remain readable and usable.

#### Scenario: 用户菜单内提供主题按钮

- **WHEN** an authenticated admin user opens the sidebar bottom user menu
- **THEN** the dropdown SHALL include a theme toggle button
- **AND** the button SHALL switch between `dark_flagship` and `system`
- **AND** the button SHALL NOT show additional visible switch copy beside it such as 「暗色旗舰」 or 「跟随系统」
- **AND** the button SHALL expose its current state or next action through `aria-label`, tooltip, or equivalent accessible metadata.

#### Scenario: 主题按钮不影响用户菜单操作

- **WHEN** the theme button is present in the user menu
- **THEN** profile navigation, password change, theme switching, and logout menu items SHALL each render a distinct suitable icon
- **AND** the theme row SHALL render a left theme icon, the visible label 「界面主题」, and a right-side switch-style toggle
- **AND** the theme row SHALL NOT render adjacent 「暗色旗舰」 or 「跟随系统」 mode explanation text
- **AND** profile navigation, password change, logout, click-outside close, and keyboard activation behavior SHALL remain available
- **AND** theme switching SHALL NOT reset current route, filters, pagination, form input, or open overlay state.

#### Scenario: 侧边栏收起与窄屏不重叠

- **WHEN** the AdminLayout sidebar is collapsed or rendered in a narrow viewport
- **THEN** the user menu SHALL remain accessible where the current responsive model exposes it
- **AND** the theme button SHALL NOT overlap avatar, menu items, user identity text, navigation items, or sidebar controls.

#### Scenario: Design System 约束

- **WHEN** implementing or styling the user-menu theme button
- **THEN** Web UI changes SHALL use existing semantic token classes, CSS variables, or established admin/sidebar classes
- **AND** TSX/CSS SHALL NOT introduce raw Hex color values for this placement change.

### Requirement: Web 主题切换与偏好持久化

The Web client MUST provide management-side theme switching for `system` and `dark_flagship`. The active mode MUST persist locally and, for authenticated users, synchronize with the account-level theme preference API. Switching themes MUST apply immediately without losing current page state. Account preference synchronization failures MUST be communicated with recoverable admin feedback that automatically dismisses or provides an explicit close affordance; the feedback MUST NOT remain persistently visible without user control.

#### Scenario: 登录前主题偏好

- **WHEN** an unauthenticated user uses local theme initialization
- **THEN** the selected mode SHALL persist locally when it is `system` or `dark_flagship`
- **AND** the Web client SHALL normalize historical local `light` to `system`
- **AND** the Web client SHALL normalize historical local `comfort_dark` to `dark_flagship`
- **AND** the login page SHALL update immediately without requiring reload
- **AND** the Web client SHALL NOT call the account-level theme preference API.

#### Scenario: 登录后账号偏好合并

- **WHEN** a user logs in successfully
- **THEN** the Web client SHALL load the account-level `theme_mode`
- **AND** `system` and `dark_flagship` SHALL be accepted as supported account modes
- **AND** historical account values `light` and `comfort_dark` SHALL be normalized before applying local visual state
- **AND** the active local theme SHALL remain visually stable while synchronization completes.

#### Scenario: 跟随系统解析

- **WHEN** the active mode is `system`
- **THEN** the Web client SHALL resolve actual visual theme from `prefers-color-scheme`
- **AND** operating-system light preference SHALL resolve to the light visual token set
- **AND** operating-system dark or unknown preference SHALL resolve to the dark visual token set.

#### Scenario: 暗色旗舰解析

- **WHEN** the active mode is `dark_flagship`
- **THEN** the Web client SHALL resolve actual visual theme to dark regardless of operating-system light preference.

#### Scenario: 主题切换失败可恢复

- **WHEN** an authenticated user changes theme and the backend persistence request fails
- **THEN** the Web client SHALL keep the local visual selection
- **AND** it SHALL show a recoverable error message using the existing toast or equivalent Design System feedback
- **AND** the error feedback SHALL automatically dismiss or provide an explicit close affordance
- **AND** the error feedback SHALL NOT persist indefinitely, stack repeatedly, or block the user from continuing management-side work.
