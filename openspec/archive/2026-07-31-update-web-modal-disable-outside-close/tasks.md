## 1. Discovery

- [x] 1.1 Inventory Web admin standard Dialog / Modal usage across SKU, brand, category, certificate, Banner, user, system settings, password, and log-related surfaces.
- [x] 1.2 Inventory Web catalog standard Dialog / Modal usage for product detail, brand detail, image preview, contact, or consultation surfaces.
- [x] 1.3 Identify shared Dialog / Modal wrappers versus feature-local custom modal implementations.
- [x] 1.4 Record any reviewed exceptions where outside click close must remain enabled.

## 2. Core Implementation

- [x] 2.1 Update shared Dialog / Modal or equivalent wrapper so backdrop, overlay, and outside empty-area clicks do not close by default.
- [x] 2.2 Update feature-local custom modal implementations that do not inherit the shared wrapper.
- [x] 2.3 Preserve explicit close paths: close icon, cancel button, back button, Esc where documented, and business-completion close.
- [x] 2.4 Update confirmation dialogs so outside click keeps the dialog open while cancel, close icon, Esc, or explicit action ends the flow.
- [x] 2.5 Keep Popover, Dropdown, Tooltip, Select dropdown, date picker, and equivalent lightweight overlays unchanged unless listed as reviewed exceptions.

## 3. Regression Coverage

- [x] 3.1 Add or update front-end tests for at least one form dialog: outside click keeps the dialog open and preserves input state.
- [x] 3.2 Add or update front-end tests for at least one confirmation dialog: outside click keeps the dialog open and does not call the target API.
- [x] 3.3 Add or update tests for explicit close affordances so dialogs remain closable after outside click is disabled.
- [x] 3.4 If upload-containing dialogs are touched, verify upload state `idle -> uploading -> done/failed`, same-session preview, and failed-state messaging.
- [x] 3.5 If upload transport, Nginx, or storage code is not touched, document Docker `:3000` upload boundary verification as N/A with reason.

## 4. UI / Design System Validation

- [x] 4.1 Verify admin modal TSX does not combine `modal-card` with feature-specific modal card classes where this change touches modal DOM.
- [x] 4.2 Verify 1440px computed width for wide and narrow admin modals affected by this change.
- [x] 4.3 Verify short viewport modal body scroll keeps header, footer, close icon, upload controls, and action buttons reachable.
- [x] 4.4 Verify no raw Hex colors or one-off modal visual system are introduced.

## 5. Documentation And Trace

- [x] 5.1 Update implementation notes or change trace with inventory results and exception list.
- [x] 5.2 Reference REQ-0084 `knowledge_base_refs` in design or apply evidence.
- [x] 5.3 Record validation results for functional AC and AC-XCUT items.
