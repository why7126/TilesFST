## Why

[BUG-0043-system-settings-duplicate-save-buttons](issues/bugs/archive/BUG-0043-system-settings-duplicate-save-buttons/) 已评审：页头与底部重复「保存设置」，对齐 `fix-profile-duplicate-save-buttons` 单 CTA 模式。

## What Changes

- 移除 `settings-hero-actions` 内「保存设置」；保留底部 footer。
- 保留页头 dirty badge。
- MODIFIED AC-009 / system-settings spec。
- 更新 `SystemSettingsPage.test.tsx`。

## Capabilities

### Modified Capabilities

- `system-settings`：MODIFIED「管理端系统设置页面与分组导航」— 单保存入口。

## Impact

Web 管理端 only；无 API/DB。

## Rollback Plan

恢复页头保存按钮与双按钮测试。
