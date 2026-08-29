---
bug_id: BUG-0143-miniapp-telemetry-request-amplification
acceptance_status: passed
created_at: 2026-08-25 22:44:14
updated_at: 2026-08-28 16:21:48
---

# 验收标准

## AC-001 遥测请求不再触发 API 性能埋点

给定小程序端调用 `track()` 上报 `/api/v1/usage-events`，当该请求成功或失败时：

- 不应额外调用 `reportPerformanceMetric()` 记录 usage-events 自身的 `api_duration` 或 `api_failed_duration`。
- `/api/v1/performance-events` 中不应出现 `page_key` 指向 `/api/v1/usage-events` 的样本。

## AC-002 首页业务请求性能观测不退化

给定小程序冷启动进入首页，当请求 `/api/v1/miniapp/home` 与 `/api/v1/miniapp/products` 时：

- 仍应正常上报业务 API 的 `api_duration`。
- `app_launch_ready` 性能事件仍应正常上报。
- 性能上报失败不得阻断首页加载。

## AC-003 商品卡曝光请求数量可控

给定首页同时渲染新品、热销和全部产品卡片，当同一页面、同一模块、同一 SKU 在首屏初始化或属性重复更新时：

- 不应重复上报同一曝光事件。
- usage-events 请求数量不应与卡片 observer 触发次数一比一增长。
- 若采用批量上报，单次 batch 应保持后端接口约束内，并保留必要事件属性。

## AC-004 行为事件字典与隐私约束保持有效

修复后，`product_card_exposure`、`miniapp_home_waterfall_load` 等事件仍应满足后端事件字典校验：

- 保留必填属性：`page_path`、`sourcePage`、`sourceModule`、`listContext`、`index`、`requestId`、`client_type` 等对应事件要求。
- 不得新增 Authorization header、Cookie、原始对象 key、内部备注、手机号、`.env` 内容或本机路径等敏感字段。
- 埋点失败仍不得阻断浏览、搜索、商品点击或分享。

## AC-005 回归测试覆盖

修复应补充或更新聚焦测试，覆盖：

- 小程序 `track()` 上报 usage-events 时不触发 RUM。
- 普通业务 `request()` 仍触发 `api_duration`。
- 商品卡曝光具备去重或批量行为，重复 observer 不导致重复请求。
- 事件 payload 仍通过后端 usage-events 字典校验。

## 自动化验证记录

| 命令 | 结果 | 覆盖 |
|---|---|---|
| `uv run pytest tests/test_miniapp_static.py -q` | passed，36 passed | 小程序请求封装、RUM 过滤、商品卡曝光去重聚合静态契约 |
| `uv run pytest tests/test_miniapp_home.py -q` | passed，44 passed | usage event 字典、聚合 `product_card_exposure` payload、禁止字段校验 |
| `node --check src/miniapp/services/api.js` | passed | 小程序 API 运行时语法 |
| `node --check src/miniapp/services/performance.js` | passed | 小程序 RUM 运行时语法 |
| `node --check src/miniapp/components/product-card/index.js` | passed | 商品卡组件运行时语法 |

## 人工补证记录

- 已补充 DevTools Network 截图：`issues/bugs/archive/BUG-0143-miniapp-telemetry-request-amplification/screenshots/20260826080932-devtools-network-home-startup.png`。
- 已补充 `event` 过滤截图：`issues/bugs/archive/BUG-0143-miniapp-telemetry-request-amplification/screenshots/20260826081200-devtools-network-event-filter.png`。
- 截图显示首页冷启动 Network 共 27 requests；按 `event` 过滤后共 7 条 event 相关请求，其中 `performance-events` 3 条、`usage-events` 4 条，并保留 `home` 与 `products?page=1&page_size=...` 业务请求。
- 截图未展示 Authorization header、Cookie、Token、真实客户隐私或本机路径。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-27 23:16:25
accepted_by: workflow-sync
source_change: fix-miniapp-telemetry-request-amplification
source_sprint: sprint-026
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

