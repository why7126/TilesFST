---
created_at: 2026-06-28 16:59:15
title: 缺陷追踪
purpose: BUG-0038 SKU弹窗规格字段下方提示样式不当
content: 记录历史 SKU 规格未匹配提示字号过大、颜色过亮
owner: product
status: done
lifecycle_stage: archive
readiness: ready
note: fix-tile-sku-modal-spec-hint-styling 已 apply + archive
updated_at: 2026-06-28 19:40:42
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0038-tile-sku-modal-spec-hint-styling
bug_name: tile-sku-modal-spec-hint-styling
severity: low
status: done
iteration: sprint-003
related_requirement: REQ-0006-tile-sku-management
related_bug: null
related_change: fix-tile-sku-modal-spec-hint-styling
suggested_fix_change: fix-tile-sku-modal-spec-hint-styling
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-28 16:59:15
  generated: 2026-06-28 17:01:36
  completed: 2026-06-28 17:02:26
  reviewed: 2026-06-28 17:08:07
  approved: 2026-06-28 17:08:07
  opsx: 2026-06-28 17:11:26
  applied: 2026-06-28 17:18:22
  archived: 2026-06-28 17:20:00
openspec_changes:
  - change_id: fix-tile-sku-modal-spec-hint-styling
    type: fix
    status: archived
    bug_id: BUG-0038-tile-sku-modal-spec-hint-styling```

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
| 根因类型 | code / frontend-ui（误用未定义 `form-hint`，应复用 `form-help`） |
| 修复面 | Web 管理端 `TileSkuFormModal.tsx` |
| 建议 Change | `fix-tile-sku-modal-spec-hint-styling` |

## 4. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 17:20:00 | `/opsx-archive` | change archived；status → done |
| 2026-06-28 17:18:22 | `/opsx-apply` | `form-hint` → `form-help`；Vitest 10/10；待 archive |
| 2026-06-28 17:11:26 | `/bug-opsx` | 创建 change `fix-tile-sku-modal-spec-hint-styling` |
| 2026-06-28 17:08:07 | `/bug-review --approve` | REV-BUG-0038-001 通过；status → approved；plan → review |
| 2026-06-28 17:02:26 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；status → pending_review |
| 2026-06-28 17:01:36 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-06-28 16:59:15 | `/bug-capture` | 记录 SKU 弹窗规格下方提示字号与颜色不符合 Design System |
