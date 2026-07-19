---
requirement_id: REQ-0040-rule-skill-read-summary-reuse-context-budget
status: done
priority: P1
created_at: 2026-07-16 08:58:55
updated_at: 2026-07-18 09:19:04
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-16 08:58:55
  generated: 2026-07-16 09:02:54
  completed: 2026-07-16 09:07:01
  reviewed: 2026-07-16 09:09:53
  approved: 2026-07-16 09:09:53
iteration: sprint-008
openspec_changes:
  - change_id: update-rule-skill-summary-reuse-context-budget
    type: update
    status: archived
related_requirements: []
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
cross_cutting_tags: []
---

```yaml
requirement_id: REQ-0040-rule-skill-read-summary-reuse-context-budget
status: done
priority: P1
created_at: 2026-07-16 08:58:55
updated_at: 2026-07-18 09:19:52
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-16 08:58:55
  generated: 2026-07-16 09:02:54
  completed: 2026-07-16 09:07:01
  reviewed: 2026-07-16 09:09:53
  approved: 2026-07-16 09:09:53
iteration: sprint-008
openspec_changes:
  - change_id: update-rule-skill-summary-reuse-context-budget
    type: update
    status: archived
related_requirements: []
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
cross_cutting_tags: []
```

# Trace

## 关联需求

| 需求 | 关系 | 说明 |
|---|---|---|
| REQ-0034-ai-token-usage-observability | parent_requirement | AI Token 使用量观测与上下文成本治理背景 |
| REQ-0035-ai-usage-snapshot-sprint-close-exps | related | Sprint close / exps 消费 AI usage snapshot |
| REQ-0037-auto-token-fact-source-for-workflow-commands | related | 工作流命令后置 hook 与紧凑输出要求 |

## 知识库引用

| 路径 | 用途 | 说明 |
|---|---|---|
| docs/knowledge-base/retrospectives/sprint-007-retrospective.md | 复盘行动项 | A-004 要求将规则/Skill 已读摘要复用纳入命令上下文预算治理 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-18 09:18:50 | lifecycle-stage-migrate | review → archive（/opsx-archive update-rule-skill-summary-reuse-context-budget） |
| 2026-07-18 09:17:08 | /opsx-archive | Change `update-rule-skill-summary-reuse-context-budget` 已归档，状态同步完成。 |
| 2026-07-16 09:30:54 | /opsx-apply | Change `update-rule-skill-summary-reuse-context-budget` apply 完成，待 archive。 |
| 2026-07-16 09:23:05 | /sprint-propose | 纳入 sprint-008 正式范围，容量估算 3.0/30.0 人天 |
| 2026-07-16 09:14:43 | /req-opsx | 创建 OpenSpec Change update-rule-skill-summary-reuse-context-budget，关联状态 proposed |
| 2026-07-16 09:10:25 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-16 09:09:53 | /req-review --approve | 评审通过，需求状态更新为 approved |
| 2026-07-16 09:07:01 | /req-complete | 补齐 user-stories、business-flow、acceptance；知识库 gate 为 N/A，状态更新为 pending_review |
| 2026-07-16 09:07:01 | knowledge-base-scan | 读取知识库索引并检索 sprint-007 复盘，确认行动项 A-004 为本需求来源；无 UI 横切标签 |
| 2026-07-16 09:02:54 | /req-generate | 生成 requirement.md，需求状态更新为 draft |
| 2026-07-16 08:58:55 | /req-capture | 记录规则/Skill 已读摘要复用纳入命令上下文预算治理需求 |

- 2026-07-18 09:17:08 workflow-sync：状态同步为 done（Change archived）
