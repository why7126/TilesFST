## ADDED Requirements

### Requirement: 接口文档列表分页回归测试
The testing capability SHALL include focused frontend regression coverage for BUG-0053 on `/admin/api-docs`.

#### Scenario: Redundant title is covered
- **WHEN** frontend tests render `/admin/api-docs`
- **THEN** they SHALL assert the route directory list does not render the redundant `系统接口` title.

#### Scenario: Pagination DOM is covered
- **WHEN** frontend tests render enough API docs routes to paginate
- **THEN** they SHALL assert `page-summary`, `page-right`, page buttons, and page-size selector elements are present.

#### Scenario: Page size options are covered
- **WHEN** frontend tests inspect the page-size selector
- **THEN** they SHALL verify the 10, 20, 50, and 100 options
- **AND** they SHOULD verify the default page size is 20.

#### Scenario: Page switching is covered
- **WHEN** frontend tests switch route directory pages
- **THEN** they SHALL verify the table displays only the current page routes.

#### Scenario: Filtering resets page
- **WHEN** frontend tests change Method, Tag, Auth, or keyword filters after navigating away from page 1
- **THEN** they SHALL verify the current page returns to page 1.

#### Scenario: Existing API docs regression remains covered
- **WHEN** BUG-0053 frontend tests are updated
- **THEN** existing admin permission, employee forbidden, OpenAPI JSON, Swagger read-only policy, Orval method name, missing method state, and route filtering assertions SHALL continue to pass.
