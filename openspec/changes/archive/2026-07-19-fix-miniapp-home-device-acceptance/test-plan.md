---
change_id: fix-miniapp-home-device-acceptance
created_at: 2026-07-19 18:14:29
updated_at: 2026-07-19 18:14:29
---

# Test Plan

## Automated

- Run `uv run pytest tests/test_miniapp_static.py`.
- If implementation changes `src/miniapp/pages/index/` or custom navigation files, add or update static tests for:
  - real runtime entry is not an empty template;
  - custom navigation is declared on the homepage;
  - WXML / WXSS does not hand-draw WeChat share, close, or capsule controls;
  - safe-area, top spacer, bottom spacer, and basic click-target constraints remain present.

## Manual DevTools

- Open `src/miniapp/` in WeChat DevTools.
- Visit `pages/index/index`.
- Capture evidence for 320、375、390、430 pt and at least one common width in 320-430 pt.
- Record DevTools version, base library version, page path, width, screenshot or summary, time, executor, and conclusion.

## Manual Device

- Use a real device where feasible.
- Record device model, OS version, WeChat version, base library version, page path, user state, screenshot or video reference, and conclusion.
- If real-device validation is unavailable, mark it as `blocked` or `follow_up` and do not claim real-device pass.

## Regression Focus

- Homepage first screen core modules.
- Native capsule and status-bar avoidance.
- fixed header and bottom TabBar not covering content.
- Empty / failed image / failed request states.
- No API, DB, Web, admin, Orval, or Docker Compose changes unless evidence exposes a separate defect.
