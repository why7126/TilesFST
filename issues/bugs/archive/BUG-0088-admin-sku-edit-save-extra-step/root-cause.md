---
bug_id: BUG-0088-admin-sku-edit-save-extra-step
status: done
created_at: 2026-07-28 23:23:36
updated_at: 2026-07-29 08:05:05
---

# Root Cause

## 直接原因

`TileSkuFormModal` 的保存成功处理对创建和编辑共用同一段 task trace feedback 逻辑：只要接口返回 `task_trace_id`，就调用 `setTaskTraceFeedback(...)` 并保持弹窗打开。

## 根本原因

SKU 表单保存成功是一个完成态操作，应直接关闭弹窗；但当前实现把 task trace feedback 当作保存成功后的中间态展示，导致创建和编辑成功后都可能出现额外步骤和上方 tips。

## 触发条件

- `mode === 'edit'`
- `updateTileSku(...)` 成功
- 响应中包含 `task_trace_id`

## 分类

code / frontend-state-flow
