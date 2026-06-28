---
created_at: 2026-06-28 16:04:18
title: 缺陷追踪
purpose: BUG-0035 Banner 弹窗使用 SKU 主图无效果
content: 记录点击使用 SKU 主图按钮无任何响应
owner: product
status: done
lifecycle_stage: archive
readiness: ready
updated_at: 2026-06-28 19:40:42
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0035-banner-modal-sku-hero-image-no-effect
bug_name: banner-modal-sku-hero-image-no-effect
severity: high
status: done
iteration: sprint-003
related_requirement: REQ-0016-banner-management
related_bug: BUG-0032-banner-modal-upload-button-label
related_change: fix-banner-admin-ui
suggested_fix_change: fix-banner-admin-ui
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-28 16:04:18
  generated: 2026-06-28 16:16:23
  completed: 2026-06-28 16:17:35
  reviewed: 2026-06-28 16:18:44
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

## 3. 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（BUG） |
| 根因类型 | code / frontend-logic + API 契约（列表无 `images[].object_key`） |
| 修复面 | Web 管理端 `BannerFormModal.tsx`；可选 SKU 列表 API |
| 建议 Change | `fix-banner-modal-sku-hero-image`（或与 BUG-0031–0036 合并 `fix-banner-modal-ui`） |

## 4. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 17:05:08 | `/sprint-propose` | 纳入 sprint-003 正式 Scope |
| 2026-06-28 16:20:00 | `/bug-opsx` | 创建 change `fix-banner-admin-ui`（合并 BUG-0030～0036） |
| 2026-06-28 16:04:18 | `/bug-capture` | 记录使用 SKU 主图功能未生效 |
| 2026-06-28 16:16:23 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-06-28 16:17:35 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；status → pending_review |
| 2026-06-28 16:18:44 | `/bug-review --approve` | REV-BUG-0035-001 通过；status → approved；plan → review |
