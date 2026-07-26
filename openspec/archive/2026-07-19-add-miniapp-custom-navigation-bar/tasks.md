## 1. OpenSpec / Planning

- [x] 1.1 Validate this Change references `REQ-0042-custom-navigation-bar` and modifies `miniapp-home`.
- [x] 1.2 Confirm Sprint trace includes REQ-0042 in `sprint-008` before implementation.

## 2. Miniapp Implementation

- [x] 2.1 Inspect `src/miniapp/pages/index/index.wxml`, `.wxss`, and `.ts/.js` runtime facts for the current `brand-header`.
- [x] 2.2 Refactor homepage top brand area so custom navigation includes brand Logo, store name, and subtitle.
- [x] 2.3 Remove `store-link` / "门店信息" from custom navigation semantics and UI.
- [x] 2.4 Ensure the custom navigation area is not bound wholesale to `openStoreInfo`.
- [x] 2.5 Reserve safe right-side space for WeChat Mini Program native share and close controls.
- [x] 2.6 Use miniapp native share behavior such as `onShareAppMessage` or platform menu support; do not draw share / close / capsule lookalikes.
- [x] 2.7 Keep the search box below the custom navigation bar and route it to existing search capability.
- [x] 2.8 Preserve REQ-0043 homepage structure: dark visual baseline, Banner, four entries, new/hot recommendations, all-product waterfall, and target TabBar labels.

## 3. State / Fallback

- [x] 3.1 Add or verify safe fallback for missing brand Logo, store name, and subtitle.
- [x] 3.2 Confirm loading, network failure, and return-to-home scenarios keep navigation height and content stable.

## 4. Tests / Validation

- [x] 4.1 Add or update static miniapp tests for no `store-link` / "门店信息" inside custom navigation.
- [x] 4.2 Add or update static miniapp tests to prevent default custom navigation binding to `openStoreInfo`.
- [x] 4.3 Add or update static checks for no hand-drawn share / close / capsule controls in the page.
- [x] 4.4 Validate 320-430 pt layout manually or with screenshot evidence; brand content must not overlap right-side native controls.
- [x] 4.5 Verify no API / DB / Orval changes. If that changes, update OpenAPI, Orval, docs, DB docs/schema, and tests before marking complete.

## 5. Documentation / Trace

- [x] 5.1 Update implementation acceptance notes with native share / close verification evidence.
- [x] 5.2 Run OpenSpec validation for `add-miniapp-custom-navigation-bar`.
- [x] 5.3 Run Workflow Sync after apply/archive steps as required.
