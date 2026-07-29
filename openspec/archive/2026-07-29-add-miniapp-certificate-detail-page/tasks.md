## 1. Backend / API Contract

- [x] 1.1 Audit current miniapp certificate list response and brand certificate data model to identify reusable fields for detail page.
- [x] 1.2 Add or extend public certificate detail service/repository logic with hidden, soft-delete, and non-public-brand filtering.
- [x] 1.3 Add `GET /api/v1/miniapp/certificates/{certificateId}` or equivalent public detail route using unified response envelope.
- [x] 1.4 Return certificate public fields, brand entry data, image list/main image, old single-file fallback, PDF/file metadata, and share payload.
- [x] 1.5 Ensure detail response never exposes admin notes, audit fields, internal user fields, raw object keys, local paths, secrets, cookies, Authorization headers, bucket internals, or unauthorized storage URLs.
- [x] 1.6 Add or update error handling for missing, invalid, hidden, deleted, and non-public certificate detail requests.

## 2. Miniapp Detail Page

- [x] 2.1 Register `pages/certificate-detail/index` or the confirmed equivalent route.
- [x] 2.2 Implement certificate detail loading state, error state, unavailable state, media hero, certificate summary, brand entry, info panel, description panel, and bottom actions.
- [x] 2.3 Implement image preview from current image with multi-image switching and stable fallback for failed image loads.
- [x] 2.4 Implement PDF or file opening via controlled URL, `wx.openDocument`, copy fallback, or project-confirmed equivalent.
- [x] 2.5 Implement brand entry navigation using `brandId` and safe fallback when brand entry is unavailable.
- [x] 2.6 Implement `onShareAppMessage` with certificate title, `certificateId`, source parameters, and main-image fallback.
- [x] 2.7 Implement custom-navigation back fallback for share-direct, loading, error, and unavailable states.
- [x] 2.8 Ensure page does not render price, favorite, recommendations, cart, buy, stock, promotion, or inquiry modules.

## 3. Miniapp Entry Integration

- [x] 3.1 Change certificate list card main click to navigate to certificate detail with `certificateId`, source, index, and request context.
- [x] 3.2 Keep file preview behavior available from the detail page and remove direct card-main preview coupling.
- [x] 3.3 Add brand detail certificate area navigation to certificate detail if that area exists in current miniapp scope; otherwise document N/A in acceptance evidence.
- [x] 3.4 Add tracking events for detail view, media switch, image preview, file open, brand click, share click, and load failures.

## 4. API / DB / Docs Sync

- [x] 4.1 Update OpenAPI and Orval or miniapp service-layer contract if the public certificate detail API is added or changed.
- [x] 4.2 Update `docs/03-api-index.md` with request, response, and error code summary for the detail API.
- [x] 4.3 Update `docs/04-database-design.md` and migrations only if new certificate/detail/share/image fields are required.
- [x] 4.4 Update error code documentation if new certificate detail errors are introduced.

## 5. Tests and Evidence

- [x] 5.1 Add backend tests for detail success, not found, hidden, deleted, non-public brand filtering, old single-file compatibility, multi-image main ordering, and safe file URLs.
- [x] 5.2 Add miniapp static or page tests for route registration, list-to-detail navigation, detail rendering, media states, share payload, brand entry, and forbidden modules not appearing.
- [x] 5.3 Add tests or fixtures for PDF/unknown/missing-file fallback and image load failure behavior.
- [x] 5.4 Record DevTools 320/375/430 pt evidence for normal, loading, error, no-image/PDF, and share-direct states.
- [x] 5.5 Record real-device evidence or mark blocked/follow_up with reason; do not report real-device pass without evidence.

## 6. Workflow Closure

- [x] 6.1 Run relevant backend pytest and miniapp static tests.
- [x] 6.2 Run OpenSpec validation for `add-miniapp-certificate-detail-page`.
- [x] 6.3 Run Workflow Sync after apply and archive events as required.
