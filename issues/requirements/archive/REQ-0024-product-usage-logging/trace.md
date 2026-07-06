---
requirement_id: REQ-0024-product-usage-logging
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-01 13:52:03
updated_at: 2026-07-05 20:33:34
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-003-retrospective.md
cross_cutting_tags:
  - admin-list
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0024-product-usage-logging
requirement_name: product-usage-logging
requirement_type: 平台治理 / 日志与埋点
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 待确认
  wechat_miniapp: 待确认
  backend_api: 本期
related_requirements: []
related_changes:
  - add-product-usage-logging
lifecycle:
  captured: 2026-07-01 13:52:03
  generated: 2026-07-02 11:51:22
  completed: 2026-07-02 13:04:31
  reviewed: 2026-07-02 14:37:02
  approved: 2026-07-02 14:37:02
iteration: sprint-004
openspec_changes:
  - add-product-usage-logging
readiness: Ready
readiness_notes: 已补齐 user-stories、business-flow、acceptance、tracking-events、prototype HTML/context/PNG 与知识库横切 AC，并已评审通过、纳入 sprint-004；OpenSpec Change 已创建为 add-product-usage-logging；日志模型采用新增 request_logs / usage_events，并以统一查询模型纳入 audit_logs。
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-003-retrospective.md
cross_cutting_tags:
  - admin-list
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - tracking-events.md
  - review.md
  - prototype/web/log-audit-list.html
  - prototype/web/log-audit-list-context.md
  - prototype/web/log-audit-detail-drawer.html
  - prototype/web/log-audit-detail-drawer-context.md
  - prototype/web/log-audit-list.png
  - prototype/web/log-audit-detail-drawer.png
expected_openspec_change: add-product-usage-logging
```

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-07-03 23:24:07 | lifecycle-stage-migrate | review → archive（/opsx-archive add-product-usage-logging） |
| 2026-07-02 21:55:08 | `/req-opsx REQ-0024-product-usage-logging` | 创建 OpenSpec Change `add-product-usage-logging`；补齐 proposal、design、delta spec、tasks 与 change trace |
| 2026-07-02 15:25:19 | `/sprint-propose REQ-0024 纳入 sprint-004` | 纳入 sprint-004 正式范围；status → in_sprint；OpenSpec Change 待 `/req-opsx REQ-0024-product-usage-logging` |
| 2026-07-02 15:15:44 | product-prototype-v2-sync | 基于产品 v2 原型更新 requirement、acceptance、prototype context，新增详情抽屉原型；PNG Golden Reference 已落盘至 `prototype/web/` |
| 2026-07-02 14:37:58 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-02 14:37:02 | `/req-review --approve` | 评审通过；status → approved；准入 `/req-opsx` 与 Sprint 规划 |
| 2026-07-02 13:04:31 | `/req-complete` | 补齐 user-stories、business-flow、acceptance、tracking-events 与管理端日志审计原型；写入 admin-list 横切 AC；status → pending_review |
| 2026-07-02 12:56:58 | `/req-generate` | 基于探索结论刷新 requirement.md；补充埋点事件字典、人工定义事件属性、代码侧枚举/Schema 校验与后端自动补上下文要求 |
| 2026-07-02 11:51:22 | `/req-generate` | 生成 requirement.md；明确产品使用行为埋点、接口请求日志、日志详情、管理端查询、脱敏与保留周期范围；status → draft |
| 2026-07-01 13:52:03 | `/req-capture` | 记录产品使用行为埋点、接口请求日志与日志详情存储需求；status → captured |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0060-audit-log-request-id-copy-error | medium | captured | — | audit log request id copy error |
