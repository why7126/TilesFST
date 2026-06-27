---
created_at: 2026-06-27 12:03:34
title: 缺陷追踪
purpose: BUG-0015 管理端四列表页状态Tips推挤页面
content: 记录品牌/用户/类目/SKU 列表状态变更 Tips 导致上下布局波动
owner: product
status: done
note: fix-admin-list-status-toast-layout 已 archive；BUG done
iteration: sprint-002
readiness: ready
updated_at: 2026-06-27 15:52:00
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0015-admin-list-status-tips-layout-shift
bug_name: admin-list-status-tips-layout-shift
severity: medium
status: done
iteration: sprint-002
related_requirement: REQ-0005-brand-management
related_bug: BUG-0003-brand-image-display-layout-shift
related_change: fix-admin-list-status-toast-layout
suggested_fix_change: fix-admin-list-status-toast-layout
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-27 12:03:34
  generated: 2026-06-27 12:39:11
  completed: 2026-06-27 12:40:41
  reviewed: 2026-06-27 12:47:06
  approved: 2026-06-27 12:47:06
  opsx_created: 2026-06-27 12:48:52
  applied: 2026-06-27 12:56:14
  archived: 2026-06-27 12:59:21
openspec_changes:
  - change_id: fix-admin-list-status-toast-layout
    type: fix
    status: archived
    bug_id: BUG-0015-admin-list-status-tips-layout-shift```

## 2. Readiness

| 文档 | 状态 |
|---|---|
| capture.md | done |
| bug.md | done |
| root-cause.md | done |
| workaround.md | done |
| acceptance.md | done |
| review.md | done |

**Readiness:** Ready

## 3. 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（既有交互规范下 notice 模式选型错误 + BUG-0003 修复未推广） |
| 根因类型 | code / design / frontend-ui |
| 修复面 | 四列表页 toast 统一；共享样式/可选 AdminToast；Vitest |
| 建议 Change | `fix-admin-list-status-toast-layout` |

## 4. 关联文档

| 文档 | 路径 |
|---|---|
| capture | `capture.md` |
| 缺陷说明 | `bug.md` |
| 根因 | `root-cause.md` |
| 规避 | `workaround.md` |
| 验收 | `acceptance.md` |
| 评审 | `review.md` |
| 参考 BUG | `issues/bugs/BUG-0003-brand-image-display-layout-shift/` |
| 参考 Change | `openspec/changes/archive/2026-06-26-fix-brand-image-display-layout-shift/` |
| 代码线索 | `UserManagementPage.tsx`、`TileCategoryManagementPage.tsx`、`TileSkuManagementPage.tsx`（`.admin-notice`）；`BrandManagementPage.tsx`（`.admin-toast-region`） |
| 样式 | `admin-home.css`（`.admin-notice`）、`brand-management.css`（`.admin-toast-*`） |

## 5. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 12:03:34 | `/capture` | 记录品牌/用户列表状态变更 Tips 推挤页面 |
| 2026-06-27 12:39:11 | `/bug-generate` | 生成 bug.md；范围扩展为品牌/用户/类目/SKU 四页统一 toast |
| 2026-06-27 12:40:41 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；Readiness → Ready |
| 2026-06-27 12:47:06 | `/bug-review` | approved（REV-BUG-0015-001）；可 bug-opsx |
| 2026-06-27 12:48:52 | `/bug-opsx` | 创建 `fix-admin-list-status-toast-layout` OpenSpec Change |
| 2026-06-27 12:51:43 | `/sprint-propose` | 纳入 `sprint-002` 正式范围 |
| 2026-06-27 12:56:14 | `/opsx-apply` | `fix-admin-list-status-toast-layout` apply 完成 |
| 2026-06-27 12:59:21 | `/opsx-archive` | archived；BUG done |

## 6. 后续动作

- 无（已修复归档）
