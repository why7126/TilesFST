---
created_at: 2026-06-27 08:42:28
title: 缺陷追踪
purpose: BUG-0005 服务重启后正确账号密码无法登录
content: 记录服务重启并刷新页面后，管理端登录页使用正确账号密码仍提示账号或密码错误的缺陷
owner: product
status: done
note: fix-admin-login-service-restart archived 2026-06-26
iteration: sprint-002
readiness: ready
updated_at: 2026-06-27 15:52:00
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0005-login-fails-after-service-restart
bug_name: login-fails-after-service-restart
severity: high
status: done
iteration: sprint-002
related_requirement: REQ-0001-user-login
related_change: fix-admin-login-service-restart
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-26 09:54:07
  generated: 2026-06-26 20:43:37
  completed: 2026-06-26 20:49:27
  reviewed: 2026-06-26 20:57:56
  approved: 2026-06-26 20:57:56
  in_sprint: 2026-06-26 21:07:06
  applied: 2026-06-26 23:17:00
  archived: 2026-06-27 08:14:56
openspec_changes:
  - change_id: fix-admin-login-service-restart
    type: fix
    status: archived```

## 2. Readiness

| 文档 | 状态 |
|---|---|
| capture.md | done |
| bug.md | done |
| root-cause.md | done |
| workaround.md | done |
| acceptance.md | done |
| review.md | done |

**Readiness:** Ready

## 3. 初步分类

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（BUG） |
| 根因类型 | seed-data / runtime-db / environment |
| 修复面 | 默认管理员初始化策略、环境变量说明、重启/持久化数据库下的账号恢复流程 |

## 4. 关联文档

| 文档 | 路径 |
|---|---|
| capture | `capture.md` |
| 缺陷说明 | `bug.md` |
| 根因分析 | `root-cause.md` |
| 临时规避 | `workaround.md` |
| 验收标准 | `acceptance.md` |
| 评审记录 | `review.md` |
| 截图 | `screenshots/login-failure-after-service-restart.png` |
| 父需求 | `issues/requirements/REQ-0001-user-login/` |

## 5. 变更记录

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-06-26 09:54:07 | `/bug-capture` | 记录服务重启后正确账号密码无法登录，页面提示「账号或密码错误」 |
| 2026-06-26 20:43:37 | `/bug-generate` | 基于 capture.md 生成正式 bug.md，状态更新为 draft |
| 2026-06-26 20:49:27 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；状态进入 pending_review |
| 2026-06-26 20:57:56 | `/bug-review` | approved（REV-BUG-0005-001），确认进入修复流程 |
| 2026-06-26 21:07:06 | Sprint scope update | 纳入 `sprint-002`，等待 `/bug-opsx` 创建 `fix-*` Change |
| 2026-06-26 21:17:49 | `/bug-opsx` | 创建 `fix-admin-login-service-restart` OpenSpec Change |
| 2026-06-26 23:17:00 | `/opsx-apply` | 完成默认管理员初始化/显式恢复策略、环境文档同步与后端认证回归测试 |

## 6. 后续动作

1. `/opsx-archive fix-admin-login-service-restart`：归档已完成修复。
