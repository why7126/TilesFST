---
change_id: add-product-usage-logging
requirement_id: REQ-0024-product-usage-logging
iteration: sprint-004
status: implemented-pending-visual-validation
created_at: 2026-07-02 21:55:08
updated_at: 2026-07-03 18:43:18
---

# OpenSpec Change Trace

## Readiness Report

```yaml
requirement: REQ-0024-product-usage-logging
status: in_sprint
readiness: Ready
approved: true
sprint: sprint-004
change: add-product-usage-logging
prototype:
  list_html: issues/requirements/review/REQ-0024-product-usage-logging/prototype/web/log-audit-list.html
  list_png: issues/requirements/review/REQ-0024-product-usage-logging/prototype/web/log-audit-list.png
  detail_html: issues/requirements/review/REQ-0024-product-usage-logging/prototype/web/log-audit-detail-drawer.html
  detail_png: issues/requirements/review/REQ-0024-product-usage-logging/prototype/web/log-audit-detail-drawer.png
```

REQ-0024 has complete PRD, user stories, business flow, acceptance criteria, tracking event dictionary, review approval, sprint inclusion, and product v2 prototype assets. It is ready for OpenSpec implementation planning.

## Impact Analysis

| Area | Impact |
|---|---|
| Backend API | Adds admin log list/detail endpoints and usage event ingestion |
| Database | Adds relational request/usage log tables and indexes |
| Web Admin | Adds `/admin/logs` route, sidebar item, list page, detail drawer |
| Security | Adds admin-only access, masking, forbidden fields, truncation |
| OpenAPI / Orval | Must regenerate after implementation |
| Docs | Must update API, database, and error-code docs when applicable |
| Docker / Env | No Docker topology change expected; `.env.example` only if new config is added |
| MinIO / Object Storage | No storage bucket or object-key change |
| Miniapp / Storefront | Design boundary only unless sprint-004 implementation explicitly enables ingestion |

## Conflict Report

Priority for conflicts:

1. Product v2 HTML prototypes
2. Product v2 PNG Golden Reference
3. Prototype context docs
4. REQ acceptance criteria
5. `rules/ui-design.md`
6. Existing OpenSpec specs

Resolved decisions:

- Route uses `/admin/logs` for the admin UI and `/api/v1/admin/logs` for APIs, matching the shortest option in the PRD and REST rules.
- UI implementation will use DS semantic tokens and existing admin list patterns while matching prototype layout and fields.
- Data storage uses dedicated `request_logs` / `usage_events`; existing `audit_logs` remains a source for unified read models.
- Log export remains out of scope even though future audit operations may need it.
- Product v2 PNG assets are present under `prototype/web/`; older trace text about missing PNG assets should be corrected.

## UI Strategy

Chosen strategy: `tailwind-ds + product-v2-golden-port`.

Implementation must preserve the product v2 information architecture and 1440x1024 visual target while translating prototype styling into existing semantic token classes and reusable admin components.

## Golden Checklist

- [ ] Compare `/admin/logs` list state with `prototype/web/log-audit-list.png` at 1440x1024. Not executed: Playwright package is available, but bundled Chromium is not installed; system Chrome/Edge headless launch is blocked by the current sandbox process controls.
- [ ] Compare `/admin/logs` drawer-open state with `prototype/web/log-audit-detail-drawer.png` at 1440x1024. Not executed for the same browser environment reason.
- [x] Verify pagination DOM follows `admin-list-page-consistency.md` (`.pagination`, `.page-summary`, `.page-right` present in `LogAuditPage.tsx`).
- [x] Verify fixed toast or equivalent feedback does not shift table layout (`AdminToast` is fixed and copy feedback does not alter table DOM).
- [x] Verify no naked hex values are introduced in TSX/CSS (`rg "#[0-9A-Fa-f]{3,8}|window\\.confirm"` checked on new log audit files).

## Implementation Summary

