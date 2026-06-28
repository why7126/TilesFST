## Why

[BUG-0046-system-settings-reset-confirm-ui-inconsistency](issues/bugs/archive/BUG-0046-system-settings-reset-confirm-ui-inconsistency/) 已评审：「恢复默认」与 dirty Tab 切换使用 `window.confirm`，与管理端 DS modal 不一致（参考 BUG-0037）。

## What Changes

- 恢复默认、Tab 切换放弃修改改用 `modal-backdrop` + `.btn` 确认弹窗。
- 移除 `window.confirm`。
- MODIFIED system-settings spec。
- Vitest 断言 dialog。

## Capabilities

### Modified Capabilities

- `system-settings`：MODIFIED「管理端系统设置页面与分组导航」— DS 确认弹窗。

## Rollback Plan

恢复 `window.confirm` 实现。
