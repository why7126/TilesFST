---
requirement_id: REQ-0023-api-docs-swagger-detail-link
title: 接口文档列表行级查看并跳转 Swagger 详情
terminal: web-admin
version: v1
status: in_sprint
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0022-admin-api-docs-menu
created_at: 2026-07-01 09:26:32
updated_at: 2026-07-02 09:17:47
---

# REQ-0023 接口文档列表行级查看并跳转 Swagger 详情

## 1. 需求背景

`REQ-0022-admin-api-docs-menu` 已在 Web 管理端提供 `/admin/api-docs` 页面，用于展示系统接口目录、OpenAPI 状态、Orval 方法名与 Swagger UI 入口。当前管理员可以通过页面右上角进入 Swagger UI，但在接口列表中查看某一行接口详情时，仍需要打开 Swagger 后手动搜索 Method、Path 或 operationId。

本需求在 `/admin/api-docs` 的接口列表中，为每个可在 OpenAPI 中定位的接口提供行级「查看」入口。管理员点击后应在新窗口打开 Swagger UI，并直接跳转到该接口对应的 `operationId` 锚点，从而快速查看请求参数、响应结构、错误信息和调试入口。

## 2. 目标用户

| 角色 | 是否可使用 | 说明 |
|---|---:|---|
| 后台管理员（`admin`） | 是 | 可在接口文档列表中逐行打开 Swagger 接口详情 |
| 后台运营（`employee`） | 否 | 无权访问 `/admin/api-docs`，因此不提供行级查看入口 |
| 店主 Web / 微信小程序用户 | 否 | 不暴露管理端接口文档和 Swagger 入口 |

## 3. 范围

### 3.1 本期包含

- 在 `/admin/api-docs` 接口列表中新增行级操作入口，文案为「查看」或等价短按钮。
- 对 `included_in_openapi=true` 且存在 `operation_id` 的路由，点击「查看」后 MUST 在新窗口打开 Swagger UI 对应 operationId 锚点。
- Swagger 详情链接 MUST 使用具体 `operationId` 锚点，而不是仅打开 `/docs` 后让用户手动搜索。
- 新窗口打开 MUST 保留当前管理端页面状态，包括筛选条件、滚动位置和登录上下文；不得在当前窗口离开 `/admin/api-docs`。
- 对 `included_in_openapi=false` 或缺少 `operation_id` 的路由，MUST 不提供可点击跳转：
  - 默认显示禁用态「查看」按钮，并给出不可用原因；
  - 必须隐藏或移除可点击的 Swagger 详情链接，防止跳转到错误接口；
  - 禁用态说明应与现有「未纳入 OpenAPI schema」状态一致。
- 行级查看入口 MUST 与现有 Method、Path、Tag、Summary、Auth、OpenAPI、Orval Method 信息共同组成同一接口表格。

### 3.2 本期不包含

- 不修改接口定义、OpenAPI schema、FastAPI 路由行为或 Orval 生成规则，除非实现阶段发现现有聚合数据无法稳定生成 Swagger 锚点。
- 不在管理端内嵌完整 Swagger UI。
- 不为 `included_in_openapi=false` 路由生成伪 Swagger 详情页。
- 不为店主 Web、微信小程序或未登录用户提供 Swagger 详情入口。
- 不自动将管理端 JWT 注入 Swagger UI，不复制 token 到 URL、query、hash、localStorage 新键或剪贴板。
- 不改变生产环境 Swagger `Try It Out` 禁用策略。

## 4. 信息架构

```text
/admin/api-docs
└── api-route-table
    ├── METHOD
    ├── PATH
    ├── TAG
    ├── SUMMARY
    ├── AUTH
    ├── OPENAPI
    ├── ORVAL METHOD
    └── ACTION
        ├── included_in_openapi=true + operation_id exists
        │   └── 查看 → new window /docs#/tag/{tag}/{operationId}
        └── included_in_openapi=false or operation_id missing
            └── 查看 disabled / no clickable href
```

## 5. 功能要求

### FR-001 行级查看入口

- MUST 在接口目录表格中为每一行预留操作列。
- MUST 对可跳转接口展示可点击的「查看」入口。
- MUST 对不可跳转接口展示禁用态入口或等价不可点击状态。
- MUST 保持表格信息密度，不得用大块卡片替代表格行。

### FR-002 Swagger operationId 深链

- MUST 使用 OpenAPI `operationId` 构造 Swagger UI 深链。
- MUST 优先跳转到具体 operationId 锚点，而不是通用 `/docs`。
- SHOULD 使用 FastAPI Swagger UI 支持的 hash 路径格式，例如：

```text
/docs#/{tag}/{operationId}
```

- MUST 对 tag、operationId 进行安全编码，避免空格、斜杠或特殊字符破坏 URL。
- SHOULD 在实现阶段验证当前 FastAPI Swagger UI 的 deepLinking 配置可定位到目标接口；如发现格式差异，必须在 OpenSpec design 中记录实际锚点规则。

