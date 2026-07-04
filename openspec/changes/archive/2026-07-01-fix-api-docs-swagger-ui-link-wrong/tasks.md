## 1. Web Proxy Implementation

- [x] 1.1 Confirm `/admin/api-docs` Swagger action uses same-origin `/docs` or equivalent same-origin path without hardcoded backend host/port.
- [x] 1.2 Add Vite dev proxy support for Swagger routes including `/docs`, `/redoc`, and required nested paths.
- [x] 1.3 Add Docker Web Nginx proxy support for Swagger routes before SPA fallback.
- [x] 1.4 Preserve existing `/api/`, `/media/`, and `/openapi.json` proxy behavior.

## 2. Production Policy

- [x] 2.1 Verify the fix does not change backend Swagger `Try It Out` environment policy.
- [x] 2.2 Verify production or production-equivalent mode keeps Swagger read-only or disables Try It Out.

## 3. Regression Tests

- [x] 3.1 Add or update `ApiDocsPage` tests for non-production **Swagger UI** link target.
- [x] 3.2 Add or update `ApiDocsPage` tests for production **Swagger 只读** link target.
- [x] 3.3 Add proxy smoke verification for Web-port `/docs` and `/openapi.json` behavior, automated where practical or recorded in acceptance notes.

## 4. Validation

- [x] 4.1 Run focused frontend tests for `ApiDocsPage`.
- [x] 4.2 Run relevant Web build or typecheck if proxy/source changes require it.
- [x] 4.3 Run Docker Web smoke or equivalent Nginx config validation.
- [x] 4.4 Update BUG trace and sprint acceptance notes with verification results.

## 5. Knowledge Base

- [x] 5.1 Decide whether this incident should be captured under `docs/knowledge-base/incidents/`; if yes, add a short note after implementation.
