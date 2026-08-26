## 背景

BUG-0144 发现 BUG-0143 治理后，小程序商品列表页与搜索页仍可能产生偏多 `/api/v1/usage-events` 请求。根因已确认为列表页页面级曝光、商品卡组件曝光、搜索结果曝光和搜索输入事件之间缺少统一口径、频控和去重窗口，导致同一 SKU 或同一次搜索上下文可能被重复计入，连续输入也可能按字符变化放大事件数量。

该问题关联 `BUG-0144-miniapp-usage-events-overreporting`，已评审通过并纳入 `sprint-026`。

## 变更内容

- 明确商品列表页曝光主口径：同一批 SKU 不得被无边界地同时计入 `product_list_item_exposure` 与 `product_card_exposure`。
- 为商品列表页、搜索结果页和通用 `product-card` 组件建立共享曝光去重策略，去重键至少覆盖页面、来源模块、列表上下文、SKU、搜索关键词或列表请求上下文、`requestId` 等维度。
- 对搜索页 `search_input` 增加防抖、合并、采样或等价频控策略，避免连续输入时 usage-events 随字符变化线性增长。
- 明确搜索结果曝光与商品卡曝光的边界：结果级事件用于结果集合或模块语义，卡片级事件用于 SKU 卡片语义；同一搜索上下文内不得重复解释为多次真实曝光。
- 保持后端事件字典、禁止字段校验和埋点失败不阻断主流程的既有边界。

## 能力范围

### 新增能力

- 无。

### 修改能力

- `product-usage-logging`：补充小程序商品列表、搜索和商品卡片组件的曝光口径治理、搜索输入频控、曝光去重窗口和测试约束。

## 影响

- 小程序：影响 `src/miniapp/pages/product-list/`、`src/miniapp/pages/search/`、`src/miniapp/components/product-card/` 和小程序 usage tracking helper。
- 后端 API：默认不新增接口，沿用既有 `POST /api/v1/usage-events`；如实现选择批量接收接口，必须同步 OpenAPI、Orval、API 文档、错误码和测试。
- 数据库：默认不涉及结构变更；保留既有 usage events 存储模型。
- Web / 管理端 / 对象存储 / Docker Compose：不涉及功能变更。

## 回滚计划

- 若曝光去重误杀真实曝光，可回滚到较窄去重键或仅关闭受影响页面的去重窗口重用，保留搜索输入频控。
- 若搜索输入频控导致关键行为缺失，可临时保留提交、清空、取消等关键事件，降低或关闭逐字符输入事件。
- 若事件字典兼容失败，回滚 payload 字段调整并优先保持既有后端事件接收能力。
- 回滚后必须重新记录商品列表首屏、搜索连续输入和搜索结果展示的 `/api/v1/usage-events` 数量与事件名分布。