| Area | Result |
|---|---|
| Backend data | Added SQLite/MySQL `request_logs` and `usage_events` tables, migration guards, indexes, repository pagination/filtering, metric aggregation, and `usage_events.duration_ms` for process-duration behavior events. |
| Backend logging | Added request-id propagation middleware, route exclusions, sanitization/masking/truncation, and non-blocking request logging. |
| Usage events | Added `POST /api/v1/usage-events` with event dictionary validation, forbidden sensitive property checks, trusted server identity enrichment, `duration_ms`, and explicit `detail_view` / `copy_request_id` behavior events. Frontend log-audit events now include `entity_type` and `entity_id` so behavior rows keep an object reference. |
| Admin API | Added admin-only `GET /api/v1/admin/logs` and `GET /api/v1/admin/logs/{log_id}` with response models, OpenAPI summaries, tags, pagination, filters, metrics, and detail drawer sections. |
| Web admin | Added `/admin/logs`, SYSTEM sidebar entry, metric cards, filters, table, fixed toast, pagination, right-side detail drawer, clickable event/summary cells, sticky right-side operation column, request_id inline copy action, differentiated type/status colors, and shared frontend tracking client calls. `page_view` is now emitted once from the shared admin layout for every registered `/admin/*` business page; log-audit still emits filter/search, copy, and detail-open interaction events. Search/detail events submit measured `duration_ms`; instant events may omit duration. |
| Docs | Updated `docs/03-api-index.md`, `docs/04-database-design.md`, `docs/standards/error-codes.md`, and `data/README.md`. `.env.example` unchanged because no environment-level log configuration was introduced. |
| OpenAPI / Orval | Ran `./scripts/generate-openapi-client.sh`; resolved Orval duplicate result type by keeping the URL query param `result` and expressing validation as an OpenAPI regex. |

## Validation Results

