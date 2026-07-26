## 1. Backend Data Model

- [x] 1.1 Design and add SQLite/MySQL-compatible schema or migration for `request_logs` and `usage_events`.
- [x] 1.2 Add indexes for `created_at`, `log_type`, `actor_user_id`, `request_id`, `status_code`, `path`, and frequent composite filters.
- [x] 1.3 Update database docs and data-management notes for log retention, no real runtime log data in Git, and cleanup strategy.
- [x] 1.4 Add repository/query layer with parameterized SQL and newest-first pagination.

## 2. Backend Logging and Events

- [x] 2.1 Add request-id generation/propagation and request logging middleware or equivalent lifecycle hook.
- [x] 2.2 Exclude health, static, Swagger/OpenAPI, and media passthrough routes by default.
- [x] 2.3 Add sanitization utilities for headers, bodies, metadata, IP summary, user-agent summary, masking, and truncation.
- [x] 2.4 Add event dictionary enums/schema validators based on `tracking-events.md`.
- [x] 2.5 Implement event enrichment from trusted server context and ignore untrusted frontend identity fields.
- [x] 2.6 Ensure usage tracking failures do not block the primary business workflow.

## 3. Backend API

- [x] 3.1 Add `GET /api/v1/admin/logs` with admin-only guard, filters, pagination, and metric summary.
- [x] 3.2 Add `GET /api/v1/admin/logs/{id}` with admin-only guard and drawer-oriented detail response.
- [x] 3.3 Add `POST /api/v1/usage-events` with event validation and controlled anonymous boundary.
- [x] 3.4 Register new error code constants/docs if a dedicated log-not-found or event-validation code is introduced.
- [x] 3.5 Add FastAPI response models, summaries, descriptions, and tags for OpenAPI.

## 4. Web Admin UI

- [x] 4.1 Add SYSTEM sidebar item `日志审计` and protected route `/admin/logs` for admin users only.
- [x] 4.2 Build list page using existing Admin Shell/list patterns, shadcn components, and semantic token classes.
- [x] 4.3 Add metric cards, filters, query/reset actions, empty/loading/error states, and newest-first table.
- [x] 4.4 Add request_id copy action with fixed toast or equivalent non-layout-shifting feedback.
- [x] 4.5 Add right-side detail drawer with sections matching the product v2 prototype.
- [x] 4.6 Preserve filter/pagination state when opening and closing the drawer.
- [ ] 4.7 Complete 1440x1024 side-by-side Golden comparison against `prototype/web/log-audit-list.png` and `prototype/web/log-audit-detail-drawer.png`.

## 5. Generated Client and Docs

- [x] 5.1 Run `./scripts/generate-openapi-client.sh` after backend API changes.
- [x] 5.2 Update `docs/03-api-index.md` with log API group, routes, permissions, filters, and errors.
- [x] 5.3 Update `docs/04-database-design.md` with log tables, indexes, retention, and SQLite/MySQL notes.
- [x] 5.4 Update `.env.example` only if implementation adds environment-level log configuration.
- [x] 5.5 Update REQ/OpenSpec trace artifacts with implementation and validation results.

## 6. Tests and Validation

- [x] 6.1 Add backend tests for request logging success/error paths, route exclusions, masking, retention query shape, and repository filters.
- [x] 6.2 Add backend tests for usage event success, unknown event, missing required properties, forbidden properties, and non-blocking behavior.
- [x] 6.3 Add backend tests for admin log list/detail permissions, filters, pagination, and missing log behavior.
- [x] 6.4 Add frontend Vitest coverage for list smoke, filters, pagination structure, request_id copy, detail drawer, and forbidden route state.
- [ ] 6.5 Run OpenSpec validation, API standard validation when API files change, directory validation, backend pytest, frontend Vitest, and Orval generation.
