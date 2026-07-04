---
created_at: 2026-07-02 09:26:53
updated_at: 2026-07-02 09:26:53
---

## Why

`/admin/api-docs` 已能展示接口目录和全局 Swagger 入口，但管理员从某一行接口查看具体 Swagger 详情时仍需手动搜索 Method、Path 或 operationId，联调效率低且容易定位错误接口。

REQ-0023 要求在接口列表内增加行级「查看」入口：OpenAPI 路由新窗口跳转到具体 operationId 锚点，未纳入 OpenAPI 的路由显示禁用态并保留全量目录上下文。

## What Changes

- 在 Web 管理端 `/admin/api-docs` 接口表格中新增 ACTION 列。
- 对 `included_in_openapi=true` 且 `operation_id` 非空的路由，生成同源 Swagger UI 深链 `/docs#/{tag}/{operationId}` 或经验证等价格式。
- 行级 Swagger 入口使用新窗口打开，并保留当前管理端筛选、分页、滚动和登录上下文。
- 对 `included_in_openapi=false` 或缺少 `operation_id` 的路由显示禁用态「查看」，不生成 href，不跳转到通用 `/docs`。
- 补充前端回归测试，覆盖 operationId 深链、非 OpenAPI 禁用态、新窗口安全属性和 token 不泄露。
- 不新增 Swagger 自动注入 token 机制，不改变生产环境 Try It Out 禁用策略。

## Capabilities

### New Capabilities

- 无。该需求是已归档 `/admin/api-docs` 能力的行级增强。

### Modified Capabilities

- `web-client`: 修改 Web 管理端接口文档 Swagger 入口要求，增加接口行级详情深链、禁用态和鉴权上下文约束。
- `testing`: 修改 Swagger 入口回归测试要求，增加行级 Swagger 详情入口相关测试覆盖。

## Impact

- Web 管理端：影响 `src/web/src/pages/admin/ApiDocsPage.tsx` 及相关样式/测试。
- 管理端权限：保持 `admin` 可访问、`employee` 不可访问的既有边界。
- API：默认不变；若实现决定由后端返回 `swagger_url` 等字段，则必须同步 OpenAPI、Orval 与 `docs/03-api-index.md`。
- 数据库：无影响。
- MinIO / 对象存储：无影响。
- 小程序 / 店主 Web：无影响。
- Docker：默认无影响；依赖 BUG-0051 已归档的同源 `/docs` Web 代理能力。
