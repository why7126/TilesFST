## ADDED Requirements

### Requirement: 管理端接口文档后端测试
The testing capability SHALL include backend tests for any admin API docs aggregation endpoint introduced by this change.

#### Scenario: Admin can fetch route inventory
- **WHEN** the change introduces a backend route inventory endpoint
- **THEN** pytest SHALL verify an authenticated `admin` can fetch the inventory successfully.

#### Scenario: Employee cannot fetch route inventory
- **WHEN** the change introduces a backend route inventory endpoint
- **THEN** pytest SHALL verify an authenticated `employee` receives 403.

#### Scenario: Non-api routes are included
- **WHEN** the change introduces a backend route inventory endpoint
- **THEN** pytest SHALL verify `/health` and `/media/{object_key:path}` are represented in the inventory.

### Requirement: 管理端接口文档前端测试
The testing capability SHALL include frontend tests for `/admin/api-docs` navigation, permissions, filtering, and Orval display.

#### Scenario: Admin navigation visible
- **WHEN** frontend tests render admin navigation for an `admin` user
- **THEN** they SHALL assert the "接口文档" menu item is visible below "系统设置".

#### Scenario: Employee navigation hidden
- **WHEN** frontend tests render admin navigation for an `employee` user
- **THEN** they SHALL assert the "接口文档" menu item is not visible.

#### Scenario: Route page behavior
- **WHEN** frontend tests render the API docs page
- **THEN** they SHALL cover filtering and Orval method-name display, including the "未生成" state.

### Requirement: 生产 Swagger 调试禁用验证
The testing capability SHALL verify that production does not allow Swagger `Try It Out` from the admin API docs page.

#### Scenario: Production disables Try It Out
- **WHEN** the app is configured as production
- **THEN** automated or documented production-equivalent verification SHALL prove Swagger `Try It Out` is hidden or disabled.

#### Scenario: Non-production allows Try It Out
- **WHEN** the app is configured as local, development, or demo
- **THEN** tests or documented verification SHALL prove the Swagger debugging policy is shown as allowed.

### Requirement: Orval and OpenAPI regression
The testing capability SHALL include OpenAPI/Orval regression checks when the change adds or changes backend API contracts.

#### Scenario: Orval generated output updated
- **WHEN** a backend aggregation endpoint or API contract changes
- **THEN** the OpenAPI export and Orval generated client SHALL be regenerated and reviewed.

#### Scenario: API governance validation
- **WHEN** a backend endpoint is added for admin API docs
- **THEN** API governance validation SHALL pass or known unrelated failures SHALL be documented.
