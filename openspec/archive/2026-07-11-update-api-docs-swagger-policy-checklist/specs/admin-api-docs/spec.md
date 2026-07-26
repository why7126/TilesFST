## MODIFIED Requirements

### Requirement: Swagger 在线调试策略

The system SHALL provide Swagger access while preventing production `Try It Out` usage. Future API docs refinements, admin API docs template changes, Swagger entry changes, Web proxy changes, or production deployment documentation changes MUST include a Swagger Web proxy and production `Try It Out` policy checklist in design, acceptance, or trace records.

#### Scenario: Non-production allows Swagger debugging

- **WHEN** the API docs page is rendered in a non-production environment
- **THEN** the API docs page SHALL provide Swagger access with online debugging enabled.

#### Scenario: Production disables Swagger Try It Out

- **WHEN** the API docs page is rendered in production or a production-equivalent environment
- **THEN** Swagger documentation MAY remain visible
- **AND** Swagger `Try It Out` SHALL be hidden or disabled.

#### Scenario: API docs refine includes Swagger proxy checklist

- **WHEN** a future change refines the admin API docs page, API docs template, Swagger entry, Web proxy, or production deployment documentation
- **THEN** its design, acceptance, or trace records MUST include a checklist covering same-origin `/docs`, `/redoc`, `/openapi.json`, Swagger UI resource routing, Vite dev proxy, Docker Web Nginx, and production reverse proxy or production-equivalent N/A rationale
- **AND** the checklist MUST state that production `Try It Out` remains disabled, hidden, or read-only
- **AND** the checklist MUST forbid hardcoded backend hosts, container service names, ports, tokens, DSNs, MinIO credentials, JWT secrets, or real environment variable values in Swagger links, URL fragments, query strings, new localStorage keys, page copy, and verification records.
