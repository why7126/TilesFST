---
change_id: fix-miniapp-telemetry-request-amplification
change_type: fix
status: archived
source_bug: BUG-0143-miniapp-telemetry-request-amplification
sprint: sprint-026
created_at: 2026-08-25 23:05:00
updated_at: 2026-08-27 23:19:01
---

# Change 追踪

## 基本信息

```yaml
change_id: fix-miniapp-telemetry-request-amplification
change_type: fix
status: archived
source_bug: BUG-0143-miniapp-telemetry-request-amplification
sprint: sprint-026
affected_capabilities:
  - real-user-performance-monitoring
  - product-usage-logging
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
orval_required: false
docker_compose_required: false
product_data_collection_observability:
  status: applicable
  standard: docs/standards/product-data-collection-observability.md
  affected_layers:
    - miniapp_request_wrapper
    - miniapp_usage_event_client
    - miniapp_real_user_performance_client
  reason: 修复小程序启动阶段遥测请求自我放大和商品卡曝光逐条上报，直接影响行为埋点、RUM 采集和小程序请求封装边界。
  not_applicable:
    api: 未新增或修改后端 usage-events、performance-events 或业务 API 契约。
    database: 未新增或修改 usage_events、request_logs、task_traces 或 task_trace_spans 表结构、索引、迁移和保留周期。
    web: 未修改 Web 管理端或店主 Web 展示端请求封装和埋点。
    admin: 未修改管理端日志审计、观测查询或权限边界。
    task_trace: 未修改后端 Task Trace helper、任务链路或流程节点。
  validation:
    - `uv run pytest tests/test_miniapp_static.py -q` 通过，覆盖小程序请求封装、RUM 过滤和商品卡曝光去重聚合静态契约。
    - `uv run pytest tests/test_miniapp_home.py -q` 通过，覆盖 usage event 字典、聚合 `product_card_exposure` payload 和禁止字段校验。
    - `node --check src/miniapp/services/api.js`、`node --check src/miniapp/services/performance.js`、`node --check src/miniapp/components/product-card/index.js` 通过。
    - DevTools Network 截图显示首页冷启动按 `event` 过滤后共 7 条 event 相关请求，其中 `performance-events` 3 条、`usage-events` 4 条。
```

## 缺陷来源

- BUG：`issues/bugs/archive/BUG-0143-miniapp-telemetry-request-amplification/`
- Sprint：`iterations/archive/sprint-026/`
- 根因状态：`confirmed`
- 目标：阻断 usage-events 自身触发 RUM，并控制商品卡曝光逐条上报导致的请求放大。

## 证据清单

| 证据 | 状态 | 说明 |
|---|---|---|
| 根因分析 | done | 见 BUG-0143 `root-cause.md`。 |
| 小程序代码定位 | done | `track()`、统一 `request()`、`reportPerformanceMetric()`、商品卡 observer 已定位。 |
| OpenSpec delta | done | 已覆盖 RUM 遥测边界与 usage 曝光控制。 |
| 单元或静态测试 | done | `uv run pytest tests/test_miniapp_static.py -q` 通过，覆盖小程序请求封装、RUM 过滤和曝光聚合静态契约。 |
| 后端字典测试 | done | `uv run pytest tests/test_miniapp_home.py -q` 通过，覆盖聚合 `product_card_exposure` payload 仍被 usage event 字典接受。 |
| JS 语法检查 | done | `node --check` 覆盖 `services/api.js`、`services/performance.js`、`components/product-card/index.js`。 |
| 冷启动网络证据 | done | `issues/bugs/archive/BUG-0143-miniapp-telemetry-request-amplification/screenshots/20260826080932-devtools-network-home-startup.png` 与 `issues/bugs/archive/BUG-0143-miniapp-telemetry-request-amplification/screenshots/20260826081200-devtools-network-event-filter.png` 显示首页冷启动 Network 共 27 requests；按 `event` 过滤后共 7 条 event 相关请求，其中 `performance-events` 3 条、`usage-events` 4 条，并保留 `home` 与 `products?page=1&page_size=...` 业务请求。 |
| API / Orval 决策 | done | 采用小程序端去重与聚合单事件上报，不新增后端 API，不涉及 DB 结构和 Orval。 |
| 产品数据采集与链路观测门禁 | done | 适用于小程序请求封装、usage event 客户端与 RUM 客户端；API、DB、Web、管理端和 Task Trace 均不适用，原因已在 `product_data_collection_observability` 中声明。 |

## 归档前文档同步结论

- 长期产品、部署、数据库与 API 文档：不适用。本次修复仅调整小程序端遥测请求边界和曝光上报压力控制，不新增后端 API、错误码、Schema、OpenAPI、Orval、数据库结构、环境变量或部署拓扑。
- OpenSpec：适用。delta spec 覆盖 `real-user-performance-monitoring` 与 `product-usage-logging` 两个能力，归档时合并至正式规格。
- Issue 验收：适用。BUG-0143 `acceptance.md` 已记录自动化测试、JS 语法检查和 DevTools Network 截图证据。
- 产品数据采集与链路观测：适用。按照 `docs/standards/product-data-collection-observability.md` 记录适用层级、N/A 原因和验证摘要。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-25 23:05:00 | `/bug-opsx` | 从 BUG-0143 创建 OpenSpec fix Change，等待 Workflow Sync 回填 Sprint scope。 |
| 2026-08-25 23:24:00 | `/opsx-apply` | 完成小程序遥测请求边界、商品卡曝光去重聚合、聚焦测试与影响结论；冷启动网络面板证据待人工补证。 |
| 2026-08-26 08:09:32 | `/opsx-apply` | 补充 DevTools Network 人工截图证据，确认启动阶段 usage/performance 请求已收敛。 |
| 2026-08-26 08:13:23 | `/opsx-apply` | 补充 `event` 过滤截图，将证据数量修正为 3 条 performance-events 与 4 条 usage-events。 |
| 2026-08-27 23:14:46 | `/opsx-archive` | 补齐产品数据采集与链路观测归档门禁声明，明确 API、DB、Web、管理端和 Task Trace 不适用原因。 |
| 2026-08-27 23:19:01 | `/opsx-archive` | Change 归档后同步 trace 状态为 archived。 |