| Command | Result |
|---|---|
| `uv run python -m compileall app` | Pass |
| `uv run pytest src/backend/tests/test_product_usage_logging.py` | Pass: 7 passed |
| `uv run pytest src/backend/tests/test_product_usage_logging.py src/backend/tests/test_auth.py` | Pass: 18 passed |
| `pnpm --dir src/web exec vitest run src/pages/admin/LogAuditPage.test.tsx src/features/auth/components/ProtectedRoute.test.tsx src/features/admin/components/AdminLayout.test.tsx` | Pass: 12 passed |
| `uv run pytest src/backend/tests/test_product_usage_logging.py` after frontend tracking event dictionary update | Pass: 8 passed |
| `pnpm --dir src/web exec vitest run src/features/tracking/api/usage-tracking.test.ts src/pages/admin/LogAuditPage.test.tsx src/features/auth/components/ProtectedRoute.test.tsx src/features/admin/components/AdminLayout.test.tsx` | Pass: 16 passed |
| `uv run pytest src/backend/tests/test_product_usage_logging.py` after requiring entity info on `copy_request_id` | Pass: 8 passed |
| `pnpm --dir src/web exec vitest run src/features/tracking/api/usage-tracking.test.ts src/pages/admin/LogAuditPage.test.tsx` after adding entity ids to frontend events | Pass: 8 passed |
| `pnpm --dir src/web exec vitest run src/pages/admin/LogAuditPage.test.tsx src/features/tracking/api/usage-tracking.test.ts` after clickable summary and sticky operation column update | Pass: 9 passed |
| `rg "#[0-9A-Fa-f]{3,8}\|window\\.confirm" src/web/src/pages/admin/LogAuditPage.tsx src/web/src/features/admin/styles/log-audit.css` | Pass: no matches |
| `./scripts/generate-openapi-client.sh` after adding `UsageEventCreate.duration_ms` | Pass |
| `uv run pytest src/backend/tests/test_product_usage_logging.py src/backend/tests/test_auth.py` after `usage_events.duration_ms` | Pass: 19 passed |
| `pnpm --dir src/web exec vitest run src/features/tracking/api/usage-tracking.test.ts src/pages/admin/LogAuditPage.test.tsx src/features/auth/components/ProtectedRoute.test.tsx src/features/admin/components/AdminLayout.test.tsx` after duration tracking | Pass: 18 passed |
| `pnpm --dir src/web exec vitest run src/pages/admin/LogAuditPage.test.tsx src/features/tracking/api/usage-tracking.test.ts` after filter/table UI refinement | Pass: 10 passed |
| `rg "resource_id\|filters\\.resource\|资源 / ID\|<th>复制</th>\|admin-(info\|success)" src/web/src/pages/admin/LogAuditPage.tsx src/web/src/features/admin/styles/log-audit.css src/web/src/pages/admin/LogAuditPage.test.tsx` | Pass: no production matches; test retains a negative assertion for `资源 / ID`. |
| `pnpm --dir src/web exec vitest run src/features/admin/components/AdminLayout.test.tsx src/pages/admin/LogAuditPage.test.tsx src/features/tracking/api/usage-tracking.test.ts` after admin-wide page view tracking | Pass: 16 passed |
| `rg "trackUsageEvent\\('page_view'\|page_view" src/web/src/pages/admin src/web/src/features/tracking` | Pass: production page-view emission is centralized in `AdminLayout.tsx`; remaining matches are tracking API/tests. |
| `rg "#[0-9A-Fa-f]{3,8}\|window\\.confirm" src/web/src/pages/admin/AdminLayout.tsx src/web/src/features/tracking/admin-page-tracking.ts src/web/src/pages/admin/LogAuditPage.tsx src/web/src/features/admin/styles/log-audit.css` after admin-wide page view tracking | Pass: no matches |
| `pnpm --dir src/web exec vitest run src/features/admin/components/AdminLayout.test.tsx src/pages/admin/LogAuditPage.test.tsx src/features/tracking/api/usage-tracking.test.ts src/features/auth/components/ProtectedRoute.test.tsx` during `/opsx-apply` continuation | Pass: 19 passed |
| `uv run pytest src/backend/tests/test_product_usage_logging.py src/backend/tests/test_auth.py` during `/opsx-apply` continuation | Pass: 19 passed |
| `./scripts/generate-openapi-client.sh` during `/opsx-apply` continuation | Pass |
| `openspec validate add-product-usage-logging --strict` during `/opsx-apply` continuation | Pass |
| `python scripts/validate-directory-structure.py` during `/opsx-apply` continuation | Pass |
| `python scripts/validate-api-standard.py` during `/opsx-apply` continuation | Fail: remaining violations are pre-existing admin route decorator `tags` gaps outside REQ-0024; the new log routes are not listed. |
| `uv run python -m compileall app` after duration tracking | Pass |
| `openspec validate add-product-usage-logging --strict` after duration tracking | Pass |
| `python scripts/validate-directory-structure.py` after duration tracking | Pass |
| `./scripts/generate-openapi-client.sh` | Pass |
| `openspec validate add-product-usage-logging --strict` | Pass |
| `python scripts/validate-directory-structure.py` | Pass |
| `python scripts/validate-api-standard.py` | Fail: remaining violations are pre-existing admin route decorator `tags` gaps outside REQ-0024; the three new REQ-0024 routes no longer appear in the violation list. |
| `pnpm --dir src/web exec tsc --noEmit` | Fail before project type-check: TypeScript 7 reports existing `baseUrl` deprecation and asks for `ignoreDeprecations: "6.0"`. |
| 1440x1024 Playwright Golden screenshot | Not executed: Playwright browser binary unavailable and system Chrome/Edge headless launch blocked in sandbox. |

## Artifacts

| Artifact | Path |
|---|---|
| Proposal | `openspec/changes/add-product-usage-logging/proposal.md` |
| Design | `openspec/changes/add-product-usage-logging/design.md` |
| Delta Spec | `openspec/changes/add-product-usage-logging/specs/product-usage-logging/spec.md` |
| Tasks | `openspec/changes/add-product-usage-logging/tasks.md` |
