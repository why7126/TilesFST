# fix-user-reset-password-confirm-ui — Acceptance

来源：`issues/bugs/archive/BUG-0017-user-reset-password-confirm-ui-inconsistency/acceptance.md`

## 重置密码 confirm

- [x] AC-001 重置须先 confirm modal，确认后 API + Toast + 结果弹窗
- [x] AC-002 MUST 禁止 `window.confirm`
- [x] AC-003 取消/遮罩/× 不调用 API，不打开结果弹窗

## 视觉与回归

- [x] AC-004 modal 对齐 Golden Reference（类目启停 / 同页冻结）
- [x] AC-005 `ResetPasswordDialog` MUST NOT 回归（逻辑未改；确认后仍 setResetPassword）
- [x] AC-006 同页冻结/删除 MUST NOT 回归
- [x] AC-007 品牌/类目启停 MUST NOT 回归

## 自动化与范围

- [x] AC-008 Vitest 重置密码 confirm 门禁
- [x] AC-009 纯前端，无 Orval
- [x] AC-010 已删除用户重置按钮状态不回归（未改 disabled 逻辑）
