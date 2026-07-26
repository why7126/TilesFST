## ADDED Requirements

### Requirement: 管理端接口文档入口
The system SHALL provide an admin-only API documentation page at `/admin/api-docs` inside the Web admin application.

#### Scenario: Admin can open API docs page
- **WHEN** an authenticated `admin` user opens `/admin/api-docs`
- **THEN** the system SHALL render the API documentation page inside the existing Admin Shell
- **AND** the SYSTEM sidebar SHALL show "接口文档" immediately below "系统设置"
- **AND** the "接口文档" item SHALL be active for the route.

#### Scenario: Employee cannot access API docs page
- **WHEN** an authenticated `employee` user opens `/admin/api-docs`
- **THEN** the system SHALL deny access with a 403 page or equivalent forbidden state
- **AND** the sidebar SHALL NOT show the "接口文档" menu item.

### Requirement: 系统全量接口目录
The system SHALL show an API route directory that covers all system routes, including routes that are not under `/api/v1`.

#### Scenario: Route inventory includes API v1 routes
- **WHEN** an admin views `/admin/api-docs`
- **THEN** the route directory SHALL include all business API routes under `/api/v1/*`.

#### Scenario: Route inventory includes health route
- **WHEN** an admin views `/admin/api-docs`
- **THEN** the route directory SHALL include `GET /health`
- **AND** it SHALL be marked as a route without the `/api/v1` prefix.

#### Scenario: Route inventory includes media passthrough route
- **WHEN** an admin views `/admin/api-docs`
- **THEN** the route directory SHALL include `/media/{object_key:path}`
- **AND** it SHALL show whether the route is included in the OpenAPI schema.

#### Scenario: Schema-excluded routes are visible
- **WHEN** a FastAPI app route is not included in `/openapi.json`
- **THEN** the route directory SHALL still show the route when it is part of the system route inventory
- **AND** it SHALL mark the route as not included in OpenAPI.

### Requirement: 接口条目信息
The system SHALL display operational metadata for each route in the API docs directory.

#### Scenario: Route row fields are visible
- **WHEN** an admin views a route row
- **THEN** the row SHALL show HTTP method, path, tag or module, summary or description, authentication requirement, OpenAPI inclusion status, and Orval method status.

#### Scenario: Sensitive values are not shown
- **WHEN** an admin views the API docs page
- **THEN** the page SHALL NOT display secret keys, database connection strings, MinIO access keys, MinIO secret keys, or real environment variable values.

### Requirement: Orval 方法名映射
The system SHALL show Orval generated method names for OpenAPI routes that are generated into the Web client.

#### Scenario: Generated method name is shown
- **WHEN** a route is included in OpenAPI and Orval generates a frontend method for it
- **THEN** the API docs page SHALL show the generated method name.

#### Scenario: Missing method name is explained
- **WHEN** a route has no Orval generated method
- **THEN** the API docs page SHALL show "未生成" or an equivalent state
- **AND** it SHALL explain likely reasons such as schema exclusion or stale OpenAPI/Orval output.

#### Scenario: Search matches Orval method name
- **WHEN** an admin searches by an Orval method name
- **THEN** the route directory SHALL filter to matching routes.

### Requirement: Swagger 在线调试策略
The system SHALL provide Swagger access while preventing production `Try It Out` usage.

#### Scenario: Non-production allows Swagger debugging
- **WHEN** the app runs in a local, development, or demo environment
- **THEN** the API docs page SHALL provide Swagger access with online debugging enabled.

#### Scenario: Production keeps docs view-only
- **WHEN** the app runs in production
- **THEN** the API docs page SHALL still be visible to admin users
- **AND** Swagger `Try It Out` SHALL be hidden or disabled.

#### Scenario: Environment policy is visible
- **WHEN** an admin views the API docs page
- **THEN** the page SHALL show whether the current environment allows online debugging or is view-only.

### Requirement: 接口目录筛选
The system SHALL support filtering the API route directory.

#### Scenario: Keyword filter
- **WHEN** an admin enters a keyword
- **THEN** the route directory SHALL match path, summary, tag, and Orval method name.

#### Scenario: Method and auth filters
- **WHEN** an admin filters by HTTP method or authentication requirement
- **THEN** the route directory SHALL only show matching routes.

#### Scenario: Empty result
- **WHEN** filters match no routes
- **THEN** the page SHALL show an explicit empty state with a way to clear filters.
