## ADDED Requirements

### Requirement: 管理端 API 文档聚合
The API governance capability SHALL support an admin-only route inventory source for the `/admin/api-docs` page when OpenAPI alone cannot represent all system routes.

#### Scenario: Admin aggregation endpoint
- **WHEN** the implementation adds a route inventory endpoint
- **THEN** the endpoint SHALL be under `/api/v1/admin`
- **AND** it SHALL require admin-only authorization.

#### Scenario: Employee forbidden for aggregation endpoint
- **WHEN** an authenticated `employee` calls the route inventory endpoint
- **THEN** the API SHALL return 403 using the unified error response structure.

#### Scenario: Route metadata schema
- **WHEN** the route inventory endpoint returns route entries
- **THEN** each entry SHALL include method, path, tag or module, summary or description, auth requirement, OpenAPI inclusion status, operation id, Orval method name, and source when known.

### Requirement: 非 /api/v1 路由文档化
The API documentation governance SHALL include non-`/api/v1` system routes in the admin-facing route inventory.

#### Scenario: Health route documented
- **WHEN** route inventory is generated
- **THEN** `GET /health` SHALL be present and marked as a health-check route.

#### Scenario: Media passthrough route documented
- **WHEN** route inventory is generated
- **THEN** `/media/{object_key:path}` SHALL be present and marked as a media passthrough route.

#### Scenario: OpenAPI inclusion is explicit
- **WHEN** a route is not included in the OpenAPI schema
- **THEN** the route inventory SHALL mark `included_in_openapi=false` or an equivalent state.

### Requirement: Orval 方法名治理
The API governance capability SHALL keep admin-displayed Orval method names aligned with the generated Web client.

#### Scenario: Generated client is source of truth
- **WHEN** API changes affect generated frontend methods
- **THEN** the implementation SHALL run the Orval generation script and commit updated generated output.

#### Scenario: Method mapping visible
- **WHEN** a route has an Orval generated method
- **THEN** route inventory or the Web client SHALL expose that method name for display on `/admin/api-docs`.

#### Scenario: Missing mapping is explicit
- **WHEN** a route has no generated Orval method
- **THEN** route inventory or the Web client SHALL expose an explicit missing state instead of an empty or misleading method value.

### Requirement: 管理端接口文档索引同步
The long-term API index SHALL document the admin API docs page and production Swagger debugging policy.

#### Scenario: API index updated
- **WHEN** the `/admin/api-docs` capability is implemented
- **THEN** `docs/03-api-index.md` SHALL mention the admin API docs page, route inventory scope, OpenAPI/Swagger/Orval relationship, and production `Try It Out` policy.
