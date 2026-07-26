---
created_at: 2026-06-28 13:00:00
updated_at: 2026-06-28 15:16:00
---

# fix-change-password-modal-errors — Trace

| 字段 | 值 |
|---|---|
| change_id | fix-change-password-modal-errors |
| bug_ids | BUG-0024、BUG-0025、BUG-0026 |
| iteration | sprint-003 |
| status | applied |

## 验收结论

| BUG | 结论 |
|---|---|
| BUG-0024 | ✓ per-field 错误分流；40022 显示在新密码字段下 |
| BUG-0025 | ✓ `.password-input-wrap` + toggle `top:50%`；error 在 wrap 外 |
| BUG-0026 | ✓ 移除 `window.confirm`；dirty 取消直接关闭 |

**测试：** `ChangePasswordModal.test.tsx` 9 passed；build ✓

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-28 15:16:00 | `/sprint-apply` | 实现 + vitest；openspec_changes → applied |
