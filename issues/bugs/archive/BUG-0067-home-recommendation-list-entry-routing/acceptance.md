---
bug_id: BUG-0067-home-recommendation-list-entry-routing
status: done
created_at: 2026-07-19 15:43:52
updated_at: 2026-07-19 19:31:31
related_requirement: REQ-0047-product-list-common-component-application
source_change: add-miniapp-product-list-component
---

# Acceptance - BUG-0067 首页推荐模块查看更多和榜单入口误跳搜索页

## 回归验收标准

- [ ] AC-BUG-001 点击首页快捷入口「新品榜」时，进入 `/pages/product-list/index?section=new` 或等价商品列表页路径，不进入 `/pages/search/index?section=new`。
- [ ] AC-BUG-002 点击首页快捷入口「热销榜」时，进入 `/pages/product-list/index?section=hot` 或等价商品列表页路径，不进入 `/pages/search/index?section=hot`。
- [ ] AC-BUG-003 点击「新品推荐」模块「查看更多」时，进入新品推荐商品列表页，列表页接收 `section=new` 并展示「新品榜」或等价标题。
- [ ] AC-BUG-004 点击「热销推荐」模块「查看更多」时，进入热销推荐商品列表页，列表页接收 `section=hot` 并展示「热销榜」或等价标题。
- [ ] AC-BUG-005 首页搜索框、Banner `jump_type=search` 和商品列表页内搜索入口仍进入搜索页，不因本修复改变搜索场景路由。
- [ ] AC-BUG-006 `src/miniapp/pages/index/index.ts` 与微信开发者工具实际加载的 `src/miniapp/pages/index/index.js` 路由逻辑保持一致。
- [ ] AC-BUG-007 商品列表页通过 `/api/v1/miniapp/products` 携带 `section=new|hot` 请求公开 SKU，分页、筛选、排序和商品详情跳转保持可用。
- [ ] AC-BUG-008 补充 `tests/test_miniapp_static.py` 或等价静态测试，断言首页推荐和榜单入口使用 `/pages/product-list/index?section=`，且不再包含 `/pages/search/index?section=` 作为这些入口的目标。

## 验收证据要求

| 类型 | 要求 |
|---|---|
| 源码 | `src/miniapp/pages/index/index.ts` 与 `src/miniapp/pages/index/index.js` 同步修复 |
| 模板 | `src/miniapp/pages/index/index.wxml` 中新品/热销入口继续绑定正确 handler 和 `data-section` |
| 静态测试 | 覆盖首页 quick entry 与推荐模块「查看更多」跳转目标 |
| 接口回归 | 复用或补充 `/api/v1/miniapp/products?section=new|hot` 的后端测试，确认公开 SKU 过滤/排序仍可用 |
| 人工验收 | 在微信开发者工具中分别点击 4 个入口，确认进入商品列表页而不是搜索页 |

## 非目标

- 本 BUG 不要求新增商品列表页 UI 能力。
- 本 BUG 不要求修改后端商品列表 API 契约。
- 本 BUG 不要求调整新品定义、热销排序算法或商品推荐算法。
- 本 BUG 不要求改动 Web 管理端、店主 Web 展示端或小程序其它 Tab 的导航结构。
