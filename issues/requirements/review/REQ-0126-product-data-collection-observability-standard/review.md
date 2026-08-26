---
review_id: REV-REQ-0126-001
requirement_id: REQ-0126-product-data-collection-observability-standard
date: 2026-08-26
participants:
  - product
  - ai
result: approved
created_at: 2026-08-26 10:27:00
updated_at: 2026-08-26 10:27:00
---

# 需求评审

## 评审结论

通过。

`REQ-0126-product-data-collection-observability-standard` 的范围清晰：将 REQ-0124 已落地的日志审计行为链路模型沉淀为跨产品可复用的数据采集与链路观测规范，覆盖小程序、店主端、App、Web 管理端和后端 API。需求已经明确 API 请求日志全量覆盖、行为事件采集口径、四层链路模型、直接 API 调用兼容、Task Trace 分级覆盖、默认保留周期、敏感字段脱敏和新产品接入清单。

本需求不直接改造所有历史产品，不接入外部 APM / OpenTelemetry，不建设第三方埋点平台、实时告警、BI 大屏、复杂用户画像或历史数据强制回填。后续实现应以规范文档、接入 checklist、验收模板和必要的治理校验为交付核心，并作为后续 REQ、BUG、OpenSpec Change 和 Sprint 验收的引用标准。

## 评审清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，覆盖适用端、API 请求日志、行为事件、链路 ID、Task Trace 分级覆盖、保留周期、脱敏边界、API / DB / Orval / 测试同步和后续引用方式。
- [x] 优先级与依赖合理，作为 `REQ-0124-log-audit-behavior-trace-model` 的规范化沉淀，并参考 `docs/standards/task-trace-coverage.md` 与 `docs/standards/api-governance.md`。
- [x] UI 类策略已决：本需求不新增具体业务 UI，Knowledge-base UI 横切 gate 为 N/A；后续日志审计或观测页面落地时再按具体页面标签补充横切 AC。
- [x] 无与现有 REQ 重复未说明；本需求是对现有日志审计链路模型的通用规范化，不替代 REQ-0124 的项目内实现。

## 条件通过项

- [ ] 后续 `/req-opsx` 或 OpenSpec Change 必须明确规范文档落点、文档索引、引用方式和验收入口，避免只形成孤立 Markdown。
- [ ] 后续实现必须提供新产品接入 checklist，覆盖前端 helper / SDK、后端 request log middleware、Task Trace helper、DB migration、OpenAPI / Orval、脱敏 helper、测试模板和验收清单。
- [ ] 后续规范必须明确 `behavior_trace_id`、`behavior_event_id`、`parent_behavior_event_id`、`request_id`、`client_request_id`、`task_trace_id` 的生成方、可信边界、格式校验和异常处理。
- [ ] 后续规范必须保留已确认的数据保留周期：`request_logs` 90 天、`usage_events` 180 天、`task_traces/task_trace_spans` 90 天、聚合数据 1 年，并说明调整周期的审批依据。
- [ ] 若后续实现引入 API、DB、Web、小程序或 App 代码改动，必须按对应治理规则同步 OpenAPI、Orval、数据库文档、测试和安全脱敏验证。

## 后续建议

推荐先纳入 Sprint，再创建 OpenSpec Change：

```text
/sprint-propose sprint-xxx --req REQ-0126-product-data-collection-observability-standard
```
