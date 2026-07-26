## 背景

`BUG-0078` 反馈生产环境微信小程序商品详情页品牌卡片跳转至搜索页，而不是品牌详情页。该缺陷关联 `REQ-0044-miniapp-sku-detail-page`，影响 SKU 商品详情页到品牌主页的核心浏览链路。

## 根因

直接原因是 SKU 详情聚合接口返回的 `brand.brand_entry_path` 指向搜索页：

```text
/pages/search/index?brandId=<brand_id>
```

品牌列表页和品牌详情页已经约定品牌主页路径为：

```text
/pages/brand-detail/index?brandId=<brand_id>
```

小程序 `brand-card` 组件按设计优先使用 `brand_entry_path` 跳转，只有缺失时才进入品牌关键词搜索 fallback。因此当接口返回搜索页路径时，前端行为虽符合组件契约，但业务路径错误。

## 修复方案

1. 在 SKU 详情服务层修正 `MiniappSkuBrandInfo.brand_entry_path` 的组装逻辑。
2. 将 `GET /api/v1/miniapp/skus/{sku_id}` 响应中的 `data.brand.brand_entry_path` 从搜索页路径改为品牌详情页路径。
3. 保持字段名、Pydantic schema、API 路径和响应结构不变。
4. 保持品牌卡片组件 fallback 规则不变：仅当 `brand_entry_path` 缺失但品牌名称可用时，才 fallback 到品牌关键词搜索页。

## 测试策略

- 后端测试：更新 SKU 详情接口成功用例，断言 `data.brand.brand_entry_path == "/pages/brand-detail/index?brandId=<brand_id>"`。
- 回归测试：保留品牌列表页 `brand_entry_path` 指向品牌详情页的既有断言。
- 小程序静态测试：确认 SKU 详情页仍使用 `brand-card`，品牌详情页仍在 `app.json` 注册。
- 负向风险：不新增接口字段，不触发数据库迁移；若实现阶段发现 schema 变化，需同步 OpenAPI / Orval / docs。

## 非目标

- 不新增品牌详情页能力。
- 不改造搜索页。
- 不新增管理端品牌配置。
- 不新增数据库字段或迁移。
- 不调整品牌详情页视觉、Tab 内容或证书展示。
- 不新增购物车、下单、支付、库存、促销、询价承诺等交易能力。
