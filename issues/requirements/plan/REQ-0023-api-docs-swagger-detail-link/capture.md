---
req_id: REQ-0023-api-docs-swagger-detail-link
status: captured
created_at: 2026-07-01 09:09:32
updated_at: 2026-07-01 09:09:32
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0022-admin-api-docs-menu
captured_via: capture
classification_rationale: 为接口文档列表中的每个接口新增查看入口并跳转到 Swagger UI 详情，属于既有接口文档页的能力扩展。
---

# 一句话

接口文档列表中的每一个接口都需要提供“查看”按钮，点击后跳转至 Swagger UI 中对应接口，便于了解具体请求、响应与调试信息。

# 原始描述

接口文档页：

5. 列表每一个接口需要支持一个查看的按钮，点击后，跳转至【Swagger UI】了解具体的接口详情。

# 背景与关联

- 父需求：`REQ-0022-admin-api-docs-menu`
- 涉及端：Web 管理端
- 涉及页面：`/admin/api-docs`
- 目标页面：Swagger UI（后端 `/docs`）
- 业务价值：减少用户从接口目录手动搜索 Swagger 的成本，提升接口文档页到运行时接口详情的可达性

# 待澄清

- [ ] Swagger UI 是否需要跳转到具体 `operationId` 锚点，还是仅打开 `/docs` 并由用户搜索
- [ ] 新窗口打开还是当前窗口跳转
- [ ] 对 `included_in_openapi=false` 的路由是否显示禁用按钮、隐藏按钮，或跳转到通用 Swagger 页面
- [ ] 点击行为是否需要保留当前管理端鉴权上下文或提示 Swagger 调试权限

# 探索结论

（/req-explore 后人工确认写入）

# 分类说明（/capture）

该条目描述为列表中每个接口新增可操作入口，当前已交付能力仅包含接口目录与 Swagger 页面入口，未明确包含逐行详情跳转，因此判定为 REQ。
