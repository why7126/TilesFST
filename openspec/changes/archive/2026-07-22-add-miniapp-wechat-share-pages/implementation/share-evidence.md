---
change_id: add-miniapp-wechat-share-pages
requirement_id: REQ-0064-miniapp-wechat-share-pages
status: static_review
created_at: 2026-07-21 22:57:26
updated_at: 2026-07-21 22:57:26
---

# Share Evidence

## Static Share Matrix

| Page | Friend share | Timeline share | Key parameters | Result |
|---|---|---|---|---|
| `pages/index/index?source=share` | `onShareAppMessage` | `onShareTimeline` | `source=share` | static_review |
| `pages/tile-detail/index?skuId=1&source=share` | `onShareAppMessage` | `onShareTimeline` | `skuId=1`, `source=share` | static_review |
| `pages/product-list/index?keyword=%E5%AE%A2%E5%8E%85&sourcePage=share` | `onShareAppMessage` | `onShareTimeline` | `keyword`, `categoryId`, `categoryLevel`, `categoryName`, `brandId`, `section`, `sourcePage` whitelist | static_review |
| `pages/brand-detail/index?brandId=1&source=share` | `onShareAppMessage` | `onShareTimeline` | `brandId=1`, `source=share` | static_review |

## Navigation And Viewport Evidence

| Viewport | Source | Scope | Status | Conclusion |
|---|---|---|---|---|
| 320pt | static_test | share direct-open paths, native capsule reserve, back fallback, content offset | static_review | Source keeps `custom-navigation`; target WXML/WXSS do not add fake share, close, or capsule controls. |
| 375pt | static_test | share direct-open paths, native capsule reserve, back fallback, content offset | static_review | Existing custom-navigation fallback returns to `/pages/index/index`; no new fixed header or bottom action layout introduced. |
| 430pt | static_test | share direct-open paths, native capsule reserve, back fallback, content offset | static_review | `.js` runtime entries include the same share methods as `.ts`; static checks are not reported as DevTools or real-device pass. |

## Runtime Entry Sync

- `pages/index/index.ts` and `pages/index/index.js` include `onShareAppMessage`, `onShareTimeline`, `trackHomeShare`, and `source=share`.
- `pages/tile-detail/index.ts` and `pages/tile-detail/index.js` include `onShareAppMessage`, `onShareTimeline`, `trackSkuShare`, `skuId`, `source=share`, and image fallback.
- `pages/product-list/index.ts` and `pages/product-list/index.js` include `PRODUCT_LIST_SHARE_KEYS`, `buildShareQuery`, encoded whitelist query, and `product_list_share_click`.
- `pages/brand-detail/index.ts` and `pages/brand-detail/index.js` include `onShareAppMessage`, `onShareTimeline`, `brandSharePath`, `brandId`, `source=share`, and `brand_detail_share_click`.

## Real Device Boundary

real_device_follow_up: Real-device validation is not available in this environment. Remaining risk is limited to WeChat client-specific timeline image rendering and physical device capsule metrics. This evidence is intentionally marked `static_review` / `real_device_follow_up`; it is not reported as DevTools or real-device pass.

## Security Boundary

Evidence and share helpers do not include Authorization, Cookie, `.env`, local absolute paths, raw object key, phone numbers, or raw page data serialization. Share paths use whitelisted route parameters and existing public media URLs or local fallback images only.
