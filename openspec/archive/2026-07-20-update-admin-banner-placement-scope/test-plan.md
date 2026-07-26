---
change_id: update-admin-banner-placement-scope
status: proposed
created_at: 2026-07-20 18:55:00
updated_at: 2026-07-20 18:55:00
---

# Test Plan

## Backend

- Banner create/update: valid miniapp home carousel succeeds.
- Banner create/update: valid miniapp brand-list carousel succeeds.
- Banner create/update: `WEB_HOME`, `TOPIC`, `HOME_MID_SLOT`, `TOPIC_TOP_BANNER` and unknown values fail validation.
- Banner list/summary: old data is excluded after migration.
- Migration: old records deleted, valid records preserved, media object keys not physically removed.

## Miniapp / API

- Home aggregation returns only home carousel.
- Brand list page query returns only brand-list carousel.
- Brand list page empty carousel does not fallback to home carousel.
- Public responses do not expose admin remarks, raw object keys, Authorization headers, cookies, or management-only fields.

## Web Admin

- Banner display client option scope is only “小程序”.
- Banner position options are only “首页轮播” and “品牌列表页轮播”.
- Create modal default is 小程序 + 首页轮播.
- Pagination DOM, MetricCard DOM, DS confirm, fixed toast and semantic token constraints remain intact.
- Banner modal width/cascade regression remains fixed.
- Banner upload state machine and same-session preview remain intact.

## Documentation / Generated

- OpenAPI updated if API schema changes.
- Orval generated client refreshed or documented as unchanged.
- API docs and database docs updated.
- `openspec validate update-admin-banner-placement-scope --strict` passes.
