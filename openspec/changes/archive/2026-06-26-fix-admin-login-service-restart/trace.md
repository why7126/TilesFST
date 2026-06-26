---
title: Change Trace
purpose: fix-admin-login-service-restart 追溯记录
change_id: fix-admin-login-service-restart
bug_id: BUG-0005-login-fails-after-service-restart
status: applied
created_at: 2026-06-26 21:17:49
---

# Trace

## 1. 来源

| 项目 | 内容 |
|---|---|
| BUG | `issues/bugs/BUG-0005-login-fails-after-service-restart` |
| Sprint | `sprint-002` |
| 严重等级 | high |
| 评审 | `REV-BUG-0005-001`，approved |
| 父需求 | `REQ-0001-user-login` |

## 2. Bug Analysis Report

| 维度 | 结论 |
|---|---|
| 现象 | 服务重启后进入 `/admin/login`，使用正确管理员账号密码仍提示「账号或密码错误」 |
| 复现 | 重启本地或 Docker 服务 → 进入 `/admin/login` → 输入管理员账号密码 → 登录失败 |
| 根因分类 | seed-data / runtime-db / environment |
| 关联需求 | `REQ-0001-user-login` |
| 修复 Change | `fix-admin-login-service-restart` |

## 3. 验收映射

| BUG AC | OpenSpec 覆盖 |
|---|---|
| AC-001 | `auth/spec.md` 首次启动空数据库时默认管理员可登录 |
| AC-002 | `auth/spec.md` 服务重启后已有管理员账号仍可按既有密码登录 |
| AC-003 | `auth/spec.md` 已存在 admin 且初始密码变化时必须有明确策略 |
| AC-004 | `auth/spec.md` 密码恢复不得绕过安全边界 |
| AC-005 | `tasks.md` Docker Compose 环境变量说明一致 |
| AC-006 | `auth/spec.md` 错误提示保持一致但排障信息可定位 |
| AC-007 | `tasks.md` 回归测试覆盖 |
| AC-008 | `auth/spec.md` 不破坏既有认证能力 |

## 4. Checklist

- [x] 通过 OpenSpec CLI 创建 change
- [x] proposal.md 包含 Why / Impact / Rollback Plan
- [x] design.md 包含根因、修复方案、测试策略
- [x] specs 覆盖管理员初始化与恢复策略
- [x] tasks.md 包含回归测试和知识库提醒
- [x] `/opsx-apply fix-admin-login-service-restart`
- [ ] `/opsx-archive fix-admin-login-service-restart`

## 5. 影响评估

| 影响面 | 结论 |
|---|---|
| API schema | 未改变 |
| Orval | 不需要 |
| 数据库结构 | 不新增表/字段；仅显式恢复时更新已有 `users.password_hash` |
| 后端 | 默认管理员 seed / 显式恢复策略已实现 |
| Web 管理端 | 登录恢复路径改善；页面不变 |
| 小程序 / 店主端 | 无影响 |
| Docker Compose | 已同步环境变量与部署说明 |
| 知识库 | 不新增事故沉淀；当前为本地/演示环境初始化策略缺陷，已在 BUG 与部署文档中闭环 |

## 6. 测试结果

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-06-26 23:17:00 | `cd src/backend && uv run pytest tests/test_auth.py` | 11 passed |
| 2026-06-26 23:17:00 | `cd src/backend && uv run pytest tests/test_admin_brands.py tests/test_auth.py` | 30 passed |
| 2026-06-26 23:17:00 | `cd src/backend && uv run ruff check app/db/seed.py app/core/config.py tests/test_auth.py` | passed |

## 7. 变更记录

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-06-26 21:17:49 | `/bug-opsx` | 创建 `fix-admin-login-service-restart` OpenSpec Change |
| 2026-06-26 23:17:00 | `/opsx-apply` | 完成默认管理员显式恢复策略、环境/部署/数据库文档同步与后端认证回归测试 |
