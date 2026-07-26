## Why

BUG-0051 reports that the admin API docs page right-side **Swagger UI** action opens the Web app homepage at `localhost:3000/` instead of FastAPI Swagger UI. The defect blocks a core entry point delivered by REQ-0022 and forces administrators to know the backend port manually.

Root cause analysis shows the page links to same-origin `/docs`, while the Web layer does not proxy Swagger routes. In Docker, `/docs` falls through to the SPA fallback and the React wildcard route redirects to `/`.

## What Changes

- Add Web-layer Swagger proxy support for local Vite dev and Docker Web Nginx.
- Keep `/admin/api-docs` Swagger actions same-origin and avoid hardcoded backend host/port values in frontend code.
- Preserve existing `/api/`, `/media/`, and `/openapi.json` proxy behavior.
- Preserve production Swagger read-only policy; the fix MUST NOT enable production Try It Out.
- Add focused frontend/proxy regression tests or documented verification for local dev and Docker routes.

## Impact

- **Web admin:** fixes `/admin/api-docs` Swagger UI entry behavior.
- **Deployment:** changes Web proxy configuration in dev and Docker.
- **API:** no business API contract change is planned.
- **Database:** no database change.
- **Orval:** not required unless implementation unexpectedly changes OpenAPI-facing API contracts.
- **Related BUG:** `issues/bugs/archive/BUG-0051-api-docs-swagger-ui-link-wrong/`
- **Related Sprint:** `iterations/change/sprint-004/`

## Rollback Plan

Revert the Web proxy route additions and any focused tests added by this change. Rollback restores the previous behavior where administrators must manually open the backend Swagger URL. No database or data rollback is required.
