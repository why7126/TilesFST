## ADDED Requirements

### Requirement: Swagger 入口回归测试
The BUG-0051 fix SHALL include focused regression coverage for the admin API docs Swagger entry and Web proxy behavior.

#### Scenario: Frontend link behavior tested
- **WHEN** frontend tests run for `ApiDocsPage`
- **THEN** they SHALL verify the non-production Swagger action uses the expected same-origin Swagger path
- **AND** they SHALL verify the production read-only Swagger action still uses the expected same-origin Swagger path.

#### Scenario: Web proxy smoke verifies docs route
- **WHEN** proxy smoke verification is performed for the Web port
- **THEN** `/docs` SHALL return backend Swagger HTML or an equivalent backend docs response
- **AND** it SHALL NOT return the Web SPA homepage.

#### Scenario: OpenAPI JSON smoke verifies no fallback
- **WHEN** proxy smoke verification requests `/openapi.json` through the Web port
- **THEN** the response SHALL include OpenAPI JSON fields such as `openapi`, `info`, and `paths`
- **AND** it SHALL NOT return Web SPA HTML.