### FR-003 新窗口打开

- 点击可用「查看」入口 MUST 使用新窗口或新标签页打开 Swagger UI。
- MUST 使用 `rel="noreferrer"` 或等价安全属性，避免新窗口反向控制管理端窗口。
- 当前 `/admin/api-docs` 页面的筛选条件、列表状态和登录态 MUST 保持不变。
- 若浏览器阻止弹窗，用户重新点击仍应能通过标准链接打开，不依赖异步脚本强制弹窗。

### FR-004 非 OpenAPI 路由处理

- 当 `included_in_openapi=false` 时，MUST 不生成可点击 Swagger 详情链接。
- 禁用态按钮 MUST 有清晰原因，例如「未纳入 OpenAPI，暂无 Swagger 详情」。
- 表格仍 MUST 展示该路由的 Method、Path、来源和 OpenAPI 状态，保持 REQ-0022 的全量路由目录能力。
- 禁用态按钮不得误导用户跳转到通用 `/docs` 或错误的 operationId。

### FR-005 鉴权上下文与安全

- 行级查看入口 MUST 保留当前管理端鉴权上下文，即不刷新、不退出、不覆盖当前登录用户状态。
- Swagger UI 新窗口的调试权限仍 MUST 遵守后端 Swagger 与当前环境策略。
- MUST NOT 将 Bearer Token、Cookie、用户信息、环境变量或密钥拼接到 Swagger URL。
- MUST NOT 为了让 Swagger 自动鉴权而新增不受控的 token 传递机制。
- 生产环境仍 MUST 只允许查看文档，隐藏或禁用 Swagger `Try It Out`。

### FR-006 错误与边界状态

- 当路由 `included_in_openapi=true` 但 `operation_id` 缺失时，MUST 按不可跳转处理，并显示原因。
- 当 Swagger UI 地址不可达时，本需求不要求在管理端行内探测或预加载；浏览器打开失败由目标页面呈现。
- 当筛选结果为空时，不需要展示操作列按钮，只保留现有空状态。

## 6. UI 约束

- MUST 继承 `/admin/api-docs` 现有管理端表格样式，不新增独立视觉体系。
- 操作列按钮 SHOULD 使用现有 `.btn`、link button 或 Design System 等价控件。
- 禁用态 MUST 在视觉上与可点击态有明确区别，并满足键盘与读屏可理解性。
- 新增 TSX/CSS MUST 使用 semantic token 或既有管理端 CSS 变量，不得新增裸 Hex。
- 按钮文案应短，建议「查看」；辅助原因可通过 `title`、`aria-label`、弱提示文案或现有状态文本表达。

## 7. 权限与安全

- 仅 `admin` 用户可访问 `/admin/api-docs` 并使用行级查看入口。
- `employee` 直链 `/admin/api-docs` 仍 MUST 被拒绝，不得因本需求新增入口而放宽权限。
- 行级链接不得泄露 token、密钥、数据库连接串、MinIO 凭据或真实环境变量。
- 新窗口打开不得改变当前管理端会话状态。

## 8. 关联需求与文档

| 关联项 | 关系 |
|---|---|
| `REQ-0022-admin-api-docs-menu` | 父需求；已提供 `/admin/api-docs` 页面、路由目录、OpenAPI 状态、operationId 与 Swagger 入口 |
| `BUG-0051-api-docs-swagger-ui-link-wrong` | 相邻缺陷；修复全局 Swagger UI 入口跳错，不替代本需求的行级详情跳转 |
| `docs/03-api-index.md` | 长期 API 索引；若本需求改变接口文档使用说明，后续 OpenSpec 阶段需评估同步 |
| `src/backend/app/api/v1/admin_api_docs.py` | 当前路由聚合接口来源；已暴露 `included_in_openapi` 与 `operation_id` |
| `src/web/src/pages/admin/ApiDocsPage.tsx` | 当前接口文档页实现位置；后续实现行级操作列 |

## 9. 状态块

```yaml
status: in_sprint
readiness: Ready
next_step: /opsx-apply add-api-docs-swagger-detail-link
expected_openspec_change: add-api-docs-swagger-detail-link
needs_prototype: true
needs_api_change: possible
needs_database_change: false
needs_orval: possible
needs_docker_validation: optional
```

## 10. 待完善项

- 已通过 `/req-opsx` 创建 OpenSpec Change `add-api-docs-swagger-detail-link`，design.md 已引用 `knowledge_base_refs` 和 prototype 优先级。
- OpenSpec design 阶段验证 Swagger UI 实际锚点格式与 FastAPI deepLinking 行为。
- 实现阶段确认是否仅前端根据 `tag` + `operation_id` 构造链接，还是由后端聚合接口返回 `swagger_url` 字段；若新增字段，需同步 OpenAPI 与 Orval。
