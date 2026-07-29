---
bug_id: BUG-0088-admin-sku-edit-save-extra-step
status: done
created_at: 2026-07-28 23:23:36
updated_at: 2026-07-29 08:05:05
---

# Acceptance

## AC-BUG-0088-01 编辑保存成功直接关闭

- **WHEN** 管理端 SKU 编辑弹窗提交合法修改且 `updateTileSku` 成功
- **THEN** 弹窗 MUST 直接关闭
- **AND** 列表 MUST 刷新

## AC-BUG-0088-02 编辑保存成功不显示弹窗内更新 tips

- **WHEN** 编辑保存成功响应包含 `task_trace_id`
- **THEN** 弹窗内 MUST NOT 显示“SKU 已更新...”任务追踪 feedback
- **AND** 商品名称上方 MUST NOT 出现成功 tips

## AC-BUG-0088-03 创建保存成功也不显示弹窗内追踪反馈

- **WHEN** 新增 SKU 成功响应包含 `task_trace_id`
- **THEN** 弹窗 MUST 直接关闭
- **AND** 弹窗内 MUST NOT 显示任务追踪 feedback 或复制追踪 ID 入口

## AC-BUG-0088-04 错误与上传中校验不回归

- **WHEN** 视频仍在上传或保存失败
- **THEN** 仍 MUST 显示原有错误提示并保持弹窗打开
