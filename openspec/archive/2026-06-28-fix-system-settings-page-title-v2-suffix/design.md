## Context

- **BUG**: BUG-0042（low）
- **REQ**: REQ-0017-system-settings
- **Parent**: `add-system-settings`

## Bug Analysis Report

| 项 | 结论 |
|---|---|
| 直接原因 | L798 硬编码 `/ V2` |
| 根因 | prototype CSS port 带入版本后缀 |
| 修复面 | 单行 TSX + prototype HTML |

## Decisions

### D1：眉标固定为 `SYSTEM / SYSTEM SETTINGS`

- 移除 `/ V2`；不重复侧栏版本 pill。

## Test Plan

- Vitest：断言 `.eyebrow` 文本。
- 手工：5 Tab 眉标一致。
