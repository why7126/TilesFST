---
requirement_id: REQ-0118-unified-web-miniapp-image-variant-consumption-matrix
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-08-22 20:32:30
updated_at: 2026-08-22 21:37:53
openspec_changes:
  - change_id: update-media-image-variant-consumption-matrix
    type: update
    status: archived
related_changes:
  - update-media-image-variant-consumption-matrix
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0118-unified-web-miniapp-image-variant-consumption-matrix
requirement_name: unified-web-miniapp-image-variant-consumption-matrix
requirement_type: 媒体治理 / 跨端图片规格消费矩阵
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 预留规范
  wechat_miniapp: 本期
related_requirements:
  - REQ-0115-media-multi-variant-images
  - REQ-0098-admin-media-list-thumbnails
  - REQ-0092-brand-certificate-image-thumbnails
  - REQ-0111-miniapp-media-four-part-acceptance-practice
related_changes:
  - update-media-image-variant-consumption-matrix
lifecycle:
  captured: 2026-08-22 20:32:30
  generated: 2026-08-22 21:00:51
  completed: 2026-08-22 21:04:14
  reviewed: 2026-08-22 21:10:53
  approved: 2026-08-22 21:10:53
iteration: sprint-025
openspec_changes:
  - change_id: update-media-image-variant-consumption-matrix
    type: update
    status: archived
readiness: Partially Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance 与 prototype 策略；命中的 knowledge-base best-practices 当前为 draft，待评审。
cross_cutting_tags:
  - admin-list
  - admin-modal
  - media-upload
  - object-storage
  - admin-web
  - miniapp
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-024-retrospective.md
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/web/context.md
expected_openspec_change: update-media-image-variant-consumption-matrix
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-22 21:35:42 | lifecycle-stage-migrate | review → archive（/opsx-archive update-media-image-variant-consumption-matrix） |
| 2026-08-22 21:35:35 | /opsx-archive | Change `update-media-image-variant-consumption-matrix` 已归档，状态同步完成。 |
| 2026-08-22 21:31:10 | /opsx-apply | Change `update-media-image-variant-consumption-matrix` apply 完成，待 archive。 |
| 2026-08-22 21:11:37 | lifecycle-stage-migrate | plan → review（/req-review） |
| 2026-08-22 20:32:30 | `/req-capture` | 记录统一 Web 与微信小程序图片三规格消费矩阵需求 |
| 2026-08-22 21:00:51 | `/req-generate` | 生成 PRD，确认只做规范矩阵、店主 Web 按预留规范处理、非原图目标场景不允许 fallback 到原图 |
| 2026-08-22 21:04:14 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 prototype 策略；读取 admin-list、admin-modal、media-upload 最佳实践和 sprint-024 媒体复盘，沉淀横切 AC |
| 2026-08-22 21:10:53 | `/req-review` | 评审通过；待纳入 Sprint 后创建 OpenSpec Change |
| 2026-08-22 21:17:46 | `/sprint-propose` | 纳入 sprint-025；待创建 OpenSpec Change |
| 2026-08-22 21:24:00 | `/req-opsx` | 创建 OpenSpec Change `update-media-image-variant-consumption-matrix`，类型 update |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-08-22 21:35:35 workflow-sync：状态同步为 done（Change archived）
