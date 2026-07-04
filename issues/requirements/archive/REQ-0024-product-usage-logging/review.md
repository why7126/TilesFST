---
review_id: REV-REQ-0024-001
requirement_id: REQ-0024-product-usage-logging
date: 2026-07-02 14:37:02
participants: []
result: approved
created_at: 2026-07-02 14:37:02
updated_at: 2026-07-02 14:37:02
---

# REQ-0024 需求评审

## 评审结论

通过。

REQ-0024 已完成从 capture、requirement 到 user-stories、business-flow、acceptance、tracking-events、trace 与管理端原型的需求补齐。需求范围聚焦于产品使用行为埋点、API 请求日志、日志详情存储、管理端查询与安全脱敏闭环；复杂 BI、第三方埋点、完整请求/响应体保存、日志导出和外部日志系统已明确排除。

本需求批准进入 OpenSpec Change 阶段，建议 Change 名称为 `add-product-usage-logging`。

## 评审清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，覆盖数据采集、模型、API、管理端、安全、事件字典与横切 AC。
- [x] 优先级与依赖合理，P1 平台治理能力，与 REQ-0017 审计配置存在可解释依赖。
- [x] UI 类原型或实现策略已决，已提供管理端日志审计列表 HTML 与 context。
- [x] 无与现有 REQ 重复未说明；已明确与 `audit_logs`、REQ-0017、REQ-0022 的关系。

## 条件通过项

- [ ] OpenSpec design MUST 明确日志模型选择：扩展 `audit_logs` 或新增 `request_logs` / `usage_events`。
- [ ] OpenSpec design MUST 明确店主 Web 展示端与微信小程序本期是否实现，或仅保留上报扩展点。
- [ ] UI 实现 Sprint 前 SHOULD 导出 `prototype/web/log-audit-list.png` 作为 1440x1024 Golden Reference。
- [ ] API 实现时 MUST 同步 OpenAPI、Orval、`docs/03-api-index.md` 与错误码文档。
- [ ] 数据库实现时 MUST 同时考虑 SQLite demo 与 MySQL production，避免 SQLite-only DDL。

## 后续动作

1. `/req-opsx REQ-0024-product-usage-logging`
2. `/sprint-propose` 纳入迭代时检查 `admin-list` 横切预防清单
