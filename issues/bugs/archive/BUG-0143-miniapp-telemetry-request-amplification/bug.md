---
bug_id: BUG-0143-miniapp-telemetry-request-amplification
title: 微信小程序启动阶段埋点请求数量异常偏高
severity: medium
status: done
owner:
discovered_at: 2026-08-25 22:34:46
environment: local
related_requirement:
related_change: fix-miniapp-telemetry-request-amplification
updated_at: 2026-08-27 23:16:25
created_at: 2026-08-25 22:41:23
---

# 现象

启动微信小程序进入首页后，网络面板短时间内出现大量埋点请求：约 28 条 `/api/v1/performance-events` 请求与 25 条 `/api/v1/usage-events` 请求。请求数量明显高于首页首屏业务请求数量，容易造成启动阶段网络噪音、服务端写入放大和观测数据污染。

# 复现步骤

1. 启动本地后端服务与微信小程序开发环境。
2. 打开微信开发者工具，进入小程序首页。
3. 清空或观察网络面板中的启动阶段请求。
4. 统计 `/api/v1/performance-events` 与 `/api/v1/usage-events` 请求数量。
5. 对比首页业务接口、商品卡片数量与埋点接口请求数量。

# 期望 vs 实际

- 期望：小程序启动和首页首屏加载阶段只产生必要业务请求与少量聚合埋点；埋点请求自身不应继续触发性能埋点；商品卡曝光应具备去重、采样或批量上报能力，避免请求数量随卡片数量线性膨胀。
- 实际：启动首页后出现约 25 条 usage-events 请求；每条 usage-events 又通过统一请求层派生一条 performance-events，加上 app launch 与首页业务 API 性能事件后，performance-events 数量达到约 28 条。

# 影响范围

- 微信小程序首页冷启动和首屏加载体验。
- `/api/v1/usage-events` 行为埋点写入量与日志审计噪音。
- `/api/v1/performance-events` RUM 数据质量，尤其是 API 耗时指标中混入埋点接口自身耗时。
- 后端日志、数据库写入量、性能观测报表和本地开发调试效率。

# 严重等级说明

严重等级为 `medium`。该问题不会阻断用户浏览、搜索、商品点击或分享，但会稳定放大启动阶段网络请求数量，并污染 usage 与 performance 两类观测数据；若进入生产环境，可能持续增加日志和数据库写入成本。

# 初步线索

- `src/miniapp/services/api.ts` 的 `track()` 通过统一 `request()` 上报 `/api/v1/usage-events`。
- `src/miniapp/services/api.ts` 的统一 `request()` 会对每个 API 成功或失败请求调用 `reportPerformanceMetric()`，因此 usage-events 请求自身会继续产生 performance-events。
- `src/miniapp/components/product-card/index.ts` 在 `product` observer 中直接上报 `product_card_exposure`，首页新品、热销和全部产品卡片同时渲染时，会导致 usage-events 按卡片数量逐条增长。
- `src/miniapp/pages/index/index.ts` 首页加载还会触发 `miniapp_home_waterfall_load`，并请求首页聚合与商品分页接口；这些业务请求本身也会产生 API 性能事件。
openspec_changes:
  - change_id: fix-miniapp-telemetry-request-amplification
    type: fix
    status: archived
