---
requirement_id: REQ-0022-admin-api-docs-menu
title: 管理端接口文档菜单与在线调试
terminal: web-admin
version: v1
status: in_sprint
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0017-system-settings
created_at: 2026-06-30 22:10:51
updated_at: 2026-07-01 00:28:26
---

# REQ-0022 管理端接口文档菜单与在线调试

## 1. 需求背景

TILESFST 后端已通过 FastAPI 暴露 OpenAPI JSON 与 Swagger UI，长期接口清单维护在 `docs/03-api-index.md`，前端 API 客户端由 Orval 从 OpenAPI 生成。当前这些入口分散在开发文档、后端 `/docs`、`/openapi.json` 与 `src/web/src/shared/api/generated.ts` 中，后台管理员在管理端内无法统一查看系统全部接口，也无法快速确认某个接口对应的 Orval 生成方法名。

本需求在 Web 管理端 SYSTEM 分组下新增「接口文档」菜单，路由为 `/admin/api-docs`。页面用于后台管理员查看系统全部接口、OpenAPI/Swagger 文档与 Orval 方法映射，并支持在允许的环境中进行 Swagger 在线调试。

## 2. 目标用户

| 角色 | 是否可访问 | 说明 |
|---|---:|---|
| 后台管理员（`admin`） | 是 | 可查看接口目录、Swagger 文档和 Orval 方法名；可在非生产环境使用 Swagger 在线调试 |
| 后台运营（`employee`） | 否 | 侧栏不展示「接口文档」；直链 `/admin/api-docs` 返回 403 |
| 店主 / 前台用户 / 小程序用户 | 否 | 不暴露该入口，不提供接口文档查看能力 |

## 3. 范围

### 3.1 本期包含

- 管理端侧栏 SYSTEM 分组在「系统设置」下方新增「接口文档」菜单。
- 注册管理端路由 `/admin/api-docs`，并在该路由下高亮「接口文档」菜单。
- 页面展示系统接口目录，范围 MUST 包含：
  - `/api/v1/*` 下所有业务 API；
  - `/health` 健康检查；
  - `/media/{object_key:path}` 媒体直出路由；
  - 其他未纳入 `/api/v1` 但属于 FastAPI app 的系统路由。
- 页面 MUST 展示每个接口的 HTTP Method、Path、Tag/模块、Summary/说明、认证要求、是否纳入 OpenAPI schema、是否有 Orval 方法名。
- 页面 MUST 显示 Orval 生成方法名，方便前端联调定位 `src/web/src/shared/api/generated.ts` 中的调用函数。
- 页面 MUST 提供 Swagger UI 入口或内嵌视图，并支持在线调试策略：
  - 本地 / 开发 / 演示环境允许 Swagger 在线调试；
  - 生产环境展示接口文档入口，但 MUST 隐藏或禁用 Swagger `Try It Out`。
- 页面 SHOULD 支持按关键字、HTTP Method、模块/Tag、认证要求筛选接口。
- 页面 SHOULD 提供到 `docs/03-api-index.md` 与 `/openapi.json` 的引用说明，帮助管理员理解运行时契约与长期文档的关系。

### 3.2 本期不包含

- 不提供接口编辑、接口启停、接口权限配置或 Mock 数据管理。
- 不提供面向店主 Web 或微信小程序的公开接口文档页面。
- 不要求在生产环境允许 Swagger 在线调试。
- 不要求通过管理端修改 OpenAPI schema、Orval 配置或后端路由定义。
- 不要求将 Markdown 文档内容完整渲染为富文本；`docs/03-api-index.md` 可作为链接或摘要来源。
- 不展示密钥、数据库连接、对象存储凭据、真实环境变量值等敏感信息。

## 4. 信息架构

```text
admin-shell
├── sidebar
│   └── SYSTEM
│       ├── 用户管理      → /admin/users
│       ├── 系统设置      → /admin/settings
│       └── 接口文档      → /admin/api-docs
└── main-content
    └── api-docs-page
        ├── page-hero（接口文档标题、环境提示、Swagger / OpenAPI 快捷入口）
        ├── summary-strip（接口总数、受保护接口数、Orval 映射数、非 /api/v1 路由数）
        ├── filter-bar（关键字、Method、模块、认证要求）
        ├── api-route-table（接口目录 + Orval 方法名）
        └── swagger-panel 或 swagger-link（按环境控制 Try It Out）
```

## 5. 功能要求

### FR-001 导航与路由

- MUST 在 `src/web/src/features/admin/data/admin-nav.ts` 的 SYSTEM 分组中，于「系统设置」下方新增「接口文档」菜单项。
- MUST 使用 `/admin/api-docs` 作为前端路由。
- MUST 使用与其他管理端菜单一致的图标按钮、收起态提示与 active 高亮规则。
- MUST 确保 `employee` 角色看不到「接口文档」菜单；直链访问 `/admin/api-docs` MUST 进入 403 页面或等价禁止访问状态。

### FR-002 接口目录展示

