## Overview

本变更修复 BUG-0087 的排序契约偏差。品牌详情页商品 Tab 是品牌主页中的商品陈列视图，用户和运营预期是按发布时间从早到晚稳定浏览当前品牌公开 SKU。当前实现复用 `/api/v1/miniapp/products` 通用默认排序，而通用默认排序为更新时间倒序，因此需要在品牌过滤场景中提供独立排序规则。

## Root Cause

- 品牌详情页商品 Tab 请求 `/api/v1/miniapp/products?brandId=<brandId>&page=<page>&pageSize=<pageSize>`。
- 后端 `MiniappHomeRepository.list_products()` 通过 `_product_order_sql(sort="default", hot_first=False)` 生成通用默认排序。
- 通用默认排序当前为 `t.updated_at DESC, t.id DESC`。
- `brandId` 场景未被识别为品牌主页商品陈列语义，导致品牌详情页商品 Tab 被更新时间倒序接管。

## Decisions

- 修复范围限定为品牌过滤场景：当请求携带 `brandId` 且没有显式进入热销、新品、价格或搜索相关排序时，后端默认返回发布时间升序、ID 升序。
- “发布时间”使用当前 SKU 数据模型中的独立字段 `t.published_at`；历史空值使用 `t.created_at` 兜底，避免空值导致排序不稳。
- 不在本变更中新增数据库字段，避免把排序修复扩大为数据模型迁移。
- 前端品牌详情页继续按接口返回顺序追加展示，不在小程序端做跨页排序。
- 保持搜索页 `list_search_products()` 相关性排序、新品榜 `only_new` 召回规则、热销榜 `hot_first` 排序不变。

## Implementation Notes

- 可在 service 或 repository 层增加品牌过滤排序分支，确保 `brand_id` 场景使用发布时间升序、ID 升序。
- 当前实现使用 `published_at` 作为发布时间，历史空值以 `created_at` 兜底，排序为：

```text
COALESCE(t.published_at, t.created_at) ASC, t.id ASC
```

## Validation

- 后端测试：构造同一品牌下多条公开 SKU，验证 `/api/v1/miniapp/products?brandId=...` 返回发布时间升序、ID 升序。
- 分页测试：使用至少超过一页的数据或模拟分页，验证第一页和第二页合并后顺序稳定且无重复遗漏。
- 回归测试：验证搜索页相关性排序、新品榜和热销榜不受品牌过滤排序修复影响。
- 手工/小程序验证：品牌详情页商品 Tab 首屏与加载更多顺序与 API 一致。

## Risks

- 如果“发布时间”字段语义不清，可能在实现阶段将 `published_at`、`created_at`、`updated_at` 混用。实现说明必须明确字段映射，禁止使用 `updated_at` 冒充发布时间。
- 如果直接修改通用默认排序，可能误改普通商品列表、分类商品列表或首页瀑布流顺序。实现应限定品牌过滤场景。
- 如果前端自行排序，跨页数据可能出现顺序漂移。排序应由后端统一完成。
