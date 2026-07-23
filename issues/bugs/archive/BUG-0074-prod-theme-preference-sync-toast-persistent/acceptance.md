---
bug_id: BUG-0074-prod-theme-preference-sync-toast-persistent
status: done
created_at: 2026-07-21 15:01:54
updated_at: 2026-07-22 08:56:27
related_requirement:
related_change: fix-theme-preference-sync-toast-persistent
---

# Acceptance - BUG-0074 生产环境主题偏好同步失败提示持续不消失

## 回归验收标准

- [ ] AC-BUG-001 生产环境 Web 管理端已登录用户切换主题时，本机主题 MUST 立即生效，页面 `data-theme-mode` / `data-theme` 与选择值一致。
- [ ] AC-BUG-002 主题偏好同步成功时，`PATCH /api/v1/auth/me/theme` MUST 返回 200，响应 `data.theme_mode` MUST 与用户选择的主题一致。
- [ ] AC-BUG-003 主题偏好同步成功后，刷新页面、重新登录或重新打开管理端时，用户账号主题偏好 MUST 保持一致。
- [ ] AC-BUG-004 当主题偏好同步失败时，页面 MUST 保留本机主题生效状态，不得回退到旧主题或系统默认主题。
- [ ] AC-BUG-005 当主题偏好同步失败时，错误提示 MUST 自动消失或提供明确关闭入口，不得持续常驻页面。
- [ ] AC-BUG-006 多次快速切换主题时，错误提示 MUST 不堆叠、不重复刷屏、不遮挡主要管理端内容。
- [ ] AC-BUG-007 未登录用户切换主题时，前端 MUST 只保存本机偏好，不得调用账号主题偏好同步接口。
- [ ] AC-BUG-008 401 / 403 / 500 / 网络失败等异常场景下，前端 MUST 展示可恢复的错误提示，并保留可诊断日志或 Network 证据。
- [ ] AC-BUG-009 修复不得改变登录、登出、Token 存储、用户权限判断或管理端路由访问控制。
- [ ] AC-BUG-010 若修复涉及 `PATCH /api/v1/auth/me/theme` 接口字段、响应结构或错误码，MUST 同步 OpenAPI、Orval、接口文档和后端集成测试；若仅调整前端 Toast 生命周期，MUST 明确说明不需要 Orval。
- [ ] AC-BUG-011 若生产同步失败来自数据库字段或迁移差异，MUST 同步 SQLite/MySQL schema、迁移、数据库文档和回归测试。

## 验收证据要求

| 类型 | 要求 |
|---|---|
| 生产 Network 证据 | 覆盖 `PATCH /api/v1/auth/me/theme` 成功保存或失败状态码、响应体 |
| 前端交互证据 | 覆盖同步失败提示自动消失或可关闭 |
| 持久化证据 | 覆盖刷新、重新登录后主题偏好仍保持 |
| 回归测试 | 覆盖主题切换成功、同步失败、未登录不调用同步接口 |
| 部署排查证据 | 如生产失败来自部署链路，需附后端日志、DB 字段或 Nginx 反代验证结论 |

## 非目标

- 本 BUG 不要求新增主题模式。
- 本 BUG 不要求调整 Design System 颜色 Token。
- 本 BUG 不要求改变认证策略、用户角色权限或 Token 生命周期。
- 本 BUG 不要求新增账号偏好管理页面。
- 本 BUG 不要求绕过后端鉴权保存主题偏好。
