## 1. Assets and Entry HTML

- [x] 1.1 Add the optimized 菲尚特 Logo static asset for Web usage, reusing `issues/requirements/archive/REQ-0025-brand-logo-fst-favicon/prototype/web/fs-logo-web.png` or an equivalent derived asset.
- [x] 1.2 Update the Web entry HTML favicon and apple-touch-icon declarations to point to the 菲尚特 Logo asset.
- [x] 1.3 Verify the static asset path works in both Vite dev and Docker Web build output.

## 2. Admin Sidebar Brand Area

- [x] 2.1 Update `AdminSidebar` brand area DOM to render Logo, `菲尚特FST`, `PRODUCT_VERSION`, `家居建材资料库`, and the collapse button in one stable brand row.
- [x] 2.2 Preserve existing Sidebar expanded/collapsed state, localStorage key, navigation active state, role-based menu filtering, and route behavior.
- [x] 2.3 Update admin Sidebar CSS using existing semantic tokens; do not add bare Hex values or new Design System tokens.
- [x] 2.4 Ensure collapsed Sidebar keeps Logo brand recognition and avoids overlap between Logo, nav icons, and collapse button.

## 3. Tests and Verification

- [x] 3.1 Add or update Vitest/Testing Library coverage for `菲尚特FST`, `家居建材资料库`, `PRODUCT_VERSION`, Logo alt text, and collapsed Sidebar behavior.
- [x] 3.2 Add or update a test/check for favicon and apple-touch-icon declarations in the Web entry HTML.
- [x] 3.3 Run the relevant Web test suite with `pnpm --dir src/web test` or the narrower existing admin sidebar tests.
- [x] 3.4 Perform visual verification at 1366×768 and 1440×1024 against `prototype/web/banner-management-list-logo.html` / PNG checklist.

## 4. Documentation and Workflow

- [x] 4.1 Update sprint-004 acceptance notes for REQ-0025 implementation results.
- [x] 4.2 Run `openspec validate update-brand-logo-fst-favicon --strict`.
- [x] 4.3 Confirm no OpenAPI, Orval, SQLite, MinIO, backend API, Docker Compose, or miniapp changes are required.
