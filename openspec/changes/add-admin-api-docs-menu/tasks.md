## 1. Backend and API Governance

- [x] 1.1 Decide whether `/api/v1/admin/api-docs` aggregation is required; document the decision in implementation notes or commit context.
- [x] 1.2 If required, add an admin-only backend route inventory endpoint guarded by admin authorization.
- [x] 1.3 Ensure route inventory includes `/api/v1/*`, `/health`, `/media/{object_key:path}`, and schema-excluded FastAPI app routes.
- [x] 1.4 Ensure route entries expose method, path, tag/module, summary, auth requirement, OpenAPI inclusion status, operation id, Orval method name, and source where available.
- [x] 1.5 Prevent secret, database DSN, object storage credential, or raw environment value exposure in all API docs payloads.

## 2. Web Admin UI

- [x] 2.1 Add "接口文档" to the SYSTEM sidebar group immediately below "系统设置" for admin users only.
- [x] 2.2 Register `/admin/api-docs` with existing admin route guard behavior and employee forbidden handling.
- [x] 2.3 Implement the API docs page using existing Admin Shell, semantic token classes, and admin table/filter patterns.
- [x] 2.4 Render summary metrics, filters, route table, OpenAPI/Swagger links or panel, and current environment debugging policy.
- [x] 2.5 Display Orval method names and an explicit "未生成" state with reasons.
- [x] 2.6 Implement production Swagger read-only behavior so `Try It Out` is hidden or disabled in production.

## 3. Documentation, OpenAPI, and Orval

- [x] 3.1 Update `docs/03-api-index.md` with `/admin/api-docs`, route inventory scope, OpenAPI/Swagger/Orval relationship, and production `Try It Out` policy.
- [x] 3.2 If a backend API is added or changed, export OpenAPI and update `src/web/openapi.json`.
- [x] 3.3 If OpenAPI changes, run `./scripts/generate-openapi-client.sh` and commit Orval generated output.
- [x] 3.4 Confirm no database migration or storage configuration change is required.

## 4. Tests

- [x] 4.1 Add backend pytest coverage for the aggregation endpoint if introduced: admin success, employee 403, `/health` and `/media/{object_key:path}` presence.
- [x] 4.2 Add frontend Vitest/Testing Library coverage for admin sidebar visibility, employee hidden/forbidden behavior, route filtering, Orval method display, and "未生成" state.
- [x] 4.3 Add or document production-equivalent verification that Swagger `Try It Out` is unavailable in production.
- [x] 4.4 Run API governance validation when backend API contracts change; document any unrelated existing failures.

## 5. Validation and Trace

- [x] 5.1 Run `openspec validate add-admin-api-docs-menu --strict`.
- [x] 5.2 Run directory structure validation.
- [x] 5.3 Update REQ-0022 acceptance/report trace after implementation.
- [x] 5.4 Confirm Sprint 004 docs reflect the change status before archive.