- MUST 从 OpenAPI JSON 或等价后端契约数据构建接口目录。
- MUST 覆盖 FastAPI app 中所有系统路由，包括 `/api/v1/*`、`/health`、`/media/{object_key:path}` 与其他非 `/api/v1` 路由。
- MUST 标识某个路由是否纳入 OpenAPI schema；如 `include_in_schema=false`，页面仍需展示该路由，并说明其来源为系统路由补充。
- MUST 展示接口 Method、Path、模块/Tag、Summary/说明、认证要求与响应结构摘要。
- SHOULD 展示接口是否需要 Bearer Token、是否仅 `admin`、是否允许 `admin/employee`。

### FR-003 Orval 方法名映射

- MUST 在接口目录中展示 Orval 生成方法名，方便前端开发联调。
- MUST 说明 Orval 来源：`src/web/orval.config.ts` 读取 OpenAPI 并生成 `src/web/src/shared/api/generated.ts`。
- SHOULD 能够通过 OpenAPI `operationId` 推导或匹配 Orval 方法名。
- 当某个接口未生成 Orval 方法名时，MUST 显示「未生成」或等价状态，并给出可能原因（如未纳入 OpenAPI schema）。

### FR-004 Swagger 在线调试

- MUST 提供 Swagger UI 入口或管理端内嵌区域。
- MUST 支持在线调试能力，但生产环境 MUST 隐藏或禁用 Swagger `Try It Out`。
- MUST 在页面上展示当前环境的调试策略：
  - 非生产：允许在线调试；
  - 生产：仅查看文档，隐藏 `Try It Out`。
- SHOULD 避免将管理员 JWT 明文持久化到页面本地存储以外的新位置。

### FR-005 筛选与检索

- MUST 支持接口关键字搜索，匹配 Path、Summary、Tag、Orval 方法名。
- SHOULD 支持 Method 筛选：GET / POST / PUT / PATCH / DELETE。
- SHOULD 支持模块/Tag 筛选，例如 auth、admin-users、admin-system-settings、uploads。
- SHOULD 支持认证要求筛选，例如公开、登录、仅 admin、admin/employee。

### FR-006 文档与治理提示

- MUST 在页面说明 OpenAPI JSON、Swagger UI、Orval 生成客户端、`docs/03-api-index.md` 的职责边界：
  - OpenAPI JSON 是运行时契约；
  - Swagger UI 是调试/查看工具；
  - Orval 方法名是前端调用入口；
  - `docs/03-api-index.md` 是长期维护的接口索引。
- MUST 在后续实现时评估是否需要同步 `docs/03-api-index.md`，尤其是新增 `/admin/api-docs` 页面说明与生产环境 Swagger 策略。

## 6. UI 约束

- MUST 继承管理端暗色旗舰风与现有 Admin Shell，不创建独立站点或营销式页面。
- MUST 优先复用现有管理端列表页/表格/筛选/按钮样式，保持与用户管理、系统设置页视觉一致。
- MUST 使用 Design System semantic token class，不得新增裸 Hex 颜色。
- SHOULD 使用紧凑的管理端信息密度：接口表格、筛选栏、状态 Badge、方法 Badge、模块标签。
- Swagger 内嵌区域如无法完全适配暗色主题，MUST 与页面容器边界清晰，避免破坏整体布局。

## 7. 权限与安全

- MUST 仅允许后台管理员访问 `/admin/api-docs`。
- MUST 不向未登录用户、店主端或小程序暴露管理端接口文档入口。
- MUST 不展示真实密钥、数据库连接串、MinIO AccessKey/SecretKey、环境变量真实值。
- 生产环境 MUST 展示入口但隐藏 Swagger `Try It Out`，防止误操作生产数据。
- 如后续新增后端接口用于补充非 OpenAPI 路由或 Orval 映射，MUST 使用 `require_system_admin` 或等价管理员权限。

## 8. 关联需求与文档

| 关联项 | 关系 |
|---|---|
| `REQ-0017-system-settings` | 父需求；本需求菜单位于系统设置下方，属于 SYSTEM 分组扩展 |
| `docs/03-api-index.md` | 长期接口索引；页面需说明其与 OpenAPI 的关系 |
| `docs/standards/api-governance.md` | OpenAPI、Orval、统一响应与错误码治理来源 |
| `src/web/orval.config.ts` | Orval 生成配置来源 |
| `src/web/src/shared/api/generated.ts` | Orval 方法名展示来源 |
| `src/backend/app/main.py` | `/health`、`/media/{object_key:path}` 等非 `/api/v1` 路由来源 |

## 9. 状态块

```yaml
status: in_sprint
readiness: Ready
next_step: /req-opsx REQ-0022-admin-api-docs-menu
expected_openspec_change: add-admin-api-docs-menu
needs_prototype: true
needs_api_change: possible
needs_database_change: false
needs_orval: likely
needs_docker_validation: optional
```

## 10. 待完善项

- `/req-complete` 阶段补齐 user-stories、business-flow、acceptance、trace 与 prototype。
- OpenSpec 阶段确认是否新增后端 `/api/v1/admin/api-docs` 聚合接口，用于补充非 OpenAPI 路由与 Orval 方法映射。
- 实现阶段确认生产环境隐藏 Swagger `Try It Out` 的技术方案：前端内嵌控制、后端 Swagger 配置，或 Nginx/环境变量控制。
