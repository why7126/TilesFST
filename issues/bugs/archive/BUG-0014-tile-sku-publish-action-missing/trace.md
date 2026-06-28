---
created_at: 2026-06-27 12:03:34
title: 缺陷追踪
purpose: BUG-0014 SKU列表已下架行缺少上架操作
content: 记录瓷砖 SKU 列表对已下架行无上架入口
owner: product
status: done
lifecycle_stage: archive
note: fix-tile-sku-publish-action-missing 已 archive；BUG done
iteration: sprint-002
readiness: ready
updated_at: 2026-06-27 22:33:15
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0014-tile-sku-publish-action-missing
bug_name: tile-sku-publish-action-missing
severity: high
status: done
iteration: sprint-002
related_requirement: REQ-0006-tile-sku-management
related_bug: BUG-0001-tile-category-enable-missing
related_change: fix-tile-sku-publish-action-missing
suggested_fix_change: fix-tile-sku-publish-action-missing
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-27 12:03:34
  generated: 2026-06-27 12:14:24
  completed: 2026-06-27 12:18:20
  reviewed: 2026-06-27 12:19:51
  approved: 2026-06-27 12:19:51
  opsx_created: 2026-06-27 12:21:11
  applied: 2026-06-27 12:25:35
  archived: 2026-06-27 12:29:15
openspec_changes:
  - change_id: fix-tile-sku-publish-action-missing
    type: fix
    status: archived
    bug_id: BUG-0014-tile-sku-publish-action-missing```

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
| 需求 vs 缺陷 | 缺陷（REQ-0006 已要求上下架/恢复；实现遗漏 DISABLED 行入口） |
| 根因类型 | code / frontend-ui（操作列条件渲染） |
| 修复面 | Web 管理端 SKU 列表页操作列 |
| 建议 Change | `fix-tile-sku-publish-action-missing` |

## 4. 关联文档

| 文档 | 路径 |
|---|---|
| capture | `capture.md` |
| 缺陷说明 | `bug.md` |
| 根因 | `root-cause.md` |
| 规避 | `workaround.md` |
| 验收 | `acceptance.md` |
| 评审 | `review.md` |
| 父需求 | `issues/requirements/archive/REQ-0006-tile-sku-management/` |
| 需求 AC | AC-018、AC-037、FR-007 |
| 业务流 | `issues/requirements/archive/REQ-0006-tile-sku-management/business-flow.md` §6 |
| 参考修复 | `openspec/changes/archive/2026-06-20-fix-tile-category-enable-action/` |
| 代码线索 | `src/web/src/pages/admin/TileSkuManagementPage.tsx`（L349–365） |
| API | `src/web/src/features/admin/api/tile-skus-api.ts` |

## 5. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 12:03:34 | `/capture` | 记录 SKU 列表已下架行缺少上架操作 |
| 2026-06-27 12:14:24 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-06-27 12:18:20 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；Readiness → Ready |
| 2026-06-27 12:19:51 | `/bug-review` | approved（REV-BUG-0014-001）；可 bug-opsx |
| 2026-06-27 12:21:11 | `/bug-opsx` | 创建 `fix-tile-sku-publish-action-missing` |
| 2026-06-27 12:22:44 | `/sprint-propose` | 纳入 `sprint-002` 正式范围 |
| 2026-06-27 12:25:35 | `/opsx-apply` | `fix-tile-sku-publish-action-missing` apply 完成 |
| 2026-06-27 12:29:15 | `/opsx-archive` | archived；BUG done |

## 6. 后续动作

- 无（已修复归档）
