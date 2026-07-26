---
requirement_id: REQ-0076-observability-dashboard
status: in_sprint
lifecycle_stage: review
priority: P1
created_at: 2026-07-26 12:49:31
updated_at: 2026-07-26 16:01:45
lifecycle:
  captured: 2026-07-26 12:49:31
  generated: 2026-07-26 12:57:48
  completed: 2026-07-26 13:02:41
  reviewed: 2026-07-26 13:09:56
  approved: 2026-07-26 13:09:56
iteration: sprint-012
openspec_changes:
  - change_id: add-observability-dashboard
    type: add
    status: in_progress
related_requirements:
  - REQ-0024-product-usage-logging
  - REQ-0069-upload-observability-trace-logs
  - REQ-0034-ai-token-usage-observability
related_bugs: []
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags:
  - admin-list
---

# Trace

```yaml
requirement_id: REQ-0076-observability-dashboard
status: in_sprint
priority: P1
created_at: 2026-07-26 12:49:31
updated_at: 2026-07-26 15:33:09
lifecycle_stage: review
lifecycle:
  captured: 2026-07-26 12:49:31
  generated: 2026-07-26 12:57:48
  completed: 2026-07-26 13:02:41
  reviewed: 2026-07-26 13:09:56
  approved: 2026-07-26 13:09:56
iteration: sprint-012
openspec_changes:
  - change_id: add-observability-dashboard
    type: add
    status: in_progress
related_requirements:
  - REQ-0024-product-usage-logging
  - REQ-0069-upload-observability-trace-logs
  - REQ-0034-ai-token-usage-observability
related_bugs: []
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags:
  - admin-list
```

## 关联文档

| 类型 | 路径 | 说明 |
|---|---|---|
| capture | `issues/requirements/review/REQ-0076-observability-dashboard/capture.md` | 原始需求记录 |
| requirement | `issues/requirements/review/REQ-0076-observability-dashboard/requirement.md` | 需求 PRD 草稿 |
| user-stories | `issues/requirements/review/REQ-0076-observability-dashboard/user-stories.md` | 用户故事与验收要点 |
| business-flow | `issues/requirements/review/REQ-0076-observability-dashboard/business-flow.md` | 排障与追踪业务流程 |
| acceptance | `issues/requirements/review/REQ-0076-observability-dashboard/acceptance.md` | 功能 AC 与横切 AC |
| review | `issues/requirements/review/REQ-0076-observability-dashboard/review.md` | 需求评审结论 |
| prototype | `issues/requirements/review/REQ-0076-observability-dashboard/prototype/web/observability-dashboard.html` | 管理端链路观测仪表原型策略 |

## 知识库横切引用

| 标签 | 引用文档 | 写入 AC |
|---|---|---|
| admin-list | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | AC-XCUT-001 ~ AC-XCUT-005 |
| admin-list | `docs/knowledge-base/retrospectives/sprint-010-retrospective.md` | AC-XCUT-006 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-26 16:01:45 | /opsx-apply | Change `add-observability-dashboard` apply 进行中，待补齐剩余验收。 |
| 2026-07-26 15:33:09 | /sprint-propose sprint-012 | 按用户要求从 sprint-011 改纳入 sprint-012；关联 Change `add-observability-dashboard`；status → in_sprint，iteration → sprint-012。 |
| 2026-07-26 15:24:00 | sprint-scope-boundary-correction | 修正 sprint.propose 同步漂移；REQ-0076 未纳入本次 REQ-0073 sprint-011 范围，状态恢复为 approved，iteration 恢复为 null。 |
| 2026-07-26 13:55:43 | /sprint-propose sprint-011 | 纳入 sprint-011 正式范围；关联 Change `add-observability-dashboard`；status → in_sprint。 |
| 2026-07-26 13:43:11 | workflow-sync-status-correction | 修正 req.opsx 后未纳入 Sprint 但状态被派生为 in_sprint 的漂移；保持 status → approved，Change `add-observability-dashboard` 仍为 proposed。 |
| 2026-07-26 13:35:51 | /req-opsx REQ-0076 | 创建 OpenSpec Change `add-observability-dashboard`；生成 proposal、design、delta spec、tasks 与 change trace。 |
| 2026-07-26 13:10:49 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-26 13:09:56 | /req-review --approve | 评审通过；范围、验收、依赖、UI 原型策略和横切 AC 满足准入；status → approved。 |
| 2026-07-26 13:02:41 | /req-complete | 补齐 user-stories、business-flow、acceptance 与 prototype/web；读取 admin-list 知识库和 sprint-010 复盘，写入横切 AC；status → pending_review。 |
| 2026-07-26 12:57:48 | /req-generate | 生成 requirement.md；明确日志审计与链路观测仪表范围、指标、追踪工作流和管理端约束；status → draft。 |
| 2026-07-26 12:49:31 | /capture | 记录日志审计升级为链路观测仪表需求。 |
