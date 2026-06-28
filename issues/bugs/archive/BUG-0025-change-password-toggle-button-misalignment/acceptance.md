---
bug_id: BUG-0025-change-password-toggle-button-misalignment
status: pending_review
created_at: 2026-06-28 12:57:00
updated_at: 2026-06-28 12:57:00
related_requirement: REQ-0014-profile-page
related_bug: BUG-0024-change-password-error-wrong-field
---

# 回归验收标准

> 修复本缺陷 MUST 使修改密码弹窗各密码字段的「显示/隐藏」按钮始终相对输入框垂直居中，且 MUST NOT 回归错误提示展示、切换功能与成功改密流程。

## AC-001 原密码字段有错误时 toggle MUST 相对 input 居中

**Given** 用户已打开「修改密码」弹窗  
**When** 原密码字段下方出现错误提示（如服务端返回或当前实现的客户端错误）  
**Then** 原密码字段「显示/隐藏」按钮 MUST 相对该字段 input 垂直居中  
**And** MUST 与同弹窗无错误字段的 toggle 垂直对齐一致

- [ ] AC-001

## AC-002 确认新密码字段有错误时 toggle MUST 相对 input 居中

**Given** 用户已打开弹窗  
**When** 新密码与确认新密码不一致，点击「保存修改」  
**Then** 确认新密码字段下方 MUST 展示 `两次输入的新密码不一致`  
**And** 确认字段「显示/隐藏」按钮 MUST 相对 input 垂直居中，MUST NOT 下沉至 error 区域

- [ ] AC-002

## AC-003 新密码字段有错误时 toggle MUST 相对 input 居中（BUG-0024 修复后）

**Given** BUG-0024 已修复，新密码相关错误挂在新密码字段  
**When** 触发新密码策略/常见密码等错误  
**Then** 新密码字段 toggle MUST 相对 input 垂直居中  
**And** MUST NOT 因 error-text 下沉

- [ ] AC-003

## AC-004 无错误时 toggle 位置 MUST 无回归

**Given** 弹窗打开且三字段均无 error  
**When** 观察各字段 toggle 位置  
**Then** MUST 与修复前无错误场景视觉一致（相对 input 居中）

- [ ] AC-004

## AC-005 显示/隐藏功能 MUST 无回归

**Given** 任一密码字段有或无错误  
**When** 点击「显示/隐藏」  
**Then** input `type` MUST 在 `password` / `text` 间切换  
**And** 按钮文案 MUST 在「显示」/「隐藏」间切换

- [ ] AC-005

## AC-006 error-text MUST 仍在 input 下方且不参与 toggle 定位

**Given** 字段展示错误  
**When** 检查 DOM 结构  
**Then** `error-text` MUST 位于 input 行（input-wrap）之外  
**And** toggle 的定位参照 MUST NOT 包含 error-text 高度

- [ ] AC-006

## AC-007 成功改密与 BUG-0024/0026 MUST 无回归

**Given** 合法输入提交成功  
**When** API 返回成功  
**Then** MUST 保持既有 onSuccess / onClose / 登出流程  
**And** MUST NOT 破坏错误字段映射（BUG-0024）或取消确认行为（BUG-0026）

- [ ] AC-007

## AC-008 修复范围 MUST 为纯前端布局

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API、SQLite、Orval、Docker  
**And** MUST NOT 影响店主端 / 小程序

- [ ] AC-008

## AC-009 单元测试 SHOULD 覆盖结构或行为

**Given** 进入 `fix-change-password-modal-errors`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** SHOULD 新增/更新用例：确认密码不一致时 toggle 位于 input-wrap 内（或等价 DOM 断言）  
**And** `cd src/web && pnpm vitest run src/features/admin/components/ChangePasswordModal` MUST 通过

- [ ] AC-009

## AC-010 视觉验收（MUST）

**Given** 修复完成  
**When** 复现 BUG-0025 截图场景（原密码字段有 error）及确认密码不一致场景  
**Then** 三字段 toggle MUST 水平对齐、相对各自 input 垂直居中  
**And** Change `trace.md` SHOULD 记录与 `screenshots/change-password-toggle-misalignment.png` 并排验收结论

- [ ] AC-010
