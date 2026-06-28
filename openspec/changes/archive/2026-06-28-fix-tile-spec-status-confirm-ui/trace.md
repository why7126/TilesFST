---
change_id: fix-tile-spec-status-confirm-ui
requirement_id: REQ-0009-tile-spec-management
bug_ids:
  - BUG-0037-tile-spec-status-confirm-ui-inconsistency
created_at: 2026-06-28 16:18:39
updated_at: 2026-06-28 16:35:12
---

# Change Trace — fix-tile-spec-status-confirm-ui

## 1. 关联

| 项 | 值 |
|---|---|
| Change | fix-tile-spec-status-confirm-ui |
| REQ | REQ-0009-tile-spec-management |
| BUG | BUG-0037-tile-spec-status-confirm-ui-inconsistency |
| 类型 | fix |
| 前置 | add-tile-spec-management、fix-tile-spec-admin-ui（已 archived） |

## 2. 验收 Checklist（apply 后填写）

| # | 项 | 参考 | 结果 |
|---|---|---|---|
| 1 | 停用 confirm vs 类目并排 | BUG-0037 AC-001/005 | ✓ vitest 文案 + modal 结构对齐 TileCategoryManagementPage |
| 2 | 启用 confirm 文案/按钮 | BUG-0037 AC-002 | ✓ 「确认启用」+ page-desc |
| 3 | 删除 confirm 文案/按钮 | BUG-0037 AC-003 | ✓ 「删除规格」+ btn primary（无 danger） |
| 4 | 取消/× 无副作用 | BUG-0037 AC-004 | ✓ 沿用 setState(null)；未改 handler |
| 5 | 无 confirm-card / danger | BUG-0037 AC-005 | ✓ 已移除 |
| 6 | Vitest 停用 confirm 门禁 | BUG-0037 AC-008 | ✓ 3/3 TileSpecManagementPage tests pass |
| 7 | 分页/刷新不回归 | BUG-0037 AC-006 | ✓ 既有用例 pass |
| 8 | REQ-0009 AC-013/018 | BUG-0037 AC-010 | ✓ spec delta 对齐；待 archive 后勾选 REQ acceptance |

## 3. 测试

| 套件 | 结果 |
|---|---|
| `TileSpecManagementPage.test.tsx` | 3/3 pass |
| `TileCategoryManagementPage.test.tsx` | 回归 pass |
| `BrandManagementPage.test.tsx` | 回归 pass |
| `npx vite build` | ✓ |

## 4. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 16:48:07 | `/opsx-archive` | archived；web-client spec MODIFIED 1 requirement |
| 2026-06-28 16:35:12 | `/opsx-apply` | 启停/删除 confirm 对齐类目页 + vitest；16/18 tasks（待 archive） |
| 2026-06-28 16:18:39 | `/bug-opsx` | 创建 change；关联 BUG-0037 |
