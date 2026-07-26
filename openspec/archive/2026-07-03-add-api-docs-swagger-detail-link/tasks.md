---
created_at: 2026-07-02 09:26:53
updated_at: 2026-07-02 10:34:20
---

## 1. Preconditions and Design Verification

- [x] 1.1 Confirm `/admin/api-docs` route inventory exposes `included_in_openapi`, `operation_id`, and a usable tag for OpenAPI routes.
- [x] 1.2 Verify the current FastAPI Swagger UI deepLinking hash format for `/docs#/{tag}/{operationId}` or record the validated equivalent in the implementation notes.
- [x] 1.3 Confirm no backend API field is required; if a `swagger_url` or equivalent field becomes necessary, update OpenAPI, Orval, `docs/03-api-index.md`, and backend tests.

## 2. Web Admin Implementation

- [x] 2.1 Add an ACTION column to `/admin/api-docs` route table without replacing the existing table, filters, metrics, or pagination structure.
- [x] 2.2 Generate row-level Swagger detail links only when `included_in_openapi=true`, `operation_id` is present, and a usable tag is available.
- [x] 2.3 Render enabled row-level `查看` links as same-origin Swagger UI operationId deep links that open in a new tab/window with `rel="noreferrer"`.
- [x] 2.4 Render `included_in_openapi=false`, missing `operation_id`, or missing tag rows with disabled `查看` state and no clickable href.
- [x] 2.5 Preserve current `/admin/api-docs` filter, pagination, scroll, and login context when an enabled row-level link is activated.
- [x] 2.6 Ensure added TSX/CSS uses semantic tokens or existing admin CSS variables, with no new hard-coded design color hex values.

## 3. Tests

- [x] 3.1 Add or update `ApiDocsPage` tests for OpenAPI route operationId deep links, including URL-safe tag/operationId encoding.
- [x] 3.2 Add or update tests for non-OpenAPI and missing-operationId disabled states with no clickable href.
- [x] 3.3 Add or update tests for new-window safety attributes and absence of token/Cookie/user/secret data in row-level links.
- [x] 3.4 Re-run existing `ApiDocsPage` regression tests for permissions, OpenAPI JSON, Swagger read-only policy, Orval method names, missing method state, filtering, pagination, and summary metrics.

## 4. Documentation and Validation

- [x] 4.1 If implementation has no API contract change, document that no OpenAPI, Orval, database, MinIO, or Docker Compose changes are required.
- [x] 4.2 If implementation changes API contract, run OpenAPI/Orval generation and update API documentation.
- [x] 4.3 Run `openspec validate add-api-docs-swagger-detail-link --strict`.
- [x] 4.4 Update REQ-0023 acceptance trace with implemented link format and validation results before archive.
