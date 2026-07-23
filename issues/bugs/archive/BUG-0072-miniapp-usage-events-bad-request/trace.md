---
bug_id: BUG-0072-miniapp-usage-events-bad-request
status: done
lifecycle_stage: archive
severity: high
created_at: 2026-07-21 08:38:39
updated_at: 2026-07-22 08:48:40
lifecycle:
  captured: 2026-07-21 08:38:39
  generated: 2026-07-21 10:10:00
  completed: 2026-07-21 14:41:14
  reviewed: 2026-07-21 14:57:01
  approved: 2026-07-21 14:57:01
iteration: sprint-010
related_requirement: REQ-0024-product-usage-logging
related_bug: null
related_change: null
source_command: /capture
captured_via: capture
classification_rationale: 已有产品使用事件上报能力下，微信小程序调用 POST /api/v1/usage-events 频繁返回 400，属于现有接口兼容性、请求体校验或小程序端上报参数与后端契约不一致导致的行为偏差。
openspec_changes:
  - change_id: fix-miniapp-usage-events-contract-drift
    type: fix
    status: archived
related_bugs: []
---

```yaml
bug_id: BUG-0072-miniapp-usage-events-bad-request
status: done
severity: high
lifecycle_stage: review
created_at: 2026-07-21 08:38:39
updated_at: 2026-07-21 15:26:34
lifecycle:
  captured: 2026-07-21 08:38:39
  generated: 2026-07-21 10:10:00
  completed: 2026-07-21 14:41:14
  reviewed: 2026-07-21 14:57:01
  approved: 2026-07-21 14:57:01
iteration: sprint-010
related_requirement: REQ-0024-product-usage-logging
related_bug: null
related_change: null
source_command: /capture
captured_via: capture
classification_rationale: 已有产品使用事件上报能力下，微信小程序调用 POST /api/v1/usage-events 频繁返回 400，属于现有接口兼容性、请求体校验或小程序端上报参数与后端契约不一致导致的行为偏差。
openspec_changes:
  - change_id: fix-miniapp-usage-events-contract-drift
    type: fix
    status: archived
related_bugs: []
scope:
  terminal: miniapp
  api: POST /api/v1/usage-events
  module: product_usage_logging
  issue_type: bad_request
readiness:
  capture: done
  bug: done
  root_cause: done
  workaround: done
  acceptance: done
  review: done
  trace: done
  next: opsx-apply
```

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| 用户反馈 | `/capture` | 微信小程序很多 `POST /api/v1/usage-events` 请求返回 400 Bad Request |
| 关联需求 | `REQ-0024-product-usage-logging` | 产品使用事件上报能力已归档，当前问题是小程序端上报与接口契约不一致或兼容性缺陷 |

## 建议复现要点

| 要点 | 说明 |
|---|---|
| 触发页面 | 定位是哪几个小程序页面或交互触发 `usage-events` 上报 |
| 请求体 | 记录 Network payload，重点检查 `event_name`、`properties`、`entity_type`、`entity_id`、`result`、`duration_ms` 等字段 |
| 响应体 | 记录 400 响应 JSON、错误码和字段校验信息 |
| 后端日志 | 对照 FastAPI 请求日志与 Pydantic 校验错误，判断是字段缺失、枚举不匹配、类型错误还是 forbidden property |
| 统计影响 | 核查使用事件缺失是否影响详情访问、热销排序、榜单或审计统计 |

## 建议验收要点

| 验收点 | 说明 |
|---|---|
| 合法事件成功 | 小程序端合法行为事件上报返回成功，不再大量出现 400 |
| 非法事件可诊断 | 后端 400 响应应包含可定位的字段原因，便于前后端修正 |
| 契约一致 | 小程序端上报字段与 `POST /api/v1/usage-events` 后端 Schema / 事件字典一致 |
| 噪音控制 | 小程序控制台不因重复无效上报被刷屏 |
| 统计完整 | 关键页面访问和交互事件可正常写入 `usage_events`，相关统计不丢失 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 08:47:49 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-usage-events-contract-drift） |
| 2026-07-22 08:47:26 | /opsx-archive | Change `fix-miniapp-usage-events-contract-drift` 已归档，状态同步完成。 |
| 2026-07-21 14:57:34 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-21 08:38:39 | /capture | 记录微信小程序 usage-events 上报接口频繁返回 400 缺陷 |
| 2026-07-21 10:10:00 | /bug-generate | 基于 capture 与 explore 结论生成 bug.md，状态更新为 draft |
| 2026-07-21 14:41:14 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态更新为 pending_review |
| 2026-07-21 14:57:01 | /bug-review --approve | 评审通过，允许进入 bug-opsx 与 Sprint 规划 |
| 2026-07-21 15:01:40 | /bug-opsx | 创建 OpenSpec Change `fix-miniapp-usage-events-contract-drift`，状态 proposed |
| 2026-07-21 15:26:34 | /sprint-propose | 纳入 `sprint-010`，等待 `/opsx-apply fix-miniapp-usage-events-contract-drift` |

- 2026-07-22 08:47:26 workflow-sync：状态同步为 done（Change archived）
