## Context

- **BUG**: BUG-0043（low），关联 BUG-0023
- **Reference**: `fix-profile-duplicate-save-buttons`

## Decisions

### D1：仅保留 footer「保存设置」

- 页头移除保存按钮；dirty badge 保留。

## Test Plan

- `getByRole('button', { name: '保存设置' })` 单断言。
- PATCH 行为无回归。
