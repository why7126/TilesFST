## MODIFIED Requirements

### Requirement: Web 层 Swagger 代理

The Web deployment layer SHALL proxy Swagger and OpenAPI documentation routes to the backend so Web-origin documentation links work in local development and Docker deployments. Future changes touching Swagger documentation routes, Web proxy configuration, or production deployment documentation MUST explicitly record the dev, Docker, and production-equivalent proxy strategy for `/docs`, `/redoc`, `/openapi.json`, and Swagger UI resource paths.

#### Scenario: Vite 开发代理转发 Swagger 路由

- **WHEN** the Web development server receives a request for `/docs`, `/redoc`, or their required nested paths
- **THEN** it SHALL proxy the request to backend
- **AND** the response SHALL NOT be handled by the Web SPA fallback.

#### Scenario: Docker Nginx 在 SPA fallback 前转发 Swagger 路由

- **WHEN** the Docker Web container receives a request for `/docs`, `/redoc`, or their required nested paths
- **THEN** Nginx SHALL proxy the request to backend
- **AND** this proxy SHALL be evaluated before the SPA fallback route.

#### Scenario: Existing backend proxy routes remain intact

- **WHEN** the Swagger proxy configuration is added
- **THEN** `/api/`, `/media/`, and `/openapi.json` SHALL continue to proxy to backend as before
- **AND** existing upload size and media proxy behavior SHALL NOT regress.

#### Scenario: 生产 Try It Out 策略保持不变

- **WHEN** production or production-equivalent configuration serves Swagger through the Web proxy
- **THEN** backend Swagger Try It Out SHALL remain hidden or disabled according to the existing environment policy.

#### Scenario: API docs deployment checklist is recorded

- **WHEN** a future change modifies Web proxy configuration, Swagger documentation routes, or production deployment documentation
- **THEN** its design, acceptance, or trace records MUST list the Vite dev proxy, Docker Web Nginx, and production reverse proxy strategy for `/docs`, `/redoc`, `/openapi.json`, and Swagger UI resource paths
- **AND** the records MUST state whether Docker Compose or production-equivalent smoke verification was run
- **AND** if production verification is not applicable, the records MUST include a concrete N/A rationale.
