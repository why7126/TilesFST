---
change_id: add-api-docs-swagger-detail-link
requirement_id: REQ-0023-api-docs-swagger-detail-link
status: applied
created_at: 2026-07-02 09:26:53
updated_at: 2026-07-02 22:09:43
---

# Change Trace

## 基本信息

```yaml
change_id: add-api-docs-swagger-detail-link
change_type: add
status: applied
source_requirement: REQ-0023-api-docs-swagger-detail-link
sprint: sprint-004
impact:
  backend: false
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - web-client
    - testing
strategy: design-system-existing-admin-table
```

## Requirement Readiness Report

| 项 | 状态 | 说明 |
|---|---|---|
| requirement.md | ready | 已生成并评审，status `in_sprint` |
| user-stories.md | ready | 覆盖管理员直达 Swagger、上下文保留、非 OpenAPI 禁用态 |
| business-flow.md | ready | 覆盖主流程、链接生成、鉴权上下文和降级 |
| acceptance.md | ready | AC-001..025 与 AC-XCUT-001..004 已齐 |
| trace.md | ready | status `in_sprint`，iteration `sprint-004` |
| prototype/web | partially ready | HTML/context 已有；PNG 暂未导出，非阻塞 |

结论：Ready，可创建 OpenSpec Change。

## Impact Analysis

```yaml
impact:
  backend: false
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - web-client
    - testing
```

实现采用前端基于现有 route metadata 构造链接，不新增 `swagger_url` 字段，不要求后端/API/Orval 变更；API 影响从 possible 收敛为 false。

## Implementation Result

| 项 | 结果 | 说明 |
|---|---|---|
| Swagger 深链格式 | implemented | 使用 `/docs#/{encodeURIComponent(tag)}/{encodeURIComponent(operation_id)}` |
| OpenAPI 路由 | implemented | `included_in_openapi=true` 且 `operation_id`、`tag` 可用时显示新窗口「查看」链接 |
| PATH 列查看 | implemented | 可跳转行的 PATH 单元格复用同一 Swagger operationId 深链；不可跳转行保持普通文本 |
| ACTION 列固定 | implemented | ACTION 表头与操作单元格使用 sticky right 固定在横向滚动表格最右侧 |
| 筛选统计 | implemented | 底部分页 summary 使用当前 filtered route count，筛选后同步更新 |
| 非 OpenAPI 路由 | implemented | `included_in_openapi=false` 时显示禁用按钮，无 href，原因「未纳入 OpenAPI，暂无 Swagger 详情」 |
| operationId 缺失 | implemented | 缺少 `operation_id` 或 tag 时显示禁用按钮，无 href，原因「缺少 operationId，暂无 Swagger 详情」 |
| 鉴权上下文 | preserved | 行级链接仅使用 same-origin `/docs` hash，不拼接 token、Cookie、用户或环境信息 |
| API / Orval | not required | 未修改后端接口契约、OpenAPI schema 或生成客户端 |
| 数据库 / MinIO / Docker | not affected | 未修改 SQLite、Pydantic Schema、对象存储或 Docker Compose 配置 |

## Validation Results

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-07-02 10:34:20 | `pnpm --dir src/web exec vitest run src/pages/admin/ApiDocsPage.test.tsx` | pass，1 file / 11 tests |
| 2026-07-02 10:34:20 | `pnpm --dir src/web exec vitest run src/pages/admin/ApiDocsPage.test.tsx src/features/admin/components/AdminLayout.test.tsx src/features/auth/components/ProtectedRoute.test.tsx` | pass，3 files / 19 tests |
| 2026-07-02 10:34:20 | `rg -n "#[0-9A-Fa-f]{3,8}|rgba\\(" src/web/src/pages/admin/ApiDocsPage.tsx src/web/src/features/admin/styles/api-docs.css` | pass，无新增裸 Hex / rgba |
| 2026-07-02 21:54:56 | `pnpm --dir src/web exec vitest run src/pages/admin/ApiDocsPage.test.tsx` | pass，1 file / 11 tests |
| 2026-07-02 22:05:09 | `pnpm --dir src/web exec vitest run src/pages/admin/ApiDocsPage.test.tsx src/features/admin/components/AdminLayout.test.tsx src/features/auth/components/ProtectedRoute.test.tsx` | pass，3 files / 19 tests |
| 2026-07-02 22:05:09 | `openspec validate add-api-docs-swagger-detail-link --strict` | pass |
| 2026-07-02 22:05:09 | `python scripts/validate-directory-structure.py` | pass |
| 2026-07-02 22:16:42 | `pnpm --dir src/web exec vitest run src/pages/admin/ApiDocsPage.test.tsx src/features/admin/components/AdminLayout.test.tsx src/features/auth/components/ProtectedRoute.test.tsx` | pass，3 files / 19 tests |
| 2026-07-02 22:16:42 | `openspec validate add-api-docs-swagger-detail-link --strict` | pass |
| 2026-07-02 22:16:42 | `python scripts/validate-directory-structure.py` | pass |

## Conflict Report

| 来源 | 优先级 | 结论 |
|---|---:|---|
| REQ-0022 api-docs HTML/context | 1 | 页面结构、summary、filter、table、pagination 继续继承父需求 |
| REQ-0023 HTML/context | 2 | ACTION 列、可点击查看、禁用态、新窗口与深链为本 change 事实源 |
| acceptance.md | 3 | 作为行为验收清单 |
| rules/ui-design.md | 4 | 约束 semantic token、表格密度、可访问性 |
| openspec/specs | 5 | 通过 MODIFIED delta 合并新行为 |

无冲突阻塞。PNG Golden 未导出，后续实现可选补验收截图。

## Prototype Checklist

| 检查项 | HTML | PNG | Context | 说明 |
|---|---|---|---|---|
| ACTION 列 | pass | pending_export | pass | `api-docs-swagger-detail-link.html` 展示行级操作 |
| operationId 深链 | pass | pending_export | pass | 示例 `/docs#/admin-api-docs/get_api_docs_api_v1_admin_api_docs_get` |
| 非 OpenAPI 禁用态 | pass | pending_export | pass | `/media/{object_key:path}` 显示禁用「查看」 |
| 新窗口与安全属性 | pass | pending_export | pass | 可用链接使用 `target="_blank"` + `rel="noreferrer"` |

## Change Log

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-07-02 09:26:53 | `/req-opsx REQ-0023` | 创建 OpenSpec Change，生成 proposal/design/specs/tasks/trace |
| 2026-07-02 10:34:20 | `/opsx-apply add-api-docs-swagger-detail-link` | 完成 ACTION 列、Swagger operationId 深链、非 OpenAPI/缺失 operationId 禁用态与前端回归测试 |
| 2026-07-02 21:54:06 | 用户追加 | PATH 列复用同一 Swagger operationId 深链，作为「查看」的第二入口 |
| 2026-07-02 22:05:09 | 用户追加 | ACTION 列固定在表格最右侧，横向滚动时保持可见 |
| 2026-07-02 22:09:43 | 用户反馈修复 | 筛选后左下角 `共 * 个接口` 改为当前筛选结果数量 |
