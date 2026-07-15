---
requirement_id: REQ-0035-ai-usage-snapshot-sprint-close-exps
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-11 23:36:05
updated_at: 2026-07-15 13:14:43
lifecycle:
  captured: 2026-07-11 23:36:05
  generated: 2026-07-11 23:42:45
  completed: 2026-07-11 23:46:16
  reviewed: 2026-07-11 23:53:21
  approved: 2026-07-11 23:53:21
iteration: sprint-007
openspec_changes:
  - change_id: update-ai-usage-snapshot-sprint-close-exps
    type: update
    status: archived
related_requirements:
  - REQ-0034-ai-token-usage-observability
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-006-retrospective.md
cross_cutting_tags: []
---

# Trace

```yaml
requirement_id: REQ-0035-ai-usage-snapshot-sprint-close-exps
status: done
priority: P1
created_at: 2026-07-11 23:36:05
updated_at: 2026-07-12 00:07:29
lifecycle:
  captured: 2026-07-11 23:36:05
  generated: 2026-07-11 23:42:45
  completed: 2026-07-11 23:46:16
  reviewed: 2026-07-11 23:53:21
  approved: 2026-07-11 23:53:21
iteration: sprint-007
openspec_changes:
  - change_id: update-ai-usage-snapshot-sprint-close-exps
    type: update
    status: archived
related_requirements:
  - REQ-0034-ai-token-usage-observability
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-006-retrospective.md
cross_cutting_tags: []
```

## 关联文档

| 类型 | 路径 | 说明 |
|---|---|---|
| capture | `issues/requirements/archive/REQ-0035-ai-usage-snapshot-sprint-close-exps/capture.md` | 原始需求记录 |
| requirement | `issues/requirements/archive/REQ-0035-ai-usage-snapshot-sprint-close-exps/requirement.md` | PRD |
| user-stories | `issues/requirements/archive/REQ-0035-ai-usage-snapshot-sprint-close-exps/user-stories.md` | 用户故事 |
| business-flow | `issues/requirements/archive/REQ-0035-ai-usage-snapshot-sprint-close-exps/business-flow.md` | 业务流程 |
| acceptance | `issues/requirements/archive/REQ-0035-ai-usage-snapshot-sprint-close-exps/acceptance.md` | 验收标准 |
| review | `issues/requirements/archive/REQ-0035-ai-usage-snapshot-sprint-close-exps/review.md` | 评审结论 |
| knowledge-base | `docs/knowledge-base/retrospectives/sprint-006-retrospective.md` | AI usage snapshot 行动项来源 |

## Readiness

| 项 | 状态 | 说明 |
|---|---|---|
| capture.md | done | 已记录原始需求 |
| requirement.md | done | 已生成 PRD |
| user-stories.md | done | 已补齐用户故事 |
| business-flow.md | done | 已补齐业务流程 |
| acceptance.md | done | 已补齐可勾选 AC；无 UI 横切标签 |
| prototype | N/A | 流程治理需求，无 UI 原型 |
| knowledge-base gate | N/A | 非 UI REQ；引用 sprint-006 复盘中的 AI usage snapshot 行动项 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-15 13:14:18 | lifecycle-stage-migrate | review → archive（/sprint-archive sprint-007） |
| 2026-07-12 00:52:25 | /opsx-archive | Change `update-ai-usage-snapshot-sprint-close-exps` 已归档，状态同步完成。 |
| 2026-07-12 00:44:24 | /opsx-apply | Change `update-ai-usage-snapshot-sprint-close-exps` apply 完成，待 archive。 |
| 2026-07-12 00:07:29 | /sprint-propose sprint-007 | 纳入 Sprint 007 正式范围，状态更新为 in_sprint |
| 2026-07-11 23:59:21 | workflow-sync-correction | 保持 `approved`；REQ-0035 尚未纳入 Sprint，不能标记为 `in_sprint` |
| 2026-07-11 23:57:08 | /req-opsx | 创建 OpenSpec Change `update-ai-usage-snapshot-sprint-close-exps` |
| 2026-07-11 23:53:53 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-11 23:53:21 | /req-review --approve | 评审通过，状态更新为 approved；准备迁移 plan → review |
| 2026-07-11 23:46:16 | /req-complete | 补齐 user-stories、business-flow、acceptance；状态更新为 pending_review；无 UI 横切标签 |
| 2026-07-11 23:46:16 | knowledge-base-scan | 读取 sprint-006 复盘，确认 AI usage snapshot 缺失导致 estimated fallback，并承接 A-001 行动项 |
| 2026-07-11 23:42:45 | /req-generate | 生成 PRD，状态更新为 draft |
| 2026-07-11 23:36:05 | /req-capture | 记录 AI usage snapshot 纳入 Sprint close / exps 默认流程需求 |

- 2026-07-12 00:52:25 workflow-sync：状态同步为 done（Change archived）
