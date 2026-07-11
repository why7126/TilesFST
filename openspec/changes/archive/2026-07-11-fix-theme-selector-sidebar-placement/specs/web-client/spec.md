## ADDED Requirements

### Requirement: 管理端主题选择器侧边栏位置

Web admin clients SHALL render the global theme selector inside the AdminLayout sidebar, positioned directly above the bottom user avatar/account block. The selector SHALL NOT render in the page top-right content or header area on AdminLayout pages.

#### Scenario: 主题选择器位于侧边栏用户区上方

- **WHEN** an authenticated admin user opens any AdminLayout page
- **THEN** the sidebar SHALL render the 「界面主题」 selector
- **AND** the selector SHALL be positioned above the bottom user avatar/account block
- **AND** the selector SHALL not overlap the avatar, username, email, user menu trigger, navigation items, or sidebar collapse control.

#### Scenario: 顶部区域不再渲染主题选择器

- **WHEN** an authenticated admin user opens pages such as `/admin/dashboard`, `/admin/users`, `/admin/settings`, or `/admin/api-docs`
- **THEN** the page top-right content/header area SHALL NOT render the 「界面主题」 selector
- **AND** page-level top actions SHALL remain reserved for page-specific commands or filters.

#### Scenario: 主题切换行为保持不变

- **WHEN** the user changes the active theme from the sidebar selector
- **THEN** the selected theme SHALL apply immediately according to existing theme switching behavior
- **AND** existing local and account-level persistence behavior SHALL remain unchanged
- **AND** current page state such as filters, pagination, forms, open dialogs, and upload state SHALL not be reset by moving the selector.

#### Scenario: 侧边栏收起与窄屏不重叠

- **WHEN** the AdminLayout sidebar is collapsed or rendered in a narrow viewport
- **THEN** the theme selector SHALL remain accessible through a compact or equivalent sidebar treatment
- **AND** text, icons, select trigger, user avatar, and menu controls SHALL not overlap or become unreadable.

#### Scenario: Design System 约束

- **WHEN** implementing or styling the sidebar theme selector
- **THEN** Web UI changes SHALL use existing semantic token classes, CSS variables, or established admin/sidebar classes
- **AND** TSX/CSS SHALL NOT introduce raw Hex color values for this placement fix.
