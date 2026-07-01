---
title: 接口文档页面原型说明
purpose: REQ-0022 /admin/api-docs HTML 原型上下文
created_at: 2026-07-01 00:16:00
updated_at: 2026-07-01 00:16:00
owner: product
status: draft
---

# 接口文档页面原型说明

## 原型文件

- HTML：`prototype/web/api-docs.html`
- PNG：`prototype/web/api-docs.png`（待导出）

## 优先级

后续 OpenSpec design MUST 声明视觉与交互优先级：

```text
1. prototype/web/api-docs.html
2. prototype/web/api-docs.png（Golden Reference，待导出）
3. prototype/web/api-docs-context.md
4. issues/requirements/review/REQ-0022-admin-api-docs-menu/acceptance.md
5. rules/ui-design.md
6. docs/knowledge-base/best-practices/admin-list-page-consistency.md
7. docs/knowledge-base/best-practices/admin-form-page-consistency.md
```

## 页面结构

```text
Admin Shell
├── Sidebar / SYSTEM
│   ├── 用户管理
│   ├── 系统设置
│   └── 接口文档（active）
└── api-docs-page
    ├── page-hero
    │   ├── eyebrow: SYSTEM / API DOCS
    │   ├── title: 接口文档
    │   ├── desc: OpenAPI、Swagger、Orval 映射说明
    │   └── actions: Swagger UI / OpenAPI JSON
    ├── summary-grid
    ├── filter-bar
    ├── api-route-table
    └── swagger-panel
```

## 状态说明

| 状态 | 原型表达 | 实现要求 |
|---|---|---|
| 非生产 | 环境 Badge：允许在线调试 | Swagger `Try It Out` 可用 |
| 生产 | 环境 Badge：仅查看 | Swagger `Try It Out` 隐藏或禁用 |
| Orval 已生成 | `getAdminUsers` 等方法名 badge | 可按方法名搜索 |
| Orval 未生成 | `未生成` muted badge | 说明 schema 外路由或未生成原因 |
| 非 `/api/v1` 路由 | `/health`、`/media/{object_key:path}` | 明确标注为系统路由补充 |

## Knowledge-base gate

- `admin-list`：接口目录表格、筛选、分页/反馈稳定性参考用户管理页。
- `admin-form`：全页管理端页面，必须避免重复 CTA、原生 confirm 与布局抖动模式；本需求无保存/恢复默认动作，对应 AC 标 N/A。

## 待导出 PNG

- 建议视口：1440x1024。
- 截图范围：完整 Admin Shell + 接口文档首屏，底部需露出 Swagger panel 顶部。
- 文件名：`prototype/web/api-docs.png`。
