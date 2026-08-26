---
requirement_id: REQ-0124-log-audit-behavior-trace-model
status: in_sprint
lifecycle_stage: review
priority: P1
created_at: 2026-08-25 22:20:40
updated_at: 2026-08-25 23:25:07
lifecycle:
  captured: 2026-08-25 22:20:40
  generated: 2026-08-25 22:24:23
  completed: 2026-08-25 22:31:11
  reviewed: 2026-08-25 22:36:42
  approved: 2026-08-25 22:36:42
iteration: sprint-026
openspec_changes:
  - change_id: add-log-audit-behavior-trace-model
    type: add
    status: applied
related_requirements:
  - REQ-0024-product-usage-logging
  - REQ-0071-request-snapshot-logging
  - REQ-0073-task-trace-parent-request-model
  - REQ-0075-audit-log-task-trace-linking
  - REQ-0076-observability-dashboard
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-022-retrospective.md
cross_cutting_tags:
  - admin-list
related_changes:
  - add-log-audit-behavior-trace-model
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0124-log-audit-behavior-trace-model
requirement_name: log-audit-behavior-trace-model
requirement_type: 可观测性 / 日志审计 / 数据采集
priority: P1
status: in_sprint
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 待确认
  wechat_miniapp: 待确认
  backend_api: 本期
related_requirements:
  - REQ-0024-product-usage-logging
  - REQ-0071-request-snapshot-logging
  - REQ-0073-task-trace-parent-request-model
  - REQ-0075-audit-log-task-trace-linking
  - REQ-0076-observability-dashboard
related_changes:
  - add-log-audit-behavior-trace-model
lifecycle:
  captured: 2026-08-25 22:20:40
  generated: 2026-08-25 22:24:23
  completed: 2026-08-25 22:31:11
  reviewed: 2026-08-25 22:36:42
  approved: 2026-08-25 22:36:42
iteration: sprint-026
openspec_changes:
  - change_id: add-log-audit-behavior-trace-model
    type: add
    status: applied
readiness: Ready
readiness_notes: 已通过需求评审；范围、验收、UI 策略、admin-list 横切门禁和后续 OpenSpec 条件通过项已明确。
cross_cutting_tags:
  - admin-list
  - log-audit
  - usage-events
  - request-logs
  - task-trace
  - observability
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-022-retrospective.md
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/web/context.md
expected_openspec_change:
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-25 23:25:07 | /opsx-apply | Change `add-log-audit-behavior-trace-model` apply 完成，待 archive。 |
| 2026-08-25 22:42:46 | `/sprint-propose` | 纳入 sprint-026 正式范围，估算 L / 5 人天，下一步创建 OpenSpec Change |
| 2026-08-25 22:37:21 | lifecycle-stage-migrate | plan → review（/req-review） |
| 2026-08-25 22:36:42 | `/req-review` | 评审通过，状态更新为 approved，并准备从 plan 阶段迁入 review 阶段 |
| 2026-08-25 22:31:11 | `/req-complete` | 补齐用户故事、业务流程、验收标准和日志审计页原型策略；命中 admin-list 横切标签并引用管理端列表一致性实践 |
| 2026-08-25 22:24:23 | `/req-generate` | 根据 capture 生成日志审计行为链路与任务链路采集模型 PRD，状态更新为 draft |
| 2026-08-25 22:20:40 | `/req-capture` | 记录日志审计补齐行为链路、请求链路与任务流程节点采集模型需求 |
