## ADDED Requirements

### Requirement: Clipboard 复制交互治理

Design System governance SHALL document or preview the Web admin Clipboard copy pattern so future copy interactions reuse the shared helper or an equivalent best-practice instead of duplicating page-local Clipboard API branching.

#### Scenario: 复制 helper 使用边界可查

- **WHEN** developers read the Web README, Design System notes, or change design produced by this change
- **THEN** they SHALL find that the Clipboard helper owns copy result normalization
- **AND** callers own toast, dialog text, usage events, and business-specific side effects.

#### Scenario: Design System 约束保持

- **WHEN** an implementation adds or modifies copy buttons, toast feedback, or modal copy status text
- **THEN** it SHALL use existing admin UI patterns, semantic token classes, CSS variables, or existing admin classes
- **AND** it SHALL NOT add raw Hex colors or one-off hardcoded design colors in production Web UI.

#### Scenario: 复制交互不引入新 UI 体系

- **WHEN** copy feedback is implemented for admin list rows or admin modal dialogs
- **THEN** it SHALL use existing fixed toast, `role="status"`, modal help text, or equivalent existing Design System feedback patterns
- **AND** it SHALL NOT introduce a new global toast/dialog library for this change.

### Requirement: Clipboard 横切验收

Design System acceptance SHALL include cross-cutting checks for admin list and admin modal copy interactions where this change touches those surfaces.

#### Scenario: 管理端列表复制反馈无布局位移

- **WHEN** an admin list page copy action succeeds, fails, or falls back to manual copy
- **THEN** feedback SHALL NOT push the page hero, filters, table, or pagination in document flow
- **AND** pagination DOM SHALL remain aligned with the admin list baseline when the page is touched by this change.

#### Scenario: 管理端弹窗复制反馈不破坏弹窗布局

- **WHEN** generated-password copy feedback is shown inside a modal
- **THEN** modal width, body scroll, input visibility, and footer button reachability SHALL remain stable
- **AND** implementation SHALL NOT combine generic `modal-card` with a feature-specific modal card class in a way that reintroduces CSS cascade width overrides.
