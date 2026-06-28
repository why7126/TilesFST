## Context

- **BUG**: BUG-0046（medium）
- **Golden Reference**: `TileSpecManagementPage` status confirm modal

## Decisions

### D1：两类 confirm 均改 DS modal

- reset confirm + dirty tab switch confirm

### D2：复用 admin-home.css modal 结构

- `role="dialog"`、`modal-backdrop`、取消/主按钮

## Test Plan

- vitest：dialog 可见；`window.confirm` 未调用
- reset API 行为无回归
