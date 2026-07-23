## 1. API 修复

- [x] 1.1 定位 `src/backend/app/services/miniapp_home_service.py` 中 `get_sku_detail()` 的 `MiniappSkuBrandInfo.brand_entry_path` 组装逻辑。
- [x] 1.2 将 SKU 详情品牌入口路径修正为 `/pages/brand-detail/index?brandId=<brand_id>`。
- [x] 1.3 确认字段名、Pydantic schema、API 路径和统一响应结构不变。

## 2. 回归测试

- [x] 2.1 更新 `tests/test_miniapp_home.py`，断言 `GET /api/v1/miniapp/skus/{sku_id}` 返回的 `data.brand.brand_entry_path` 指向品牌详情页。
- [x] 2.2 回归品牌列表页品牌卡片入口仍返回 `/pages/brand-detail/index?brandId=<brand_id>`。
- [x] 2.3 回归小程序静态测试，确认 SKU 详情页仍使用 `brand-card`，品牌详情页仍注册在 `app.json`。
- [x] 2.4 如字段结构未变化，在实现输出中说明不需要 OpenAPI / Orval；如实际改变 API 字段或 schema，必须同步 OpenAPI、Orval、`docs/03-api-index.md` 和相关测试。

## 3. 验收与追踪

- [x] 3.1 验证商品详情页品牌卡片点击后进入对应品牌详情页，不再进入搜索页。
- [x] 3.2 验证品牌详情页收到正确 `brandId` 并加载对应品牌信息。
- [x] 3.3 更新 `BUG-0078` trace、Change trace 与验收证据。
- [x] 3.4 修复完成后评估是否需要沉淀到 `docs/knowledge-base/incidents/`；若无复用价值，在验收输出中说明不新增知识库条目。
