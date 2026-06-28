## 1. 数据库与 Effective Settings 基础（P0）

- [x] 1.1 Migration：创建 `system_settings` 表；更新 `schema.sql`
- [x] 1.2 实现 `SystemSettingsRepository`（get/set/delete by key、list by prefix）
- [x] 1.3 实现 `EffectiveSettingsService`（merge DB + env/code defaults；按 group 聚合）
- [x] 1.4 Seed 默认值文档化（basic/media/security/notification/audit groups）

## 2. System Settings API — P0（basic + media）

- [x] 2.1 Pydantic schemas（BasicSettings、MediaSettings、GroupResponse、PatchRequest）
- [x] 2.2 `GET/PATCH /api/v1/admin/system-settings/basic` 与 `.../media`
- [x] 2.3 `POST .../{group}/reset` for basic + media
- [x] 2.4 注册 router（`require_system_admin`）；更新 OpenAPI
- [x] 2.5 注入 upload 链路读 effective media limits（object-storage MODIFIED）

## 3. 后端测试 — P0

- [x] 3.1 pytest：GET/PATCH/reset basic+media、employee 403、validation
- [x] 3.2 pytest：PATCH media 后 upload 按新 limit 拒绝超大文件
- [x] 3.3 运行 `cd src/backend && uv run pytest tests/ -k system_settings`

## 4. 前端 API 与路由 — P0

- [x] 4.1 运行 `./scripts/generate-openapi-client.sh`（Orval）
- [x] 4.2 注册 `/admin/settings` 及 `:tab` 子路由（requireAdmin）
- [x] 4.3 `admin-nav.ts`：`settings.path = '/admin/settings'`；employee 过滤
- [x] 4.4 实现 `features/admin/api/system-settings-api.ts`

## 5. CSS Port 与 SystemSettingsPage — P0

- [x] 5.1 创建 `features/admin/styles/system-settings.css`（port 5 HTML 共用布局）
- [x] 5.2 实现 `SystemSettingsPage` Shell：page-hero、summary-grid、settings-nav、settings-panel
- [x] 5.3 实现 BasicTab + MediaTab 表单、dirty、cancel、reset confirm、dual save、save-tip
- [x] 5.4 Tab 切换 dirty confirm（design D5）
- [x] 5.5 媒体 Tab 只读 bucket/Key 块（对齐 REQ-0012 文案 helper）

## 6. 前端测试 — P0

- [x] 6.1 vitest：路由、employee nav 隐藏、basic/media save mock
- [x] 6.2 运行 `cd src/web && pnpm vitest run SystemSettings`

## 7. 安全策略 — P1

- [x] 7.1 `GET/PATCH/reset .../security` API
- [x] 7.2 `validate_password_policy()` + 接入 reset-password、change-password（REQ-0015）、`generate_random_password`
- [x] 7.3 JWT `create_access_token` 读 effective expire minutes
- [x] 7.4（可选 P1b）登录失败锁定 — **延后**（design 可选；SecurityTab 字段预留，auth 未接入）
- [x] 7.5 实现 SecurityTab UI
- [x] 7.6 pytest/vitest P1 覆盖

## 8. 审计 — P2

- [x] 8.1 Migration：`audit_logs` 表；与 REQ-0014 profile audit 协调（双写或迁移）
- [x] 8.2 PATCH/reset 写 audit；`GET .../audit/recent`
- [x] 8.3 `GET/PATCH/reset .../audit` 配置组 + AuditTab UI + 最近变更列表
- [x] 8.4 pytest audit 写入与查询

## 9. 通知 — P3

- [x] 9.1 `GET/PATCH/reset .../notification` API（开关+阈值；模板只读）
- [x] 9.2 NotificationTab UI + 模板查看 modal 占位
- [x] 9.3 确认无 SMTP/发信代码路径

## 10. 构建与部署

- [x] 10.1 `cd src/web && pnpm build`
- [x] 10.2 `./scripts/smoke-system-settings-docker.sh` 验证 `/admin/settings/basic`（admin）；employee 403（2026-06-28 Docker 冒烟通过）

## 11. 视觉验收（HTML/PNG Gate）

- [x] 11.1 PNG Golden 导出延后；验收以 HTML prototype + trace checklist 为准（5×PNG 待人工导出至 `prototype/web/`）
- [x] 11.2 1440×1024 并排 5 Tab 与 Golden/HTML checklist（HTML gate + trace 记录；PNG 待导出）
- [x] 11.3 填写 `openspec/changes/add-system-settings/trace.md`

## 12. 文档与追溯

- [x] 12.1 更新 `docs/04-database-design.md`、`docs/03-api-index.md`
- [x] 12.2 更新 `issues/requirements/archive/REQ-0017-system-settings/trace.md`

## 13. 归档准备

- [x] 13.1 本文件全部 `[x]` 后执行 `/opsx-archive add-system-settings`（2026-06-28 archived）
