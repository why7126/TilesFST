---
title: 管理端一次性密码复制可靠性修复设计
purpose: 说明 BUG-0059 的根因、修复方案、测试与安全边界
created_at: 2026-07-06 15:33:45
updated_at: 2026-07-06 16:05:44
status: archived
owner: frontend
related_bug: BUG-0059-user-password-copy-not-working
---

# Design

## Bug Analysis Report

| Item | 内容 |
|---|---|
| BUG | `BUG-0059-user-password-copy-not-working` |
| 严重等级 | high |
| 影响端 | Web 管理端 |
| 影响页面 | `/admin/users` |
| 影响组件 | `src/web/src/features/admin/components/ResetPasswordDialog.tsx` |
| 关联需求 | `REQ-0005-user-management` |
| 关联 Sprint | `sprint-005` |

### 现象

- 创建新用户成功后，一次性初始密码弹窗展示，但点击「复制密码」后无法可靠粘贴出当前展示的 `initial_password`。
- 重置已有用户密码成功后，一次性随机密码弹窗展示，但点击「复制密码」后无法可靠粘贴出当前展示的 `password`。
- 点击复制后缺少成功或失败反馈，管理员无法判断复制是否完成。

### 根因分类

| 分类 | 结论 |
|---|---|
| API | 暂未发现后端返回缺失；创建用户与重置密码接口均返回一次性明文密码 |
| DB | 不涉及 schema 或持久化缺陷 |
| Frontend Interaction | 主要根因；复制动作假设 Clipboard API 必然可用且必然成功 |
| Test Coverage | 现有 `UserManagementPage.test.tsx` mock 掉 `ResetPasswordDialog`，未覆盖复制按钮 |
| Security | 涉及一次性密码交付可靠性，但不涉及权限绕过 |

## Current Behavior

`ResetPasswordDialog` 当前复制逻辑直接执行：

```typescript
await navigator.clipboard.writeText(password);
```

缺口：

- 未判断 `navigator.clipboard` 或 `writeText` 是否存在。
- Clipboard API 写入失败时进入空 `catch`，管理员无感知。
- 成功时没有 UI/ARIA 反馈。
- 失败时没有手动复制指引或选中文本 fallback。
- 组件没有专项测试。

## Proposed Solution

### 1. 复制状态模型

在 `ResetPasswordDialog` 内维护轻量复制状态：

| State | 触发 | UI |
|---|---|---|
| idle | 弹窗初始打开 | 仅展示一次性密码和风险提示 |
| success | `writeText(password)` resolve | 展示「已复制」或等价成功提示 |
| fallback | Clipboard API 不存在或 `writeText` reject | 展示失败提示和手动复制指引，尽可能选中输入框文本 |

实现建议：

- 使用 `useRef<HTMLInputElement>` 绑定密码输入框。
- 成功前优先检测 `navigator.clipboard?.writeText`。
- 失败或不可用时调用 `inputRef.current?.focus()` 与 `inputRef.current?.select()`，帮助管理员手动复制。
- 不吞掉异常；不需要把异常细节展示给用户，避免泄露浏览器/环境信息。
- 反馈文案可使用弹窗内 `role="status"` / `aria-live="polite"` 的轻量状态区域。

### 2. 安全边界

- 一次性明文密码仍只来自现有 API 返回并保存在当前页面内存状态。
- 不写入 localStorage、sessionStorage、IndexedDB、URL、日志、审计事件或长期文档。
- 不新增再次查询一次性明文密码的接口。
- 关闭弹窗后仍不可再次查看同一密码。

### 3. UI 与 Design System

- 沿用现有 `modal-backdrop` / `modal-card` 结构，不引入新的弹窗宽度策略。
- 若新增提示样式，必须使用既有管理端 CSS 变量或 semantic token，不新增裸 Hex。
- 复制成功/失败提示不得推挤弹窗布局造成明显抖动。
- 对照 `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`，不得新增通用 `modal-card` 与专属类双挂载冲突。

## Test Plan

### Frontend Unit / Component Tests

新增 `ResetPasswordDialog` 组件测试，建议路径：

```text
src/web/src/features/admin/components/ResetPasswordDialog.test.tsx
```

覆盖：

- 成功路径：点击「复制密码」后调用 `navigator.clipboard.writeText(currentPassword)`。
- 成功反馈：页面展示「已复制」或等价成功提示。
- 失败路径：`writeText` reject 时展示失败提示或手动复制指引。
- Clipboard API 不存在：展示 fallback，并尽可能选中密码输入框。
- 安全提示：继续展示「关闭后不可再次查看」或等价风险说明。
- 关闭行为：点击关闭后由父级关闭，不新增密码持久化。

### Regression Tests

- 保留或更新 `UserManagementPage.test.tsx` 中创建用户/重置密码链路测试，确认弹窗仍由 API 返回的一次性密码触发。
- 确认受保护账号的重置密码按钮仍置灰，不调用 reset-password API。
- 不运行 Orval，除非 apply 阶段发现 API 契约被修改。

## Acceptance Mapping

| BUG AC | Design / Test 对应 |
|---|---|
| AC-001 | `writeText(initial_password)` 成功路径与成功反馈 |
| AC-002 | `writeText(password)` 成功路径与成功反馈 |
| AC-003 | Clipboard 不可用 / reject fallback 与手动复制指引 |
| AC-004 | 关闭后不可再次查看提示与无查询接口 |
| AC-005 | 创建用户、重置密码、受保护账号链路回归 |
| AC-006 | `ResetPasswordDialog` 组件测试 |
| AC-007 | Non-goals 与安全边界 |
