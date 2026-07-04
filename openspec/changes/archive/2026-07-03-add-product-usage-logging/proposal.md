## Why

The platform currently has business audit records for selected admin operations, but it does not provide a unified way to capture product usage events, API request logs, and log detail context for troubleshooting and security audit. REQ-0024 is in `sprint-004` and has product v2 prototypes for the admin log audit page, so this change formalizes the contract before implementation.

## What Changes

- Add backend request logging with `request_id`, method, path, status, duration, actor, client type, error summary, and sanitized metadata.
- Add product usage event collection based on a manually maintained event dictionary (`tracking-events.md`), with server-side validation, context enrichment, and forbidden-field filtering.
- Add admin-only log query APIs for paginated list and detail drawer data.
- Add a Web admin SYSTEM / 日志审计 page using the product v2 list and detail-drawer prototype as Golden Reference.
- Add relational storage for request logs and usage events, with unified query semantics alongside existing `audit_logs`.
- Add security rules for masking, truncation, retention, and sensitive-field exclusion.
- Update API docs, OpenAPI, Orval output, database documentation, tests, and workflow trace during implementation.

No breaking API changes are intended.

## Capabilities

### New Capabilities

- `product-usage-logging`: Product usage event collection, API request logging, admin log audit query/detail UI, storage, security, and event dictionary enforcement.

### Modified Capabilities

- None. Existing `audit_logs` behavior remains valid; this change introduces a unified log audit capability that can include audit records in its query model without changing archived spec requirements.

## Impact

- Backend: FastAPI middleware or equivalent request lifecycle hook, usage event endpoint, admin logs endpoints, repository/service layer, Pydantic schemas, error handling, tests.
- Database: new relational log tables and indexes for SQLite demo and MySQL production; docs and migration/update scripts required.
- Web admin: SYSTEM navigation entry, route guard, list page, filters, metric cards, pagination, request_id copy, detail drawer, Vitest coverage.
- API contract: `GET /api/v1/admin/logs`, `GET /api/v1/admin/logs/{id}`, `POST /api/v1/usage-events`; OpenAPI and Orval must be regenerated.
- Security: admin-only log query/detail access, sensitive field masking, body/header whitelist, metadata truncation, no secret exposure.
- Documentation and workflow: update `docs/03-api-index.md`, `docs/04-database-design.md`, `docs/standards/error-codes.md` if new codes are added, REQ trace, and OpenSpec change trace.
