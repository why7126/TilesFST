---
requirement_id: REQ-0047-product-list-common-component-application
title: 微信小程序商品列表页通用组件并应用
terminal: miniapp
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-07-19 01:21:11
updated_at: 2026-07-19 15:19:43
---

# 微信小程序商品列表页通用组件并应用需求文档

## 1. 背景

菲尚特微信小程序已经规划首页、分类列表页、搜索组件和 SKU 详情页，用户从分类、搜索、品牌或首页推荐进入商品浏览时，都需要稳定一致的商品列表体验。如果每个入口分别实现列表布局、筛选、排序、分页、加载态和空状态，后续容易出现交互差异、接口参数重复拼装和维护成本上升。

本需求沉淀微信小程序端可复用的商品列表页通用组件，并优先应用到分类商品列表与搜索结果中的 SKU 列表场景，统一商品展示、筛选排序、分页加载和异常状态。

## 2. 目标用户

| 用户 | 核心诉求 |
|---|---|
| 装修客户 | 从分类、搜索或首页入口快速浏览瓷砖商品，并进入 SKU 详情页继续了解 |
| 设计师 | 按空间、规格、色系、品牌等条件筛选候选商品，辅助方案选型 |
| 门店导购 | 在小程序内快速定位商品列表，并打开 SKU 详情页向客户介绍 |
| 普通访客 | 在不同浏览入口获得一致的列表、加载、空状态和返回体验 |

## 3. 范围

### 3.1 包含

- 微信小程序商品列表页通用容器：标题、来源上下文、列表区域、筛选/排序入口、加载与空状态。
- 微信小程序商品卡片组件：主图、商品名称、SKU 编码、品牌、分类、规格、参考价格和点击跳转。
- 分类商品列表应用：从分类页二级分类进入 `pages/product-list/index?categoryId={id}` 后展示对应商品。
- 搜索结果 SKU 列表应用：承接搜索关键词、筛选条件和排序条件，展示 SKU 结果。
- 分页或无限加载：首屏加载、下拉刷新、上拉加载更多、无更多数据状态。
- 筛选与排序接入：品牌、分类、规格、价格区间、推荐/最新/价格排序等基础能力。
- 状态治理：首次加载、局部加载、空列表、接口异常、图片失败和参数无效。
- 商品列表行为埋点：曝光、点击、筛选、排序、加载更多、刷新、异常。

### 3.2 不包含

- Web 管理端商品列表通用组件。
- 店主 Web 展示端商品列表通用组件。
- 后台商品管理列表改造、批量操作、上下架、库存、价格编辑等管理能力。
- 新增商品数据模型或商品后台录入能力。
- 购物车、询价、在线下单、客服找砖和收藏能力。
- 瀑布流、3D 展示、AR 铺贴预览或复杂推荐算法。

## 4. 页面与入口

| 入口 | 列表上下文 | 行为 |
|---|---|---|
| 分类页二级分类 | `categoryId` | 展示当前分类下可用 SKU，默认按后台推荐排序 |
| 搜索结果页 SKU Tab | `keyword` + filter | 展示命中关键词和筛选条件的 SKU 列表 |
| 首页推荐模块 | `source` + optional filter | 可复用列表组件展示推荐商品集合 |
| 品牌相关页面 | `brandId` | 可复用列表组件展示品牌下 SKU |

## 5. 功能要求

### FR-001 商品列表页通用容器

- 组件 MUST 支持外部传入列表来源、标题、查询参数、初始筛选条件和空状态文案。
- 组件 MUST 统一承载首屏加载、刷新、加载更多、无更多数据、空状态和错误状态。
- 组件 MUST 支持分类、搜索、品牌、推荐等不同上下文复用。
- 组件 MUST 避免业务页面重复实现分页状态机和列表异常处理。

### FR-002 商品卡片

- 商品卡片 MUST 展示主图、商品名称、SKU 编码、品牌、规格和参考价格。
- 商品卡片 SHOULD 展示分类名称或适用空间等辅助信息，但不得挤压核心标题和图片。
- 商品主图加载失败时 MUST 使用统一占位图或占位背景，不展示破图。
- 整个商品卡片 MUST 可点击并进入 SKU 详情页。
- v1 不在卡片上提供收藏、加入询价、购物车或快捷联系商家按钮。

### FR-003 查询参数与上下文

