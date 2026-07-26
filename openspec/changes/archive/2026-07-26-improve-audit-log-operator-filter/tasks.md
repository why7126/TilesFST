## 1. API and Contract Precheck

- [x] 1.1 Confirm `GET /api/v1/admin/users` supports system-admin-only access, `keyword`, `page_size`, and fields needed for operator options: `id`, `display_name`, `username`, `role`, `status`.
- [x] 1.2 Confirm `GET /api/v1/admin/logs` keeps `actor_user_id` filtering semantics and does not require backend changes for the primary path.
- [x] 1.3 Decide whether deleted or disabled users must appear as historical log operator candidates; document the result in implementation notes or tests.
- [x] 1.4 If a new lightweight operator-candidate API is required, add backend route/service/schema tests and sync OpenAPI, Orval, API docs, and error-code docs.

## 2. Web UI Implementation

- [x] 2.1 Add operator candidate loading state to `/admin/logs`, mapping user records to searchable single-select options with display name plus username/role/status helper text.
- [x] 2.2 Replace the current User ID input with a single-select searchable dropdown, reusing `SearchableSelect` or extending it in a backward-compatible Design System-friendly way.
- [x] 2.3 Ensure selected operator state stores `user.id`, displays user name or name plus account, and sends `actor_user_id=<user.id>` to the logs query.
- [x] 2.4 Implement clear and reset behavior so operator filtering can be removed and the log list returns to page 1 with all operators.
- [x] 2.5 Implement loading, empty, and failed candidate states without blocking other log filters.
- [x] 2.6 Keep status/result, log type, time range, path/request_id, pagination, detail drawer, and request_id copy behavior unchanged.

## 3. Admin List and Responsive UI

- [x] 3.1 Verify `/admin/logs` retains title → metrics → filters → table module order after the operator dropdown change.
- [x] 3.2 Verify metrics DOM uses `.metric-label`, `.metric-value`, and `.metric-desc`.
- [x] 3.3 Verify pagination DOM retains left `.page-summary` and right `.page-right` controls.
- [x] 3.4 Ensure candidate errors and log errors use fixed toast or equivalent layout-stable feedback with no hero/filter/table vertical shift.
- [x] 3.5 Ensure implementation does not introduce `window.confirm` or `window.alert`.
- [x] 3.6 Verify the operator dropdown, filter grid, table wrapper, and pagination are usable at 1440x1024, 390x844, and 375x812 viewports.

## 4. Tests

- [x] 4.1 Add or update LogAuditPage tests for operator dropdown render, keyword search, option selection, clear, reset, and `actor_user_id` request parameter.
- [x] 4.2 Add or update tests for empty results, candidate loading failure, and same-display-name users with distinguishing helper text.
- [x] 4.3 Add or update admin-list cross-cutting tests for pagination DOM, metric card DOM, layout-stable feedback, and absence of native dialogs.
- [x] 4.4 Run focused frontend tests for `LogAuditPage` and related shared UI components.
- [x] 4.5 If backend/API changed, run focused backend tests for user candidate search, log filtering, permissions, and OpenAPI/Orval generation checks.

## 5. Documentation and Verification

- [x] 5.1 Update implementation notes in the Change or evidence to state whether the existing user list API was reused or a new candidate API was added.
- [x] 5.2 If API changed, update API index and generated client artifacts through the approved generation command, not by hand-editing generated files.
- [x] 5.3 Capture or document UI verification for desktop and mobile filter/dropdown behavior; PNG Golden Reference may remain N/A if context and tests are sufficient.
- [x] 5.4 Run `openspec status --change improve-audit-log-operator-filter --json` and resolve any incomplete artifact or spec validation issue before apply completion.
