---
title: 管理端一次性密码复制可靠性修复
purpose: 将 BUG-0059 转为 OpenSpec fix change，修复用户管理一次性密码弹窗复制失败
created_at: 2026-07-06 15:33:45
updated_at: 2026-07-06 16:05:44
status: archived
owner: product
related_bug: BUG-0059-user-password-copy-not-working
related_requirement: REQ-0005-user-management
related_sprint: sprint-005
---

# fix-user-password-copy-not-working

## Why

`BUG-0059-user-password-copy-not-working` 已通过评审并纳入 `sprint-005`。管理端 `/admin/users` 中，一次性密码结果弹窗的「复制密码」在创建用户成功后的 `initial_password` 与重置密码成功后的 `password` 两条链路中均无法可靠完成复制。

该问题影响管理员安全交付一次性密码：弹窗关闭后明文密码不可再次查看，若复制失败且没有反馈，管理员只能重新重置密码，容易造成交付失败或重复操作。

## What Changes

- 修复 `ResetPasswordDialog` 的复制动作，确保成功时将当前展示的一次性密码写入剪贴板。
- 增加复制成功反馈，避免管理员无法判断是否复制完成。
- 增加 Clipboard API 不可用或写入失败时的失败提示与手动复制兜底。
- 补充 `ResetPasswordDialog` 组件测试，覆盖成功复制、失败 fallback、Clipboard API 不存在与安全提示不回归。
- 保持创建用户、重置密码、受保护账号禁用态、列表刷新和 Toast 行为不回归。

## Non-Goals

- 不修改用户管理 API 请求路径、响应字段或错误码。
- 不修改 SQLite / MySQL schema。
- 不将一次性明文密码持久化到数据库、日志、审计事件或长期文档。
- 不新增再次查询一次性明文密码的接口或入口。
- 不涉及店主 Web 或微信小程序。

## Impact

| Area | Impact |
|---|---|
| Web 管理端 | 影响 `/admin/users` 一次性密码结果弹窗复制交互 |
| API | 无请求、响应、错误码或 OpenAPI 语义变更 |
| Database | 无 schema 或数据迁移变更 |
| Orval | 不需要执行，除非 apply 阶段意外触碰 API 契约 |
| Docker | 不需要 Docker Compose 验证；可在 Web 本地/Vitest 验证 |
| Security | 保持一次性明文密码仅弹窗内短暂展示，不落库、不入日志 |

## Rollback Plan

1. 回退 `ResetPasswordDialog` 复制反馈、fallback 与测试改动。
2. 重新运行相关 Vitest，确认用户管理页面既有测试仍通过。
3. 人工验证创建用户和重置密码仍能展示一次性密码结果弹窗。
4. 若回退后复制可靠性缺陷恢复，将 BUG-0059 重新标记为未修复并阻止归档。
