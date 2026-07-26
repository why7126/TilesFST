## MODIFIED Requirements

### Requirement: 管理端接口文档 Swagger 入口

The Web admin API docs page SHALL open backend Swagger documentation through a same-origin Web route instead of sending users to the Web app homepage. The page SHALL also provide row-level Swagger detail links for OpenAPI routes that can be mapped to a concrete operationId, while keeping non-OpenAPI routes visible but unavailable for Swagger detail navigation. Future changes touching this page, its Swagger entry, or its proxy assumptions MUST document and verify the Swagger Web proxy and production `Try It Out` checklist.

#### Scenario: Swagger UI link uses same-origin docs path

- **WHEN** an authenticated `admin` user opens `/admin/api-docs`
- **THEN** the Swagger action SHALL point to `/docs` or an equivalent same-origin Web route
- **AND** the action SHALL NOT hardcode the backend host, container service name, or port.

#### Scenario: 生产 Swagger 操作保持只读

- **WHEN** the Web client is configured for production
- **THEN** the Swagger action MAY be labeled as read-only
- **AND** it SHALL still use the same-origin Web docs route
- **AND** the frontend SHALL NOT enable production Try It Out.

#### Scenario: 未知 Web 路由 fallback 不用于 Swagger

- **WHEN** an admin opens the Swagger action from `/admin/api-docs`
- **THEN** the user SHALL see FastAPI Swagger UI or an equivalent backend docs response
- **AND** the Web SPA fallback SHALL NOT serve the Web homepage for that docs route.

#### Scenario: 行级 Swagger operationId 深链

- **WHEN** an authenticated `admin` user views a `/admin/api-docs` route row with `included_in_openapi=true` and a non-empty `operation_id`
- **THEN** the row-level Swagger view action SHALL be enabled
- **AND** the action SHALL link to a same-origin Swagger UI deep link for that specific operationId, such as `/docs#/{tag}/{operationId}` after URL-safe encoding.
- **AND** the PATH cell MAY provide the same safe Swagger UI deep link as an additional row-level view affordance.

#### Scenario: 行级 Swagger 链接安全打开新上下文

- **WHEN** an admin activates an enabled row-level Swagger view action
- **THEN** the link SHALL open in a safe new browsing context or an equivalently safe navigation mode
- **AND** it SHALL use attributes such as `rel="noreferrer"` when opening a new tab.

#### Scenario: 非 OpenAPI 路由不可跳转

- **WHEN** an admin views a route row with `included_in_openapi=false`
- **THEN** the row-level Swagger view action SHALL be disabled or equivalently unavailable
- **AND** it SHALL NOT navigate to `/docs` or an incorrect operationId
- **AND** the PATH cell SHALL NOT include a clickable Swagger detail href
- **AND** the page SHALL communicate that the route is not included in OpenAPI or has no Swagger detail.

#### Scenario: 缺少 operationId 的 OpenAPI 路由不可跳转

- **WHEN** an admin views a route row with `included_in_openapi=true` but no usable `operation_id`
- **THEN** the row-level Swagger view action SHALL be disabled or equivalently unavailable
- **AND** it SHALL NOT navigate to the generic `/docs` page or an incorrect operationId.
- **AND** the PATH cell SHALL NOT navigate to the generic `/docs` page or an incorrect operationId.

#### Scenario: 行级 Swagger 链接不泄露认证上下文

- **WHEN** row-level Swagger view actions are rendered
- **THEN** the generated URL SHALL NOT include bearer tokens, session data, database DSNs, MinIO credentials, JWT secrets, or real environment variable values in the path, query string, hash fragment, or persisted browser storage
- **AND** the Web client SHALL NOT add a new Swagger token auto-injection mechanism for this feature.

#### Scenario: API docs refine records Swagger proxy checklist

- **WHEN** a future Web client change modifies `/admin/api-docs`, Swagger actions, row-level Swagger links, or docs route proxy assumptions
- **THEN** its design, acceptance, or trace records MUST include the Swagger Web proxy and production `Try It Out` checklist
- **AND** the checklist MUST state whether `docs/03-api-index.md` and `docs/standards/api-governance.md` need updates
- **AND** if either document is not updated, the trace MUST record the reason.
