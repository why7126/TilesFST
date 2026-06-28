---
change_id: fix-tile-spec-admin-ui
requirement_id: REQ-0009-tile-spec-management
bug_ids:
  - BUG-0027-tile-spec-list-ui-inconsistency
  - BUG-0028-tile-spec-modal-form-layout
  - BUG-0029-tile-spec-list-not-refresh-after-create
created_at: 2026-06-28 13:23:18
updated_at: 2026-06-28 15:28:00
---

# Change Trace — fix-tile-spec-admin-ui

## 1. 关联

| 项 | 值 |
|---|---|
| Change | fix-tile-spec-admin-ui |
| REQ | REQ-0009-tile-spec-management |
| BUG | BUG-0027、BUG-0028、BUG-0029 |
| 类型 | fix |
| 前置 | add-tile-spec-management（已 archive） |

## 2. 验收 Checklist（apply 后填写）

| # | 项 | 参考 | 结果 |
|---|---|---|---|
| 1 | 列表分页 vs 用户管理并排 | BUG-0027 AC-001 | ✓ vitest DOM + 结构对齐 UserManagementPage |
| 2 | 尺寸名称列字号协调 | BUG-0027 AC-003 | ✓ `.size-name` 12px |
| 3 | 弹窗字段顺序 | BUG-0028 AC-001 | ✓ vitest 标签顺序断言 |
| 4 | 备注 textarea 整行 | BUG-0028 AC-003 | ✓ `.form-full` + width 100% + height 112px |
| 5 | 新增/编辑保存后列表刷新 | BUG-0029 AC-001 | ✓ onSuccess + loadSpecs；vitest fetch×2 |
| 6 | 弹窗 vs modal HTML 并排 | AC-046 | ✓ 字段顺序与 prototype 一致 |

**延后**：BUG-0028 AC-010（AC-021 宽长冲突 inline 提示）— 本 sprint 不做。

## 3. 测试

| 套件 | 结果 |
|---|---|
| `TileSpecManagementPage.test.tsx` | 2/2 pass |
| `TileSpecFormModal.test.tsx` | 2/2 pass |
| `vite build` | ✓ |

## 4. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 15:28:00 | `/sprint-apply` | 分页/弹窗/刷新修复 + vitest；30/31 tasks（待 archive） |
| 2026-06-28 13:23:18 | `/bug-opsx` | 创建 change；关联 BUG-0027/0028/0029 |
