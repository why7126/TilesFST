---
created_at: 2026-06-27 08:42:28
title: 缺陷追踪
purpose: BUG-0001 瓷砖类目停用行缺少启用入口
content: 关联 REQ、Change 与代码位置
owner: product
status: done
note: /opsx-apply + archive 完成（2026-06-20）
iteration: sprint-002
readiness: ready
updated_at: 2026-06-27 15:52:00
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0001-tile-category-enable-missing
bug_name: tile-category-enable-missing
severity: high
status: done
iteration: sprint-002
related_requirement: REQ-0005-tile-category-management
related_change: add-tile-category-management
suggested_fix_change: fix-tile-category-enable-action
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-20
  generated: 2026-06-20
  completed: 2026-06-20
  reviewed: 2026-06-20
  approved: 2026-06-20
openspec_changes:
  - change_id: fix-tile-category-enable-action
    type: fix
    status: archived
    bug_id: BUG-0001-tile-category-enable-missing```

## 2. Readiness

| 文档 | 状态 |
|---|---|
| capture.md | ✓ |
| bug.md | ✓ |
| root-cause.md | ✓ |
| workaround.md | ✓ |
| acceptance.md | ✓ |
| trace.md | ✓ |
| review.md | ✓ approved |

**Readiness:** Ready

## 3. 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | **缺陷（BUG）** |
| 根因类型 | code（前端条件渲染） |
| 修复面 | 仅 Web 管理端列表操作列 + vitest |

## 4. 关联文档

| 文档 | 路径 |
|---|---|
| capture | `capture.md` |
| 缺陷说明 | `bug.md` |
| 根因 | `root-cause.md` |
| 规避 | `workaround.md` |
| 验收 | `acceptance.md` |
| 父需求 | `issues/requirements/REQ-0005-tile-category-management/` |
| 实现 | `src/web/src/pages/admin/TileCategoryManagementPage.tsx` |
| 参考 | `src/web/src/pages/admin/BrandManagementPage.tsx` |

## 5. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-20 | `/bug-capture` | 记录停用+SKU=0 行缺少启用入口 |
| 2026-06-20 | `/bug-complete` | 补齐 bug / root-cause / workaround / acceptance；status → pending_review |
| 2026-06-20 | `/bug-review` | approved（REV-BUG-0001-001） |
| 2026-06-20 | `/bug-opsx` | 创建 `fix-tile-category-enable-action` |
| 2026-06-20 | `/sprint-propose` | 纳入 sprint-002 |
| 2026-06-20 | `/opsx-apply` | 修复操作列；vitest 3/3；build 通过 |
| 2026-06-20 | `/opsx-archive` | 归档至 `2026-06-20-fix-tile-category-enable-action`（--skip-specs） |

## 6. 后续动作

1. ~~`/opsx-archive fix-tile-category-enable-action`~~ ✓ 已归档
