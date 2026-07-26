## 1. Backend Audit Logging

- [x] 1.1 Inspect all current `audit_logs` write paths and produce the first-batch sensitive operation checklist for system settings, brand certificates, media/uploads, SKU, Banner, and any other existing audit writers.
- [x] 1.2 Extend `AuditLogRepository.insert()` or the equivalent audit write entrypoint to accept optional `task_trace_id` and `task_type` while preserving compatibility for callers that do not pass them.
- [x] 1.3 Pass existing Task Trace context into task-type audit write paths and keep non-task audit operations nullable.
- [x] 1.4 Reuse the existing metadata sanitization path and add coverage for Authorization, Cookie, Token, password, AccessKey, SecretKey, DSN, `.env`, internal path, and real customer data redaction.

## 2. Database And API Contract

- [x] 2.1 Verify SQLite schema, SQLite migrations, MySQL baseline, and MySQL migration paths all include compatible `audit_logs.task_trace_id` and `audit_logs.task_type` fields.
- [x] 2.2 Add or adjust indexes/query paths so `task_trace_id` filtering uses structured fields rather than metadata fuzzy search.
- [x] 2.3 Ensure admin logs list/detail response schemas expose audit type task summary fields when present.
- [x] 2.4 Regenerate and verify OpenAPI and Orval output after API schema changes.
- [x] 2.5 Update `docs/03-api-index.md`, `docs/04-database-design.md`, and applicable error code documentation if fields, responses, or errors change.

## 3. Web Admin UI

- [x] 3.1 Reuse the existing `/admin/logs` page and detail drawer to display audit type `task_trace_id`, `task_type`, task status, and task timeline or task entry when present.
- [x] 3.2 Preserve the no-task state for audit logs without `task_trace_id` without empty timeline errors or layout regressions.
- [x] 3.3 Implement copy/query feedback for `task_trace_id` using fixed toast or equivalent non-layout-shifting feedback.
- [x] 3.4 Keep pagination DOM, metric card DOM, no `window.confirm`, responsive smoke, and semantic token requirements aligned with `docs/knowledge-base/best-practices/admin-list-page-consistency.md`.

## 4. Tests And Validation

- [x] 4.1 Add backend tests for audit write with task context, audit write without task context, task_trace_id filtering, permission rejection, not-found behavior, and metadata redaction.
- [x] 4.2 Add or update database schema drift tests covering SQLite/MySQL `audit_logs` task fields.
- [x] 4.3 Add Web tests for audit log list rendering, task trace filter/search, copy success/fallback/failure, detail drawer Task Trace group, no-task state, forbidden state, and pagination structure.
- [x] 4.4 Run focused backend pytest, focused frontend Vitest, OpenSpec validation, and any existing OpenAPI/Orval validation scripts required by changed contracts.

## 5. Workflow And Trace

- [x] 5.1 Update REQ-0075 trace and this Change trace as implementation progresses.
- [x] 5.2 Before `/opsx-apply`, ensure this Change has been formally added to a Sprint scope because it is REQ-sourced.
