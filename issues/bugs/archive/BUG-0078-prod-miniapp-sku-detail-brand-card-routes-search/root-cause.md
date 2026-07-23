---
bug_id: BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search
status: done
created_at: 2026-07-21 14:40:30
updated_at: 2026-07-22 09:00:40
classification: api/code
related_requirement: REQ-0044-miniapp-sku-detail-page
related_change:
---

# Root Cause - BUG-0078 生产环境小程序商品详情页品牌卡片误跳搜索页

## 直接原因

SKU 详情聚合接口返回给小程序的品牌入口路径不正确。

当前 `GET /api/v1/miniapp/skus/{sku_id}` 在组装 `brand.brand_entry_path` 时返回 `/pages/search/index?brandId=<brand_id>`。小程序 `brand-card` 组件点击品牌卡片时会优先使用接口返回的 `brand_entry_path` 跳转，因此用户点击商品详情页品牌卡片后进入搜索页，而不是品牌详情页。

## 根本原因

根本原因是 SKU 详情接口与品牌入口页 / 品牌详情页之间的路由契约不一致：

- 品牌列表页和品牌详情页约定品牌主页路径为 `/pages/brand-detail/index?brandId=<brand_id>`。
- SKU 详情聚合接口的品牌信息却将 `brand_entry_path` 指向搜索页。
- 现有回归测试覆盖了品牌列表页的 `brand_entry_path`，但缺少 SKU 详情接口中 `brand.brand_entry_path` 必须指向品牌详情页的断言。
- 小程序 `brand-card` 组件设计为信任 `brand_entry_path`，没有在已有有效 `brand_id` 时强制改写为品牌详情页路径。

因此，只要 SKU 详情接口返回搜索页路径，前端就会稳定跳转到搜索页。

## 触发条件

满足以下条件时可稳定触发：

1. 打开微信小程序生产环境。
2. 进入一个公开 SKU 商品详情页。
3. 当前 SKU 关联启用品牌，且页面展示品牌卡片。
4. 点击品牌卡片。
5. 接口返回的 `brand.brand_entry_path` 为 `/pages/search/index?brandId=<brand_id>`。

## 分类

| 分类 | 判断 |
|---|---|
| api | 是。SKU 详情接口返回的品牌入口路径与品牌主页路由契约不一致 |
| code | 是。服务层组装 `brand_entry_path` 时写入了搜索页路径 |
| ux | 是。品牌卡片文案和用户预期是查看品牌主页，但实际进入搜索页 |
| design | 否。品牌详情页和品牌入口能力已存在，问题不是信息架构新增 |
| db | 否。无需新增或调整数据库字段 |
| security | 否。未发现权限、上传、密钥或敏感信息风险 |

## 证据

| 位置 | 证据 |
|---|---|
| `src/backend/app/services/miniapp_home_service.py` | SKU 详情 `brand_entry_path` 当前组装为 `/pages/search/index?brandId={record.brand_id}` |
| `src/backend/app/services/miniapp_home_service.py` | 品牌列表卡片 `_to_brand_card()` 组装为 `/pages/brand-detail/index?brandId={record.id}` |
| `src/miniapp/components/brand-card/index.ts` | `openBrand()` 使用 `normalized.entryPath || fallbackSearchPath(...)` 作为跳转 URL |
| `src/miniapp/app.json` | 已注册 `pages/brand-detail/index`，品牌详情页路由存在 |

## 影响判断

该缺陷影响 SKU 商品详情页到品牌主页的核心浏览链路。用户仍可查看商品详情页主体内容，也可通过其他入口进入品牌页，因此暂不构成 blocker；但生产环境品牌入口误跳会持续降低品牌主页可达性和浏览转化，建议进入常规 BUG 修复流程。
