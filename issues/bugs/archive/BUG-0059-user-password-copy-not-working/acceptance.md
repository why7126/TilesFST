---
bug_id: BUG-0059-user-password-copy-not-working
title: 管理端一次性密码复制修复验收标准
status: pending_review
severity: high
owner: product
created_at: 2026-07-06 14:56:29
updated_at: 2026-07-06 14:56:29
related_requirement: REQ-0005-user-management
related_change: null
---

# 验收标准

## AC-001 创建用户后可复制初始密码

- GIVEN 管理员在 `/admin/users` 创建新用户成功。
- WHEN 一次性初始密码弹窗展示，并点击「复制密码」。
- THEN 系统应将弹窗中展示的完整 `initial_password` 写入剪贴板。
- AND 管理员粘贴验证时内容应与弹窗展示完全一致。
- AND 页面应展示复制成功反馈。

## AC-002 重置密码后可复制新随机密码

- GIVEN 管理员对已有可操作用户执行「重置密码」并确认成功。
- WHEN 一次性随机密码弹窗展示，并点击「复制密码」。
- THEN 系统应将弹窗中展示的完整 `password` 写入剪贴板。
- AND 管理员粘贴验证时内容应与弹窗展示完全一致。
- AND 页面应展示复制成功反馈。

## AC-003 剪贴板不可用时提供可理解兜底

- GIVEN 当前浏览器不支持 Clipboard API、剪贴板权限被拒绝，或 `navigator.clipboard.writeText` 执行失败。
- WHEN 管理员点击「复制密码」。
- THEN 页面不得静默失败。
- AND 页面应展示失败提示或手动复制指引。
- AND 应尽可能选中一次性密码文本，帮助管理员手动复制。

## AC-004 关闭弹窗前风险提示保持清晰

- GIVEN 一次性密码弹窗处于打开状态。
- WHEN 管理员查看弹窗说明。
- THEN 页面应继续提示「关闭后不可再次查看」或等价风险说明。
- AND 修复不得新增再次查询一次性明文密码的接口或入口。

## AC-005 创建用户与重置密码链路不回归

- GIVEN 管理员创建用户或重置密码。
- WHEN 后端返回一次性明文密码。
- THEN 前端仍应展示同一个一次性密码结果弹窗。
- AND 创建用户成功 Toast、重置密码成功 Toast、用户列表刷新行为不得回归。
- AND 受保护账号的重置密码按钮仍应置灰，不得绕过既有权限边界。

## AC-006 测试覆盖

- MUST 新增或更新前端测试覆盖 `ResetPasswordDialog` 的复制行为。
- MUST 覆盖复制成功路径，断言 `navigator.clipboard.writeText` 使用当前展示密码调用。
- MUST 覆盖复制失败路径，断言页面出现失败提示或手动复制指引。
- SHOULD 覆盖 Clipboard API 不存在时的 fallback 行为。

## AC-007 非目标范围

- 本缺陷修复不应修改用户管理 API 请求路径、响应字段或错误码。
- 本缺陷修复不应修改数据库 schema。
- 本缺陷修复不应将一次性明文密码持久化到数据库、日志、审计事件或长期文档。
- 本缺陷修复不涉及小程序或店主展示端。
