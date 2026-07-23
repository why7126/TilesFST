---
requirement_id: REQ-0066-admin-sku-image-removal-main-image-rules
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-22 08:54:30
updated_at: 2026-07-22 10:17:09
iteration: sprint-010
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0066-admin-sku-image-removal-main-image-rules
requirement_name: admin-sku-image-removal-main-image-rules
requirement_type: 管理端 / SKU 图片编辑
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
related_requirements:
  - REQ-0006-tile-sku-management
related_changes:
  - add-admin-sku-image-removal-main-image-rules
lifecycle_stage: review
lifecycle:
  captured: 2026-07-22 08:54:30
  generated: 2026-07-22 09:17:23
  completed: 2026-07-22 09:19:53
  reviewed: 2026-07-22 09:24:44
  approved: 2026-07-22 09:24:44
iteration: sprint-010
openspec_changes:
  - change_id: add-admin-sku-image-removal-main-image-rules
    type: update
    status: archived
readiness: Ready
readiness_notes: 五件套已补齐；UI 类 prototype 策略已落 prototype/web；knowledge-base 横切 AC 已写入 acceptance.md，待 req-review。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/web/admin-sku-image-removal-main-image-rules.html
  - prototype/web/admin-sku-image-removal-main-image-rules-context.md
expected_openspec_change: add-admin-sku-image-removal-main-image-rules
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-009-retrospective.md
cross_cutting_tags:
  - admin-modal
  - media-upload
knowledge_base_gate: Pass
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 10:13:21 | lifecycle-stage-migrate | review → archive（/opsx-archive add-admin-sku-image-removal-main-image-rules） |
| 2026-07-22 10:13:00 | /opsx-archive | Change `add-admin-sku-image-removal-main-image-rules` 已归档，状态同步完成。 |
| 2026-07-22 09:59:15 | /opsx-apply | Change `add-admin-sku-image-removal-main-image-rules` apply 完成，待 archive。 |
| 2026-07-22 09:26:29 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-22 08:54:30 | `/capture` | 记录管理端 SKU 编辑弹窗支持商品图片移除与主图兜底规则 |
| 2026-07-22 09:17:23 | `/req-generate` | 生成 requirement.md，状态更新为 draft |
| 2026-07-22 09:19:53 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 prototype；读取 admin-modal/media-upload best-practices 和 sprint-009 复盘，状态更新为 pending_review |
| 2026-07-22 09:24:44 | `/req-review --approve` | 评审通过；准备从 plan 迁移到 review |
| 2026-07-22 09:31:00 | `/req-opsx` | 创建 OpenSpec Change `add-admin-sku-image-removal-main-image-rules` |
| 2026-07-22 09:45:10 | `/sprint-propose` | 纳入 sprint-010，关联 Change `add-admin-sku-image-removal-main-image-rules` |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-07-22 10:13:00 workflow-sync：状态同步为 done（Change archived）
