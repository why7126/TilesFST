## 1. 事件字典与小程序 payload 修复

- [x] 1.1 梳理 `src/miniapp/**` 当前所有 `track()` 字面量事件，并列出动态事件名样例。
- [x] 1.2 补齐后端 `EVENT_DEFINITIONS` 中收藏页事件：`favorite_list_page_view`、`favorite_list_load_failed`、`favorite_list_empty_action_click`、`favorite_list_item_click`、`favorite_list_remove`。
- [x] 1.3 补齐品牌详情页事件：`brand_detail_view`、`brand_detail_tab_click`、`brand_products_load`、`brand_products_load_more`、`brand_products_load_failed`、`brand_certificates_load`、`brand_certificates_load_failed`、`brand_certificate_click`。
- [x] 1.4 补齐商品卡片事件：`product_card_exposure`、`product_card_click`、`product_card_unavailable_click`、`product_card_image_failed`。
- [x] 1.5 补齐品牌卡片事件：`brand_card_click`、`brand_card_unavailable_click`、`brand_card_image_failed`。
- [x] 1.6 统一小程序 payload 字段，确保每个合法事件包含后端 required 字段。
- [x] 1.7 保留未知事件和禁止属性拒绝逻辑，不接受任意 `event_name`。

## 2. 回归测试

- [x] 2.1 增加后端测试，覆盖本 Change 新增或修正的全部小程序合法事件返回 200。
- [x] 2.2 增加写入验证，确认合法事件写入 `usage_events` 且 `client_type=wechat_miniapp`。
- [x] 2.3 增加防漂移测试：小程序 `track()` 字面量事件必须在后端事件字典中有定义。
- [x] 2.4 为动态事件名调用点维护测试样例，避免只覆盖字面量事件。
- [x] 2.5 保留并扩展负向测试：未知事件返回 400，禁止字段返回 400。

## 3. 文档与生成物同步

- [x] 3.1 若 API Schema 或错误响应细节变化，同步 OpenAPI、Orval、`docs/03-api-index.md` 和 API 测试。
- [x] 3.2 若仅补齐事件字典且接口 Schema 不变，在实现输出中说明不需要 Orval。
- [x] 3.3 如测试发现数据库字段不足，先补充 DB 设计、schema、migration 和测试；否则明确不涉及 DB 变更。

## 4. 验收与追溯

- [x] 4.1 在微信开发者工具 macOS / mp 2.01.2510290 / lib 3.16.2 环境复测关键页面。
- [x] 4.2 验证收藏页、品牌详情页、SKU 详情页品牌入口、商品/品牌卡片组件不再大量出现 `POST /api/v1/usage-events 400`。
- [x] 4.3 更新 `BUG-0072` trace、Change trace 与验收证据。
- [x] 4.4 修复完成后评估是否需要沉淀到 `docs/knowledge-base/incidents/`；若无复用价值，在验收输出中说明不新增知识库条目。
