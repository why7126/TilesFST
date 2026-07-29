---
change_id: fix-admin-sku-edit-save-extra-step
created_at: 2026-07-28 23:23:36
updated_at: 2026-07-28 23:34:32
---

# Design

## Root Cause

编辑和创建共用保存成功后的 task trace feedback 分支。当前实现只要响应包含 `task_trace_id`，就展示弹窗内反馈并保持弹窗打开；该反馈对 SKU 表单保存流程都是多余步骤。

## Approach

- 在 `handleSave` 成功分支中忽略响应中的 `task_trace_id` 展示状态。
- 创建、保存草稿、编辑成功时均调用对应 `onSuccess(...)` 并关闭弹窗。
- 移除弹窗内 task trace feedback、复制追踪 ID 状态和 footer 完成按钮分支。
- 不改请求 payload、接口响应处理、错误处理和上传中拦截。

## Testing

- 更新 `TileSkuFormModal.test.tsx`：
  - 编辑保存成功且响应包含 `task_trace_id` 时直接关闭弹窗。
  - 创建成功且响应包含 `task_trace_id` 时直接关闭弹窗。
  - 不显示弹窗内 task trace feedback / 复制追踪 ID。

## Impact

- Backend/API/DB/Orval：无影响。
- Web Admin：影响 SKU 编辑弹窗成功态。
- Miniapp/Storage/Docker：无影响。
