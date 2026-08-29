---
bug_id: BUG-0143-miniapp-telemetry-request-amplification
created_at: 2026-08-25 22:44:14
updated_at: 2026-08-25 22:44:14
---

# 临时规避

## 可用规避

在正式修复前，可采用以下临时方式降低影响：

1. 本地调试时在微信开发者工具网络面板中按业务接口过滤，暂时排除 `/api/v1/usage-events` 与 `/api/v1/performance-events`，避免埋点噪音干扰功能排查。
2. 观察性能报表时，临时排除 `page_key=/api/v1/usage-events` 的 RUM 样本，避免把埋点接口自身耗时误读为业务 API 性能。
3. 若测试环境写入量明显影响调试，可暂时减少首页测试数据中的新品、热销和第一页商品数量，降低商品卡曝光事件数量。

## 不建议规避

- 不建议直接关闭后端 usage-events 或 performance-events 接口，否则会影响其他页面真实行为与性能观测。
- 不建议在后端静默丢弃全部小程序埋点，否则会掩盖真实数据质量问题。
- 不建议通过删除商品卡曝光事件定义规避；应在小程序端补充去重、采样或批量策略。

## 后续修复后处理

修复完成后，需要重新冷启动小程序首页，确认：

1. usage-events 请求数量不再随首屏卡片数量逐条膨胀。
2. performance-events 不再包含 usage-events 请求自身的 API duration。
3. 首页业务 API 性能上报仍保留。
