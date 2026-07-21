## 1. Data, Migration, and API Contract

- [x] 1.1 Confirm final enum strategy: keep `display_client=MINIAPP_HOME` as compatibility storage value and show “小程序” in UI/API docs.
- [x] 1.2 Add `MINIAPP_BRAND_LIST_CAROUSEL` position support and update shared/backend/frontend display label mappings.
- [x] 1.3 Implement database migration or cleanup logic that deletes old Banner records outside the two miniapp positions and records delete count/conditions.
- [x] 1.4 Ensure migration does not physically delete MinIO objects or unrelated media references.
- [x] 1.5 Update SQLite schema/migrations, MySQL schema, and database documentation for Banner display scope.
- [x] 1.6 Update Admin Banner create/update validation to reject old display clients and old positions.
- [x] 1.7 Update Admin Banner list/summary defaults so old data cannot appear in pagination or metrics.
- [x] 1.8 Update OpenAPI, API docs, Orval generated client, and related type usage after API/schema changes.

## 2. Web Admin Banner UI

- [x] 2.1 Update `/admin/banners` display client filter to show only “小程序” or equivalent readonly expression.
- [x] 2.2 Update display position options to only “首页轮播” and “品牌列表页轮播”.
- [x] 2.3 Update Banner create modal defaults: display client “小程序”, default position “首页轮播”.
- [x] 2.4 Ensure old Banner records have no edit path after cleanup.
- [x] 2.5 Preserve Banner list columns, metric cards, pagination DOM, fixed toast, DS confirm modal, and semantic token usage.
- [x] 2.6 Verify `BannerFormModal` does not reintroduce `modal-card` + `banner-modal-card` dual class cascade issue.
- [x] 2.7 Verify Banner image upload state machine and same-session preview remain intact.
- [x] 2.8 Add `BRAND_DETAIL` jump type with brand searchable selection and brand Logo image behavior aligned with SKU detail.

## 3. Miniapp Carousel Split

- [x] 3.1 Update miniapp home banner query to read only home carousel position.
- [x] 3.2 Update brand list page carousel query to read only brand-list carousel position.
- [x] 3.3 Ensure brand list page does not fallback to home carousel when brand-list carousel is empty.
- [x] 3.4 Ensure public miniapp responses do not expose raw object keys, admin remarks, Authorization headers, cookies, or management-only fields.
- [x] 3.5 Coordinate with `add-brand-list-page` if that Change is still active, replacing its temporary home-carousel reuse implementation.
- [x] 3.6 Ensure miniapp home and brand-list carousel clicks can navigate to brand detail when public Banner `jump_type=brand`.

## 4. Tests and Validation

- [x] 4.1 Add/update backend tests for old display client/position rejection.
- [x] 4.2 Add/update migration tests for deleting old Banner records and preserving valid miniapp records.
- [x] 4.3 Add/update miniapp/API tests proving home and brand-list carousel data isolation.
- [x] 4.4 Add/update frontend tests for display client and position option scope.
- [x] 4.5 Add/upload regression test or manual evidence for Banner image upload through Web Docker `:3000` boundary.
- [x] 4.6 Run focused tests for Banner API, miniapp home/brand-list carousel, and admin Banner UI.
- [x] 4.7 Add/update backend and frontend tests for `BRAND_DETAIL` jump validation, payload, and public miniapp mapping.

## 5. Documentation and Trace

- [x] 5.1 Update implementation notes with enum decision, delete count, delete condition, and rollback/backup boundary.
- [x] 5.2 Update docs/API/database references as required by acceptance.
- [x] 5.3 Validate OpenSpec with `openspec validate update-admin-banner-placement-scope --strict`.
- [x] 5.4 Update acceptance evidence references before marking apply complete.
