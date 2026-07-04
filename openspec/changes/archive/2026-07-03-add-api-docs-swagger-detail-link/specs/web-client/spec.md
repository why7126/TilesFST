## MODIFIED Requirements

### Requirement: 管理端接口文档 Swagger 入口

The Web admin API docs page SHALL open backend Swagger documentation through a same-origin Web route instead of sending users to the Web app homepage. The page SHALL also provide row-level Swagger detail links for OpenAPI routes that can be mapped to a concrete operationId, while keeping non-OpenAPI routes visible but unavailable for Swagger detail navigation.

#### Scenario: Swagger UI link uses same-origin docs path

- **WHEN** an admin views `/admin/api-docs` in a non-production environment
- **THEN** the Swagger action SHALL point to `/docs` or an equivalent same-origin Web route
- **AND** the frontend SHALL NOT hardcode a backend host or port such as `localhost:8000`.

#### Scenario: Production Swagger action remains read-only

- **WHEN** an admin views `/admin/api-docs` in a production environment
- **THEN** the Swagger action MAY be labeled as read-only
- **AND** the action SHALL still use a same-origin Web route
- **AND** the frontend SHALL NOT enable production Try It Out.

#### Scenario: Unknown Web route fallback is not used for Swagger

- **WHEN** an admin opens the Swagger action from `/admin/api-docs`
- **THEN** the user SHALL see FastAPI Swagger UI or an equivalent backend docs response
- **AND** the user SHALL NOT be redirected to `/` by the Web SPA fallback.

#### Scenario: OpenAPI route row links to operationId

- **WHEN** an authenticated `admin` user views a `/admin/api-docs` route row with `included_in_openapi=true` and a non-empty `operation_id`
- **THEN** the route row SHALL render an ACTION entry labeled `查看` or an equivalent short view action
- **AND** the action SHALL link to a same-origin Swagger UI deep link for that specific operationId, such as `/docs#/{tag}/{operationId}` after URL-safe encoding.
- **AND** the PATH cell MAY provide the same safe Swagger UI deep link as an additional row-level view affordance.

#### Scenario: Row-level Swagger link opens a new context safely

- **WHEN** an admin activates an enabled row-level Swagger view action
- **THEN** the action SHALL open in a new browser tab or window
- **AND** the current `/admin/api-docs` page SHALL remain on the same filter, pagination, scroll, and login context
- **AND** the link SHALL use `rel="noreferrer"` or an equivalent safe new-window attribute.

#### Scenario: Non-OpenAPI route row is disabled

- **WHEN** an admin views a route row with `included_in_openapi=false`
- **THEN** the route row SHALL remain visible in the API docs directory
- **AND** its row-level `查看` action SHALL be disabled or equivalently unavailable
- **AND** the disabled action SHALL NOT include a clickable href
- **AND** the PATH cell SHALL NOT include a clickable Swagger detail href
- **AND** the page SHALL communicate that the route is not included in OpenAPI or has no Swagger detail.

#### Scenario: Missing operationId row is disabled

- **WHEN** an admin views a route row with `included_in_openapi=true` but no usable `operation_id`
- **THEN** the row-level Swagger view action SHALL be disabled or equivalently unavailable
- **AND** it SHALL NOT navigate to the generic `/docs` page or an incorrect operationId.
- **AND** the PATH cell SHALL NOT navigate to the generic `/docs` page or an incorrect operationId.

#### Scenario: Row-level Swagger links do not leak authentication context

- **WHEN** row-level Swagger view actions are rendered
- **THEN** their href, hash, query, accessible label, and visible text SHALL NOT include Bearer tokens, Cookies, user identifiers, database URLs, MinIO credentials, or real environment variable values
- **AND** the Web client SHALL NOT add a new Swagger token auto-injection mechanism for this feature.

#### Scenario: API docs table layout remains consistent

- **WHEN** the ACTION column is added to `/admin/api-docs`
- **THEN** the table SHALL keep the existing admin table/list visual language and horizontal scrolling behavior
- **AND** the ACTION column SHALL remain fixed at the right edge of the horizontally scrollable table when route content overflows
- **AND** the pagination summary SHALL reflect the current filtered route count after keyword, method, tag, or auth filters change
- **AND** empty results SHALL keep the existing empty-state behavior without rendering misleading row-level actions
- **AND** TSX/CSS changes SHALL use semantic tokens or existing admin CSS variables without adding hard-coded design color hex values.
