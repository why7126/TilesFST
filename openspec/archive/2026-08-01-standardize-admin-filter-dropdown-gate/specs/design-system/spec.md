## ADDED Requirements

### Requirement: 管理端筛选下拉统一 Gate
Design System SHALL define a mandatory admin filter dropdown gate for any new or modified admin filter-area Select, Dropdown, Popover, Combobox, date picker, searchable select, or equivalent dropdown control.

#### Scenario: 命中管理端筛选下拉变更
- **WHEN** a Change adds or modifies an admin filter-area dropdown control
- **THEN** implementation MUST reference the admin list page consistency best practice before editing Web UI
- **AND** implementation MUST prefer `AdminFilterSelect`, `SearchableSelect`, or an equivalent shared admin filter wrapper aligned with the tile category page baseline
- **AND** implementation MUST NOT introduce page-local one-off dropdown overlays, raw Hex colors, token-equivalent hardcoded colors, or native controls that diverge from the shared admin filter baseline

#### Scenario: Gate 验收状态覆盖
- **WHEN** an admin filter dropdown gate is evaluated
- **THEN** acceptance MUST cover normal dropdown, searchable dropdown when applicable, disabled state, selected state, empty state, loading state, reset or clear state, focus state, hover state, and narrow admin viewport behavior
- **AND** acceptance MUST confirm the overlay aligns with the trigger and is not clipped by tables, scroll containers, dialogs, sticky action columns, or page containers

#### Scenario: Gate 保持筛选语义
- **WHEN** implementation unifies admin filter dropdown UI
- **THEN** existing filter query parameter names, result semantics, pagination reset behavior, permission boundaries, and error or empty-state recovery MUST remain unchanged unless the Change explicitly specifies a behavior change
- **AND** tests MUST cover the changed shared component or representative affected page so UI unification cannot silently change filter behavior

#### Scenario: Gate 页面矩阵记录
- **WHEN** a Change affects multiple admin pages or a shared admin filter dropdown component
- **THEN** the apply evidence MUST list the affected admin page matrix or explain why only a single page is in scope
- **AND** the matrix SHOULD include representative pages from brand, tile category, tile spec, brand certificate, Banner, user, logs, API docs, settings, or theme surfaces when those pages are affected
