---
change_id: fix-user-password-copy-not-working
bug_id: BUG-0059-user-password-copy-not-working
requirement_id: REQ-0005-user-management
sprint: sprint-005
status: archived
lifecycle_stage: archive
created_at: 2026-07-06 15:33:45
updated_at: 2026-07-06 16:05:44
---

# Change Trace — fix-user-password-copy-not-working

## 关联

| 类型 | 值 |
|---|---|
| BUG | `BUG-0059-user-password-copy-not-working` |
| 关联需求 | `REQ-0005-user-management` |
| Sprint | `sprint-005` |
| 能力 | `user-management` |
| 影响端 | Web 管理端 |

## 状态

| 阶段 | 状态 | 时间 | 说明 |
|---|---|---|---|
| proposed | done | 2026-07-06 15:33:45 | `/bug-opsx BUG-0059` 创建 fix change |
| applied | done | 2026-07-06 15:40:09 | `/opsx-apply` 完成组件修复与相关 Vitest |
| archived | done | 2026-07-06 16:05:44 | `/opsx-archive` 归档，delta spec 已同步至 `openspec/specs/user-management/spec.md` |

## 验收映射

| BUG AC | OpenSpec Delta | 验证方式 | 状态 |
|---|---|---|---|
| AC-001 | `管理端用户表单弹窗` / 创建用户后复制初始密码成功 | `ResetPasswordDialog` 组件测试 + 页面链路回归 | pass |
| AC-002 | `管理端用户列表行操作` / 重置密码后复制新随机密码成功 | `ResetPasswordDialog` 组件测试 + reset-password 页面回归 | pass |
| AC-003 | 两个 fallback scenarios | Clipboard reject / API 不存在测试 | pass |
| AC-004 | 一次性密码安全边界 | 组件断言 + code review | pass |
| AC-005 | 既有用户管理链路 | `UserManagementPage` 相关测试 | pass |
| AC-006 | tasks 3.x | Vitest / Testing Library | pass |
| AC-007 | proposal Non-Goals | code review | pass |

## 知识沉淀评估

本次修复复用既有 `admin-modal-width-css-cascade.md` 横切 gate，未发现新的可复用事故模式；暂不新增 `docs/knowledge-base/incidents/`。

## 变更记录

| 时间 | 说明 |
|---|---|
| 2026-07-06 16:05:44 | `/opsx-archive` 同步 user-management spec 并归档 Change |
| 2026-07-06 15:40:09 | `/opsx-apply` 完成 `ResetPasswordDialog` 复制成功/失败/fallback 修复，验证 `pnpm --dir src/web test -- ResetPasswordDialog UserManagementPage` 通过 |
| 2026-07-06 15:33:45 | `/bug-opsx BUG-0059` 创建 `fix-user-password-copy-not-working` |
