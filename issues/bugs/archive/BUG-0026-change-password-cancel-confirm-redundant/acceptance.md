---
bug_id: BUG-0026-change-password-cancel-confirm-redundant
status: pending_review
created_at: 2026-06-28 13:06:10
updated_at: 2026-06-28 13:06:10
related_requirement: REQ-0014-profile-page
related_bug: BUG-0024-change-password-error-wrong-field
---

# 回归验收标准

> 修复本缺陷 MUST 使修改密码弹窗在有输入时关闭不再弹出浏览器二次确认，且 MUST NOT 回归提交校验、成功改密登出与其它弹窗能力。

## AC-001 footer「取消」有输入时 MUST 直接关闭

**Given** 用户已打开「修改密码」弹窗并在任一密码字段输入内容  
**When** 点击 footer「取消」  
**Then** MUST 立即关闭弹窗  
**And** MUST NOT 调用 `window.confirm`  
**And** MUST NOT 出现浏览器原生「当前填写内容尚未保存，确认关闭吗？」对话框

- [ ] AC-001

## AC-002 × / Esc / 遮罩关闭 MUST 同样无 confirm

**Given** 表单已有输入  
**When** 分别点击右上角 ×、按 Esc、点击遮罩  
**Then** 每种方式 MUST 直接关闭弹窗  
**And** MUST NOT 调用 `window.confirm`

- [ ] AC-002

## AC-003 空表单关闭 MUST 无回归

**Given** 三个密码字段均为空  
**When** 使用任一关闭方式  
**Then** MUST 直接关闭，行为与修复前一致

- [ ] AC-003

## AC-004 再次打开 MUST 重置表单

**Given** 用户曾在 dirty 状态下关闭弹窗  
**When** 再次打开「修改密码」弹窗  
**Then** 原密码、新密码、确认新密码 MUST 均为空  
**And** 错误提示 MUST 已清除

- [ ] AC-004

## AC-005 提交与成功改密 MUST 无回归

**Given** 用户填写合法原密码、新密码与确认密码  
**When** 点击「保存修改」且 API 成功  
**Then** MUST 调用 `changePassword`、触发 `onSuccess` 与 `onClose`  
**And** MUST NOT 改变 Toast、logout、跳转登录页既有行为

- [ ] AC-005

## AC-006 客户端校验 MUST 无回归

**Given** 新密码与确认新密码不一致  
**When** 点击「保存修改」  
**Then** MUST 仍在确认字段下方展示 `两次输入的新密码不一致`  
**And** MUST NOT 调用 change-password API

- [ ] AC-006

## AC-007 与管理端其它表单弹窗行为一致

**Given** 修复已合并  
**When** 对比 `BrandFormModal` / `UserFormModal` 关闭行为  
**Then** 改密弹窗关闭 MUST 为直接 `onClose`，无 dirty guard  
**And** `ChangePasswordModal.tsx` MUST NOT 含 `window.confirm`

- [ ] AC-007

## AC-008 单元测试 MUST 更新并通过

**Given** 进入 `fix-change-password-modal-errors`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** `ChangePasswordModal.test.tsx` MUST 移除或改写「dirty 关闭须 confirm」断言  
**And** MUST 新增用例：dirty 时点击「取消」不调用 `window.confirm` 且 `onClose` 被调用  
**And** `cd src/web && pnpm vitest run src/features/admin/components/ChangePasswordModal` MUST 通过

- [ ] AC-008

## AC-009 OpenSpec / REQ-0015 delta MUST 同步

**Given** 缺陷修复经评审批准  
**When** fix change 归档  
**Then** delta spec MUST **MODIFIED**「关闭与脏确认」Scenario（移除或改写脏表单二次确认要求）  
**And** REQ-0015 `acceptance.md` AC-007、AC-040 MUST 与修复行为一致

- [ ] AC-009

## AC-010 修复范围 MUST 为纯前端（除 spec delta）

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** 运行时 MUST NOT 变更 API 契约、SQLite、Orval、Docker  
**And** MUST NOT 影响店主端 / 小程序

- [ ] AC-010

## AC-011 视觉验收（SHOULD）

**Given** 修复完成  
**When** 复现 `screenshots/change-password-cancel-browser-confirm.png` 场景（dirty 后点取消）  
**Then** MUST 直接关闭弹窗，无浏览器对话框  
**And** Change `trace.md` SHOULD 记录取消流程验收结论

- [ ] AC-011
