---
bug_id: BUG-0046-system-settings-reset-confirm-ui-inconsistency
status: pending_review
created_at: 2026-06-28 18:35:49
updated_at: 2026-06-28 18:35:49
root_cause_type: code
---

# 根因分析

## 1. 直接原因

### 1.1 恢复默认使用 `window.confirm`

`SystemSettingsPage.tsx` L176：

```tsx
if (!window.confirm('确定恢复该分组为默认配置吗？此操作不可撤销。')) return;
```

### 1.2 Tab 切换 dirty 确认亦用原生 confirm

L163：`window.confirm('有未保存的修改，确定放弃并切换分组吗？')`

### 1.3 管理端其它页已统一为 inline modal

`BrandManagementPage`、`TileSpecManagementPage`、`UserManagementPage` 等使用 `modal-backdrop` + `role="dialog"` + `.btn` / `.btn.primary` 模式（BUG-0037 已修复规格页）。

## 2. 根本原因

### 2.1 实现 shortcut 未 follow 项目 confirm 惯例

`add-system-settings` 开发时以 `window.confirm` 快速满足 AC-011「二次确认」语义，未 port Design System modal 结构。

### 2.2 AC-011 未限定 confirm 呈现形式

REQ 只要求「恢复默认二次确认」，未禁止原生对话框；与全站 UI/UE 一致性目标存在 gap。

## 3. 触发条件

1. 点击底部「恢复默认」→ 原生 confirm。
2. dirty 态切换 Tab → 原生 confirm。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / frontend-ui |
| 关联 BUG | BUG-0037、BUG-0017 |
| 建议 Change | `fix-system-settings-reset-confirm-ui` |

## 5. 后续修复建议

1. 新增 `resetConfirmOpen` / `tabSwitchConfirmTarget` state。
2. 复用 `TileSpecManagementPage` modal 结构与 `admin-home.css`。
3. vitest 断言 dialog 出现，不再 mock `window.confirm`。
