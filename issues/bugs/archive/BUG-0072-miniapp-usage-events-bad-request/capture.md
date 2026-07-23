---
bug_id: BUG-0072-miniapp-usage-events-bad-request
title: 微信小程序 usage-events 上报接口频繁返回 400
status: done
created_at: 2026-07-21 08:38:39
updated_at: 2026-07-22 08:47:45
severity_hint: high
environment: 微信小程序 DevTools / macOS / mp 2.01.2510290 / lib 3.16.2
source: 用户反馈
source_command: /capture
captured_via: capture
classification_rationale: 已有产品使用事件上报能力下，微信小程序调用 POST /api/v1/usage-events 频繁返回 400，属于现有接口兼容性、请求体校验或小程序端上报参数与后端契约不一致导致的行为偏差。
related_requirement: REQ-0024-product-usage-logging
related_bug:
---

# 现象

微信小程序运行过程中多次出现使用事件上报请求失败：

```text
POST http://127.0.0.1:8010/api/v1/usage-events 400 (Bad Request)
(env: macOS, mp, 2.01.2510290; lib: 3.16.2)
```

# 复现步骤

1. 在 macOS 微信开发者工具中运行小程序。
2. 进入会触发行为统计或使用事件上报的页面或交互。
3. 观察开发者工具 Console / Network 请求。
4. 查看 `POST /api/v1/usage-events` 是否频繁返回 400。

# 期望 vs 实际

期望：小程序端上报的合法使用事件应被后端接受并返回成功；若事件不合法，应给出可定位的错误码和字段原因，且前端不应持续产生无效上报噪音。

实际：小程序端大量 `POST /api/v1/usage-events` 请求返回 400，影响控制台可用性，并可能导致使用行为统计缺失或热销/访问统计不准确。

# 附件

- 用户提供报错文本：`POST http://127.0.0.1:8010/api/v1/usage-events 400 (Bad Request)(env: macOS,mp,2.01.2510290; lib: 3.16.2)`
- 暂无请求体、响应体、触发页面截图；后续 `/bug-explore` 阶段需补充 Network payload、响应 JSON 和触发页面。
