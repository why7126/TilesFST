---
requirement_id: REQ-0108-admin-banner-list-display-optimization
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-08-11 08:33:52
updated_at: 2026-08-11 23:21:27
lifecycle:
  captured: 2026-08-11 08:33:52
  generated: 2026-08-11 08:35:44
  completed: 2026-08-11 08:37:56
  reviewed: 2026-08-11 08:40:56
  approved: 2026-08-11 08:40:56
iteration: sprint-022
openspec_changes:
  - change_id: update-admin-banner-list-display-optimization
    type: update
    status: archived
related_requirements: []
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-020-retrospective.md
cross_cutting_tags:
  - admin-list
---

# Trace

## 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-08-11 23:20:43 | lifecycle-stage-migrate | review → archive（/opsx-archive update-admin-banner-list-display-optimization） |
| 2026-08-11 23:20:31 | /opsx-archive | Change `update-admin-banner-list-display-optimization` 已归档，状态同步完成。 |
| 2026-08-11 22:56:55 | /opsx-modify | Change `update-admin-banner-list-display-optimization` 验收返修已同步，后续已归档。 |
| 2026-08-11 09:02:02 | /opsx-apply | Change `update-admin-banner-list-display-optimization` apply 完成，后续已归档。 |
| 2026-08-11 08:48:00 | req.opsx | 创建 OpenSpec Change `update-admin-banner-list-display-optimization`。 |
| 2026-08-11 08:45:03 | sprint.propose | 纳入 sprint-022 正式范围。 |
| 2026-08-11 08:41:16 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-08-11 08:40:56 | req.review | 需求评审通过，状态更新为 approved。 |
| 2026-08-11 08:37:56 | req.complete | 补齐 user-stories、business-flow、acceptance 与 prototype context；状态更新为 pending_review。 |
| 2026-08-11 08:35:44 | req.generate | 生成 requirement.md，状态更新为 draft。 |
| 2026-08-11 08:33:52 | req.capture | 记录 Banner 列表页显示内容优化需求。 |

## 知识库横切引用

| 标签 | 引用文档 | 写入 acceptance 的 AC |
|---|---|---|
| admin-list | docs/knowledge-base/best-practices/admin-list-page-consistency.md | AC-XCUT-001 ~ AC-XCUT-008 |

## 复盘摘要

- sprint-020 复盘提示 SKU/Banner 列表优先使用缩略图，并将“列表展示字段 / 生成策略 / 历史维护”拆分验收；本需求聚焦列表展示字段，明确 Banner 列只展示主图并保留图片 fallback。
- Web 管理端列表仍需持续防范分页 DOM、toast、confirm 与表格布局回归，本需求已将 admin-list 横切 AC 写入 acceptance。
- 2026-08-11 23:20:31 workflow-sync：状态同步为 done（Change archived）
