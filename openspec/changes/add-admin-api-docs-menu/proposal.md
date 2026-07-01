## Why

Backend API documentation, Swagger UI, OpenAPI JSON, and Orval-generated frontend method names are currently scattered across developer-facing locations. Admin users need a single in-admin view to inspect all system routes, including non-`/api/v1` routes such as health checks and media passthrough, while production deployments must keep Swagger debugging view-only.

## What Changes

- Add an admin-only `/admin/api-docs` page under the SYSTEM sidebar group, immediately below "系统设置".
- Show a searchable/filterable route directory that includes `/api/v1/*`, `/health`, `/media/{object_key:path}`, and other FastAPI app routes.
- Show OpenAPI inclusion status and Orval generated method names, with a clear "未生成" state for schema-excluded routes.
- Provide a Swagger UI entry or embedded panel that allows `Try It Out` in local/development/demo environments and hides or disables it in production.
- Add or extend an admin-only backend aggregation endpoint if runtime route inventory, non-schema route metadata, or Orval method mapping cannot be derived safely on the client alone.
- Update API documentation and tests for the admin API docs page, route inventory, Orval mapping, and production Swagger policy.

## Capabilities

### New Capabilities

- `admin-api-docs`: Admin-facing API documentation page, route inventory, Swagger policy, and Orval method mapping.

### Modified Capabilities

- `web-client`: Adds an admin route, sidebar item, role guard behavior, and admin UI acceptance for `/admin/api-docs`.
- `api-governance`: Extends API documentation governance to cover in-admin route inventory, non-`/api/v1` routes, OpenAPI inclusion status, and Orval method names.
- `testing`: Adds required backend/frontend regression coverage for the admin API docs page and production Swagger `Try It Out` policy.

## Impact

- Backend: possible new `GET /api/v1/admin/api-docs` aggregation endpoint guarded by admin-only authorization; no database schema change.
- Web admin: new `/admin/api-docs` route, sidebar navigation item, route guard, table/filter UI, Swagger/OpenAPI links or panel.
- API/OpenAPI/Orval: may require OpenAPI export and Orval regeneration if a backend aggregation endpoint is introduced or route metadata changes.
- Documentation: `docs/03-api-index.md` must describe the admin API docs entry and production Swagger policy when implemented.
- Testing: backend pytest and frontend Vitest/Testing Library coverage are required; Docker or production-equivalent verification is required for production `Try It Out` disabled behavior.
