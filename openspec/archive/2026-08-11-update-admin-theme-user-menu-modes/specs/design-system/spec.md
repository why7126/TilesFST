## MODIFIED Requirements

### Requirement: Web 多主题 Design Token

Web Design System MUST expose two user-selectable theme modes for the current product surface: `system` and `dark_flagship`. Theme behavior MUST be implemented through semantic tokens and theme-scoped CSS variables, not business-component raw Hex values. Existing industrial stone dark values remain the `dark_flagship` mode baseline. The `system` mode MUST resolve to the light visual token set when the operating system prefers light and to the dark visual token set otherwise. Historical `comfort_dark` and `light` values MUST NOT remain visible user options, though migration or normalization code MAY continue recognizing them for backward compatibility.

#### Scenario: 主题模式收敛

- **WHEN** Web initializes user-selectable Design System theme modes
- **THEN** only `system` and `dark_flagship` modes SHALL be available to users
- **AND** `comfort_dark` and independent `light` SHALL NOT be exposed as user-selectable modes.

#### Scenario: 系统模式可解析浅色

- **WHEN** the active user-selectable mode is `system`
- **AND** the operating system prefers light colors
- **THEN** the resolved visual token set SHALL use the light theme variables
- **AND** semantic classes such as `bg-page`, `text-primary`, `text-brand-gold`, and `border-border-default` SHALL continue to resolve without business-page rewrites.

#### Scenario: 暗色旗舰保持品牌基线

- **WHEN** the active mode is `dark_flagship`
- **THEN** the visual result SHALL preserve the existing industrial stone flagship dark brand baseline
- **AND** existing semantic classes such as `bg-page`, `text-primary`, `text-brand-gold`, and `border-border-default` SHALL continue to resolve without business-page rewrites.

#### Scenario: 业务 UI 禁止裸 Hex

- **WHEN** business Web pages or components are modified for this change
- **THEN** they MUST consume semantic tokens or Design System utilities
- **AND** they MUST NOT introduce raw Hex color values in business UI code.

### Requirement: Design System 主题预览与舒适度验收

The `/design-system` page MUST provide a theme preview surface for the current supported user-selectable theme modes and include representative surfaces affected by theme behavior.

#### Scenario: 主题切换可预览

- **WHEN** a user opens `/design-system`
- **THEN** the page SHALL allow switching between `system` and `dark_flagship`
- **AND** token previews and representative components SHALL update immediately
- **AND** the page SHALL NOT expose `comfort_dark` or independent `light` as selectable modes.

#### Scenario: 管理端主题按钮验收

- **WHEN** `/design-system` or equivalent admin design acceptance is used for this Change
- **THEN** it SHALL support verification that user-menu theme controls use semantic tokens
- **AND** the evidence SHALL cover `dark_flagship` and `system` with operating-system light resolution where feasible.

