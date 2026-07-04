---
title: 需求验收标准
purpose: REQ-0022-admin-api-docs-menu 接口文档菜单、接口目录、Swagger 与 Orval 映射验收
content: 基于 requirement.md v1、capture.md、req-explore 结论与 knowledge-base 横切 gate 提炼
source: AI 根据 PRD 与知识库生成，项目团队确认
update_method: PRD、原型或 knowledge-base 变更时同步更新
owner: product
status: implemented
created_at: 2026-07-01 00:16:00
updated_at: 2026-07-01 08:48:56
note: REQ-0022-admin-api-docs-menu
---

# 验收标准

## 1. 功能验收 — 导航与权限

- [x] **AC-001** `admin` 登录后，管理端侧栏 SYSTEM 分组在「系统设置」下方展示「接口文档」菜单。
- [x] **AC-002** 点击「接口文档」进入 `/admin/api-docs`，当前菜单 active 高亮；侧栏收起态仍有可访问名称。
- [x] **AC-003** `employee` 侧栏不展示「接口文档」；直链 `/admin/api-docs` 进入 403 页面或等价禁止访问状态。
- [x] **AC-004** 店主 Web 与微信小程序不展示接口文档入口。
- [x] **AC-005** 如新增后端聚合接口，必须使用管理员权限；`employee` 调用返回 403。

## 2. 功能验收 — 接口目录

- [x] **AC-006** 接口目录展示 `/api/v1/*` 下所有业务 API。
- [x] **AC-007** 接口目录展示 `/health` 健康检查，且标注其无 `/api/v1` 前缀。
- [x] **AC-008** 接口目录展示 `/media/{object_key:path}` 媒体直出路由，并标注是否纳入 OpenAPI schema。
- [x] **AC-009** 接口目录展示其他属于 FastAPI app 但未纳入 `/api/v1` 的系统路由；若无其他路由，页面显示「无更多非 /api/v1 路由」。
- [x] **AC-010** 每条接口展示 Method、Path、Tag/模块、Summary/说明、认证要求、OpenAPI schema 状态、Orval 方法名状态。
- [x] **AC-011** schema 外路由展示来源说明，不能伪装成 Orval 已生成接口。

## 3. 功能验收 — Orval 方法名

- [x] **AC-012** 已纳入 OpenAPI 且被 Orval 生成的接口展示对应方法名。
- [x] **AC-013** 未生成 Orval 方法名的接口展示「未生成」或等价状态，并说明可能原因。
- [x] **AC-014** 支持按 Orval 方法名搜索接口。
- [x] **AC-015** 页面说明 Orval 来源为 `src/web/orval.config.ts` 与 `src/web/src/shared/api/generated.ts`。

## 4. 功能验收 — Swagger 在线调试

- [x] **AC-016** 页面提供 Swagger UI 入口或内嵌 Swagger 区域。
- [x] **AC-017** 本地 / 开发 / 演示环境允许 Swagger `Try It Out`。
- [x] **AC-018** 生产环境展示接口文档入口与 Swagger 文档，但隐藏或禁用 Swagger `Try It Out`。
- [x] **AC-019** 页面展示当前环境的调试策略，例如「当前环境允许在线调试」或「生产环境仅查看」。
- [x] **AC-020** 页面不得将管理员 JWT 明文写入新的不受控持久化位置。

## 5. 功能验收 — 筛选与信息展示

- [x] **AC-021** 支持关键字搜索，匹配 Path、Summary、Tag、Orval 方法名。
- [x] **AC-022** 支持 Method 筛选，至少覆盖 GET、POST、PUT、PATCH、DELETE。
- [x] **AC-023** 支持模块/Tag 筛选。
- [x] **AC-024** 支持认证要求筛选，例如公开、登录、仅 admin、admin/employee。
- [x] **AC-025** 顶部 summary 显示接口总数、受保护接口数、Orval 映射数、非 `/api/v1` 路由数。
- [x] **AC-026** 空筛选结果展示明确空态，可一键清除筛选。

## 6. UI 与安全验收

- [x] **AC-027** 页面继承 Admin Shell 与暗色旗舰风，不创建独立站点或营销式页面。
- [x] **AC-028** 使用 semantic token class；实现阶段 TSX/CSS 不得新增裸 Hex。
- [x] **AC-029** 接口表格、筛选栏、状态 Badge、方法 Badge 与管理端列表页视觉一致。
- [x] **AC-030** Swagger 区域如无法完全暗色化，必须有清晰容器边界，且不破坏页面布局。
- [x] **AC-031** 页面不得展示真实密钥、数据库连接串、MinIO AccessKey/SecretKey、环境变量真实值。
- [x] **AC-032** 页面提供 `docs/03-api-index.md`、`/openapi.json`、Swagger UI 与 Orval 职责边界说明。

## 7. 文档与工程验收

