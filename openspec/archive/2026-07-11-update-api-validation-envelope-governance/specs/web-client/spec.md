## ADDED Requirements

### Requirement: 管理端表单校验错误解析

Web 管理端 MUST provide a shared or equivalent error parsing strategy for management admin form, modal, and upload API failures. The parser MUST prioritize the unified envelope `message`, SHOULD map `data.errors[]` to field-level errors when possible, and MUST safely fall back to a global toast, modal fixed error area, or upload control error state when field mapping is unavailable. Web admin code MUST NOT rely on raw `detail[0].msg` as the only validation error source.

#### Scenario: Envelope message becomes global feedback

- **WHEN** a management admin form API returns `{ code, message, data }` for a validation failure
- **THEN** the Web admin client MUST use `message` as the preferred global error feedback
- **AND** existing business error messages for users, brands, categories, SKUs, specs, banners, system settings, profile, password, and uploads MUST remain compatible.

#### Scenario: Field errors map when possible

- **WHEN** a validation error response includes `data.errors[]`
- **AND** an error item can be mapped to a visible form field
- **THEN** the Web admin client SHOULD display or expose the field-level message for that field
- **AND** unmapped field errors MUST safely degrade to global feedback.

#### Scenario: Raw detail is not the only source

- **WHEN** a management admin form request fails validation
- **THEN** Web admin code MUST NOT depend on raw `detail[0].msg` as the only path for user-facing errors
- **AND** any legacy `detail` compatibility branch MUST be secondary to the unified envelope.

#### Scenario: Error display uses existing Design System

- **WHEN** validation errors are displayed in admin pages, modals, or upload controls
- **THEN** the display MUST use existing admin fixed toast, inline field text, modal fixed error area, or upload fixed error area patterns
- **AND** it MUST NOT add naked Hex colors, independent light error cards, `window.alert`, or `window.confirm`
- **AND** it MUST NOT visibly push modal footer buttons, resize modal width, or break upload `idle → uploading → done/failed` state.

#### Scenario: Upload validation failure keeps preview state stable

- **WHEN** an admin upload API returns a validation envelope for missing `file` or invalid file parameter
- **THEN** the upload control MUST show a stable failure state or toast
- **AND** a successful preview from the same session MUST NOT be cleared unless the user explicitly replaces or removes it.
