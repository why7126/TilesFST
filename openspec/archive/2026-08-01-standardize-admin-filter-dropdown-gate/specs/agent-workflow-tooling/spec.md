## ADDED Requirements

### Requirement: `/opsx-apply` 管理端筛选下拉 Checklist
`/opsx-apply` SHALL include a dedicated checklist gate for Changes that add or modify admin filter dropdown controls, in addition to the existing cross-cutting admin list gate.

#### Scenario: Apply 前识别筛选下拉标签
- **WHEN** `/opsx-apply` reads a Change whose proposal, design, tasks, specs, trace, or affected file paths mention admin filter dropdowns, filter-area Select, Dropdown, Popover, Combobox, date picker, searchable select, `AdminFilterSelect`, `SearchableSelect`, `admin-filter-dropdown`, or equivalent terms
- **THEN** the Cross-cutting Apply Gate MUST add an `admin-filter-dropdown` tag
- **AND** the gate MUST read `docs/knowledge-base/best-practices/admin-list-page-consistency.md` or the successor best-practice document before editing `src/`

#### Scenario: Apply checklist 输出
- **WHEN** the `admin-filter-dropdown` tag is active
- **THEN** `/opsx-apply` MUST report checklist results for best-practice read, shared component reuse or justified equivalent wrapper, page-local overlay CSS absence, state coverage, overlay clipping check, query parameter semantics, and regression test plan
- **AND** the verdict MUST be `BLOCKED` if a new or modified admin filter dropdown lacks both shared-component reuse and an explicit equivalent-wrapper rationale

#### Scenario: Apply 中完成任务
- **WHEN** implementation tasks touch admin filter dropdown UI
- **THEN** tasks MUST include focused verification for component classes or DOM contract, open/select/clear/reset behavior, empty or loading state when applicable, disabled or selected state, and at least one representative affected page
- **AND** tasks MUST record whether visual smoke or Playwright verification is required for desktop and narrow admin viewports

#### Scenario: 非相关 Change 不误阻断
- **WHEN** a Change does not affect admin filter dropdown controls
- **THEN** `/opsx-apply` MAY mark the `admin-filter-dropdown` checklist as `n/a`
- **AND** the checklist MUST NOT block backend-only, database-only, release-only, or non-filter UI Changes solely because the admin list best-practice document exists
