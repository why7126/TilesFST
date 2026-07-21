---
requirement_id: REQ-0051-category-list-product-list-entry-by-level
status: done
created_at: 2026-07-19 14:58:41
updated_at: 2026-07-19 21:20:26
owner: product
source: requirement.md
---

# 验收清单

## 功能 AC

- [ ] AC-001 分类列表页允许用户从一级分类进入商品列表页。
- [ ] AC-002 分类列表页允许用户从二级分类进入商品列表页。
- [ ] AC-003 左侧一级分类点击继续用于切换当前一级分类，不得因新增商品列表入口破坏既有切换行为。
- [ ] AC-004 一级分类商品列表入口与一级分类切换交互有清晰区分，例如位于右侧当前一级分类标题区或等价区域。
- [ ] AC-005 一级分类商品列表入口跳转 `pages/product-list/index` 时携带 `categoryId={primaryId}`、`categoryName={encodedName}`、`categoryLevel=primary`、`sourcePage=category`。
- [ ] AC-006 二级分类商品列表入口跳转 `pages/product-list/index` 时携带 `categoryId={secondaryId}`、`categoryName={encodedName}`、`categoryLevel=secondary`、`sourcePage=category`。
- [ ] AC-007 一级分类商品列表展示该一级分类下所有启用二级分类商品的聚合结果。
- [ ] AC-008 一级分类商品列表不得错误地只展示直接挂载在一级分类下的商品。
- [ ] AC-009 二级分类商品列表仅展示该二级分类下商品。
- [ ] AC-010 若一级分类无启用二级分类，进入商品列表后展示分类无商品空状态或在入口侧提供不可用反馈。
- [ ] AC-011 若一级分类下启用二级分类均无商品，商品列表页展示分类无商品空状态。
- [ ] AC-012 若二级分类无商品，商品列表页展示分类无商品空状态。
- [ ] AC-013 分类已下架、参数无效或接口异常时，商品列表页展示可恢复提示和重试/返回能力，不得白屏。
- [ ] AC-014 一级和二级分类商品列表入口点击均在 300ms 内防重复触发，避免重复打开页面。
- [ ] AC-015 从商品列表或 SKU 详情返回分类页后，恢复当前一级分类、左侧滚动位置和右侧滚动位置。

## 商品列表上下文 AC

- [ ] AC-016 商品列表页可解析 `categoryLevel=primary|secondary`。
- [ ] AC-017 一级分类列表页标题使用一级分类名称，搜索提示和空状态体现一级分类上下文。
- [ ] AC-018 二级分类列表页标题使用二级分类名称，搜索提示和空状态体现二级分类上下文。
- [ ] AC-019 一级分类上下文中的筛选项限制在该一级分类聚合结果相关范围内。
- [ ] AC-020 二级分类上下文中的筛选项限制在该二级分类结果相关范围内。
- [ ] AC-021 商品列表页筛选、排序、分页、下拉刷新和上拉加载更多不得丢失 `categoryId` 与 `categoryLevel`。

## 埋点 AC

- [ ] AC-022 一级分类商品入口点击记录 `primary_category_product_list_click`，或在既有 `primary_category_click` 中携带 `action=product_list_entry`。
- [ ] AC-023 二级分类点击继续记录 `secondary_category_click`，并携带 `action=product_list_entry` 或等价跳转上下文。
- [ ] AC-024 商品列表页浏览埋点包含 `categoryId`、`categoryName`、`categoryLevel`、`sourcePage`、`resultCount` 和 `requestId`。
- [ ] AC-025 埋点不得记录手机号等与商品浏览无关的个人敏感信息。

## UI AC

- [ ] AC-UI-001 分类页继续沿用“工业石材 · 暗色旗舰风”，与现有小程序首页、分类页和商品列表页保持一致。
- [ ] AC-UI-002 新增一级分类商品入口不破坏现有左右双栏布局、底部 TabBar 和二级分类三列宫格。
- [ ] AC-UI-003 一级分类商品入口可点击区域不小于 44px。
- [ ] AC-UI-004 二级分类卡片可点击区域不小于 44px。
- [ ] AC-UI-005 新增入口使用品牌金或等价激活语义表达，但不得让页面变成大面积金色。
- [ ] AC-UI-006 页面标题、入口文案、空状态和错误状态文案不遮挡商品内容，且在小屏下不换行溢出。

## 文档与原型 AC

- [ ] AC-026 `prototype/miniapp/context.md` 与 `prototype/miniapp/prototype.html` 可作为后续设计与实现验收参考。
- [ ] AC-027 `prototype/miniapp/prototype.png` 可在后续从 HTML 导出；缺 PNG 不阻塞评审。
- [ ] AC-028 后续 `/req-opsx` 的 design.md 必须说明一级分类聚合查询策略、二级分类精确查询策略、分类层级参数、跳转防抖和埋点。
- [ ] AC-029 若后续实现新增或调整 API，必须同步 OpenAPI、Orval、接口文档和测试；若仅小程序消费已有接口，需在 Change 中说明复用依据。

## 横切 AC（knowledge-base）

本 REQ 为微信小程序访客端分类/商品列表入口，不命中 `req-complete` 规定的 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 标签；无需要转化的管理端横切 AC。
