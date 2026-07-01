## ADDED Requirements

### Requirement: 管理端接口文档路由
The Web admin client SHALL register `/admin/api-docs` as an admin-only route that renders inside the existing Admin Shell.

#### Scenario: Admin route renders
- **WHEN** an authenticated `admin` user navigates to `/admin/api-docs`
- **THEN** the Web client SHALL render the API docs page
- **AND** the page SHALL use the existing Admin Shell layout.

#### Scenario: Forbidden direct navigation
- **WHEN** an authenticated `employee` user navigates directly to `/admin/api-docs`
- **THEN** the Web client SHALL render a 403 page or equivalent forbidden state.

### Requirement: 管理端 Sidebar 接口文档菜单
The Web admin client SHALL add an "接口文档" item to the SYSTEM sidebar group immediately below "系统设置".

#### Scenario: Admin sees API docs menu
- **WHEN** an authenticated `admin` user views the sidebar
- **THEN** the SYSTEM group SHALL include "接口文档" immediately below "系统设置".

#### Scenario: Employee menu hidden
- **WHEN** an authenticated `employee` user views the sidebar
- **THEN** the SYSTEM group SHALL NOT include "接口文档".

#### Scenario: Collapsed sidebar remains accessible
- **WHEN** the sidebar is collapsed
- **THEN** the API docs menu item SHALL retain an accessible name or tooltip for "接口文档".

### Requirement: 管理端接口文档页面 UI
The Web admin client SHALL render the API docs page according to the REQ-0022 prototype and Design System constraints.

#### Scenario: Prototype-led layout
- **WHEN** an admin opens `/admin/api-docs`
- **THEN** the page SHALL include a page hero, environment policy, summary metrics, filters, route table, and Swagger panel or link.

#### Scenario: Semantic token styling
- **WHEN** implementing the API docs page
- **THEN** new TSX/CSS SHALL use semantic token classes rather than hard-coded design color hex values.

#### Scenario: Admin list consistency
- **WHEN** the route table includes pagination
- **THEN** pagination DOM SHALL align with the `/admin/users` baseline using left `page-summary` and right `page-right` controls.

#### Scenario: Layout-stable feedback
- **WHEN** the API docs page shows loading, refresh, or error feedback
- **THEN** the feedback SHALL NOT insert a document-flow notice between hero and table that causes vertical layout shift.

#### Scenario: No native dialogs
- **WHEN** the API docs page needs a confirmation interaction
- **THEN** it SHALL use the Design System modal pattern
- **AND** it SHALL NOT use `window.confirm` or `window.alert`.
