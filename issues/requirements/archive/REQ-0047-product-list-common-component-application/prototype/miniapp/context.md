---
requirement_id: REQ-0047-product-list-common-component-application
status: pending_review
created_at: 2026-07-19 01:25:41
updated_at: 2026-07-19 01:25:41
owner: product
source: acceptance.md
---

# 小程序原型说明

## 1. 原型文件

| 文件 | 说明 |
|---|---|
| `prototype.html` | 商品列表页静态 HTML 原型，用于表达页面结构、卡片密度、筛选排序入口和状态区域 |
| `prototype.png` | 待后续从 HTML 导出；非阻塞 |

## 2. 页面结构

```text
ProductListPage
├── SafeAreaHeader
│   ├── BackButton
│   ├── ContextTitle
│   └── SearchSummary
├── FilterSortBar
│   ├── FilterButton
│   ├── SortButton
│   └── ActiveFilterChips
├── ProductList
│   └── ProductCard[]
├── LoadMoreState
└── FilterDrawer
```

## 3. 关键交互

- 返回按钮回到来源页面，不能清空来源页面原有滚动或选中状态。
- 筛选按钮打开底部抽屉，抽屉内支持重置和确认。
- 排序入口展示默认、最新、价格升序、价格降序。
- 商品卡片整卡点击进入 SKU 详情页。
- 下拉刷新和上拉加载更多由页面容器统一处理。

## 4. 状态策略

| 状态 | 处理 |
|---|---|
| 首屏加载 | 使用与商品卡片比例一致的骨架屏 |
| 有结果 | 展示商品卡片列表和筛选排序入口 |
| 无商品 | 展示上下文相关文案 |
| 筛选无匹配 | 展示清空筛选入口 |
| 加载更多 | 底部展示加载中，不遮挡现有商品 |
| 无更多 | 底部展示轻量无更多状态 |
| 网络异常 | 保留已有数据并提供重试 |

## 5. 后续实现提示

- 优先复用搜索组件的关键词展示和筛选入口模式。
- 商品列表容器需要隔离分页状态，避免分类、搜索、品牌页面重复实现。
- 商品卡片图片比例应稳定，避免真实图片加载后改变列表高度。
