---
requirement_id: REQ-0092-brand-certificate-image-thumbnails
status: done
priority: P1
created_at: 2026-08-02 16:56:28
updated_at: 2026-08-02 19:32:35
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-02 16:56:28
  generated: 2026-08-02 17:51:32
  completed: 2026-08-02 17:55:40
  reviewed: 2026-08-02 18:01:12
  approved: 2026-08-02 18:01:12
iteration: sprint-017
openspec_changes:
  - change_id: add-brand-certificate-image-thumbnails
    type: add
    status: archived
related_requirements:
  - REQ-0005-brand-management
  - REQ-0038-brand-certificate-management
source_bug: BUG-0101-thumbnail-optimization-size-regression
readiness: Ready
knowledge_base_gate: Pass
cross_cutting_tags:
  - admin-list
  - admin-modal
  - media-upload
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-016-retrospective.md
---

# REQ Trace

```yaml
requirement_id: REQ-0092-brand-certificate-image-thumbnails
status: done
priority: P1
created_at: 2026-08-02 16:56:28
updated_at: 2026-08-02 18:01:59
lifecycle_stage: review
lifecycle:
  captured: 2026-08-02 16:56:28
  generated: 2026-08-02 17:51:32
  completed: 2026-08-02 17:55:40
  reviewed: 2026-08-02 18:01:12
  approved: 2026-08-02 18:01:12
iteration: sprint-017
openspec_changes:
  - change_id: add-brand-certificate-image-thumbnails
    type: add
    status: archived
related_requirements:
  - REQ-0005-brand-management
  - REQ-0038-brand-certificate-management
source_bug: BUG-0101-thumbnail-optimization-size-regression
readiness: Ready
knowledge_base_gate: Pass
cross_cutting_tags:
  - admin-list
  - admin-modal
  - media-upload
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-016-retrospective.md
```

## Readiness Report

| 项 | 结论 | 说明 |
|---|---|---|
| readiness | Ready | requirement、user-stories、business-flow、acceptance、trace 齐全；UI 类 prototype 策略已写入 `prototype/web/`。 |
| knowledge-base gate | Pass | 已读取并转化 admin-list、admin-modal、media-upload 横切 best-practices。 |
| cross-cutting tags | admin-list, admin-modal, media-upload | 管理端列表/卡片、弹窗上传、媒体上传链路均受影响。 |
| prototype | Ready | HTML + context 已提供；PNG Golden Reference 后续设计阶段导出。 |

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 |
|---|---|---:|
| admin-list | docs/knowledge-base/best-practices/admin-list-page-consistency.md | 4 |
| admin-modal | docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md | 2 |
| media-upload | docs/knowledge-base/best-practices/admin-media-upload-chain.md | 6 |
| retrospective | docs/knowledge-base/retrospectives/sprint-016-retrospective.md | 已转化到 AC-010、AC-011、AC-XCUT-010、AC-XCUT-012 |

复盘摘要：Sprint 016 指出媒体能力不能只验证对象存在，必须覆盖对象 key、URL 可访问、缩略图真实尺寸/体积收益、端上渲染和历史补齐脚本幂等性。本需求已将该模式写入功能 AC 与横切 AC。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-02 19:20:12 | lifecycle-stage-migrate | review → archive（/opsx-archive add-brand-certificate-image-thumbnails） |
| 2026-08-02 19:17:28 | /opsx-archive | Change `add-brand-certificate-image-thumbnails` 已归档，状态同步完成。 |
| 2026-08-02 18:44:43 | /opsx-apply | Change `add-brand-certificate-image-thumbnails` apply 完成，待 archive。 |
| 2026-08-02 18:16:03 | `/sprint-propose sprint-017` | REQ-0092 与 Change `add-brand-certificate-image-thumbnails` 纳入 sprint-017 正式范围。 |
| 2026-08-02 18:07:10 | `/req-opsx` | 创建 OpenSpec Change `add-brand-certificate-image-thumbnails`；后续已归档闭环。 |
| 2026-08-02 18:01:49 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-08-02 18:01:12 | `/req-review --approve` | 评审通过，状态推进为 approved；准备从 plan 阶段迁移到 review 阶段。 |
| 2026-08-02 17:55:40 | `/req-complete` | 补齐 user-stories、business-flow、acceptance、trace 扩展与 prototype/web；状态推进为 pending_review；知识库标签 admin-list/admin-modal/media-upload 已转化为横切 AC。 |
| 2026-08-02 17:51:32 | `/req-generate` | 生成 requirement.md，状态推进为 draft。 |
| 2026-08-02 16:56:28 | `/req-capture` | 根据用户澄清，将 BUG-0101 重新分类为品牌与证书图片支持真实缩略图生成的需求。 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0101-thumbnail-optimization-size-regression | high | rejected | — | SKU 缩略图回归误报，转为品牌与证书图片缩略图需求 |
- 2026-08-02 19:17:28 workflow-sync：状态同步为 done（Change archived）
