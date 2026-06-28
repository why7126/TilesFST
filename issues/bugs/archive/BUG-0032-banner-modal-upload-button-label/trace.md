---
created_at: 2026-06-28 16:04:18
title: 缺陷追踪
purpose: BUG-0032 Banner 弹窗上传按钮文案不一致
content: 记录自定义上传按钮文案应改为选择/更换
owner: product
status: done
lifecycle_stage: archive
readiness: ready
note: merged fix-banner-admin-ui; /bug-opsx 2026-06-28 16:20:00
updated_at: 2026-06-28 19:40:42
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0032-banner-modal-upload-button-label
bug_name: banner-modal-upload-button-label
severity: low
status: done
iteration: sprint-003
related_requirement: REQ-0016-banner-management
related_bug: BUG-0031-banner-modal-image-section-label
related_change: fix-banner-admin-ui
suggested_fix_change: fix-banner-admin-ui
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-28 16:04:18
  generated: 2026-06-28 16:15:16
  completed: 2026-06-28 16:17:02
  reviewed: 2026-06-28 16:18:19
  approved: 2026-06-28 16:18:19
openspec_changes:
  - change_id: fix-banner-admin-ui
    type: fix
    status: archived
  opsx: 2026-06-28 16:20:00```

## 2. Readiness

| 文档 | 状态 |
|---|---|
| capture.md | done |
| bug.md | done |
| root-cause.md | done |
| workaround.md | done |
| acceptance.md | done |
| review.md | done |

**Readiness:** Ready — merged `fix-banner-admin-ui`

## 3. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 17:03:05 | `/sprint-propose` | 纳入 sprint-003 正式 Scope |
| 2026-06-28 16:20:00 | `/bug-opsx` | 创建 change `fix-banner-admin-ui`（合并 BUG-0030～0036） |
| 2026-06-28 16:18:19 | `/bug-review --approve` | REV-BUG-0032-001 通过；plan → review；status → approved |
| 2026-06-28 16:17:02 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；status → pending_review |
| 2026-06-28 16:15:16 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-06-28 16:04:18 | `/bug-capture` | 记录 Banner 图片上传按钮文案 |

## 4. 修复线索

| 项 | 说明 |
|---|---|
| 问题文件 | `src/web/src/features/admin/components/BannerFormModal.tsx` |
| 基准参考 | `src/web/src/features/admin/components/BrandFormModal.tsx` |
| 测试参考 | `src/web/src/features/admin/components/BrandFormModal.test.tsx` |
| 建议 Change | `fix-banner-modal-upload-button-label` 或合并 `fix-banner-modal-ui`（含 BUG-0031/0033–0036） |
| 截图 | `screenshots/` 待 apply 阶段补充 |
