---
bug_id: BUG-0024-change-password-error-wrong-field
status: pending_review
created_at: 2026-06-28 12:55:16
updated_at: 2026-06-28 12:55:16
related_requirement: REQ-0014-profile-page
related_bug: BUG-0025-change-password-toggle-button-misalignment
---

# 回归验收标准

> 修复本缺陷 MUST 使修改密码弹窗的错误提示按字段正确挂载，且 MUST NOT 回归确认密码校验、成功改密登出与其它弹窗能力。

## AC-001 新密码客户端校验错误 MUST 显示在新密码字段下方

**Given** 用户已打开「修改密码」弹窗  
**When** 填写原密码后，新密码不符合 8–32 位或缺少字母/数字，点击「保存修改」  
**Then** MUST 在新密码 `PasswordField` 下方展示 `新密码不符合安全策略`（或等价文案）  
**And** MUST NOT 在原密码字段下方展示该文案  
**And** 错误区域 MUST 含 `role="alert"`

- [ ] AC-001

## AC-002 新密码与原密码相同错误 MUST 显示在新密码字段下方

**Given** 用户已打开弹窗  
**When** 新密码与原密码相同且确认一致，点击「保存修改」  
**Then** MUST 在新密码字段下方展示 `新密码不能与原密码相同`  
**And** MUST NOT 在原密码字段下方展示该文案

- [ ] AC-002

## AC-003 服务端「过于常见」错误 MUST 显示在新密码字段下方

**Given** 用户填写正确原密码与过于常见的新密码（如 `password123` 类），确认一致  
**When** 点击「保存修改」触发 API 返回 `PASSWORD_CHANGE_WEAK`（40022）  
**Then** MUST 在新密码字段下方展示 `新密码过于常见，请更换`  
**And** MUST NOT 在原密码字段下方展示该文案

- [ ] AC-003

## AC-004 原密码不正确错误 MUST 仍显示在原密码字段下方

**Given** 用户填写错误原密码与合法新密码  
**When** 点击「保存修改」触发 API 返回 `PASSWORD_CHANGE_OLD_INCORRECT`（40020）  
**Then** MUST 在原密码字段下方展示 `原密码不正确`（或等价文案）  
**And** 新密码字段 MUST NOT 误显示该错误

- [ ] AC-004

## AC-005 确认新密码不一致 MUST 无回归

**Given** 新密码与确认新密码不一致  
**When** 点击「保存修改」  
**Then** MUST 仍在确认新密码字段下方展示 `两次输入的新密码不一致`  
**And** MUST NOT 调用 change-password API

- [ ] AC-005

## AC-006 错误时对应输入框 MUST 应用 error 样式

**Given** 任一字段展示错误提示  
**When** 检查该字段 `input` 元素  
**Then** MUST 含 `error` class（或等价 DS 错误态）  
**And** 无错误的字段 MUST NOT 误标 error 态

- [ ] AC-006

## AC-007 成功改密流程 MUST 无回归

**Given** 用户填写合法原密码、新密码与确认密码  
**When** 点击「保存修改」且 API 成功  
**Then** MUST 调用 `changePassword`、触发 `onSuccess` 与 `onClose`  
**And** MUST NOT 改变登出/重登既有行为

- [ ] AC-007

## AC-008 修复范围 MUST 为纯前端

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API 契约、SQLite、Orval、Docker  
**And** MUST NOT 影响店主端 / 小程序

- [ ] AC-008

## AC-009 单元测试 MUST 覆盖字段位置

**Given** 进入 `fix-change-password-modal-errors`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** `ChangePasswordModal.test.tsx` MUST 新增/更新用例断言新密码相关错误出现在新密码字段容器内  
**And** 原密码错误、确认不一致、成功提交既有用例 MUST 仍通过  
**And** `cd src/web && pnpm vitest run src/features/admin/components/ChangePasswordModal` MUST 通过

- [ ] AC-009

## AC-010 视觉验收（SHOULD）

**Given** 修复完成  
**When** 复现 BUG-0024 截图场景（常见密码失败）  
**Then** 红色错误文案 MUST 位于「新密码」输入框正下方  
**And** Change `trace.md` SHOULD 记录字段对齐验收结论

- [ ] AC-010
