---
requirement_id: REQ-0075-audit-log-task-trace-linking
status: done
lifecycle_stage: archive
priority: P2
created_at: 2026-07-26 12:49:31
updated_at: 2026-07-26 17:09:40
lifecycle:
  captured: 2026-07-26 12:49:31
  generated: 2026-07-26 12:57:58
  completed: 2026-07-26 13:02:25
  reviewed: 2026-07-26 13:09:44
  approved: 2026-07-26 13:09:44
iteration: sprint-012
openspec_changes:
  - change_id: link-audit-logs-to-task-trace
    type: update
    status: archived
related_requirements:
  - REQ-0024-product-usage-logging
  - REQ-0069-upload-observability-trace-logs
  - REQ-0073-task-trace-parent-request-model
  - REQ-0074-task-trace-coverage-expansion
related_bugs: []
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags:
  - admin-list
---

# Trace

```yaml
requirement_id: REQ-0075-audit-log-task-trace-linking
status: done
priority: P2
created_at: 2026-07-26 12:49:31
updated_at: 2026-07-26 17:12:37
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-26 12:49:31
  generated: 2026-07-26 12:57:58
  completed: 2026-07-26 13:02:25
  reviewed: 2026-07-26 13:09:44
  approved: 2026-07-26 13:09:44
iteration: sprint-012
openspec_changes:
  - change_id: link-audit-logs-to-task-trace
    type: update
    status: archived
related_requirements:
  - REQ-0024-product-usage-logging
  - REQ-0069-upload-observability-trace-logs
  - REQ-0073-task-trace-parent-request-model
  - REQ-0074-task-trace-coverage-expansion
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
| capture | `issues/requirements/archive/REQ-0075-audit-log-task-trace-linking/capture.md` | 原始需求记录 |
| requirement | `issues/requirements/archive/REQ-0075-audit-log-task-trace-linking/requirement.md` | PRD 初稿 |
| user-stories | `issues/requirements/archive/REQ-0075-audit-log-task-trace-linking/user-stories.md` | 用户故事 |
| business-flow | `issues/requirements/archive/REQ-0075-audit-log-task-trace-linking/business-flow.md` | 业务流程 |
| acceptance | `issues/requirements/archive/REQ-0075-audit-log-task-trace-linking/acceptance.md` | 验收标准 |
| review | `issues/requirements/archive/REQ-0075-audit-log-task-trace-linking/review.md` | 评审记录 |
| prototype | `issues/requirements/archive/REQ-0075-audit-log-task-trace-linking/prototype/web/context.md` | 管理端日志审计任务链路展示原型说明 |
| prototype | `issues/requirements/archive/REQ-0075-audit-log-task-trace-linking/prototype/web/audit-log-task-trace.html` | 管理端日志审计任务链路低保真 HTML |

## 关联 OpenSpec Changes

| Change | 类型 | 状态 | 说明 |
|---|---|---|---|
| link-audit-logs-to-task-trace | update | applied | 补齐 audit log 与 Task Trace 的写入、查询、展示和横切验收要求。 |

## 关联需求

| REQ | 关系 |
|---|---|
| REQ-0024-product-usage-logging | 父需求：产品使用日志与审计能力事实源。 |
| REQ-0069-upload-observability-trace-logs | 复用 Task Trace 时间线与日志审计详情展示能力。 |
| REQ-0073-task-trace-parent-request-model | 审计日志任务字段需与主请求、子请求关联模型保持一致。 |
| REQ-0074-task-trace-coverage-expansion | 后续更多任务型接口接入后继续复用审计日志任务关联字段。 |

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 |
|---|---|---:|
| admin-list | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 5 |
| retrospective | `docs/knowledge-base/retrospectives/sprint-010-retrospective.md` | 1 |

摘要：REQ-0075 命中管理端日志审计列表/详情场景，已将分页 DOM、指标卡 DOM、fixed toast、无 `window.confirm`、危险操作 confirm N/A、管理端 smoke matrix 前置写入 `acceptance.md`。Sprint 010 复盘中“管理端 UI 细节反复修复”和“Dashboard/列表/弹窗/上传横切测试继续组件化”已转化为 AC-XCUT-006。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-26 17:09:13 | lifecycle-stage-migrate | review → archive（/opsx-archive link-audit-logs-to-task-trace） |
| 2026-07-26 17:08:40 | /opsx-archive | Change `link-audit-logs-to-task-trace` 已归档，状态同步完成。 |
| 2026-07-26 15:56:56 | /opsx-apply | Change `link-audit-logs-to-task-trace` apply 完成，待 archive。 |
| 2026-07-26 15:56:22 | /opsx-apply | Change `link-audit-logs-to-task-trace` apply 进行中，待补齐剩余验收。 |
| 2026-07-26 15:40:00 | /sprint-propose | 按用户要求改纳入 `sprint-012`，状态进入 in_sprint，关联 Change `link-audit-logs-to-task-trace` 进入 Sprint 012 范围。 |
| 2026-07-26 15:24:00 | sprint-scope-boundary-correction | 修正 sprint.propose 同步漂移；REQ-0075 未纳入本次 REQ-0073 sprint-011 范围，状态恢复为 approved，iteration 恢复为 null。 |
| 2026-07-26 15:15:41 | /sprint-propose | 纳入 `sprint-011`，状态进入 in_sprint，关联 Change `link-audit-logs-to-task-trace` 进入 Sprint 范围。 |
| 2026-07-26 13:55:47 | sprint-scope-boundary-correction | 修正 sprint.propose 同步漂移；REQ-0075 未纳入 sprint-011，状态保持 approved，iteration 保持 null。 |
| 2026-07-26 13:42:39 | req-opsx-status-correction | 保留 Change 关联；因 Workflow Sync 报告 Sprint skipped 且 iteration 为 null，REQ 状态保持 approved，待 /sprint-propose 后再进入 in_sprint。 |
| 2026-07-26 13:35:56 | /req-opsx | 创建 OpenSpec Change `link-audit-logs-to-task-trace`，状态 proposed。 |
| 2026-07-26 13:10:35 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-26 13:09:44 | /req-review --approve | 评审通过，状态进入 approved，准备迁移至 review 阶段目录。 |
| 2026-07-26 13:02:25 | /req-complete | 补齐 user-stories、business-flow、acceptance、trace 与 prototype/web，状态进入 pending_review；知识库横切标签 admin-list 已写入验收。 |
| 2026-07-26 12:57:58 | /req-generate | 生成 requirement.md，需求状态进入 draft。 |
| 2026-07-26 12:49:31 | /capture | 记录审计操作日志补齐任务链路关联字段需求。 |

- 2026-07-26 17:08:40 workflow-sync：状态同步为 done（Change archived）
