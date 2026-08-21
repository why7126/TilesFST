## MODIFIED Requirements

### Requirement: 管理端列表页一致性回归测试

测试治理 SHALL require focused regression coverage for admin list page consistency, including pagination DOM, table column display, sticky action column behavior, fixed toast feedback, Design System confirm modal usage, admin filter overlay behavior, and backend pagination contracts when a Change modifies admin list pages or shared admin list foundations.

#### Scenario: 分页 DOM 回归测试
- **WHEN** a Change modifies an admin list page, shared admin list template, or pagination component
- **THEN** Vitest, Testing Library, or equivalent frontend tests SHALL verify `page-summary` and `page-right` exist
- **AND** tests SHALL verify the displayed total uses backend total count or a documented equivalent test double
- **AND** tests SHALL verify page-size, search, filter, or sort changes reset to a valid page

#### Scenario: 列展示回归测试
- **WHEN** a Change modifies admin table columns or shared column rendering
- **THEN** tests SHALL verify table headers default to non-wrapping behavior through stable class, DOM contract, or equivalent assertion
- **AND** tests SHALL verify normal text fields use single-line truncation or equivalent behavior
- **AND** tests SHALL verify effective-period fields are the only documented two-line exception in the representative page unless the Change records another exception

#### Scenario: sticky 操作列回归测试
- **WHEN** a Change modifies admin table action cells, table width, horizontal scrolling, or column count
- **THEN** tests or documented visual evidence SHALL verify action entry points remain reachable
- **AND** checks SHALL confirm sticky action cells do not cover pagination, filter overlays, dialogs, or toasts
- **AND** disabled, loading, permission-denied, hover, and focus states SHALL remain stable where applicable

#### Scenario: 真实分页回归测试
- **WHEN** a Change modifies admin list data loading, API pagination parameters, or API pagination responses
- **THEN** backend tests, frontend API mocks, or integration tests SHALL verify page and page-size parameters are sent to the backend
- **AND** tests SHALL verify the UI uses backend total count rather than client-side array length from full-data slicing
- **AND** API contract changes SHALL update Pydantic Schema, OpenAPI, Orval generated types, API docs, and tests

#### Scenario: 横切交互不回退
- **WHEN** a Change modifies admin list state actions, dangerous actions, or action feedback
- **THEN** tests SHALL verify fixed toast feedback does not insert document-flow notices into the list layout
- **AND** tests SHALL verify dangerous actions use Design System confirm modal
- **AND** tests SHALL verify no new `window.confirm` usage is introduced in touched admin list code

