## ADDED Requirements

### Requirement: Web 多主题 Design Token

Web Design System MUST support four theme modes: `system`, `dark_flagship`, `comfort_dark`, and `light`. Theme modes MUST be implemented through semantic tokens and theme-scoped CSS variables, not business-component raw Hex values. Existing industrial stone dark values remain the `dark_flagship` mode baseline; `comfort_dark` and `light` MUST provide complete token values for page, surface, text, border, accent, focus, danger, success, warning, shadow, and overlay semantics.

#### Scenario: 主题模式完整

- **WHEN** Web initializes Design System tokens
- **THEN** `system`, `dark_flagship`, `comfort_dark`, and `light` modes SHALL be available
- **AND** each mode SHALL define complete semantic token values for core page, surface, text, border, accent, focus, feedback, shadow, and overlay semantics.

#### Scenario: 暗色旗舰保持品牌基线

- **WHEN** the active mode is `dark_flagship`
- **THEN** the visual result SHALL preserve the existing industrial stone flagship dark brand baseline
- **AND** existing semantic classes such as `bg-page`, `text-primary`, `text-brand-gold`, and `border-border-default` SHALL continue to resolve without business-page rewrites.

#### Scenario: 业务 UI 禁止裸 Hex

- **WHEN** business Web pages or components are modified for this change
- **THEN** they MUST consume semantic tokens or Design System utilities
- **AND** they MUST NOT introduce raw Hex color values in business UI code.

### Requirement: Design System 主题预览与舒适度验收

The `/design-system` page MUST provide a theme preview surface for all supported theme modes and include representative tile SKU components used in REQ-0020 acceptance.

#### Scenario: 主题切换可预览

- **WHEN** a user opens `/design-system`
- **THEN** the page SHALL allow switching among `system`, `dark_flagship`, `comfort_dark`, and `light`
- **AND** token previews and representative components SHALL update immediately.

#### Scenario: 瓷砖 SKU 组件覆盖

- **WHEN** `/design-system` is used for REQ-0020 acceptance
- **THEN** it SHALL include representative previews for buttons, inputs, tables, dialogs, toast, media upload state, and tile SKU list/form/modal components
- **AND** those previews SHALL be usable to verify login/list/form/modal comfort regressions across themes.
