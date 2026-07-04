## ADDED Requirements

### Requirement: Web 层 Swagger 代理
The Web deployment layer SHALL proxy Swagger and OpenAPI documentation routes to the backend so Web-origin documentation links work in local development and Docker deployments.

#### Scenario: Vite development proxy forwards Swagger routes
- **WHEN** the Web development server receives a request for `/docs`, `/redoc`, or their required nested paths
- **THEN** the request SHALL be proxied to the backend service
- **AND** the response SHALL NOT be the Web SPA `index.html`.

#### Scenario: Docker Nginx forwards Swagger routes before SPA fallback
- **WHEN** the Docker Web container receives a request for `/docs`, `/redoc`, or their required nested paths
- **THEN** Nginx SHALL proxy the request to backend
- **AND** the request SHALL be matched before the SPA fallback route.

#### Scenario: Existing proxies remain intact
- **WHEN** the Swagger proxy configuration is added
- **THEN** `/api/`, `/media/`, and `/openapi.json` SHALL continue to proxy to backend as before
- **AND** `/admin/api-docs` SHALL continue to be served by the Web SPA.

#### Scenario: Production Try It Out policy is preserved
- **WHEN** production or production-equivalent configuration serves Swagger through the Web proxy
- **THEN** backend Swagger Try It Out SHALL remain hidden or disabled according to the existing environment policy.
