---
requirement_id: REQ-0078-certificate-multiple-images-main-image
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-28 22:23:23
updated_at: 2026-07-29 09:07:43
iteration: sprint-013
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0078-certificate-multiple-images-main-image
requirement_name: certificate-multiple-images-main-image
requirement_type: 管理端 / 品牌证书 / 媒体上传与展示规则
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 待评估
  wechat_miniapp: 待评估
related_requirements:
  - REQ-0038-brand-certificate-management
related_changes:
  - update-certificate-multiple-images-main-image
lifecycle:
  captured: 2026-07-28 22:23:23
  generated: 2026-07-28 22:29:24
  completed: 2026-07-28 22:32:00
  reviewed: 2026-07-28 22:38:51
  approved: 2026-07-28 22:38:51
iteration: sprint-013
openspec_changes:
  - change_id: update-certificate-multiple-images-main-image
    type: update
    status: archived
readiness: Ready
readiness_notes: 五件套已补齐，UI 原型策略已落地；已通过评审、创建 OpenSpec Change，并纳入 sprint-013。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/web/prototype-context.md
  - prototype/web/certificate-multiple-images-main-image.html
expected_openspec_change: update-certificate-multiple-images-main-image
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-012-retrospective.md
cross_cutting_tags:
  - admin-list
  - admin-modal
  - media-upload
  - brand-certificate
knowledge_base_summary: 已将列表分页/toast/confirm、弹窗 CSS cascade/computed width/矮视口滚动、上传状态机/即时回显/Docker 3000 边界验收转化为 12 条 AC-XCUT；Sprint-012 复盘提醒媒体类任务需写清纳入边界并继续复用 admin-list fixed toast 模式。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-29 07:54:33 | lifecycle-stage-migrate | review → archive（/opsx-archive update-certificate-multiple-images-main-image） |
| 2026-07-29 07:54:16 | /opsx-archive | Change `update-certificate-multiple-images-main-image` 已归档，状态同步完成。 |
| 2026-07-29 00:10:51 | docs-sync | 补充记录 follow-up：小程序证书卡片 `file_url` 优先使用主图、证书列表卡片高度放大、底部 tabbar 返回首页激活态修复，以及管理端证书列表移除预览按钮、证书图片上传提示对齐 SKU 样式。 |
| 2026-07-28 23:18:40 | /opsx-apply | Change `update-certificate-multiple-images-main-image` apply 完成，待 archive。 |
| 2026-07-28 23:18:21 | /opsx-apply | Change `update-certificate-multiple-images-main-image` apply 进行中，待补齐剩余验收。 |
| 2026-07-28 22:59:15 | `/sprint-propose` | 纳入 `sprint-013` 正式范围，关联 Change `update-certificate-multiple-images-main-image`。 |
| 2026-07-28 22:48:48 | `/req-opsx` | 创建 OpenSpec Change `update-certificate-multiple-images-main-image`，状态 proposed。 |
| 2026-07-28 22:39:30 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-28 22:38:51 | `/req-review --approve` | 需求评审通过，允许进入 /req-opsx 与 Sprint 规划。 |
| 2026-07-28 22:32:00 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 prototype/web；写入 admin-list/admin-modal/media-upload 横切 AC，状态更新为 pending_review。 |
| 2026-07-28 22:29:24 | `/req-generate` | 生成 requirement.md，状态更新为 draft。 |
| 2026-07-28 22:23:23 | `/capture` | 记录证书支持多张图片上传与主图设置需求。 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0089-admin-certificate-edit-image-filename-noise | low | done | fix-admin-certificate-image-filename-noise | 管理端证书编辑弹窗图片下方显示无意义文件名 |
