## Context

REQ-0042 is an approved and in-sprint refinement of `REQ-0041-miniapp-home`, with `REQ-0043-miniapp-home-style-optimization` as the current visual and information architecture baseline.

Existing homepage structure already has a `brand-header` above the search box:

- `store-logo`
- `store-name`
- `store-subtitle`
- `store-link` / "门店信息"

This Change narrows the intended custom navigation semantics: the brand display portion becomes the custom navigation bar, while "门店信息" remains outside this navigation bar. The right side must preserve WeChat Mini Program native share and close controls instead of page-rendered lookalikes.

## Requirement Readiness Report

Result: **Ready**.

- `requirement.md`: present, status `in_sprint`.
- `user-stories.md`: present.
- `business-flow.md`: present.
- `acceptance.md`: present.
- `trace.md`: present, status `in_sprint`, iteration `sprint-008`.
- `prototype/miniapp/context.md` and `prototype.html`: present.

## Impact Analysis

```yaml
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - miniapp-home
change_type: update
```

## Conflict Report

Priority used:

```text
REQ-0043 prototype.html / prototype.png
  > REQ-0042 prototype/miniapp/context.md
  > REQ-0042 acceptance.md
  > rules/ui-design.md
  > openspec/specs/miniapp-home/spec.md
```

Resolved conflicts:

- Existing `miniapp-home` spec says Header must not simulate WeChat status bar, share button, close button, or capsule controls. REQ-0042 keeps this gate but clarifies that native WeChat Mini Program share and close controls are required on the right.
- Existing home implementation has `store-link` / "门店信息" inside `brand-header`. REQ-0042 excludes it from custom navigation semantics and requires removing default `openStoreInfo` binding from the custom navigation bar.
- REQ-0043 dark homepage remains the visual baseline. REQ-0042 must not restore the earlier warm white homepage or old five-entry structure.

## Design Decisions

### D1. Custom Navigation Boundary

The custom navigation bar is the brand display area above the search box. It includes brand logo, store name, and subtitle. It excludes store detail navigation.

Implementation should avoid making the whole brand area a tap target for `openStoreInfo`. If the home page still needs a store info entry, it must be placed outside this custom navigation area or covered by a future requirement.

### D2. Native Right-Side Controls

The right side of the custom navigation area must reserve space for WeChat Mini Program native share and close controls. The page must not draw custom WXML / WXSS controls that visually imitate the system capsule, share button, or close button.

Share behavior should use standard miniapp share capabilities such as `onShareAppMessage` or platform menu behavior. Close behavior must remain native miniapp behavior.

### D3. Search Remains Below Navigation

The search box remains below the custom navigation bar and continues to route to the existing search page. The navigation bar must not add a second main search entry.

### D4. No API / DB Expansion By Default

Brand copy and logo reuse the home store / brand data already available through the homepage flow. Missing logo/name/subtitle must use safe local or text fallback. If implementation discovers a backend contract gap, that gap must be explicitly reflected in this Change before code implementation expands API / DB / Orval.

## Validation Strategy

- Static miniapp checks should verify the home navigation no longer includes `store-link` as part of custom navigation and is not bound wholesale to `openStoreInfo`.
- Static checks should detect hand-drawn system-control lookalikes where feasible, especially custom elements named or styled as capsule/share/close controls inside the home page.
- Visual/manual validation should cover 320-430 pt widths and confirm brand content does not overlap native right-side controls.
- Existing homepage modules from REQ-0043 must remain: search, Banner, four entries, new/hot recommendations, all-product waterfall, and target TabBar labels.
