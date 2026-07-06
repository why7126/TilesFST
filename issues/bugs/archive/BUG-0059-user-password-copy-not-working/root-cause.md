---
bug_id: BUG-0059-user-password-copy-not-working
title: 管理端一次性密码弹窗复制密码未生效根因分析
status: pending_review
severity: high
owner: product
created_at: 2026-07-06 14:56:29
updated_at: 2026-07-06 14:56:29
related_requirement: REQ-0005-user-management
related_change: null
---

# 根因分析

## 结论

该缺陷属于 Web 管理端前端交互可靠性缺陷，主要集中在一次性密码结果弹窗的「复制密码」按钮实现。

后端创建用户和重置密码接口均已返回一次性明文密码，前端页面也已将返回值传入 `ResetPasswordDialog`。当前可见问题不是密码未生成或未返回，而是弹窗内复制动作对 Clipboard API 的可用性和失败路径处理不足。

## 直接原因

`ResetPasswordDialog` 中的复制逻辑直接调用：

```typescript
await navigator.clipboard.writeText(password);
```

但该调用存在以下缺口：

- 未判断 `navigator.clipboard` 或 `writeText` 是否存在。
- Clipboard API 写入失败时只进入空 `catch`，没有错误反馈。
- 没有复制成功反馈，管理员无法判断复制是否完成。
- 没有手动复制或选中文本 fallback。
- 没有专门测试覆盖一次性密码弹窗复制按钮。

因此，当浏览器权限、运行上下文、测试环境、WebView 或非预期兼容场景导致剪贴板写入失败时，用户只能感知为「点击无效」。

## 根本原因

一次性密码弹窗把「复制」作为关键交付动作，但实现上将剪贴板写入视为必然成功，缺少面向安全上下文和权限失败的交互设计。

从质量保障角度看，当前 `UserManagementPage.test.tsx` 将 `ResetPasswordDialog` mock 为 `null`，只覆盖了重置密码确认弹窗和 API 调用链路，没有覆盖结果弹窗中的复制行为。这使得复制交互回归无法被现有测试发现。

## 触发条件

满足以下任一条件时可能触发：

- 管理员在创建用户成功后，点击一次性初始密码弹窗中的「复制密码」。
- 管理员在重置密码成功后，点击一次性随机密码弹窗中的「复制密码」。
- 浏览器拒绝剪贴板权限、Clipboard API 不可用或写入失败。
- 运行环境对 `navigator.clipboard.writeText` 支持不完整。
- 用户点击后因没有成功提示而无法确认复制结果。

## 影响链路

```text
POST /api/v1/admin/users
  → 返回 data.initial_password
  → UserFormModal.onSuccess('用户已创建', initial_password)
  → UserManagementPage.setResetPassword(initialPassword)
  → ResetPasswordDialog 展示一次性密码
  → 点击「复制密码」未可靠写入剪贴板
```

```text
POST /api/v1/admin/users/{id}/reset-password
  → 返回 data.password
  → resetUserPassword() 返回 password
  → UserManagementPage.setResetPassword(password)
  → ResetPasswordDialog 展示一次性密码
  → 点击「复制密码」未可靠写入剪贴板
```

## 分类

| 维度 | 分类 |
|---|---|
| 缺陷类型 | code / frontend interaction |
| 影响层级 | Web 管理端 UI 交互 |
| 主要模块 | `src/web/src/features/admin/components/ResetPasswordDialog.tsx` |
| 次要模块 | `src/web/src/pages/admin/UserManagementPage.tsx`、用户管理相关测试 |
| 接口层 | 暂未发现接口缺陷 |
| 数据库层 | 不涉及 |
| 安全层 | 涉及一次性密码交付可靠性，但不涉及权限绕过或明文持久化 |

## 证据

- `ResetPasswordDialog` 只调用 `navigator.clipboard.writeText(password)`，失败时空 `catch`。
- `UserManagementPage` 创建用户成功后会把 `initialPassword` 写入 `resetPassword` 状态并展示结果弹窗。
- `UserManagementPage` 重置密码成功后会把返回的 `password` 写入 `resetPassword` 状态并展示结果弹窗。
- `users-api.ts` 中 `resetUserPassword` 正确从响应 `data.password` 取值。
- `UserManagementPage.test.tsx` mock 了 `ResetPasswordDialog`，未覆盖结果弹窗复制行为。

## 修复方向建议

后续 `bug-opsx` / `opsx-apply` 可考虑：

- 为 `ResetPasswordDialog` 增加复制成功和失败状态提示。
- 在 Clipboard API 不可用或写入失败时，自动选中密码输入框，并提示管理员手动复制。
- 避免将异常静默吞掉。
- 为 `ResetPasswordDialog` 新增组件测试，覆盖成功复制、失败 fallback、按钮反馈和展示密码一致性。
- 保持一次性密码只展示在结果弹窗中，不新增持久化存储或后续查询接口。