- [x] **AC-033** 如实现新增或调整接口文档聚合 API，必须同步 `docs/03-api-index.md` 与 OpenAPI。
- [x] **AC-034** 如 OpenAPI 或 Orval 生成逻辑变化，必须运行 `./scripts/generate-openapi-client.sh` 并提交生成结果。
- [x] **AC-035** 前端测试覆盖：管理员可见、employee 不可见/403、筛选、Orval 方法名展示、生产隐藏 Try It Out。
- [x] **AC-036** 后端测试覆盖：如新增聚合接口，则验证 admin 允许、employee 403、非 `/api/v1` 路由补充存在。
- [x] **AC-037** Docker 或生产等价配置验证：生产环境 Swagger `Try It Out` 不可用。

## 8. 原型 trace checklist

| 检查项 | HTML | PNG | Context | 实现 |
|---|---|---|---|---|
| Admin Shell + SYSTEM 接口文档菜单 | ✓ | 待导出 | ✓ | 已实现：`admin-nav.ts`、`AdminSidebar.tsx`、`App.tsx` |
| page-hero + 环境策略提示 | ✓ | 待导出 | ✓ | 已实现：`ApiDocsPage.tsx` |
| summary-strip 指标 | ✓ | 待导出 | ✓ | 已实现：`ApiDocsPage.tsx` |
| filter-bar + api-route-table | ✓ | 待导出 | ✓ | 已实现：`ApiDocsPage.tsx`、`api-docs.css` |
| Swagger panel / link | ✓ | 待导出 | ✓ | 已实现：开发可调试，生产只读 |
| Orval 方法名状态 | ✓ | 待导出 | ✓ | 已实现：显示生成方法名或「未生成」原因 |

> PNG Golden 文件待从 HTML 导出至 `prototype/web/api-docs.png`；当前以 HTML + context 为开发优先参考。

## 9. 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-form-page-consistency.md` — 预防 Sprint 002/003 复发类缺陷

- [x] **AC-XCUT-001** 接口目录表格若有分页，分页 DOM MUST 对齐 `/admin/users` 基准：左侧 `page-summary`，右侧 `page-right` 页码与每页条数。
- [x] **AC-XCUT-002** 接口目录加载、筛选或刷新产生的成功/失败反馈 MUST 使用 fixed toast 或不推挤布局的固定反馈，不得在 hero 与表格之间插入文档流 notice 导致纵向位移。
- [x] **AC-XCUT-003** N/A — 本需求无状态变更、启停、删除、重置密码等危险操作；若实现阶段新增清空缓存、重新生成文档等危险操作，MUST 使用 DS confirm modal。
- [x] **AC-XCUT-004** 实现阶段 MUST NOT 使用 `window.confirm` / `window.alert` 处理接口文档页交互；如需确认，使用 DS modal。
- [x] **AC-XCUT-005** N/A — 本需求不是可保存表单页，不应出现「保存设置/保存修改」CTA；若实现阶段新增配置表单，页面全局 accessible name 为「保存*」的按钮 MUST 仅 1 个且位于 footer。
- [x] **AC-XCUT-006** 页面 hero MUST NOT 重复渲染保存按钮；接口文档页首屏仅保留标题、说明、环境策略、Swagger/OpenAPI 快捷入口。
- [x] **AC-XCUT-007** N/A — 本需求无恢复默认或 dirty Tab 切换；若后续新增配置项，恢复默认/放弃 dirty 切换 MUST 使用 DS modal，禁止原生对话框。
- [x] **AC-XCUT-008** Swagger 或接口目录刷新成功/失败提示不得引起主内容区域垂直位移；验收需在 1440x1024 视口下观察 `api-docs-page` 主布局稳定。

## 11. 实施验收记录

| 时间 | 类型 | 结果 |
|---|---|---|
| 2026-07-01 08:48:56 | 后端测试 | `cd src/backend && uv run pytest tests/test_admin_api_docs.py` 通过：4 passed |
| 2026-07-01 08:48:56 | 前端测试 | `pnpm --dir src/web exec vitest run src/pages/admin/ApiDocsPage.test.tsx src/features/admin/components/AdminLayout.test.tsx src/features/auth/components/ProtectedRoute.test.tsx` 通过：11 passed |
| 2026-07-01 08:48:56 | OpenAPI/Orval | `./scripts/generate-openapi-client.sh` 已执行并生成 `src/web/openapi.json`、`src/web/src/shared/api/generated.ts` |
| 2026-07-01 08:48:56 | API 标准 | 本次新增 `admin_api_docs.py` 已补 decorator tags；剩余失败为既有管理端路由历史缺少 tags |

## 10. 范围外（不验收）

- 接口编辑、接口启停、接口权限配置、Mock 数据管理。
- 面向店主 Web 或微信小程序的公开接口文档页面。
- 生产环境 Swagger 在线调试。
- 管理端修改 OpenAPI schema、Orval 配置或后端路由定义。
- 完整 Markdown 富文本渲染 `docs/03-api-index.md`。
