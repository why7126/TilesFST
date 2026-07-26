---
change_id: fix-miniapp-home-preview-runtime-entry
status: proposed
created_at: 2026-07-16 13:13:44
updated_at: 2026-07-16 13:13:44
related_bug: BUG-0065-miniapp-home-preview-deviation
---

# Tasks

## 1. Runtime Entry Fix

- [x] 1.1 Confirm current WeChat miniapp runtime entry behavior for `src/miniapp/pages/index/index`.
- [x] 1.2 Choose and document the runtime source strategy: synchronized `.js` scripts or verifiable TypeScript compile chain.
- [x] 1.3 Ensure `pages/index/index` runtime script initializes homepage state and calls `loadHome()` on page load.
- [x] 1.4 Remove or replace empty template runtime scripts for homepage and other critical miniapp pages where they shadow business `.ts` logic.
- [x] 1.5 Verify homepage share, service contact, Banner navigation, shortcut navigation and product navigation handlers are present in the runtime script.

## 2. Homepage Regression

- [ ] 2.1 Verify WeChat Developer Tools preview renders brand navigation, search, Banner, shortcut entries and at least one recommendation module when demo/public data is available.
- [x] 2.2 Verify no-product state keeps Banner, shortcut entries and service area visible or safely degraded.
- [x] 2.3 Verify network failure shows retry/error state without causing blank or frozen page.
- [x] 2.4 Verify image failure uses placeholder or module-level fallback.
- [ ] 2.5 Verify page layout at 375x812, 390x844 and 320-430 pt width range has no horizontal scroll, overlap, major truncation or TabBar obstruction.

## 3. Tests

- [x] 3.1 Add static regression test that fails when critical miniapp `.js` page files remain empty templates.
- [x] 3.2 Add static or smoke test that homepage runtime script contains the key `Page` data/methods needed to load `/api/v1/miniapp/home`.
- [x] 3.3 Extend tests to cover search, product detail and store-info runtime scripts are not empty templates.
- [x] 3.4 Run miniapp static tests.
- [x] 3.5 Run existing miniapp home/backend tests to ensure API behavior remains compatible.

## 4. Scope and Documentation Checks

- [x] 4.1 Confirm no backend API contract changed; if changed, update OpenAPI, Orval, docs and tests.
- [x] 4.2 Confirm no SQLite/MySQL schema or Pydantic Schema changed; if changed, update database docs and tests.
- [x] 4.3 Confirm no Web admin, Web storefront, Docker Compose or unrelated page behavior changed.
- [x] 4.4 Update BUG-0065 trace with implementation evidence during apply/archive.
- [x] 4.5 If the incident has reusable engineering value, add or update `docs/knowledge-base/incidents/` with the miniapp runtime entry lesson.
