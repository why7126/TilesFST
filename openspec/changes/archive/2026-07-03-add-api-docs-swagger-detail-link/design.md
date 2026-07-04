---
created_at: 2026-07-02 09:26:53
updated_at: 2026-07-02 09:26:53
---

## Context

REQ-0022 已提供 `/admin/api-docs` 管理端页面，展示接口目录、OpenAPI 纳入状态、Orval 方法名和全局 Swagger 入口。BUG-0051 已修复 Web 同源 `/docs` 代理，避免 Swagger UI 入口落入 SPA fallback。BUG-0053 已让接口列表分页和管理端列表页基准对齐。

REQ-0023 是 `/admin/api-docs` 表格的行级增强：管理员需要从具体接口行直接打开 Swagger UI 对应 operationId，而不是进入 Swagger 后手动搜索。该能力必须继续保留非 OpenAPI 路由在目录中的可见性，同时明确这类路由没有 Swagger 详情可跳转。

## Goals / Non-Goals

**Goals:**

- 在 `/admin/api-docs` 接口列表中增加 ACTION 列。
- 对可定位 OpenAPI operation 的路由生成具体 operationId 深链。
- 使用新窗口打开 Swagger UI，保留当前管理端列表和登录上下文。
- 对非 OpenAPI 或缺失 operationId 的路由展示禁用态，不生成 href。
- 补充 Vitest 回归，覆盖链接格式、禁用态、安全属性和 token 不泄露。

**Non-Goals:**

- 不内嵌 Swagger UI。
- 不新增公开接口文档站点。
- 不为 `included_in_openapi=false` 的路由生成伪 Swagger 详情。
- 不把 JWT、Cookie、用户信息或环境变量拼接到 Swagger URL。
- 不改变生产环境 Swagger Try It Out 只读/禁用策略。
- 默认不新增后端字段、不改数据库、不改 MinIO、不改小程序。

## D1 UI Strategy

采用 **Design System / existing admin table pattern**，不做独立 CSS Port。

理由：

- REQ-0023 是现有 `/admin/api-docs` 表格的行级增强，视觉应继承已实现的管理端表格、分页、badge、button/link 样式。
- 原型 `prototype/web/api-docs-swagger-detail-link.html` 只表达 ACTION 列、可点击态、禁用态和深链语义，不要求整页 CSS 高保真搬运。
- 该页面已受 `admin-list-page-consistency.md` gate 约束，继续复用现有 `page-summary`、`page-right`、表格横向滚动和 semantic token 更稳妥。

## Conflict Resolution

优先级按 REQ-0023 prototype context 声明执行：

1. `issues/requirements/archive/REQ-0022-admin-api-docs-menu/prototype/web/api-docs.html`
2. `issues/requirements/archive/REQ-0022-admin-api-docs-menu/prototype/web/api-docs-context.md`
3. `issues/requirements/archive/REQ-0023-api-docs-swagger-detail-link/prototype/web/api-docs-swagger-detail-link.html`
4. `issues/requirements/archive/REQ-0023-api-docs-swagger-detail-link/acceptance.md`
5. `rules/ui-design.md`
6. `openspec/specs/`

冲突处理：

- REQ-0022 原型定义页面主体、hero、summary、filters 和列表总体结构；REQ-0023 原型只覆盖行级 ACTION 列。
- 若 acceptance 与 HTML 原型冲突，以 HTML 表达的 ACTION 列、OpenAPI 可点击态、非 OpenAPI 禁用态和新窗口安全属性为准。
- PNG Golden 尚未导出，不作为阻塞项；实现阶段可按 1440x1024 导出截图供人工比对。
- 若 FastAPI Swagger UI 的实际 deepLinking hash 与 `/docs#/{tag}/{operationId}` 不一致，以实现阶段验证后的格式为准，并在任务记录中说明。

## Decisions

### D2 Swagger 深链构造

优先由前端基于已返回的 route metadata 构造链接：

```text
/docs#/{encodeURIComponent(tag)}/{encodeURIComponent(operation_id)}
```

可点击条件：

- `included_in_openapi === true`
- `operation_id` 非空
- 可用 tag 非空；若当前数据存在多个 tags，使用与 OpenAPI operation 对应的主 tag 或页面当前展示的 tag。

理由：

- REQ-0022 聚合接口已暴露 `included_in_openapi` 与 `operation_id`。
- 不新增后端字段可避免 OpenAPI / Orval 变更和契约漂移。
- 前端可通过 focused Vitest 直接验证链接格式与禁用态。

备选方案：

- 后端返回 `swagger_url` 字段。仅当现有 route metadata 无法稳定推导 Swagger UI hash 时采用；采用后必须同步 OpenAPI、Orval、`docs/03-api-index.md` 和后端测试。

### D3 新窗口与鉴权上下文

可用入口使用标准链接而非异步 `window.open`：

```html
<a href="/docs#/{tag}/{operationId}" target="_blank" rel="noreferrer">查看</a>
```

理由：

- 标准 `<a target="_blank">` 更容易被浏览器允许，也保留用户复制链接和重新点击能力。
- 当前管理端页不会被导航或刷新，因此筛选、分页、滚动和登录上下文保持不变。
- `rel="noreferrer"` 防止新窗口反向控制 opener。

安全约束：

- href 仅包含同源 `/docs` 与 hash，不包含 Bearer Token、Cookie、用户信息或环境变量。
- 不新增 Swagger Authorize 自动注入能力。

### D4 禁用态

不可跳转条件下渲染禁用态按钮或等价不可点击元素：

- `included_in_openapi=false`
- `operation_id` 缺失
- 必要 tag 缺失

禁用态 MUST NOT 渲染 href；原因通过 `title`、`aria-label`、弱提示或现有状态文案表达。默认文案为「未纳入 OpenAPI，暂无 Swagger 详情」或「缺少 operationId，暂无 Swagger 详情」。

## Risks / Trade-offs

- Swagger UI hash 格式与预期不一致 -> 在实现阶段以真实 FastAPI Swagger UI deepLinking 验证为准，并更新测试 fixture。
- ACTION 列增加后表格拥挤 -> 保持短文案「查看」，沿用横向滚动和管理端表格密度；在 1440x1024 与窄视口检查不重叠。
- 链接误泄露鉴权上下文 -> 测试断言 href 不包含 token、Cookie、Bearer、用户信息等敏感片段。
- 非 OpenAPI 路由误跳转到通用 `/docs` -> 禁用态不渲染 href，测试覆盖 `/media/{object_key:path}` 等示例。
- 若改为后端返回 `swagger_url` 会扩大 API 面 -> 仅在前端无法稳定推导时采用，并同步 OpenAPI、Orval 与文档。

## Migration Plan

本 change 不涉及数据迁移。上线时复用 BUG-0051 已归档的 Web 同源 Swagger 代理路径。

回滚方式：移除 ACTION 列或关闭行级链接渲染，保留原全局 Swagger UI 入口。

## Open Questions

- 实现阶段需要确认当前 FastAPI Swagger UI 的 deepLinking hash 是否完全支持 `/docs#/{tag}/{operationId}`；如不支持，应记录实际可定位格式。
