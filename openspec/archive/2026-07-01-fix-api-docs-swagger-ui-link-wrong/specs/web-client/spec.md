## ADDED Requirements

### Requirement: 管理端接口文档 Swagger 入口
The Web admin API docs page SHALL open backend Swagger documentation through a same-origin Web route instead of sending users to the Web app homepage.

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
