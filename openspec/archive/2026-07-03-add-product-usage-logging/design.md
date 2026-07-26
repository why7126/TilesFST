## Context

REQ-0024 adds a platform governance capability for product usage behavior tracking, API request logging, and admin log audit lookup. The project already has a relational database baseline (`SQLite` for local/demo, MySQL 8.0+ for production), an `audit_logs` table used by system settings, unified API response conventions, Orval-generated Web clients, and a dark industrial Design System.

The product v2 prototype is authoritative for the admin UI:

1. `issues/requirements/review/REQ-0024-product-usage-logging/prototype/web/log-audit-list.html`
2. `issues/requirements/review/REQ-0024-product-usage-logging/prototype/web/log-audit-detail-drawer.html`
3. `issues/requirements/review/REQ-0024-product-usage-logging/prototype/web/log-audit-list.png`
4. `issues/requirements/review/REQ-0024-product-usage-logging/prototype/web/log-audit-detail-drawer.png`
5. `issues/requirements/review/REQ-0024-product-usage-logging/prototype/web/*-context.md`
6. `issues/requirements/review/REQ-0024-product-usage-logging/acceptance.md`
7. `rules/ui-design.md`
8. Existing `openspec/specs/*`

## Goals / Non-Goals

**Goals:**

- Capture API request summaries with request correlation, latency, status, actor, client, and sanitized error context.
- Capture product usage events from a human-defined event dictionary, not arbitrary DOM or raw payload collection.
- Store log data in the relational database and support indexed, paginated, admin-only queries.
- Provide `SYSTEM / LOG AUDIT` Web admin list and detail drawer aligned with product v2 Golden Reference.
- Keep sensitive values out of storage and UI by default.
- Generate OpenAPI/Orval artifacts and tests for the new API surface during implementation.

**Non-Goals:**

- No third-party analytics platform integration.
- No funnel analysis, BI dashboard, realtime wallboard, or user profiling.
- No full raw request/response body storage by default.
- No log export/download in this change.
- No external log system, queue, partitioning, or distributed tracing stack.
- No implementation code in this `/req-opsx` step.

## Decisions

### D1. Storage Strategy: Dedicated Request and Usage Tables

Implementation SHALL introduce dedicated relational tables for high-volume log domains, tentatively `request_logs` and `usage_events`, while preserving existing `audit_logs` for business operation audit.

Rationale:

- Request logs and usage events have different write volume, retention, fields, and indexes from existing business audit records.
- Dedicated tables reduce risk of degrading existing audit queries.
- A unified repository/service can still return a combined admin list with `log_type = request | usage_event | audit`.

Alternatives considered:

- Extending only `audit_logs`: simpler schema, but mixes high-frequency request records with lower-frequency audit operations and makes retention/indexing harder.
- Storing logs in files or object storage: rejected because REQ-0024 explicitly needs query/filter/detail in the admin UI and the project default is relational persistence.

### D2. Data Model and Indexing

Implementation SHALL support SQLite demo and MySQL production. Common fields SHALL include `id`, `log_type`, `request_id`, `actor_user_id`, `actor_role`, `client_type`, `event_name`, `method`, `path`, `status_code`, `duration_ms`, `ip_address_masked`, `user_agent_summary`, `summary`, `error_code`, `result`, `metadata`, and `created_at` as applicable.

Indexes SHALL cover the main filters and ordering:

- `created_at`
- `log_type`
- `actor_user_id`
- `request_id`
- `status_code`
- `path`
- suitable composite indexes for `created_at DESC` plus frequent filters

Implementation MUST use repository/data-access abstractions and parameterized SQL. MySQL DDL MUST avoid SQLite-only syntax.

### D3. Request Logging Boundary

Request logging SHALL be implemented in a centralized FastAPI middleware or equivalent lifecycle hook. It SHALL generate or propagate a `request_id`, measure duration, and record status/error summaries after request completion.

Default excluded routes:

- `/health`
- `/docs`, `/redoc`, `/openapi.json`
- static assets
- media passthrough routes such as `/media/{object_key:path}`

The logger MUST not store raw `Authorization`, `Cookie`, passwords, tokens, MinIO credentials, database DSNs, or complete raw bodies by default.

### D4. Event Dictionary Enforcement

Product usage events SHALL use `issues/requirements/review/REQ-0024-product-usage-logging/tracking-events.md` as the product dictionary source. Stable events SHALL be represented in code by enums, schema validators, or equivalent allowlists.

The backend SHALL validate:

- allowed `event_name`
- required properties by event
- property types and length limits
- forbidden properties
- metadata JSON serialization

The backend SHALL override or enrich user identity, role, client type, request_id, timestamp, user agent summary, and IP summary from trusted server context. Frontend-supplied identity is not trusted.

### D4.1 Web Admin Page View Coverage

