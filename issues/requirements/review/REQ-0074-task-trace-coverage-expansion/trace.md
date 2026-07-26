---
requirement_id: REQ-0074-task-trace-coverage-expansion
status: in_sprint
lifecycle_stage: review
priority: P1
created_at: 2026-07-26 12:49:31
updated_at: 2026-07-26 15:58:44
lifecycle:
  captured: 2026-07-26 12:49:31
  generated: 2026-07-26 12:57:18
  completed: 2026-07-26 13:02:05
  reviewed: 2026-07-26 13:09:36
  approved: 2026-07-26 13:09:36
iteration: sprint-012
openspec_changes:
  - change_id: update-task-trace-coverage-expansion
    type: update
    status: applied
related_requirements:
  - REQ-0069-upload-observability-trace-logs
related_bugs: []
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags: []
---

# Trace

```yaml
requirement_id: REQ-0074-task-trace-coverage-expansion
status: in_sprint
priority: P1
created_at: 2026-07-26 12:49:31
updated_at: 2026-07-26 15:34:18
lifecycle_stage: review
lifecycle:
  captured: 2026-07-26 12:49:31
  generated: 2026-07-26 12:57:18
  completed: 2026-07-26 13:02:05
  reviewed: 2026-07-26 13:09:36
  approved: 2026-07-26 13:09:36
iteration: sprint-012
openspec_changes:
  - change_id: update-task-trace-coverage-expansion
    type: update
    status: applied
related_requirements:
  - REQ-0069-upload-observability-trace-logs
related_bugs: []
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags: []
```

## 关联文档

| 类型 | 路径 | 说明 |
|---|---|---|
| capture | `issues/requirements/review/REQ-0074-task-trace-coverage-expansion/capture.md` | 原始需求记录 |
| requirement | `issues/requirements/review/REQ-0074-task-trace-coverage-expansion/requirement.md` | PRD |
| user-stories | `issues/requirements/review/REQ-0074-task-trace-coverage-expansion/user-stories.md` | 用户故事 |
| business-flow | `issues/requirements/review/REQ-0074-task-trace-coverage-expansion/business-flow.md` | 业务流程 |
| acceptance | `issues/requirements/review/REQ-0074-task-trace-coverage-expansion/acceptance.md` | 验收标准 |
| prototype | `issues/requirements/review/REQ-0074-task-trace-coverage-expansion/prototype/web/task-trace-feedback.html` | 复杂任务追踪标识反馈 HTML 原型 |
| prototype-context | `issues/requirements/review/REQ-0074-task-trace-coverage-expansion/prototype/web/task-trace-feedback-context.md` | 原型说明 |
| review | `issues/requirements/review/REQ-0074-task-trace-coverage-expansion/review.md` | 评审结论 |

## Readiness

| 项 | 状态 | 说明 |
|---|---|---|
| overall | Ready | 五件套齐全，已补轻量 HTML/context 原型策略 |
| requirement.md | done | 已生成 PRD |
| user-stories.md | done | 已补齐用户故事 |
| business-flow.md | done | 已补齐业务流程 |
| acceptance.md | done | 已补齐功能 AC；本 REQ 无匹配 UI 知识库标签，横切 AC 为 N/A |
| prototype | done | 已补 HTML/context；PNG Golden Reference 待后续设计确认时导出 |
| knowledge-base gate | N/A | 未命中 admin-list / admin-form / admin-modal / media-upload 标签；已读取 Sprint 010 复盘并写入 trace 引用 |

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 |
|---|---|---:|
| N/A | `docs/knowledge-base/retrospectives/sprint-010-retrospective.md` | 0 |

## 复盘经验摘要

- Sprint 010 建议生产 smoke 在 apply 中段落盘；本 REQ 后续若涉及生产 DB、对象存储、上传或异步任务边界，OpenSpec tasks 应前置 evidence stub。
- Sprint 010 建议把 Dashboard / 列表 / 弹窗 / 上传横切测试继续组件化；本 REQ 当前未命中固定 UI 标签，但后续若实际改动日志审计列表、上传控件或弹窗，必须补读对应 best-practices 并补 AC-XCUT。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-26 15:58:44 | /opsx-apply | Change `update-task-trace-coverage-expansion` apply 完成，待 archive。 |
| 2026-07-26 15:34:18 | /sprint-propose | 按用户要求改纳入 `sprint-012`，关联 Change `update-task-trace-coverage-expansion`。 |
| 2026-07-26 15:17:02 | /sprint-propose | 纳入 `sprint-011`，关联 Change `update-task-trace-coverage-expansion`，状态推进为 in_sprint。 |
| 2026-07-26 13:34:21 | workflow-sync-correction | 保持 `approved`；REQ-0074 尚未纳入 Sprint，不能标记为 `in_sprint`。 |
| 2026-07-26 13:34:21 | /req-opsx | 创建 OpenSpec Change `update-task-trace-coverage-expansion`，状态 proposed。 |
| 2026-07-26 13:10:24 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-26 13:09:36 | /req-review --approve | 评审通过，状态推进为 approved；准备迁移 plan → review。 |
| 2026-07-26 13:02:05 | /req-complete | 补齐用户故事、业务流程、验收标准、trace 扩展和复杂任务追踪标识反馈原型，状态推进为 pending_review。 |
| 2026-07-26 12:57:18 | /req-generate | 生成任务型接口 Task Trace 覆盖扩展 PRD，状态推进为 draft。 |
| 2026-07-26 12:49:31 | /capture | 记录任务型接口全面接入 Task Trace 需求。 |
