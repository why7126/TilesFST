## 1. Backend and Data Contract

- [x] 1.1 Update SKU create validation so `sku_code` is not required from admin frontend for `draft` or `create` save modes.
- [x] 1.2 Ensure backend generates a unique, stable SKU code for new draft and create records, with collision handling covered by tests.
- [x] 1.3 Ensure SKU update does not regenerate or mutate `sku_code` when product name or other fields change.
- [x] 1.4 Add compatibility handling or a migration/backfill check for historical records missing SKU code.
- [x] 1.5 Update Pydantic schemas, OpenAPI docs and Orval generation if `sku_code` request fields become read-only or omitted.

## 2. Admin Web

- [x] 2.1 Rename admin SKU form label from “SKU 名称” to “商品名称”.
- [x] 2.2 Remove required manual SKU code input from create/edit UX or convert it to read-only/internal generated-code hint.
- [x] 2.3 Keep admin keyword search compatible with product name and SKU code, with placeholder “商品名称 / SKU 编码” or equivalent.
- [x] 2.4 Ensure admin list and status/delete confirmations use product name as the primary label and SKU code only as weak internal auxiliary text.
- [x] 2.5 Preserve admin-list and admin-modal cross-cutting gates: pagination DOM, fixed toast, DS confirm modal, `sku-modal-card` width and short-viewport scroll.

## 3. Miniapp / Storefront Public Surfaces

- [x] 3.1 Hide SKU code from miniapp/storefront product cards, product list entries, recommendations and favorites.
- [x] 3.2 Hide SKU code from SKU detail title and parameter rows.
- [x] 3.3 Update SKU detail share title/summary/card text to use brand name + product name without SKU code.
- [x] 3.4 Keep backend search compatibility for SKU code where applicable, but do not render code in public search results or no-result copy.

## 4. Tests and Verification

- [x] 4.1 Add backend tests for auto-generated SKU code, uniqueness, update stability and historical compatibility.
- [x] 4.2 Add admin web tests for no manual code requirement, product-name primary display, search placeholder and confirm copy.
- [x] 4.3 Add miniapp/static tests proving product cards, detail parameters, recommendations, favorites, search results and share titles do not display SKU code.
- [x] 4.4 Run focused backend, web and miniapp tests; include OpenAPI/Orval generation verification when API contract changes.
- [x] 4.5 Record admin modal computed width and short-viewport scroll evidence in change trace before archive.
