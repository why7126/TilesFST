## 1. Share Context Utilities

- [x] 1.1 Inventory existing share behavior in `src/miniapp/pages/index`, `tile-detail`, `product-list`, and `brand-detail`.
- [x] 1.2 Define page-local or shared helper strategy for share title, path, query encoding, image fallback, and channel tracking.
- [x] 1.3 Ensure helper logic does not serialize raw page data, Authorization headers, Cookies, raw object keys, or local paths.

## 2. Page Share Implementation

- [x] 2.1 Add or update homepage `onShareAppMessage` and `onShareTimeline` with stable title, homepage path, source marker, and non-blocking tracking.
- [x] 2.2 Add or update SKU detail `onShareAppMessage` and `onShareTimeline` with `skuId`, `source=share`, title fallback, image fallback, and non-blocking tracking.
- [x] 2.3 Add product-list `onShareAppMessage` and `onShareTimeline` with list title, whitelisted query retention, encoded Chinese parameters, and non-blocking tracking.
- [x] 2.4 Add or update brand-detail `onShareAppMessage` and `onShareTimeline` with `brandId`, `source=share`, title fallback, and non-blocking tracking.
- [x] 2.5 Confirm share direct-open states continue to provide return or homepage fallback for SKU detail, product list, and brand detail.

## 3. Runtime Entry Synchronization

- [x] 3.1 Synchronize TypeScript source changes to the actual miniapp runtime `.js` files loaded by WeChat DevTools.
- [x] 3.2 Verify target runtime `.js` files are not empty templates and include the expected share methods.
- [x] 3.3 Confirm no new self-drawn WeChat share, close, or capsule controls are introduced in WXML/WXSS.

## 4. Tests And Evidence

- [x] 4.1 Add or update miniapp static tests for `onShareAppMessage` and `onShareTimeline` on all four target pages.
- [x] 4.2 Add or update static tests for product-list share query retention and encoding.
- [x] 4.3 Add or update tests that detect `.ts` share logic drifting from runtime `.js` share logic.
- [x] 4.4 Record DevTools 320 / 375 / 430 pt or equivalent static viewport evidence for share direct-open, native capsule reserve, back fallback, and content offset.
- [x] 4.5 Record real-device evidence, or mark `blocked` / `follow_up` with reason and remaining risk.

## 5. Documentation And Validation

- [x] 5.1 Update implementation trace or acceptance evidence with share matrix results for home, SKU detail, product list, and brand detail.
- [x] 5.2 If implementation unexpectedly adds or changes API contracts, synchronize OpenAPI, Orval, docs, and tests before completion.
- [x] 5.3 If implementation unexpectedly adds persistence, synchronize SQLite/MySQL schema, database docs, and tests before completion.
- [x] 5.4 Run focused tests for miniapp static behavior and any touched backend/API code.
- [x] 5.5 Run `openspec validate add-miniapp-wechat-share-pages --strict` before marking tasks complete.
