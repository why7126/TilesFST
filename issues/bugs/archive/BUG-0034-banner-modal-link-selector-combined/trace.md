---
created_at: 2026-06-28 16:04:18
title: 缺陷追踪
purpose: BUG-0034 Banner 弹窗关联专题/SKU 选择器交互
content: 记录搜索框与下拉框应合并为可搜索选择组件
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
bug_id: BUG-0034-banner-modal-link-selector-combined
bug_name: banner-modal-link-selector-combined
severity: medium
status: done
iteration: sprint-003
related_requirement: REQ-0016-banner-management
related_change: fix-banner-admin-ui
related_bug:
suggested_fix_change: fix-banner-admin-ui
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-28 16:04:18
  generated: 2026-06-28 16:15:53
  completed: 2026-06-28 16:17:29
  reviewed: 2026-06-28 16:18:39
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
| 根因类型 | design / frontend-ui（双控件近似搜索，未对齐原型单 Combobox） |
| 修复面 | `BannerFormModal.tsx` 关联 SKU / 专题选择器；MAY 新增 `shared/ui` SearchableSelect |
| 建议 Change | `fix-banner-modal-ui`（建议与 BUG-0030–0036 合并） |

## 4. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 17:05:08 | `/sprint-propose` | 纳入 sprint-003 正式 Scope |
| 2026-06-28 16:20:00 | `/bug-opsx` | 创建 change `fix-banner-admin-ui`（合并 BUG-0030～0036） |
| 2026-06-28 16:18:39 | `/bug-review --approve` | 评审通过；plan → review；status → approved |
| 2026-06-28 16:17:29 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；status → pending_review |
| 2026-06-28 16:15:53 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-06-28 16:04:18 | `/bug-capture` | 记录关联专题/SKU 双框交互不合理 |
