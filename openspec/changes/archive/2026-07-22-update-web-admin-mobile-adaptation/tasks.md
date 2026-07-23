## 1. Scope and Baseline

- [x] 1.1 Confirm the implemented `/admin/*` route list and map each route to the REQ-0027 acceptance matrix.
- [x] 1.2 Inspect existing `AdminLayout`, admin shared components, page CSS, modal components, pagination DOM, and upload controls before editing.
- [x] 1.3 Record the baseline mobile issues for `375x812`, `390x844`, `768x1024`, and `1440x1024`.

## 2. Shell and Shared Admin Layout

- [x] 2.1 Update Admin Shell and content layout so `≤1023px` and `≤639px` viewports do not produce Shell-level or page-level uncontrolled horizontal scrolling.
- [x] 2.2 Ensure Sidebar or narrow-screen navigation remains accessible, scrollable when needed, and keeps active route indication.
- [x] 2.3 Hide, disable, or adapt the desktop collapse chevron on narrow screens so it does not overlap navigation or trigger layout jumps.
- [x] 2.4 Verify `/admin/login`, `/admin/dashboard`, and `/admin/forbidden` mobile regressions against the REQ-0027 matrix.

## 3. List Pages and Pagination

- [x] 3.1 Update list filter layouts for `/admin/brands`, `/admin/banners`, `/admin/tile-categories`, `/admin/tile-specs`, `/admin/tile-skus`, `/admin/users`, `/admin/logs`, and `/admin/api-docs` so mobile filters do not overlap or overflow.
- [x] 3.2 Ensure wide tables scroll inside table containers and keep key identifiers, status, and operation columns accessible.
- [x] 3.3 Preserve the unified pagination DOM with `page-summary`, `page-right`, `page-buttons`, and `page-size-wrap`, allowing mobile wrapping without changing semantics.
- [x] 3.4 Preserve admin-list cross-cutting contracts: metric card structure, fixed toast feedback, DS confirm modal, and no `window.confirm` regression.

## 4. Forms, Modals, Drawers, and Upload Controls

- [x] 4.1 Update business modals and confirmation modals so `375px` width and short viewport heights keep title, close button, body scroll, and footer actions accessible.
- [x] 4.2 Validate SKU and Banner wide modals with computed width/max-width checks and avoid conflicting `modal-card` plus dedicated modal classes.
- [x] 4.3 Update `/admin/profile` and `/admin/settings/:tab` mobile layouts so form sections, dirty-state confirmations, save/reset actions, and password dialogs remain single-column or otherwise readable and operable.
- [x] 4.4 Validate `/admin/logs` detail drawer on phone width so it can close, scroll, and avoid page-level horizontal overflow.
- [x] 4.5 Verify existing Logo, Banner, SKU image/video, and avatar upload controls preserve visible uploading, success, failure, and same-session preview states on mobile.

## 5. Tests and Acceptance Evidence

- [x] 5.1 Add Playwright or equivalent browser smoke coverage for `375x812`, `390x844`, `768x1024`, and `1440x1024`.
- [x] 5.2 Smoke test at least `/admin/login`, `/admin/dashboard`, `/admin/tile-skus`, `/admin/brands`, `/admin/users`, `/admin/logs`, and `/admin/settings/basic`.
- [x] 5.3 Record smoke results for page-level horizontal overflow, overlapping controls, uncloseable modals, unreachable footer buttons, and unusable filters or pagination.
- [x] 5.4 Run `pnpm --dir src/web test` or an equivalent focused frontend test suite and document any skipped coverage or residual risk.
- [x] 5.5 Confirm no API, database, Orval, Docker Compose, MinIO, or miniapp changes were introduced; if any are required, stop and split a separate REQ/Change.

## 6. Trace and Documentation

- [x] 6.1 Update the Change trace with implementation decisions, screenshot or Playwright evidence, tested viewports, and N/A reasons.
- [x] 6.2 Update REQ-0027 trace through Workflow Sync after apply/archive events rather than hand-editing derived Sprint scope blocks.
