---
requirement_id: REQ-0106-admin-banner-title-hidden
status: done
priority: P1
created_at: 2026-08-10 22:27:41
updated_at: 2026-08-11 23:17:14
lifecycle:
  captured: 2026-08-10 22:27:41
  generated: 2026-08-10 22:38:20
  completed: 2026-08-10 22:40:54
  reviewed: 2026-08-10 22:45:06
  approved: 2026-08-10 22:45:06
iteration: sprint-022
openspec_changes:
  - change_id: update-banner-title-hidden-display
    type: update
    status: archived
related_requirements: []
lifecycle_stage: archive
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-020-retrospective.md
cross_cutting_tags:
  - admin-list
  - admin-modal
  - media-upload
---

# Trace

## 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-08-11 23:17:14 | lifecycle-stage-migrate | review → archive（/opsx-archive update-banner-title-hidden-display） |
| 2026-08-11 23:17:04 | /opsx-archive | Change `update-banner-title-hidden-display` 已归档，状态同步完成。 |
| 2026-08-10 23:11:33 | /opsx-apply | Change `update-banner-title-hidden-display` apply 完成，待 archive。 |
| 2026-08-10 22:45:41 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-08-10 22:27:41 | req.capture | 记录 Banner 标题隐藏与小程序前台标题遮罩移除需求。 |
| 2026-08-10 22:38:20 | req.generate | 生成 requirement.md，状态更新为 draft。 |
| 2026-08-10 22:40:54 | req.complete | 补齐 user-stories、business-flow、acceptance 与 prototype context；状态更新为 pending_review。 |
| 2026-08-10 22:45:06 | req.review | 需求评审通过，状态更新为 approved。 |
| 2026-08-10 22:50:49 | sprint.propose | 纳入 sprint-022 正式范围。 |
| 2026-08-10 23:02:22 | req.opsx | 创建 OpenSpec Change `update-banner-title-hidden-display`。 |

## 知识库横切引用

| 标签 | 引用文档 | 写入 acceptance 的 AC |
|---|---|---|
| admin-list | docs/knowledge-base/best-practices/admin-list-page-consistency.md | AC-XCUT-001 ~ AC-XCUT-004 |
| admin-modal | docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md | AC-XCUT-005 ~ AC-XCUT-006 |
| media-upload | docs/knowledge-base/best-practices/admin-media-upload-chain.md | AC-XCUT-007 ~ AC-XCUT-009 |

## 复盘摘要

- sprint-020 复盘提示 SKU/Banner 列表优先使用缩略图并明确列表资源与详情资源分工，本需求的列表识别与图片回显验收已纳入横切 AC。
- sprint-019 复盘提示小程序端上行为需要真实环境确认，本需求要求小程序 UI 验收记录 DevTools、体验版或真机来源。
- 2026-08-11 23:16:37 workflow-sync：状态同步为 done（Change archived）
