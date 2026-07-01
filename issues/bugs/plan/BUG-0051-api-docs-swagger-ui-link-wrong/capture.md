---
bug_id: BUG-0051-api-docs-swagger-ui-link-wrong
status: captured
created_at: 2026-07-01 09:09:32
updated_at: 2026-07-01 09:09:32
severity_hint: high
environment: local
related_requirement: REQ-0022-admin-api-docs-menu
related_bug:
captured_via: capture
classification_rationale: 已交付接口文档页的 Swagger UI 入口跳转到 localhost:3000/，与预期 Swagger 页面不一致，属于既有功能异常。
---

# 现象

接口文档页右上角点击【Swagger UI】后，没有进入对应 Swagger 页面，而是进入 `localhost:3000/`。

# 复现步骤

1. 打开 Web 管理端接口文档页。
2. 点击页面右上角【Swagger UI】。
3. 观察跳转目标。

# 期望 vs 实际

- 期望：点击【Swagger UI】进入后端 Swagger UI 页面，通常为 `/docs`，用于查看运行时 OpenAPI 文档。
- 实际：点击后进入 `localhost:3000/`，未进入 Swagger UI。

# 影响范围

- Web 管理端 `/admin/api-docs`
- 已交付能力：`REQ-0022-admin-api-docs-menu`
- 影响用户通过接口文档页快速进入 Swagger UI。

# 附件

暂无。

# 分类说明（/capture）

该条目具有明确的期望与实际偏差，且 Swagger UI 入口属于已交付接口文档页能力，因此判定为 BUG。
