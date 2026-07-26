## Why

REQ-0042 clarifies that the top brand area above the miniapp home search box must become the homepage brand custom navigation bar, while removing the misleading "门店信息" entry from that navigation semantics.

The current `miniapp-home` spec already covers the dark REQ-0043 homepage baseline, but it does not explicitly define the custom navigation boundary, the native share / close controls on the right, or the no-hand-drawn-system-controls gate.

## What Changes

- Add a `miniapp-home` requirement for the homepage brand custom navigation bar.
- Define the custom navigation source as the current home `brand-header` brand display area above the search box.
- Include brand logo, store name, brand subtitle, and right-side native WeChat Mini Program share / close controls.
- Exclude `store-link`, "门店信息", default `openStoreInfo` navigation, multi-store switching hints, and any hand-drawn share / close / capsule controls.
- Keep the search box below the custom navigation bar and preserve REQ-0043 dark homepage structure.
- Add validation gates for native-button avoidance, 320-430 pt layout, fallback brand copy, and no API / DB changes unless a later contract gap is explicitly approved.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `miniapp-home`: add homepage brand custom navigation bar behavior and validation requirements.

## Impact

- **Miniapp:** impacts `src/miniapp/pages/index/` WXML / WXSS / TS around the home `brand-header`, click behavior, native navigation safety area, and visual validation.
- **API:** no default API change; reuse existing home store / brand data. Any later contract gap must update OpenAPI, Orval, docs, and tests.
- **Database:** no default DB change.
- **Web / Admin:** not affected.
- **Storage:** no new object storage behavior; logo/media must remain safe public URL or local fallback.
- **Testing:** add or update static/miniapp validation for navigation content, no `store-link` inclusion, no `openStoreInfo` default binding, no hand-drawn system controls, and responsive layout.
