---
sprint_id: sprint-009
status: planning
created_at: 2026-07-19 12:50:12
updated_at: 2026-07-19 15:52:45
---

# sprint-009 发布说明草案

## 发布主题

微信小程序商品浏览、分类导航、顶部导航、首页推荐入口与搜索体验优化。

## 计划范围

| 类型 | 编号 | 标题 | 发布说明 |
|---|---|---|---|
| REQ | REQ-0049-miniapp-product-card-component | 微信小程序商品卡片组件 | 统一小程序各类商品列表中的商品卡片展示、图片占位、点击跳转和异常状态 |
| REQ | REQ-0050-miniapp-brand-header-page-title-rules | 小程序 brand-header 页面标题规则 | 统一首页双行品牌文案与非首页单行标题规则，优化返回、状态栏和微信原生胶囊避让体验 |
| REQ | REQ-0051-category-list-product-list-entry-by-level | 分类列表页支持一二级分类商品列表入口 | 支持从一级分类查看下属二级分类商品聚合结果，并保留二级分类精确商品列表入口 |
| BUG | BUG-0066-search-component-prototype-deviation | 搜索组件整体交互与原型差异较大 | 修复小程序搜索页与 REQ-0046 原型在搜索首页、联想、结果、筛选和无结果状态上的体验偏差 |
| BUG | BUG-0067-home-recommendation-list-entry-routing | 首页推荐模块查看更多和榜单入口误跳搜索页 | 修复首页新品榜、热销榜和推荐模块「查看更多」误入搜索页的问题，进入对应商品列表页 |

## 当前状态

- Sprint 状态：planning
- OpenSpec Change：待 `/req-opsx REQ-0049-miniapp-product-card-component`、`/req-opsx REQ-0050-miniapp-brand-header-page-title-rules`、`/req-opsx REQ-0051-category-list-product-list-entry-by-level`、`/bug-opsx BUG-0066-search-component-prototype-deviation` 与 `/bug-opsx BUG-0067-home-recommendation-list-entry-routing` 创建
- 发布结论：待实现与验收后更新

## 不包含

- 商品列表容器、筛选、排序、分页状态机
- SKU 详情页能力
- Web 端商品卡片
- 商品后台管理和交易能力
- 三级及以上分类模型、后台分类管理或分类页直接展示商品卡片
- 后台搜索配置中心、热门词维护、同义词维护或自然语言搜索
- brand-header 后台文案配置、底部 TabBar 改造或小程序整体视觉重设计
- 商品列表页 UI 重构、后端 section 语义调整或推荐算法调整
