## Why

`BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search` 已评审通过。生产环境微信小程序 SKU 商品详情页中，用户点击品牌卡片后进入搜索页，而不是对应品牌详情页，导致商品详情页到品牌主页、品牌商品和品牌证书的浏览链路被打断。

根因是 SKU 详情聚合接口在返回品牌展示对象时，将 `brand.brand_entry_path` 组装为 `/pages/search/index?brandId=<brand_id>`。小程序品牌卡片组件会优先使用该路径跳转，因此前端稳定进入搜索页。

## What Changes

- 修改 SKU 详情接口品牌入口路径规范：`GET /api/v1/miniapp/skus/{sku_id}` 返回的 `data.brand.brand_entry_path` MUST 指向 `/pages/brand-detail/index?brandId=<brand_id>`。
- 要求商品详情页品牌卡片点击后进入对应品牌详情页，不再进入搜索页。
- 补充后端回归测试，覆盖 SKU 详情接口中的 `brand.brand_entry_path`。
- 回归品牌列表页品牌卡片、首页 Banner 品牌跳转和品牌详情页分享路径不受影响。
- 明确本修复仅调整响应字段值，不新增字段、不改变 schema、不修改数据库结构、不新增交易类能力。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `miniapp-sku-detail-page`: 修正 SKU 详情页品牌入口路径契约，确保品牌卡片进入品牌详情页。

## Impact

- **api:** 修改 `GET /api/v1/miniapp/skus/{sku_id}` 响应中既有字段 `data.brand.brand_entry_path` 的取值；字段名和 schema 不变。实现时需更新后端测试；若实际改变字段结构，必须同步 OpenAPI、Orval、接口文档和测试。
- **miniapp:** SKU 详情页品牌卡片将按接口返回路径进入品牌详情页；品牌卡片组件本身的 fallback 规则预计无需改动。
- **database:** 不涉及表结构、迁移或数据修复。
- **web/admin:** 不涉及。
- **tests:** 需要补充或更新 `tests/test_miniapp_home.py`，断言 SKU 详情接口品牌入口路径为品牌详情页；建议回归小程序静态测试中品牌详情页和品牌卡片契约。

## Rollback Plan

如修复后 SKU 详情页品牌卡片无法进入品牌详情页或引入接口回归，可回滚服务层 `brand_entry_path` 组装逻辑到修复前版本，并保留本 Change 文档记录回滚原因。回滚后 `BUG-0078` 不得关闭，需重新评估是品牌详情页参数、品牌可见性还是前端导航失败导致。
