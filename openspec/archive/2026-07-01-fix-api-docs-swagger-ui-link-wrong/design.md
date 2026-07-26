## Context

REQ-0022 added `/admin/api-docs` as an admin-only interface documentation page. The page exposes a Swagger UI entry, OpenAPI JSON entry, interface inventory, and Orval mapping. The Swagger entry currently uses same-origin `/docs`, which is correct for a Web-layer proxy design, but the Web dev server and Docker Web Nginx do not proxy `/docs`.

This change fixes the routing boundary rather than hardcoding a backend URL in frontend code. That keeps dev, Docker, and production deployment behavior consistent and preserves host port overrides.

## Bug Analysis

- **Symptom:** clicking **Swagger UI** on `/admin/api-docs` opens `http://localhost:3000/`.
- **Cause:** `/docs` resolves to the Web origin. Vite does not proxy `/docs`; Docker Nginx does not proxy `/docs`; SPA fallback handles the path and React redirects unknown routes to `/`.
- **Severity:** high, because the delivered API docs page exposes a broken primary action.
- **Affected capability:** REQ-0022 admin API docs page and Swagger policy.

## Decisions

### D1. Use Web-layer proxy Swagger

Implementation MUST keep the Web page using same-origin Swagger URLs and add proxy support in the Web layer.

The implementation MUST NOT hardcode `localhost:8000` or any backend host/port in React source. The backend target MUST continue to come from existing Vite proxy and Docker upstream configuration.

### D2. Proxy Swagger routes without weakening production policy

Implementation SHOULD cover at least:

- `/docs`
- `/docs/` and nested docs assets or redirects when served by FastAPI
- `/redoc`
- `/redoc/` when applicable
- `/openapi.json`

Existing `/api/` and `/media/` proxy rules MUST remain unchanged except for mechanical ordering needed to avoid route conflicts.

Production `Try It Out` MUST remain hidden or disabled according to the existing backend environment policy. The Web proxy only changes reachability; it MUST NOT change the backend Swagger UI parameters that control supported submit actions.

### D3. Keep SPA fallback behind explicit proxy paths

Docker Nginx MUST match Swagger/OpenAPI proxy routes before the SPA fallback. `/docs` MUST NOT be served by `index.html`.

### D4. Test the behavior at the page and proxy boundary

Implementation MUST include focused frontend tests for the Swagger link behavior. Docker/proxy behavior MAY be covered by an automated smoke or a documented manual command, but acceptance MUST record that `/docs` through the Web port returns Swagger HTML, not the SPA homepage.

## Risks

- **Proxy precedence regression:** a broad location block could accidentally capture `/admin/*`; mitigate with exact or scoped Swagger locations and route-order checks.
- **Production debugging regression:** proxying `/docs` may make production Swagger more reachable; mitigate by verifying Try It Out remains disabled.
- **OpenAPI JSON regression:** `/openapi.json` already has proxy behavior; keep it intact and verify it still returns JSON, not `index.html`.

## Implementation Notes

Likely files:

- `src/web/src/pages/admin/ApiDocsPage.tsx`
- `src/web/vite.config.ts`
- `src/web/nginx.conf`
- frontend tests for `ApiDocsPage`

No backend, database, MinIO, or Orval change is expected.
