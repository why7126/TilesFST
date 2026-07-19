---
requirement_id: REQ-0051-category-list-product-list-entry-by-level
status: pending_review
created_at: 2026-07-19 14:58:41
updated_at: 2026-07-19 14:58:41
owner: product
source: acceptance.md
---

# 小程序原型说明

## 1. 原型文件

| 文件 | 说明 |
|---|---|
| `prototype.html` | 分类页入口与商品列表页上下文的静态 HTML 原型，用于表达一级分类聚合入口、二级分类精确入口和列表页标题语义 |
| `prototype.png` | 待后续从 HTML 导出；非阻塞 |

## 2. 页面结构

```text
CategoryPage
├── CustomNavigation
├── CategoryBody
│   ├── PrimaryCategoryNav
│   │   └── PrimaryCategoryItem[]      # tap = 切换一级分类
│   └── SecondaryCategoryPanel
│       ├── PrimaryCategoryHeader
│       │   ├── CurrentPrimaryName
│       │   └── ViewAllProductsEntry   # tap = 一级分类聚合列表
│       └── SecondaryCategoryGrid
│           └── SecondaryCategoryCard[] # tap = 二级分类精确列表
└── CustomTabBar

ProductListPage
├── CustomNavigation(title = categoryName)
├── ContextBar(categoryLevelLabel)
├── FilterSortBar
├── ProductList
└── Empty/Error/LoadMoreState
```

## 3. 关键交互

- 左侧一级分类项只负责切换当前一级分类。
- 右侧标题区提供“查看全部商品”入口，进入一级分类聚合商品列表。
- 二级分类卡片进入二级分类精确商品列表。
- 一级/二级入口均需要防重复点击。
- 商品列表页返回分类页后，分类页保留当前一级分类和滚动位置。

## 4. 参数策略

| 入口 | categoryId | categoryName | categoryLevel | sourcePage |
|---|---|---|---|---|
| 一级分类商品入口 | 一级分类 ID | 一级分类名称 | `primary` | `category` |
| 二级分类商品入口 | 二级分类 ID | 二级分类名称 | `secondary` | `category` |

## 5. 状态策略

| 状态 | 处理 |
|---|---|
| 一级分类无启用二级分类 | 入口可展示不可用态，或进入列表后展示分类无商品空状态 |
| 一级分类聚合无商品 | 商品列表页展示分类无商品空状态 |
| 二级分类无商品 | 商品列表页展示分类无商品空状态 |
| 参数无效/分类下架 | 商品列表页展示可恢复提示 |
| 网络异常 | 商品列表页展示重试；有缓存时不清空分类页 |

## 6. 后续实现提示

- 优先在右侧一级分类标题区增加入口，避免改变左侧一级分类导航的既有 tap 语义。
- 商品列表接口或查询层需要显式支持 `categoryLevel=primary` 的子分类聚合语义。
- 若接口仅支持二级分类 ID，后续 Change 必须说明一级分类 ID 到二级分类 ID 集合的展开位置。
