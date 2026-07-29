---
change_id: fix-admin-sku-edit-save-extra-step
type: fix
created_at: 2026-07-28 23:23:36
updated_at: 2026-07-28 23:34:32
source_bug: BUG-0088-admin-sku-edit-save-extra-step
---

# Proposal

## Why

`BUG-0088-admin-sku-edit-save-extra-step` 反馈：管理端商品 SKU 编辑弹窗在保存成功后没有直接关闭，而是在商品名称上方显示“SKU 已更新...”任务追踪反馈，导致编辑流程多了一步。

## What

- 修复 `TileSkuFormModal` 保存成功后的前端分支。
- 创建、保存草稿、编辑成功时直接触发 `onSuccess(...)` 与 `onClose()`。
- 不再展示弹窗内 task trace feedback 或复制追踪 ID 能力。
- 补充前端回归测试。

## Out Of Scope

- 不修改后端接口。
- 不修改数据库。
- 不修改后端任务追踪生成或响应字段。
- 不修改管理端列表、上架、下架、删除流程。

## Rollback Plan

如修复引发编辑弹窗关闭或列表刷新异常，回滚 `TileSkuFormModal` 保存成功分支和对应测试即可；无 DB/API 迁移回滚。
