---
title: 小程序商品列表排序最佳实践
purpose: 统一小程序公开 SKU 列表跨入口默认排序、分页稳定性和不影响分支验收
content: 小程序商品列表排序 best-practice
source: BUG-0091-miniapp-product-list-sort-consistency
update_method: 小程序商品列表排序、搜索相关性或分页契约变化时更新
owner: 小程序负责人
status: draft
created_at: 2026-07-30 23:52:59
updated_at: 2026-07-30 23:52:59
note: 适用于品牌、分类、关键词商品列表排序相关 BUG、REQ 和 OpenSpec Change
---

# 小程序商品列表排序最佳实践

## 适用范围

适用于 `GET /api/v1/miniapp/products` 支撑的小程序商品列表页，包括品牌过滤、一级分类聚合、二级分类精确查询和普通关键词查询。

不适用时必须写明 N/A reason，例如：仅修改首页推荐卡片样式、仅修改商品详情页媒体展示、仅修改后台 SKU 管理列表。

## 排序事实源

- 后端公开 SKU 查询是分页排序事实源，小程序端不得在分页追加后做跨页重排。
- 品牌、分类和普通关键词入口在 `sort=default` 且非 `section=new|hot` 时，默认按 `COALESCE(published_at, created_at) ASC, id ASC` 返回。
- `published_at` 为空的历史 SKU 使用 `created_at` 兜底；多条 SKU 排序时间相同时，使用 SKU ID 升序稳定排序。
- 搜索页若显式使用相关性排序，相关性优先；同相关性或无差异时使用发布时间升序、SKU ID 升序兜底。

## 不影响分支

排序修复必须明确不改变以下分支：

- 首页“全部产品”无筛选列表。
- 新品榜 `section=new`。
- 热销榜 `section=hot`。
- 价格升序 / 降序。
- 搜索页显式相关性排序的优先级。

## 验收矩阵

| 场景 | 必验点 |
|---|---|
| 品牌过滤 | 与品牌主页商品 Tab 默认顺序一致 |
| 一级分类聚合 | 覆盖一级直挂 SKU 和启用二级分类 SKU |
| 二级分类精确 | 只返回该二级分类公开 SKU，并保持默认排序 |
| 普通关键词 | 匹配结果使用默认排序，不使用更新时间倒序 |
| 分页加载更多 | 多页合并后无重复、漏项或已加载顺序跳动 |
| 回归分支 | 首页全部产品、新品榜、热销榜和价格排序不变 |

## 测试建议

- 样本应覆盖不同 `published_at`、相同 `published_at`、空 `published_at`、不同 SKU ID。
- 后端测试应直接断言分页合并后的 SKU 编码顺序。
- 小程序静态或页面测试应确认列表入口携带 `keyword`、`categoryId`、`categoryLevel`、`brandId`、`sourcePage`，并确认没有端侧本地重排逻辑。
