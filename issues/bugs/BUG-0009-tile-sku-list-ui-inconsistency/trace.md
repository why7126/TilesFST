---
created_at: 2026-06-27 08:56:54
title: 缺陷追踪
purpose: BUG-0009 瓷砖SKU列表页分页与表格标题行 UI 不一致
content: 记录 SKU 列表分页与用户管理页不一致、表头上方多余标题行问题
owner: product
status: done
note: fix-tile-sku-list-ui-inconsistency 已 archive；BUG done
iteration: sprint-002
readiness: ready
updated_at: 2026-06-27 15:52:00
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0009-tile-sku-list-ui-inconsistency
bug_name: tile-sku-list-ui-inconsistency
severity: medium
status: done
iteration: sprint-002
related_requirement: REQ-0006-tile-sku-management
related_change: fix-tile-sku-list-ui-inconsistency
suggested_fix_change: fix-tile-sku-list-ui-inconsistency
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-27 08:56:54
  generated: 2026-06-27 10:12:15
  completed: 2026-06-27 10:18:43
  reviewed: 2026-06-27 10:20:38
  approved: 2026-06-27 10:20:38
  in_sprint: 2026-06-27 10:22:09
  opsx_created: 2026-06-27 10:24:16
  applied: 2026-06-27 10:32:30
  archived: 2026-06-27 10:40:49
openspec_changes:
  - change_id: fix-tile-sku-list-ui-inconsistency
    type: fix
    status: archived
    bug_id: BUG-0009-tile-sku-list-ui-inconsistency```

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
| 需求 vs 缺陷 | 缺陷（BUG） |
| 根因类型 | design / frontend-ui（分页 DOM 复用废弃 brand 结构；table-card 内多余标题行） |
| 修复面 | Web 管理端瓷砖 SKU 列表页 |
| 建议 Change | `fix-tile-sku-list-ui-inconsistency` |

## 4. 关联文档

| 文档 | 路径 |
|---|---|
| capture | `capture.md` |
| 缺陷说明 | `bug.md` |
| 根因 | `root-cause.md` |
| 规避 | `workaround.md` |
| 验收 | `acceptance.md` |
| 评审 | `review.md` |
| 父需求 | `issues/requirements/REQ-0006-tile-sku-management/` |
| 需求 AC-019～021 / AC-051 / AC-054 | `issues/requirements/REQ-0006-tile-sku-management/acceptance.md` |
| UI 规范 | `rules/ui-design.md` |
| 列表原型 | `issues/requirements/REQ-0006-tile-sku-management/prototype/web/tile-sku-management-list.html` |
| 参考页面 | `src/web/src/pages/admin/UserManagementPage.tsx` |
| 代码线索 | `src/web/src/pages/admin/TileSkuManagementPage.tsx` |
| 样式 | `src/web/src/features/admin/styles/tile-sku-management.css` |
| 同类修复参考 | BUG-0002 / `BrandManagementPage.test.tsx` |
| OpenSpec | `openspec/changes/archive/2026-06-27-fix-tile-sku-list-ui-inconsistency/` |

## 5. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 08:56:54 | `/bug-capture` | 记录 SKU 列表分页不一致与表头上方多余标题行 |
| 2026-06-27 10:12:15 | `/bug-generate` | 生成 `bug.md`，trace 状态 → draft |
| 2026-06-27 10:18:43 | `/bug-complete` | 补齐 root-cause / workaround / acceptance；状态 → pending_review |
| 2026-06-27 10:20:38 | `/bug-review` | approved（REV-BUG-0009-001），可 bug-opsx |
| 2026-06-27 10:22:09 | Sprint scope update | 纳入 `sprint-002` |
| 2026-06-27 10:24:16 | `/bug-opsx` | 创建 `fix-tile-sku-list-ui-inconsistency` |
| 2026-06-27 10:32:30 | `/opsx-apply` | 分页对齐 + 移除 table-head + Vitest；change → applied |
| 2026-06-27 10:40:49 | `/opsx-archive` | 归档 `fix-tile-sku-list-ui-inconsistency`；BUG → done |

## 6. 后续动作

已完成，无后续动作。
