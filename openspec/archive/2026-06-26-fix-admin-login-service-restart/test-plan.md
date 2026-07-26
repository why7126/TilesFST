---
title: Test Plan
purpose: fix-admin-login-service-restart 测试计划
change_id: fix-admin-login-service-restart
bug_id: BUG-0005-login-fails-after-service-restart
status: applied
created_at: 2026-06-26 21:17:49
---

# Test Plan

## 1. 后端自动化测试

| 编号 | 场景 | 预期 |
|---|---|---|
| TP-001 | 空 SQLite 数据库，配置 `ADMIN_INITIAL_PASSWORD`，启动/seed 后登录 admin | 登录成功，返回 token 与 admin 用户信息 |
| TP-002 | 已存在 admin，重复执行 seed 或模拟服务重启 | 原密码仍可登录，不被新的 `ADMIN_INITIAL_PASSWORD` 覆盖 |
| TP-003 | 已存在 admin，修改 `ADMIN_INITIAL_PASSWORD`，未开启恢复策略 | 新密码不能登录，旧密码仍可登录 |
| TP-004 | 已存在 admin，开启显式恢复策略 | 新密码可登录，旧密码不可登录 |
| TP-005 | 错误账号或错误密码 | 返回统一凭证错误，不区分用户不存在与密码错误 |
| TP-006 | 禁用用户 | 仍返回禁用错误，不受 seed 修复影响 |

## 2. 文档与配置检查

| 编号 | 场景 | 预期 |
|---|---|---|
| TP-101 | 查看根目录 `.env.example` | 存在 `ADMIN_USERNAME`、`ADMIN_INITIAL_PASSWORD` 与恢复策略说明 |
| TP-102 | 查看 `docs/02-deployment.md` | 说明 Docker Compose 持久化 SQLite 与管理员密码恢复行为 |
| TP-103 | 查看 `docs/04-database-design.md` | 说明默认管理员 seed 与 `users.password_hash` 的关系 |

## 3. 非目标回归

- 不需要前端 Vitest，除非实现阶段修改登录页面。
- 不需要 Orval，除非实现阶段改变认证 API schema。
- 不需要新增数据库迁移，除非实现阶段新增字段。

## 4. 建议命令

```bash
cd src/backend
uv run pytest tests/test_auth.py
```

如实现影响用户管理或权限依赖，追加：

```bash
cd src/backend
uv run pytest tests/test_admin_users.py tests/test_auth.py
```
