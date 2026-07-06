---
requirement_id: REQ-0030-api-docs-swagger-policy-checklist
title: 接口文档页 Swagger 代理与生产调试策略 checklist - 业务流程
status: pending_review
owner: product
created_at: 2026-07-04 22:19:09
updated_at: 2026-07-04 22:19:09
---

# 业务流程

## 1. 流程总览

```text
Sprint 004 复盘 A-006
        │
        ▼
REQ-0030 沉淀 checklist
        │
        ▼
后续 API docs refine / 接口文档页模板化
        │
        ├─ design 声明 dev / Docker / production 代理路径
        ├─ design 声明生产 Try It Out 禁用或只读策略
        ├─ acceptance 转化为可勾选验证项
        └─ tests / smoke / trace 记录验证结果
        │
        ▼
/req-review approve
        │
        ▼
/req-opsx 创建 update-* Change
        │
        ▼
实现文档/测试/必要配置同步
        │
        ▼
/opsx-archive 后成为长期规范
```

## 2. 与父需求差异

| 项目 | `REQ-0022-admin-api-docs-menu` | `REQ-0030-api-docs-swagger-policy-checklist` |
|---|---|---|
| 目标 | 新增 `/admin/api-docs` 页面与接口目录能力 | 将 Swagger 代理和生产调试策略固化为模板 checklist |
| 交付对象 | 页面、路由、接口聚合、Swagger/Orval 展示 | PRD/design/acceptance/checklist/文档治理项 |
| 是否新增 UI | 是 | 否，除非后续 refine 选择同步页面提示文案 |
| 是否新增 API | 可能 | 默认不新增 |
| 核心风险 | 权限、路由目录完整性、Swagger 可用性 | checklist 分散、部署代理遗漏、生产 `Try It Out` 被误放开 |

## 3. checklist 使用流程

```text
API docs 相关变更启动
        │
        ▼
确认是否触发 REQ-0030 checklist
        │
        ├─ 修改 Swagger 入口？────────────── yes
        ├─ 修改 /docs / /redoc / openapi? ── yes
        ├─ 修改 Web 代理或部署文档？──────── yes
        ├─ 修改生产 APP_ENV 策略？────────── yes
        └─ 仅改无关文案？────────────────── may skip with trace note
        │
        ▼
按环境填写验证矩阵
        │
        ├─ Vite dev proxy
        ├─ Docker Nginx
        └─ production-equivalent proxy
        │
        ▼
确认安全门禁
        │
        ├─ same-origin docs path
        ├─ no backend host hardcode
        ├─ no token in URL/hash/query
        └─ production Try It Out disabled
```

## 4. 环境验证矩阵

| 环境 | 验证对象 | 期望 |
|---|---|---|
| 本地开发 | Vite dev proxy | `/docs`、`/redoc`、`/openapi.json` 可到达后端文档响应 |
| Docker Compose | `src/web/nginx.conf` | `/docs` 不进入 Web 首页或 SPA fallback；`/openapi.json` 仍转发后端 |
| 生产等价 | 生产反代 / 部署说明 / 后端 `APP_ENV` | 文档入口可见；`Try It Out` 禁用、隐藏或等价只读 |

## 5. 例外流程

- 若后续实现采用非 `/docs` 的同源路径，必须在 design 中说明替代路径、代理规则和原因。
- 若部分验证无法自动化，必须在 acceptance 或 trace 中记录人工验证步骤、环境和结果。
- 若变更仅涉及无关文案，不触发 Swagger 路径或生产调试策略，允许在 trace 中记录 N/A 原因。

## 6. prototype 策略

本需求不生成 `prototype/web/*`。原因：`REQ-0030` 不新增或改造可见页面布局，核心交付是接口文档页模板 checklist、验收项与后续 OpenSpec design 约束。若后续 API docs refine 同步修改页面提示文案，可在对应 OpenSpec Change 中补充页面截图或轻量原型。
