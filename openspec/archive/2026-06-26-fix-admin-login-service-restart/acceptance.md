---
title: Acceptance
purpose: fix-admin-login-service-restart 验收标准
change_id: fix-admin-login-service-restart
bug_id: BUG-0005-login-fails-after-service-restart
status: applied
created_at: 2026-06-26 21:17:49
---

# Acceptance

| BUG AC | OpenSpec 覆盖 | 验收方式 |
|---|---|---|
| AC-001 | `auth/spec.md` 默认管理员首次创建 | pytest + 本地启动验证 |
| AC-002 | `auth/spec.md` 已有 admin 重启不破坏密码 | pytest |
| AC-003 | `auth/spec.md` 显式恢复策略 | pytest + 文档检查 |
| AC-004 | `auth/spec.md` 密码安全与权限边界 | pytest + 代码审查 |
| AC-005 | tasks 文档同步 | `.env.example` / docs 检查 |
| AC-006 | `auth/spec.md` 登录错误语义不变 | pytest |
| AC-007 | tasks 测试覆盖 | pytest 结果 |
| AC-008 | `auth/spec.md` 认证回归 | pytest |

## 通过条件

1. 所有 tasks 完成。
2. `tests/test_auth.py` 或等价后端测试覆盖默认管理员首次创建、重复 seed、显式恢复和错误登录语义。
3. 根目录 `.env.example`、`docs/02-deployment.md`、`docs/04-database-design.md` 同步说明恢复策略。
4. 未改变登录接口响应 schema；若改变，必须补 OpenAPI / Orval / API 文档。
