---
requirement_id: REQ-0030-api-docs-swagger-policy-checklist
title: 接口文档页 Swagger 代理与生产调试策略 checklist - 验收标准
status: in_sprint
owner: product
created_at: 2026-07-04 22:19:09
updated_at: 2026-07-04 22:30:20
---

# 验收标准

## 功能 AC

- [ ] AC-001 checklist 固定章节：后续 API docs refine、接口文档页模板化或 Swagger 入口调整的 design / acceptance MUST 包含“Swagger Web 代理与生产 Try It Out 策略”检查章节。
- [ ] AC-002 触发范围：checklist MUST 明确在 Swagger 入口调整、Web 代理调整、`/docs` / `/redoc` / `/openapi.json` 路由调整、生产部署说明调整时触发。
- [ ] AC-003 同源入口：Swagger 主入口 MUST 使用 `/docs` 或经 design 说明的等价同源 Web 路径，MUST NOT 在前端硬编码后端 host、端口或容器服务名。
- [ ] AC-004 行级深链：若 API docs 页面提供行级 Swagger 查看，链接 MUST 使用同源 deep link，且仅对 `included_in_openapi=true` 且存在可用 `operation_id` 的路由启用。
- [ ] AC-005 不可跳转路由：非 OpenAPI 路由或缺少 `operation_id` 的路由 MUST 保持可见但不可点击跳转，不得跳到通用 `/docs` 或错误接口。
- [ ] AC-006 Vite 代理：checklist MUST 要求本地开发环境验证 `/docs`、`/redoc`、`/openapi.json` 可进入后端文档响应或等价响应。
- [ ] AC-007 Docker 代理：checklist MUST 要求 Docker Web 环境验证 `/docs` 不进入 Web 首页、React Router fallback 或其他非后端文档页面。
- [ ] AC-008 生产代理：checklist MUST 要求生产等价环境记录 `/docs`、`/redoc`、`/openapi.json` 的反向代理策略或 N/A 原因。
- [ ] AC-009 生产只读：生产环境 Swagger 文档 MAY 可见，但 `Try It Out` MUST 禁用、隐藏或等价只读。
- [ ] AC-010 后端策略：后续 OpenSpec design MUST 检查后端 `APP_ENV` 与 Swagger UI 参数策略，确保生产环境不依赖前端文案单点防护。
- [ ] AC-011 页面文案一致：若 `/admin/api-docs` 页面展示调试策略，文案 MUST 与实际环境策略一致，生产环境不得展示“可在线调试”等误导信息。
- [ ] AC-012 敏感信息：Swagger 链接、hash、query、localStorage 新键、页面文案和验收记录 MUST NOT 包含 Bearer Token、JWT Secret、数据库 DSN、MinIO AccessKey/SecretKey 或真实环境变量值。
- [ ] AC-013 文档同步评估：后续 OpenSpec Change MUST 明确是否同步 `docs/03-api-index.md` 与 `docs/standards/api-governance.md`；若不同步，必须在 design 或 trace 中说明原因。
- [ ] AC-014 复盘行动项闭环：后续 review MUST 能追踪到 Sprint 004 复盘 A-006，并说明该行动项通过本 REQ 进入正式需求链路。
- [ ] AC-015 验证记录：后续实现或文档变更 MUST 在 trace / tasks / acceptance 中记录本地、Docker、生产等价策略的验证结果；无法自动化时必须标注人工验证方式。

## 横切 AC（knowledge-base）

本 REQ 判定为 API/docs 治理需求，不命中 `source-command-req-complete` 定义的 UI 横切标签：

| 标签 | 判定 | 原因 |
|---|---|---|
| `admin-list` | N/A | 不新增管理端 CRUD 列表页、表格分页或行内操作；仅沉淀接口文档页 Swagger checklist |
| `admin-form` | N/A | 不新增管理端表单页、Tab 面板或保存流程 |
| `admin-modal` | N/A | 不新增管理端弹窗 |
| `media-upload` | N/A | 不涉及图片、视频、头像或 Logo 上传链路 |

因此本节不新增 `AC-XCUT-*`。后续若 API docs refine 同时修改管理端列表 DOM、分页或弹窗，应由对应 REQ/BUG 命中相关 knowledge-base 横切 AC。
