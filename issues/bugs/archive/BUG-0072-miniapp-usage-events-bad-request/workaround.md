---
bug_id: BUG-0072-miniapp-usage-events-bad-request
title: 微信小程序 usage-events 上报接口频繁返回 400
status: done
severity: high
created_at: 2026-07-21 14:41:14
updated_at: 2026-07-22 08:47:45
related_requirement: REQ-0024-product-usage-logging
related_change: fix-miniapp-usage-events-contract-drift
---

# 临时规避方案

当前无服务端配置级开关可以安全地绕过该问题。后端拒绝未知事件和敏感字段属于安全边界，不建议为了消除 400 噪音而放宽校验或接受任意事件。

# 可选临时措施

在正式修复前，可按风险由低到高选择以下临时措施：

| 措施 | 适用场景 | 风险 |
|---|---|---|
| 在小程序调试时过滤 `usage-events` 400 日志 | 开发者临时排查其他问题 | 只能减少噪音，不恢复统计 |
| 暂停高频未知事件上报 | 某个页面 400 严重刷屏 | 会进一步丢失行为统计 |
| 前端仅对明确已注册事件调用 `track()` | 临时发布止血 | 需要维护临时 allowlist，容易与后端再次漂移 |

# 不建议方案

- 不建议后端直接接受未知 `event_name`，否则会破坏事件字典治理，导致统计口径不可控。
- 不建议关闭禁止字段校验，否则可能引入 Authorization、Cookie、对象存储 key、原始 payload 等敏感信息写入日志的风险。
- 不建议在小程序端吞掉所有上报而不记录，因为这会隐藏合法行为统计缺失。

# 推荐处理策略

该缺陷应通过常规修复闭环：

1. 后端补齐小程序合法事件定义。
2. 小程序 payload 与后端 required 字段统一。
3. 增加测试和静态校验，防止后续新增小程序埋点时再次出现字典漂移。

在修复完成前，产品统计口径应标记“微信小程序部分行为事件缺失”，避免使用 `usage_events` 数据做精确运营判断。
