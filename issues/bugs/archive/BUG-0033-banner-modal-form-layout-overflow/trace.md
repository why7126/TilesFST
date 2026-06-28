---
created_at: 2026-06-28 16:04:18
title: 缺陷追踪
purpose: BUG-0033 Banner 弹窗表单布局溢出
content: 记录运营备注宽度、占位符字号及底部按钮超出弹窗
owner: product
status: done
lifecycle_stage: archive
readiness: ready
updated_at: 2026-06-28 19:40:42
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0033-banner-modal-form-layout-overflow
bug_name: banner-modal-form-layout-overflow
severity: high
status: done
iteration: sprint-003
related_requirement: REQ-0016-banner-management
related_change: fix-banner-admin-ui
suggested_fix_change: fix-banner-admin-ui
related_bug:
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-28 16:04:18
  generated: 2026-06-28 16:15:39
  completed: 2026-06-28 16:17:14
  reviewed: 2026-06-28 16:18:27
  approved: 2026-06-28 16:18:27
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
| 根因类型 | design / frontend-ui（modal scroll 缺失；textarea CSS port 不完整） |
| 修复面 | Web 管理端 `banner-management.css`（+ 必要时 `BannerFormModal`） |
| 建议 Change | `fix-banner-modal-form-layout-overflow`（可与 BUG-0031～0035 合并为 `fix-banner-modal-ui`） |

## 4. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 17:05:08 | `/sprint-propose` | 纳入 sprint-003 正式 Scope |
| 2026-06-28 16:20:00 | `/bug-opsx` | 创建 change `fix-banner-admin-ui`（合并 BUG-0030～0036） |
| 2026-06-28 16:18:27 | `/bug-review --approve` | 评审通过；status → approved；plan → review |
| 2026-06-28 16:17:14 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；status → pending_review |
| 2026-06-28 16:15:39 | `/bug-generate` | 生成 bug.md，status → draft |
| 2026-06-28 16:04:18 | `/bug-capture` | 记录 Banner 弹窗布局溢出与缺少滚动 |
