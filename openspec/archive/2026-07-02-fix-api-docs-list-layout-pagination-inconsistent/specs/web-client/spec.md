## ADDED Requirements

### Requirement: 管理端接口文档列表标题与分页一致性
The Web admin client SHALL fix `/admin/api-docs` route directory list layout so the list removes the redundant `系统接口` section title and uses the existing admin list pagination interaction and DOM baseline.

#### Scenario: Redundant list title is removed
- **WHEN** an authenticated `admin` user opens `/admin/api-docs`
- **THEN** the route directory list area SHALL NOT render the redundant `系统接口` title
- **AND** the implementation SHALL NOT keep the title by renaming it
- **AND** the implementation SHALL NOT treat `系统接口` as a real API route data row to filter out.

#### Scenario: Route directory paginates filtered results
- **WHEN** the route directory has more routes than the selected page size
- **THEN** the table SHALL render only the routes for the current page
- **AND** the pagination total SHALL be calculated from the currently filtered route count.

#### Scenario: Pagination controls match admin list baseline
- **WHEN** an admin views the route directory pagination
- **THEN** the pagination SHALL include previous-page, current-page, and next-page controls
- **AND** the pagination DOM SHALL use the existing admin list structure with `page-summary` on the left and `page-right` on the right
- **AND** page buttons SHALL use the existing `page-buttons`, `page-btn`, and `active` class pattern.

#### Scenario: Page size selector matches tile SKU page
- **WHEN** an admin changes the route directory page size
- **THEN** the selector SHALL offer 10, 20, 50, and 100 rows per page
- **AND** the default page size SHOULD be 20
- **AND** the selector SHALL use the existing `page-size-wrap` and `page-size` class pattern.

#### Scenario: Filtering resets pagination
- **WHEN** an admin changes Method, Tag, Auth, or keyword filters
- **THEN** the route directory SHALL reset the current page to page 1
- **AND** the page count SHALL be recalculated from the filtered results.

#### Scenario: Empty and single-page states remain valid
- **WHEN** route filters match no routes
- **THEN** the page SHALL show an explicit empty state
- **AND** pagination SHALL NOT show invalid page numbers
- **AND** previous-page and next-page actions SHALL be disabled or equivalently unavailable.

#### Scenario: API docs behavior does not regress
- **WHEN** the list pagination fix is implemented
- **THEN** `/admin/api-docs` SHALL still show route metadata, OpenAPI inclusion status, Orval method status, and missing-method reasons
- **AND** OpenAPI JSON access, Swagger UI/read-only policy, route filtering, and admin-only access SHALL continue to work
- **AND** shop-owner Web and WeChat miniapp clients SHALL NOT expose an API docs entry.

#### Scenario: No backend contract change
- **WHEN** implementing the list pagination fix
- **THEN** the Web client SHALL NOT require backend API request, response, or error-code changes
- **AND** it SHALL NOT require database schema changes, MinIO changes, Orval generation, or Docker Compose changes.
