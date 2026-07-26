---
requirement_id: REQ-0072-client-request-identity-standard
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-26 12:49:31
updated_at: 2026-07-26 16:54:26
lifecycle:
  captured: 2026-07-26 12:49:31
  generated: 2026-07-26 12:57:10
  completed: 2026-07-26 13:01:32
  reviewed: 2026-07-26 13:10:48
  approved: 2026-07-26 13:10:48
iteration: sprint-012
openspec_changes:
  - change_id: standardize-client-request-identity
    type: update
    status: archived
related_requirements:
  - REQ-0024-product-usage-logging
related_bugs: []
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags:
  - admin-list
---

# Trace

```yaml
requirement_id: REQ-0072-client-request-identity-standard
status: done
priority: P1
created_at: 2026-07-26 12:49:31
updated_at: 2026-07-26 15:17:24
lifecycle_stage: review
lifecycle:
  captured: 2026-07-26 12:49:31
  generated: 2026-07-26 12:57:10
  completed: 2026-07-26 13:01:32
  reviewed: 2026-07-26 13:10:48
  approved: 2026-07-26 13:10:48
iteration: sprint-012
openspec_changes:
  - change_id: standardize-client-request-identity
    type: update
    status: archived
related_requirements:
  - REQ-0024-product-usage-logging
related_bugs: []
readiness: Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance、prototype web context/html，并写入 admin-list 横切 AC；已评审通过，准入 /req-opsx 与 Sprint 规划。
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags:
  - admin-list
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/web/client-request-identity-context.md
  - prototype/web/client-request-identity.html
expected_openspec_change: standardize-client-request-identity
```

## 关联文档

| 类型 | 路径 | 说明 |
|---|---|---|
| capture | `issues/requirements/archive/REQ-0072-client-request-identity-standard/capture.md` | 原始需求记录 |
| requirement | `issues/requirements/archive/REQ-0072-client-request-identity-standard/requirement.md` | PRD 草稿 |
| user-stories | `issues/requirements/archive/REQ-0072-client-request-identity-standard/user-stories.md` | 用户故事 |
| business-flow | `issues/requirements/archive/REQ-0072-client-request-identity-standard/business-flow.md` | 业务流程 |
| acceptance | `issues/requirements/archive/REQ-0072-client-request-identity-standard/acceptance.md` | 验收清单 |
| review | `issues/requirements/archive/REQ-0072-client-request-identity-standard/review.md` | 评审结论 |
| prototype | `issues/requirements/archive/REQ-0072-client-request-identity-standard/prototype/web/client-request-identity-context.md` | UI 字段与交互策略 |
| prototype | `issues/requirements/archive/REQ-0072-client-request-identity-standard/prototype/web/client-request-identity.html` | 管理端日志审计字段展示原型 |

## 知识库横切引用

| 标签 | 引用文档 | 写入 AC | 说明 |
|---|---|---|---|
| admin-list | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 4 | 日志审计列表字段、复制反馈、分页和指标卡一致性 |
| retrospective | `docs/knowledge-base/retrospectives/sprint-010-retrospective.md` | 0 | 最近复盘提醒继续组件化 Dashboard/列表/弹窗/上传横切测试，并前置 smoke evidence |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-26 16:54:02 | lifecycle-stage-migrate | review → archive（/opsx-archive standardize-client-request-identity） |
| 2026-07-26 16:53:27 | /opsx-archive | Change `standardize-client-request-identity` 已归档，状态同步完成。 |
| 2026-07-26 15:48:23 | /opsx-apply | Change `standardize-client-request-identity` apply 完成，待 archive。 |
| 2026-07-26 13:11:29 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-26 12:49:31 | /capture | 记录前台后台与小程序统一客户端请求标识需求。 |
| 2026-07-26 12:57:10 | /req-generate | 生成 requirement.md，状态推进为 draft。 |
| 2026-07-26 13:01:32 | /req-complete | 补齐 user-stories、business-flow、acceptance 与 prototype；写入 admin-list 横切 AC；状态推进为 pending_review。 |
| 2026-07-26 13:10:48 | /req-review --approve | 评审通过；状态推进为 approved，准入 /req-opsx 与 Sprint 规划。 |
| 2026-07-26 13:38:31 | /req-opsx | 创建 OpenSpec Change `standardize-client-request-identity`；状态 proposed。 |
| 2026-07-26 15:17:24 | /sprint-propose | 纳入 Sprint `sprint-012`。 |

- 2026-07-26 16:53:27 workflow-sync：状态同步为 done（Change archived）
