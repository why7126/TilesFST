---
created_at: 2026-07-19 18:26:06
updated_at: 2026-07-19 18:26:06
---

# fix-miniapp-home-recommendation-routing

## Why

`BUG-0067-home-recommendation-list-entry-routing` 已评审并纳入 `sprint-009`。微信小程序首页的「新品榜」「热销榜」快捷入口，以及「新品推荐」「热销推荐」模块的「查看更多」当前仍跳转到 `/pages/search/index?section=...`，与 `REQ-0047-product-list-common-component-application` 已交付的商品列表页入口能力不一致。

该偏差导致首页推荐流量无法进入新品/热销商品列表页，搜索页也被迫承接非搜索语义入口。需要通过 fix Change 收敛首页推荐与榜单入口路由，使其进入商品列表页并携带 `section=new|hot`。

## What Changes

- 修改首页快捷入口策略：`新品榜` / `热销榜` 进入 `/pages/product-list/index?section=new|hot`。
- 修改首页推荐模块「查看更多」策略：`新品推荐` / `热销推荐` 进入商品列表页对应 `section`。
- 保留搜索页边界：搜索框、搜索关键词入口和 Banner `jump_type=search` 继续进入搜索页。
- 同步 `.ts` 与微信开发者工具实际加载的 `.js` 首页路由逻辑。
- 补充静态回归测试，防止首页推荐和榜单入口再次回退到搜索页。

## Impact

- 影响终端：微信小程序。
- 影响页面：`pages/index/index` 与 `pages/product-list/index` 路由契约。
- API：不新增接口；复用 `/api/v1/miniapp/products?section=new|hot`。
- 数据库：不涉及表结构或数据迁移。
- Orval：不需要。
- Docker Compose：不需要专项验证。

## Rollback Plan

如修复后商品列表页承接出现不可恢复问题，可在同一 Change 的回滚提交中将首页新品/热销入口临时恢复为安全提示或已有可返回页面；不得恢复到错误的搜索页语义作为长期方案。回滚后必须保留测试用例并调整断言为临时降级行为，直到商品列表承接恢复。