- 列表页 MUST 支持 `categoryId`、`keyword`、`brandId`、`spec`、`priceRange`、`sort`、`page` 和 `pageSize` 等基础参数。
- 当入口携带分类上下文时，筛选项 SHOULD 默认限制在该分类相关数据内。
- 当入口携带搜索关键词时，页面 MUST 保留关键词展示，并支持返回搜索页继续调整。
- 参数无效或对应分类/品牌已下架时 MUST 展示可恢复的空状态或返回提示。

### FR-004 筛选

- 列表页 MUST 提供品牌、分类、规格等基础筛选入口。
- 完整筛选 SHOULD 使用底部抽屉呈现，并支持重置和确认。
- 筛选确认后 MUST 重置分页并重新拉取第一页。
- 已选筛选项 SHOULD 在列表顶部以紧凑标签展示，并支持快速移除。
- 筛选项数量 SHOULD 基于当前上下文动态聚合；接口暂不支持时可先隐藏数量。

### FR-005 排序

- 列表页 MUST 支持默认排序。
- 列表页 SHOULD 支持最新、价格升序、价格降序等基础排序。
- 切换排序后 MUST 重置分页并回到列表顶部。
- v1 不支持个性化推荐排序、人工置顶配置或复杂多字段排序编辑。

### FR-006 分页与刷新

- 首屏 MUST 请求第一页数据。
- 下拉刷新 MUST 清空旧分页游标并重新请求第一页。
- 上拉加载更多 MUST 防止重复请求。
- 接口返回无更多数据时 MUST 展示统一无更多状态。
- 请求失败时 MUST 保留已加载数据，并提供重试入口。

### FR-007 空状态与异常

- 无商品时 MUST 根据上下文展示不同文案，例如分类无商品、搜索无结果、筛选无匹配。
- 搜索无结果 SHOULD 提示用户缩短关键词、替换品牌/规格或清空筛选。
- 网络异常 MUST 展示重试按钮。
- 图片失败、价格缺失、品牌缺失等单项异常不得导致整页不可用。

### FR-008 埋点

小程序商品列表 SHOULD 记录以下事件：

- `product_list_page_view`
- `product_list_item_exposure`
- `product_list_item_click`
- `product_list_filter_open`
- `product_list_filter_apply`
- `product_list_sort_change`
- `product_list_refresh`
- `product_list_load_more`
- `product_list_load_failed`

公共参数 SHOULD 包含 sourcePage、categoryId、brandId、keyword、filterSnapshot、sort、page、pageSize、resultCount、skuId 和 requestId。

## 6. UI 约束

- 视觉风格 MUST 与菲尚特小程序深色企业轻奢风保持一致。
- 商品列表 SHOULD 优先采用单列大卡或双列卡片中的一种，并在 `/req-complete` 阶段结合原型确定。
- 商品图片区域 MUST 使用稳定比例，避免加载前后卡片高度跳动。
- 筛选、排序、搜索上下文标签 SHOULD 保持紧凑，避免遮挡商品内容。
- 加载态、空状态、错误态和无更多状态 MUST 使用统一视觉语义。
- 可点击区域 SHOULD 不小于 44px，适配小程序触控场景。
- 不得在 v1 为商品卡片堆叠过多操作按钮，优先保证浏览和进入详情效率。

## 7. 关联需求

- `REQ-0045-category-list-page`：分类页二级分类点击后进入分类商品列表。
- `REQ-0046-search-component-application`：搜索结果中的 SKU 列表可复用商品列表组件。
- `REQ-0044-miniapp-sku-detail-page`：商品列表卡片点击后进入 SKU 详情页。
- `REQ-0041-miniapp-home`：首页推荐或搜索入口可复用商品列表能力。

## 8. 状态块

```yaml
requirement_id: REQ-0047-product-list-common-component-application
status: done
terminal: miniapp
version: v1
source: capture.md
priority: P1
scope_summary: 微信小程序商品列表页通用组件、商品卡片、分类/搜索/品牌等入口应用、筛选排序、分页加载和状态治理
excluded_scope:
  - Web 管理端商品列表组件
  - 店主 Web 商品列表组件
  - 后台商品管理列表改造
  - 商品数据模型新增
  - 购物车、询价、在线下单、收藏
next: /opsx-apply add-miniapp-product-list-component
```
