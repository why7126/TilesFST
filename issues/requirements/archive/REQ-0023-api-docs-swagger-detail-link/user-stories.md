---
requirement_id: REQ-0023-api-docs-swagger-detail-link
title: 接口文档列表行级查看并跳转 Swagger 详情 - User Stories
status: pending_review
owner: product
source: requirement.md
created_at: 2026-07-01 13:55:01
updated_at: 2026-07-01 13:55:01
---

# User Stories

## US-001 管理员从接口列表直达 Swagger 详情

作为后台管理员，  
我希望在 `/admin/api-docs` 接口列表的每一行看到「查看」入口，  
以便从具体接口行直接打开 Swagger UI 对应 `operationId` 详情，而不需要手动搜索。

验收要点：

- 接口行存在可识别的操作列。
- `included_in_openapi=true` 且有 `operation_id` 的接口可点击「查看」。
- 点击后新窗口打开 Swagger UI，并定位到对应 operationId 锚点。

## US-002 保留当前管理端工作上下文

作为后台管理员，  
我希望点击「查看」时不要离开当前管理端接口文档页，  
以便查看 Swagger 详情后仍能回到原筛选条件和列表位置。

验收要点：

- 「查看」使用新窗口或新标签页打开。
- 当前 `/admin/api-docs` 页不刷新、不跳转、不清空筛选条件。
- 行级链接不把 token、用户信息或环境变量拼接到 URL。

## US-003 明确不可跳转的非 OpenAPI 路由

作为后台管理员，  
我希望对未纳入 OpenAPI 的系统路由看到明确不可用状态，  
以便理解这些路由没有 Swagger 详情页，而不是误以为功能坏了。

验收要点：

- `included_in_openapi=false` 的路由仍显示在接口列表中。
- 此类路由的「查看」入口为禁用态或等价不可点击状态。
- 禁用原因明确，例如「未纳入 OpenAPI，暂无 Swagger 详情」。

## US-004 保持接口文档表格一致性

作为后台管理员，  
我希望新增操作列后接口文档页仍保持管理端列表页的一致体验，  
以便在筛选、分页、查看详情之间保持稳定、紧凑的信息浏览效率。

验收要点：

- 表格、分页、筛选、空状态不因新增操作列出现布局抖动。
- 反馈提示不插入文档流，不推挤 hero 或表格。
- 不使用 `window.confirm` / `window.alert` 等原生弹窗。

## 关联与边界

| 项 | 说明 |
|---|---|
| 父需求 | `REQ-0022-admin-api-docs-menu` |
| 相邻缺陷 | `BUG-0051-api-docs-swagger-ui-link-wrong` 修全局 Swagger 入口；本 REQ 做行级详情入口 |
| 不涉及 | 数据库、小程序、店主 Web、接口编辑、Swagger 自动注入鉴权 |
