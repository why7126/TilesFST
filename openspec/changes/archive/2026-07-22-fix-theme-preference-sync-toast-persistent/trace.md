---
change_id: fix-theme-preference-sync-toast-persistent
type: fix
status: archived
created_at: 2026-07-21 15:26:11
updated_at: 2026-07-22 08:57:20
source_bug: BUG-0074-prod-theme-preference-sync-toast-persistent
source_requirement:
sprint: sprint-010
---

# Trace - fix-theme-preference-sync-toast-persistent

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| BUG | `BUG-0074-prod-theme-preference-sync-toast-persistent` | 生产环境主题偏好同步失败提示持续不消失 |

## 关联 Issue

| Issue | 类型 | 状态 | 说明 |
|---|---|---|---|
| `BUG-0074-prod-theme-preference-sync-toast-persistent` | bug | done | 已归档，BUG 文档包已迁入 `issues/bugs/archive/` |

## 实现证据

| 类型 | 证据 | 结论 |
|---|---|---|
| Web 修复 | `src/web/src/pages/admin/AdminLayout.tsx` | 管理端 layout toast 增加 3200ms 自动清理，主题同步失败提示不再常驻 |
| Web 测试 | `src/web/src/features/admin/components/AdminLayout.test.tsx` | 覆盖失败 Toast 自动消失、本机主题保持、多次失败不堆叠、未登录不调用同步接口 |
| 主题上下文回归 | `src/web/src/features/theme/ThemeContext.test.tsx` | 覆盖本机主题写入与同步失败时本机主题保持 |
| API 回归 | `tests/integration/api/test_auth_theme_preference.py` | 覆盖 200 保存、400 非法主题、401 未认证、403 禁用用户 |
| 反代 / 鉴权 / DB 等价排查 | `src/web/src/features/auth/api/auth-api.ts`、`src/web/nginx.conf`、`src/backend/app/db/schema.sql`、`src/backend/app/db/schema.mysql.sql`、`src/backend/app/db/migrations.py` | Bearer Header、`/api/` 反代、`users.theme_mode` schema/迁移均存在；本次不需要 API、DB、OpenAPI 或 Orval 变更 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-21 15:26:11 | /bug-opsx | 从 BUG-0074 创建 OpenSpec fix Change |
| 2026-07-21 15:32:13 | /sprint-propose | 纳入 sprint-010 正式范围 |
| 2026-07-21 22:56:54 | /opsx-apply | 修复管理端主题同步失败 Toast 生命周期，补充 Web 与 API 回归测试证据 |
| 2026-07-22 08:57:20 | /opsx-archive | 合并 auth/web-client delta spec，归档 Change，并推动 BUG-0074 进入 archive |
