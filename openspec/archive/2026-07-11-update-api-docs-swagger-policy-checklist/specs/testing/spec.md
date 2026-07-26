## MODIFIED Requirements

### Requirement: Swagger 入口回归测试

The BUG-0051 fix and REQ-0023 enhancement SHALL include focused regression coverage for the admin API docs Swagger entry, row-level Swagger operation links, and Web proxy behavior. Future API docs refinements, Swagger entry changes, and Web proxy changes MUST include automated tests or documented smoke verification for the Swagger Web proxy and production `Try It Out` checklist.

#### Scenario: Swagger main entry uses same-origin path

- **WHEN** frontend tests render the admin API docs page in non-production and production configurations
- **THEN** they SHALL verify the non-production Swagger action uses the expected same-origin Swagger path
- **AND** they SHALL verify the production read-only Swagger action still uses the expected same-origin Swagger path.

#### Scenario: Row-level Swagger operation link is generated

- **WHEN** frontend tests render an API docs route with `included_in_openapi=true` and a non-empty `operation_id`
- **THEN** they SHALL verify the row-level `查看` action links to a same-origin Swagger UI operationId deep link such as `/docs#/{tag}/{operationId}`
- **AND** they SHALL verify the PATH cell link, if present, uses the same safe deep link.

#### Scenario: Unavailable Swagger operation links stay disabled

- **WHEN** frontend tests render a route with `included_in_openapi=false` or a missing `operation_id`
- **THEN** they SHALL verify the row-level Swagger action is disabled or equivalently unavailable
- **AND** they SHALL verify the disabled state has no clickable href to `/docs` or an incorrect operationId.
- **AND** they SHALL verify the PATH cell does not expose a clickable Swagger detail href for unavailable routes.

#### Scenario: Row-level Swagger link security tested

- **WHEN** frontend tests inspect row-level Swagger links
- **THEN** they SHALL verify the link does not contain bearer tokens, session data, database DSNs, MinIO credentials, JWT secrets, or real environment variable values.

#### Scenario: Existing API docs regression remains covered

- **WHEN** API docs frontend regressions are updated
- **THEN** existing admin permission, employee forbidden, OpenAPI JSON, Swagger read-only policy, Orval method name, missing method state, route filtering, pagination, and API docs summary metric assertions SHALL continue to pass.

#### Scenario: Web 代理 smoke 验证 docs 路由

- **WHEN** proxy smoke verification requests `/docs` through the Web port
- **THEN** `/docs` SHALL return backend Swagger HTML or an equivalent backend docs response
- **AND** it SHALL NOT return the Web app homepage or React Router fallback shell.

#### Scenario: OpenAPI JSON smoke 验证无 fallback

- **WHEN** proxy smoke verification requests `/openapi.json` through the Web port
- **THEN** the response SHALL include OpenAPI JSON fields such as `openapi`, `info`, and `paths`
- **AND** it SHALL NOT return the Web app homepage or static HTML shell.

#### Scenario: Swagger checklist verification is recorded

- **WHEN** a future change modifies API docs refine behavior, Swagger entry behavior, or Web proxy configuration
- **THEN** its tasks, trace, acceptance report, or test output MUST record verification for local Web proxy, Docker Web proxy, and production-equivalent `Try It Out` policy
- **AND** if an item cannot be automated, the record MUST name the manual smoke method and environment.

### Requirement: 生产 Swagger 调试禁用验证

The testing capability SHALL verify that production does not allow Swagger `Try It Out` from the admin API docs page. Future API docs and Swagger proxy changes MUST preserve this production read-only verification gate.

#### Scenario: Production disables Try It Out

- **WHEN** production or production-equivalent Swagger documentation is verified
- **THEN** automated or documented production-equivalent verification SHALL prove Swagger `Try It Out` is hidden or disabled.

#### Scenario: Non-production allows Try It Out

- **WHEN** non-production API docs behavior is verified
- **THEN** tests or documented verification SHALL prove the Swagger debugging policy is shown as allowed.

#### Scenario: Production read-only gate remains part of API docs checklist

- **WHEN** a future API docs refine, Swagger route, or Web proxy change is implemented
- **THEN** its acceptance or trace records MUST explicitly state that production `Try It Out` remains disabled, hidden, or read-only
- **AND** the records MUST NOT rely on frontend copy alone as the only enforcement mechanism.
