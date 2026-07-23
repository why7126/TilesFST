---
bug_id: BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search
status: done
created_at: 2026-07-21 14:40:30
updated_at: 2026-07-22 09:00:40
related_requirement: REQ-0044-miniapp-sku-detail-page
related_change:
---

# Acceptance - BUG-0078 生产环境小程序商品详情页品牌卡片误跳搜索页

## 回归验收标准

- [ ] AC-BUG-001 `GET /api/v1/miniapp/skus/{sku_id}` 返回的 `data.brand.brand_entry_path` MUST 指向 `/pages/brand-detail/index?brandId=<brand_id>`。
- [ ] AC-BUG-002 商品详情页品牌卡片点击后 MUST 跳转到当前 SKU 关联品牌的品牌详情页。
- [ ] AC-BUG-003 品牌详情页 MUST 收到正确 `brandId`，并能加载对应品牌信息。
- [ ] AC-BUG-004 点击商品详情页品牌卡片 MUST 不再跳转到 `/pages/search/index` 或搜索结果页。
- [ ] AC-BUG-005 品牌列表页品牌卡片、首页 Banner 品牌跳转和品牌详情页分享路径 MUST 不受本修复影响。
- [ ] AC-BUG-006 SKU 未关联可访问品牌或品牌信息不可用时 MUST 展示明确不可查看提示，不得误导跳转搜索页。
- [ ] AC-BUG-007 修复 MUST 补充或更新后端测试，覆盖 SKU 详情接口中的 `brand.brand_entry_path`。
- [ ] AC-BUG-008 若仅调整响应字段值且不改变字段结构，MUST 明确说明不需要 OpenAPI / Orval；若实际改变 API 字段或 schema，MUST 同步 OpenAPI、Orval、接口文档和测试。
- [ ] AC-BUG-009 修复不得新增购物车、下单、支付、库存、促销、询价承诺或其他 `REQ-0044` 范围外能力。

## 验收证据要求

| 类型 | 要求 |
|---|---|
| API 证据 | 测试或接口响应证明 SKU 详情 `brand.brand_entry_path` 为品牌详情页路径 |
| 小程序交互证据 | 微信开发者工具、体验版或真机点击商品详情页品牌卡片进入品牌详情页 |
| 回归证据 | 品牌列表页品牌卡片仍进入品牌详情页 |
| 负向证据 | 点击商品详情页品牌卡片不进入搜索页 |
| 影响说明 | 明确是否影响 API 字段结构、数据库、小程序页面和 Orval |

## 非目标

- 本 BUG 不要求新增品牌详情页能力。
- 本 BUG 不要求改造搜索页能力。
- 本 BUG 不要求新增或修改数据库字段。
- 本 BUG 不要求新增管理端品牌配置项。
- 本 BUG 不要求调整品牌详情页视觉设计或 Tab 内容。
