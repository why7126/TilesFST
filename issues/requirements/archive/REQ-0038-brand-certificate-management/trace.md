---
requirement_id: REQ-0038-brand-certificate-management
status: done
priority: P1
created_at: 2026-07-14 22:37:23
updated_at: 2026-07-15 13:14:43
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-14 22:37:23
  generated: 2026-07-14 22:41:33
  completed: 2026-07-14 22:41:33
  reviewed: 2026-07-14 22:59:33
  approved: 2026-07-14 22:59:33
iteration: sprint-007
openspec_changes:
  - change_id: add-brand-certificate-management
    type: add
    status: archived
related_requirements:
  - REQ-0005-brand-management
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-006-retrospective.md
cross_cutting_tags:
  - admin-list
  - admin-modal
  - media-upload
---

```yaml
requirement_id: REQ-0038-brand-certificate-management
status: done
priority: P1
created_at: 2026-07-14 22:37:23
updated_at: 2026-07-14 23:31:34
lifecycle_stage: review
lifecycle:
  captured: 2026-07-14 22:37:23
  generated: 2026-07-14 22:41:33
  completed: 2026-07-14 22:41:33
  reviewed: 2026-07-14 22:59:33
  approved: 2026-07-14 22:59:33
iteration: sprint-007
openspec_changes:
  - change_id: add-brand-certificate-management
    type: add
    status: archived
related_requirements:
  - REQ-0005-brand-management
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-006-retrospective.md
cross_cutting_tags:
  - admin-list
  - admin-modal
  - media-upload
```

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 |
|---|---|---:|
| admin-list | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 4 |
| admin-modal | `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | 3 |
| media-upload | `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | 3 |

最近复盘参考：`docs/knowledge-base/retrospectives/sprint-006-retrospective.md` 延续了列表页、弹窗、上传链路 best-practices 作为后续新增页面的横切验收来源。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-15 13:14:20 | lifecycle-stage-migrate | review → archive（/sprint-archive sprint-007） |
| 2026-07-15 09:35:50 | /opsx-archive | Change `add-brand-certificate-management` 已归档，状态同步完成。 |
| 2026-07-15 09:14:40 | /opsx-apply | Change `add-brand-certificate-management` apply 完成，待 archive。 |
| 2026-07-14 23:00:20 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-14 22:37:23 | /req-capture | 捕获需求：新增品牌证书管理页。 |
| 2026-07-14 22:41:33 | /req-complete | 补齐 user-stories、business-flow、acceptance，归一 requirement 元数据并写入 knowledge_base_refs。 |
| 2026-07-14 22:59:33 | /req-review --approve | 评审通过，允许进入 /req-opsx 与 Sprint 规划。 |
| 2026-07-14 23:17:02 | /req-opsx | 创建 OpenSpec Change：add-brand-certificate-management。 |
| 2026-07-14 23:31:34 | /sprint-propose sprint-007 | 纳入 sprint-007 正式范围。 |

- 2026-07-15 09:35:50 workflow-sync：状态同步为 done（Change archived）
