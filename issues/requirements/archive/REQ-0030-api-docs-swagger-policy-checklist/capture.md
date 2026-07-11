---
req_id: REQ-0030-api-docs-swagger-policy-checklist
status: captured
created_at: 2026-07-04 15:42:05
updated_at: 2026-07-04 15:42:05
recorded_by: product
source: Sprint 004 复盘行动项 / 用户输入
priority_hint: P2
parent_requirement: REQ-0022-admin-api-docs-menu
---

# 一句话

将 Swagger Web 代理路径和生产环境 `Try It Out` 只读策略写入接口文档页模板 checklist，避免后续 API docs refine 或同类管理端文档页遗漏部署代理与生产调试门禁。

# 原始描述

/req-capture 或下一次 API docs refine，将 Swagger Web 代理和生产 Try It Out 策略写入接口文档页模板 checklist

补充上下文：

- Sprint 004 复盘行动项 A-006：将 Swagger Web 代理和生产 `Try It Out` 策略写入接口文档页模板 checklist；建议入口为 `/req-capture` 或下一次 API docs refine。
- 该需求是 `REQ-0022-admin-api-docs-menu` 的后续 refinement，目标不是重新实现接口文档页，而是沉淀模板 checklist，减少后续页面或文档治理时遗漏。
- 关联经验来自接口文档页 Swagger 入口修复：Web 层需要代理 `/docs`、`/redoc`、`/openapi.json` 等后端文档相关路径，且生产环境必须保持 Swagger `Try It Out` 禁用或只读。
- checklist 应覆盖本地 Vite dev proxy、Docker Nginx、生产部署策略、前端入口链接、行级 Swagger 深链与测试/验收记录。

# 待澄清

- [ ] checklist 应落在接口文档页 `design.md` 模板、管理端列表页模板、长期 docs，还是同时进入 OpenSpec delta 与知识库。
- [ ] 是否需要将 `/docs`、`/redoc`、`/openapi.json` 以及 Swagger UI 静态资源路径列为固定代理检查项。
- [ ] 生产环境文案应统一为“只读”还是“已禁用在线调试”，以及是否需要在页面中可见展示。
- [ ] 下一次 API docs refine 是否与 `AdminListPage` 模板化工作合并，还是单独创建 `update-*` OpenSpec Change。

# 探索结论

（/req-explore 后人工确认写入）
