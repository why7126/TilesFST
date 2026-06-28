## Why

[BUG-0047-system-settings-save-tip-layout-shift](issues/bugs/archive/BUG-0047-system-settings-save-tip-layout-shift/) 已评审：保存成功 `settings-save-tip` 插入文档流导致 layout shift；对齐 BUG-0015 `AdminToast` 模式。

## What Changes

- 保存/恢复成功反馈改用 `AdminLayout` `AdminToast`（或等价 fixed 层）。
- 移除条件渲染 `settings-save-tip` 推挤布局。
- MODIFIED system-settings spec AC-012。
- Vitest 断言 toast region。

## Capabilities

### Modified Capabilities

- `system-settings`：MODIFIED「管理端系统设置页面与分组导航」— 非推挤成功提示。

## Rollback Plan

恢复 inline `settings-save-tip`。
