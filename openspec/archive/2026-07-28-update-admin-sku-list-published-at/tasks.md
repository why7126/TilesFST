## 1. Contract And Data Source

- [x] 1.1 Inspect current `GET /api/v1/admin/tile-skus` response, Pydantic schemas, repository/service mapping, and frontend generated type to determine whether a semantic published-at field already exists.
- [x] 1.2 N/A — no existing semantic published-at field was present in the current admin SKU list response or generated type.
- [x] 1.3 If no semantic published-at field exists, add or map a backend list response field for published time without changing pagination, summary, auth, or error response shape.
- [x] 1.4 If backend/API schema changes are required, update API docs and run OpenAPI/Orval generation from the project script.

## 2. Web Admin Implementation

- [x] 2.1 Add the “发布时间” column to the admin SKU list before “更新时间”.
- [x] 2.2 Reuse the existing “更新时间” date formatting path for “发布时间”, including timezone and seconds behavior.
- [x] 2.3 Render a stable placeholder such as `-` when published time is null, missing, or invalid.
- [x] 2.4 Preserve existing list search, filters, pagination, default sorting, loading, empty, failed, and row action behavior.
- [x] 2.5 Verify the table layout at 1440x1024 and a narrow viewport so the added time column does not overlap core fields or actions.

## 3. Tests

- [x] 3.1 Add or update frontend tests asserting that “发布时间” exists and appears before “更新时间”.
- [x] 3.2 Add or update frontend tests asserting that published time and updated time use the same formatting strategy.
- [x] 3.3 Add or update frontend tests for null/missing/invalid published time placeholder rendering.
- [x] 3.4 If backend/API response changes are required, add backend tests for list response field presence, type, null handling, auth preservation, and unchanged pagination/summary shape.
- [x] 3.5 If OpenAPI/Orval changes are required, verify generated client types and frontend typecheck/tests.

## 4. Knowledge-base Gates

- [x] 4.1 Verify SKU list pagination DOM remains aligned with the user-management baseline: `.page-summary` plus `.page-right`.
- [x] 4.2 Verify fixed toast or equivalent feedback does not cause page header, filter area, or table layout shift.
- [x] 4.3 Verify no `window.confirm` is introduced; if this change touches any dangerous state action, verify DS confirm modal is used.
- [x] 4.4 Record admin-list cross-cutting acceptance evidence in the Change `trace.md`.

## 5. Validation

- [x] 5.1 Run focused backend tests if backend/API contract changes are made.
- [x] 5.2 Run focused frontend tests for admin SKU list behavior.
- [x] 5.3 Run OpenSpec validation for `update-admin-sku-list-published-at`.
- [x] 5.4 Update trace with implementation evidence, API/DB/Orval impact conclusion, and any residual risks.
