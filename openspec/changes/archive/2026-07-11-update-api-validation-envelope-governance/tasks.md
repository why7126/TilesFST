## 1. Backend Validation Envelope

- [x] 1.1 Inspect existing FastAPI exception handling, envelope helpers, `AppError`, and error code registry.
- [x] 1.2 Add or update the `RequestValidationError` handler to return HTTP 422 with `{ code, message, data.errors[] }`.
- [x] 1.3 Normalize validation errors into `field`, `message`, `type`, and `location` without exposing sensitive values.
- [x] 1.4 Ensure existing business `AppError` paths keep their original code, HTTP status, and message.
- [x] 1.5 Add or update OpenAPI response metadata for representative management admin form and upload APIs.

## 2. Web Admin Error Parsing

- [x] 2.1 Inspect existing Axios / Orval error parsing and admin form error display paths.
- [x] 2.2 Update the shared or equivalent parser to prefer envelope `message`.
- [x] 2.3 Map `data.errors[]` to form fields where practical and safely fall back to global feedback.
- [x] 2.4 Verify modal, page form, and upload failures use existing Design System display patterns without layout regressions.

## 3. Tests

- [x] 3.1 Add backend tests for JSON body missing or invalid field validation envelope.
- [x] 3.2 Add backend tests for path, query, or enum validation envelope.
- [x] 3.3 Add backend tests for admin upload missing `file` or invalid file parameter validation envelope.
- [x] 3.4 Add backend regression tests proving at least one existing business `AppError` is not overwritten.
- [x] 3.5 Add frontend tests for envelope `message`, `data.errors[]` mapping, and global fallback.
- [x] 3.6 Add or update OpenAPI / Orval contract checks for management admin form validation errors.

## 4. Documentation And Generated Contracts

- [x] 4.1 Update `docs/standards/api-governance.md` with management admin form validation envelope rules.
- [x] 4.2 Update `docs/03-api-index.md` for the management admin form validation error contract.
- [x] 4.3 Update `docs/standards/error-codes.md` and `src/backend/app/core/error_codes.py` only if a new error code is introduced.
- [x] 4.4 Export `src/web/openapi.json` and run Orval generation after backend contract changes.

## 5. Verification

- [x] 5.1 Run focused backend pytest for validation envelope, upload, and business error compatibility.
- [x] 5.2 Run focused frontend Vitest coverage for admin error parsing.
- [x] 5.3 Run API governance validation and relevant OpenSpec validation.
- [x] 5.4 Record any Docker Web `:3000` upload validation smoke result or N/A rationale in the implementation acceptance notes.
