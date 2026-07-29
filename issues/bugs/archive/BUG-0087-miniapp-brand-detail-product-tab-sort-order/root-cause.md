---
bug_id: BUG-0087-miniapp-brand-detail-product-tab-sort-order
status: done
created_at: 2026-07-28 22:36:46
updated_at: 2026-07-29 07:54:10
classification: code/design
related_requirement: REQ-0058-brand-detail-home-page
related_change:
---

# Root Cause - BUG-0087 品牌详情页商品 Tab 排序未按发布时间升序和 ID 升序

## 直接原因

品牌详情页商品 Tab 请求 `GET /api/v1/miniapp/products?brandId=<brandId>&page=<page>&pageSize=<pageSize>` 时未携带专门的品牌商品排序参数，因此后端进入 `/miniapp/products` 的通用默认排序分支。

当前后端公开商品列表通用默认排序为：

```text
t.updated_at DESC, t.id DESC
```

这会让品牌详情页商品 Tab 按更新时间倒序和 ID 倒序返回，而不是按期望的发布时间升序、ID 升序稳定展示。

## 根本原因

根本原因是品牌详情页商品 Tab 的业务排序契约没有被单独固化：

- 品牌详情页商品 Tab 需要的是“品牌主页内商品陈列顺序”，期望按发布时间升序、ID 升序。
- 后端 `/miniapp/products` 同时承载普通商品列表、分类列表、品牌商品列表、新品榜、热销榜和部分兼容筛选场景。
- 现有排序函数只提供通用 `default`、价格排序和热度优先排序，未区分 `brandId` 场景。
- 品牌详情页前端请求未显式声明排序意图，导致品牌商品 Tab 被通用默认排序接管。
- 现有测试缺少“品牌过滤场景下默认排序为发布时间升序、ID 升序”的断言。

## 触发条件

满足以下条件时可稳定触发：

1. 同一品牌下存在多条公开 SKU。
2. 这些 SKU 的 `published_at` 或历史空值兜底字段 `created_at` 存在先后顺序。
3. 用户打开微信小程序品牌详情页，并查看商品 Tab。
4. 品牌详情页请求 `/api/v1/miniapp/products` 时仅携带 `brandId`、分页参数，未携带品牌商品专用排序。
5. 后端使用通用默认排序返回数据。

## 分类

| 分类 | 判断 |
|---|---|
| code | 是。后端查询排序逻辑未覆盖品牌商品 Tab 期望排序 |
| design | 是。`/miniapp/products` 多入口复用时缺少品牌过滤场景的排序契约 |
| api | 轻微相关。可在不改变响应结构的情况下修复；若新增排序参数或字段才需要同步 API 契约 |
| db | 已确认。当前 `tiles.published_at` 已存在并由 SKU 发布流程维护，本修复无需 DB 变更；历史空值用 `created_at` 兜底排序 |
| ui | 轻微相关。前端需保持后端返回顺序，不应自行重排 |
| security | 否。未发现权限、上传、密钥或敏感信息风险 |

## 证据

| 位置 | 证据 |
|---|---|
| `src/miniapp/pages/brand-detail/index.ts` | 品牌详情页商品 Tab 请求 `/api/v1/miniapp/products?brandId=...&page=...&pageSize=...` |
| `src/backend/app/repositories/miniapp_home_repository.py` | `_product_order_sql(sort="default")` 返回 `t.updated_at DESC, t.id DESC` |
| `src/backend/app/services/miniapp_home_service.py` | `search_products()` 将 `brand_id` 透传给 repository，但未对品牌场景指定发布时间升序排序 |

## 影响判断

该缺陷不阻断品牌详情页加载，也不会导致商品不可点击，但会影响品牌主页商品陈列顺序的稳定性和验收一致性。由于排序错误会影响运营期望、分页稳定性和用户浏览顺序，严重等级维持 `medium`。

## 待确认事项

- “发布时间”在当前实现中使用独立字段 `published_at`；历史空值使用 `created_at` 兜底，禁止使用 `updated_at` 冒充发布时间。
- 修复范围是否限定为 `brandId` 过滤场景，避免影响普通商品列表、搜索页、新品榜和热销榜。