Web admin `page_view` events SHALL be emitted from the shared admin layout layer for every registered `/admin/*` business page instead of being implemented separately inside each page component. The route-to-module dictionary is maintained in Web tracking code and mirrored in `tracking-events.md`.

This keeps page coverage broad while still respecting the human-defined event dictionary: the client reports route pattern, page title, module, `entity_type = admin_page`, and stable `entity_id`; it does not auto-collect arbitrary DOM clicks or page content.

### D5. API Contract

Implementation SHALL add:

- `GET /api/v1/admin/logs`: admin-only paginated log list with filters and metric summary.
- `GET /api/v1/admin/logs/{id}`: admin-only log detail for the drawer.
- `POST /api/v1/usage-events`: usage event ingestion, authenticated where available and anonymous only when explicitly supported by client boundary.

All responses SHALL use the unified `ApiResponse` envelope. List data SHALL include `items`, `total`, `page`, and `page_size`. Invalid parameters SHALL use documented parameter errors; missing log detail SHALL return a 404-class error registered in `error_codes.py` and `docs/standards/error-codes.md` if a new code is introduced.

### D6. UI Strategy: Tailwind DS + Product v2 Golden Port

Implementation SHALL compose the page from existing admin shell/list patterns, shadcn base components, semantic Tailwind token classes, and small page-local composition where necessary. The product v2 HTML/PNG defines layout, hierarchy, fields, and visual target; implementation MUST translate prototype colors and spacing into existing semantic tokens instead of copying hard-coded prototype hex values.

Required UI elements:

- SYSTEM sidebar entry `日志审计`, active at `/admin/logs`.
- Breadcrumb `SYSTEM / LOG AUDIT`, title `日志审计`, and explanatory copy.
- Metric cards: `TODAY LOGS`, `API ERRORS`, `SLOW REQUESTS`, `SENSITIVE OPS`.
- Filters: log type, time range, actor, status/result, resource/ID, path/request_id.
- Table columns: time, type, event/summary, actor, client, status/result, duration, request_id, copy, detail.
- Right drawer detail sections: basic info, request info, actor/client, operation context, event properties, metadata JSON.
- Pagination aligned with admin list consistency knowledge base.

Visual acceptance MUST use 1440x1024 side-by-side comparison against:

- `prototype/web/log-audit-list.png`
- `prototype/web/log-audit-detail-drawer.png`

### D7. Retention and Configuration

The implementation SHALL align default retention with the existing system settings audit retention policy. If implementation discovers that request logs and usage events need independent retention fields, it MUST document the new setting, update API/system-setting contracts, and update `.env.example` only if environment-level configuration is added.

### D8. Documentation and Generated Client

Because this change adds API endpoints and database tables, implementation MUST update:

- `docs/03-api-index.md`
- `docs/04-database-design.md`
- `docs/standards/error-codes.md` when adding new error codes
- `src/web/openapi.json`
- `src/web/src/shared/api/generated.ts`

The implementation MUST run `./scripts/generate-openapi-client.sh` after backend OpenAPI changes.

## Risks / Trade-offs

- [Log volume grows quickly] -> use dedicated tables, indexed pagination, route exclusions, and retention cleanup planning.
- [Sensitive data leakage] -> use backend masking/filtering as the security boundary, prohibit raw secrets, and test forbidden fields.
- [Request logging affects latency] -> keep MVP synchronous writes minimal; if needed later, introduce async queue through a separate OpenSpec change.
- [Event dictionary drift] -> require dictionary-first changes and enforce code-level allowlists/tests.
- [UI repeats prior admin list regressions] -> reuse existing admin shell/list patterns and apply `admin-list-page-consistency.md` checks.
- [SQLite/MySQL schema divergence] -> maintain compatible DDL/migrations and test query behavior at repository level.

## Migration Plan

1. Add database schema/migration support for request and usage event logs.
2. Add backend schemas, repositories, services, middleware, and routes.
3. Add Web admin route, sidebar entry, log audit page, detail drawer, and generated API usage.
4. Update docs, OpenAPI, Orval output, and tests.
5. Verify strict OpenSpec validation, backend tests, frontend tests, directory validation, and UI Golden comparison.

Rollback:

- Disable/remove `/admin/logs` route and sidebar entry.
- Remove request logging middleware and usage event route.
- Leave new log tables in place or drop them through the paired rollback/migration strategy if they contain no required audit data.

## Open Questions

- Whether `POST /api/v1/usage-events` should be enabled for shop-owner Web and miniapp in sprint-004, or only implemented for admin Web plus backend extension points.
- Whether request logs and usage events need separate retention days in system settings, or can share the existing audit retention policy for MVP.
- Whether existing `audit_logs` should be displayed by direct union query in the first implementation or adapted through a normalized read model.
