## MODIFIED Requirements

### Requirement: Swagger 入口回归测试

The BUG-0051 fix and REQ-0023 enhancement SHALL include focused regression coverage for the admin API docs Swagger entry, row-level Swagger operation links, and Web proxy behavior.

#### Scenario: Frontend link behavior tested

- **WHEN** frontend tests run for `ApiDocsPage`
- **THEN** they SHALL verify the non-production Swagger action uses the expected same-origin Swagger path
- **AND** they SHALL verify the production read-only Swagger action still uses the expected same-origin Swagger path.

#### Scenario: Row-level operationId link tested

- **WHEN** frontend tests render an API docs route with `included_in_openapi=true` and a non-empty `operation_id`
- **THEN** they SHALL verify the row-level `查看` action links to a same-origin Swagger UI operationId deep link such as `/docs#/{tag}/{operationId}`
- **AND** they SHALL verify the PATH cell can use the same deep link when it is available
- **AND** they SHALL verify tag and operationId values are URL-safe encoded where needed.

#### Scenario: Row-level disabled state tested

- **WHEN** frontend tests render a route with `included_in_openapi=false` or a missing `operation_id`
- **THEN** they SHALL verify the row-level `查看` action is disabled or equivalently unavailable
- **AND** they SHALL verify the disabled state has no clickable href to `/docs` or an incorrect operationId.
- **AND** they SHALL verify the PATH cell does not expose a clickable Swagger detail href for unavailable routes.

#### Scenario: Row-level Swagger link security tested

- **WHEN** frontend tests inspect row-level Swagger links
- **THEN** they SHALL verify enabled links open in a new tab or window with a safe rel attribute such as `noreferrer`
- **AND** they SHALL verify the href and rendered text do not contain token, Bearer, Cookie, user, password, database, MinIO, or environment-secret content.

#### Scenario: Existing API docs regression remains covered

- **WHEN** frontend tests are updated for REQ-0023
- **THEN** existing admin permission, employee forbidden, OpenAPI JSON, Swagger read-only policy, Orval method name, missing method state, route filtering, pagination, and API docs summary metric assertions SHALL continue to pass.
- **AND** they SHALL verify the pagination summary count updates to the filtered route count after filters change.

#### Scenario: Sticky action column tested

- **WHEN** frontend tests render the API docs table
- **THEN** they SHALL verify the ACTION header and row action cells expose the sticky action-column class or equivalent stable selector.

#### Scenario: Web proxy smoke verifies docs route

- **WHEN** proxy smoke verification is performed for the Web port
- **THEN** `/docs` SHALL return backend Swagger HTML or an equivalent backend docs response
- **AND** it SHALL NOT return the Web SPA homepage.

#### Scenario: OpenAPI JSON smoke verifies no fallback

- **WHEN** proxy smoke verification requests `/openapi.json` through the Web port
- **THEN** the response SHALL include OpenAPI JSON fields such as `openapi`, `info`, and `paths`
- **AND** it SHALL NOT return Web SPA HTML.
