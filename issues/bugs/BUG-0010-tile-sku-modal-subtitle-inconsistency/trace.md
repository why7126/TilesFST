---
created_at: 2026-06-27 08:56:54
title: 缺陷追踪
purpose: BUG-0010 SKU弹窗副标题与品牌弹窗样式不一致
content: 记录 SKU 新增/编辑弹窗副标题 Typography 未对齐管理端弹窗规范
owner: product
status: done
note: fix-tile-sku-modal-subtitle-inconsistency 已 apply；待 archive
iteration: sprint-002
readiness: ready
updated_at: 2026-06-27 15:52:00
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0010-tile-sku-modal-subtitle-inconsistency
bug_name: tile-sku-modal-subtitle-inconsistency
severity: medium
status: done
iteration: sprint-002
related_requirement: REQ-0006-tile-sku-management
related_change: fix-tile-sku-modal-subtitle-inconsistency
suggested_fix_change: fix-tile-sku-modal-subtitle-inconsistency
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-27 08:56:54
  generated: 2026-06-27 12:02:52
  completed: 2026-06-27 12:02:52
  reviewed: 2026-06-27 12:02:52
  approved: 2026-06-27 12:02:52
  in_sprint: 2026-06-27 12:02:52
  opsx_created: 2026-06-27 12:02:52
  applied: 2026-06-27 12:02:52
openspec_changes:
  - change_id: fix-tile-sku-modal-subtitle-inconsistency
    type: fix
    status: archived
    bug_id: BUG-0010-tile-sku-modal-subtitle-inconsistency```

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

## 5. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 08:56:54 | `/bug-capture` | 记录 SKU 弹窗副标题与品牌弹窗样式不一致 |
| 2026-06-27 12:02:52 | 副标题 UI 修复并入 | 共享 modal-desc；创建 fix change 并标记 applied |

## 6. 后续动作

- `/opsx-archive fix-tile-sku-modal-subtitle-inconsistency`
