---
requirement_id: REQ-0036-clipboard-helper-best-practice-docs
status: done
lifecycle_stage: archive
priority: P2
created_at: 2026-07-11 23:37:42
updated_at: 2026-07-12 00:33:27
lifecycle:
  captured: 2026-07-11 23:37:42
  generated: 2026-07-11 23:42:20
  completed: 2026-07-11 23:47:07
  reviewed: 2026-07-11 23:53:49
  approved: 2026-07-11 23:53:49
iteration: sprint-007
openspec_changes:
  - change_id: add-clipboard-helper-best-practice-docs
    type: add
    status: archived
related_requirements:
  - REQ-0032-clipboard-copy-helper-best-practice
knowledge_base_refs:
  - docs/knowledge-base/README.md
  - docs/knowledge-base/retrospectives/sprint-006-retrospective.md
cross_cutting_tags: []
readiness: Ready
knowledge_base_gate: N/A
---

# Trace

```yaml
requirement_id: REQ-0036-clipboard-helper-best-practice-docs
status: done
priority: P2
created_at: 2026-07-11 23:37:42
updated_at: 2026-07-12 00:03:31
lifecycle:
  captured: 2026-07-11 23:37:42
  generated: 2026-07-11 23:42:20
  completed: 2026-07-11 23:47:07
  reviewed: 2026-07-11 23:53:49
  approved: 2026-07-11 23:53:49
iteration: sprint-007
openspec_changes:
  - change_id: add-clipboard-helper-best-practice-docs
    type: add
    status: archived
related_requirements:
  - REQ-0032-clipboard-copy-helper-best-practice
knowledge_base_refs:
  - docs/knowledge-base/README.md
  - docs/knowledge-base/retrospectives/sprint-006-retrospective.md
cross_cutting_tags: []
readiness: Ready
knowledge_base_gate: N/A
```

## 关联文档

| 类型 | 路径 | 说明 |
|---|---|---|
| capture | `issues/requirements/archive/REQ-0036-clipboard-helper-best-practice-docs/capture.md` | 原始需求记录 |
| requirement | `issues/requirements/archive/REQ-0036-clipboard-helper-best-practice-docs/requirement.md` | PRD |
| user-stories | `issues/requirements/archive/REQ-0036-clipboard-helper-best-practice-docs/user-stories.md` | 用户故事 |
| business-flow | `issues/requirements/archive/REQ-0036-clipboard-helper-best-practice-docs/business-flow.md` | 业务流程 |
| acceptance | `issues/requirements/archive/REQ-0036-clipboard-helper-best-practice-docs/acceptance.md` | 验收标准 |
| review | `issues/requirements/archive/REQ-0036-clipboard-helper-best-practice-docs/review.md` | 评审记录 |

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 将写入 acceptance 的 AC 条数 |
|---|---|---|
| N/A | `docs/knowledge-base/README.md`；`docs/knowledge-base/retrospectives/sprint-006-retrospective.md` | 0 |

判定：本 REQ 为 Clipboard helper best-practice 文档治理需求，不涉及管理端 CRUD 列表页、表单页、弹窗新建/编辑或媒体上传，因此无横切 AC。Sprint 006 复盘中 `best-practices/clipboard-fallback.md` 建议后续新建，已作为知识库追溯来源写入 acceptance。

## Readiness

| 项 | 状态 | 说明 |
|---|---|---|
| capture.md | done | 已记录原始需求 |
| requirement.md | done | 已生成 PRD |
| user-stories.md | done | 已补齐 |
| business-flow.md | done | 已补齐 |
| acceptance.md | done | 已补齐 |
| prototype | N/A | 文档治理需求，无 UI 原型 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-12 00:33:14 | lifecycle-stage-migrate | review → archive（/opsx-archive add-clipboard-helper-best-practice-docs） |
| 2026-07-12 00:30:43 | /opsx-archive | Change `add-clipboard-helper-best-practice-docs` 已归档，状态同步完成。 |
| 2026-07-12 00:23:44 | /opsx-apply | Change `add-clipboard-helper-best-practice-docs` apply 完成，待 archive。 |
| 2026-07-11 23:54:29 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-11 23:37:42 | /req-capture | 记录 Clipboard helper best-practice 文档需求 |
| 2026-07-11 23:42:20 | /req-generate | 生成 requirement.md，需求状态更新为 draft |
| 2026-07-11 23:47:07 | /req-complete | 补齐 user-stories、business-flow、acceptance；无匹配 UI 横切标签，状态更新为 pending_review |
| 2026-07-11 23:53:49 | /req-review --approve | 需求评审通过，状态更新为 approved；待迁移至 review 阶段目录 |
| 2026-07-11 23:57:08 | /req-opsx | 创建 OpenSpec Change：add-clipboard-helper-best-practice-docs |
| 2026-07-12 00:03:31 | /sprint-propose | 纳入 sprint-007 正式范围 |

- 2026-07-12 00:30:43 workflow-sync：状态同步为 done（Change archived）
