---
change_id: fix-miniapp-telemetry-request-amplification
change_type: fix
status: applied
source_bug: BUG-0143-miniapp-telemetry-request-amplification
sprint: sprint-026
created_at: 2026-08-25 23:05:00
updated_at: 2026-08-26 08:13:23
---

# Change 追踪

## 基本信息

```yaml
change_id: fix-miniapp-telemetry-request-amplification
change_type: fix
status: applied
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
```

## 缺陷来源

- BUG：`issues/bugs/review/BUG-0143-miniapp-telemetry-request-amplification/`
- Sprint：`iterations/change/sprint-026/`
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
| 冷启动网络证据 | done | `issues/bugs/review/BUG-0143-miniapp-telemetry-request-amplification/screenshots/20260826080932-devtools-network-home-startup.png` 与 `issues/bugs/review/BUG-0143-miniapp-telemetry-request-amplification/screenshots/20260826081200-devtools-network-event-filter.png` 显示首页冷启动 Network 共 27 requests；按 `event` 过滤后共 7 条 event 相关请求，其中 `performance-events` 3 条、`usage-events` 4 条，并保留 `home` 与 `products?page=1&page_size=...` 业务请求。 |
| API / Orval 决策 | done | 采用小程序端去重与聚合单事件上报，不新增后端 API，不涉及 DB 结构和 Orval。 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-25 23:05:00 | `/bug-opsx` | 从 BUG-0143 创建 OpenSpec fix Change，等待 Workflow Sync 回填 Sprint scope。 |
| 2026-08-25 23:24:00 | `/opsx-apply` | 完成小程序遥测请求边界、商品卡曝光去重聚合、聚焦测试与影响结论；冷启动网络面板证据待人工补证。 |
| 2026-08-26 08:09:32 | `/opsx-apply` | 补充 DevTools Network 人工截图证据，确认启动阶段 usage/performance 请求已收敛。 |
| 2026-08-26 08:13:23 | `/opsx-apply` | 补充 `event` 过滤截图，将证据数量修正为 3 条 performance-events 与 4 条 usage-events。 |
