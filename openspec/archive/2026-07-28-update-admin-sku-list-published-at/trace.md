---
change_id: update-admin-sku-list-published-at
status: applied
type: update
created_at: 2026-07-28 22:57:10
updated_at: 2026-07-28 23:45:00
source_requirement: REQ-0079-admin-sku-list-published-at
source_requirement_path: issues/requirements/archive/REQ-0079-admin-sku-list-published-at/
sprint: sprint-013
capabilities:
  modified:
    - tile-sku-management
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: true
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-012-retrospective.md
prototype_refs:
  - issues/requirements/archive/REQ-0079-admin-sku-list-published-at/prototype/web/admin-sku-list-published-at.html
  - issues/requirements/archive/REQ-0079-admin-sku-list-published-at/prototype/web/prototype-context.md
png_checklist:
  required: false
  status: pending
  note: PNG Golden Reference 暂无；HTML prototype 与 context 已覆盖列顺序、格式和空值策略。
---

# Change Trace

## 来源

- REQ：`REQ-0079-admin-sku-list-published-at`
- 评审状态：`approved`
- 父需求：`REQ-0006-tile-sku-management`
- Change 类型：`update`

## Requirement Readiness Report

| 项 | 结论 |
|---|---|
| status | approved |
| readiness | Ready |
| 五件套 | capture、requirement、user-stories、business-flow、acceptance、trace、review 均存在 |
| UI prototype | HTML + context 已存在，PNG 暂无且不阻塞 |
| Knowledge-base gate | Pass，已写入 admin-list AC-XCUT |

## Conflict Report

| 来源 | 优先级 | 结论 |
|---|---:|---|
| HTML prototype | 1 | 列顺序与空值示例明确：发布时间位于更新时间前，空值为 `-`。 |
| PNG | 2 | 暂无，不阻塞。 |
| prototype context | 3 | 与 HTML 一致，要求复用现有列表和 DS token。 |
| acceptance | 4 | 与 prototype 一致，包含功能 AC 与 admin-list 横切 AC。 |
| ui-design | 5 | 支持管理端列表复用模板和 semantic token。 |
| existing spec | 6 | 已有列表 API 规范，使用 MODIFIED requirement 扩展。 |

结论：无冲突。实施优先遵循 HTML prototype 和 context；验收按 acceptance 与 AC-XCUT 执行。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-28 23:15:05 | `/opsx-apply` | 已实现管理端 SKU 列表“发布时间”列；后端列表项新增 `published_at`，已上架 SKU 返回兼容发布时间，未上架为空；前端复用更新时间格式化路径。 |
| 2026-07-28 23:45:00 | scope-adjust | 修正发布时间语义：新增 `tiles.published_at` 真实字段，上架/恢复上架时刷新，恢复上架视为重新发布。 |
| 2026-07-28 23:03:00 | `/sprint-propose` | 纳入 sprint-013 正式范围。 |
| 2026-07-28 22:57:10 | `/req-opsx` | 创建 OpenSpec Change，并生成 proposal、design、delta spec、tasks 与 trace。 |

## Implementation Evidence

| 项 | 结论 |
|---|---|
| API/Orval | 已运行 `./scripts/generate-openapi-client.sh`，`TileSkuAdminItem` 生成类型包含 `published_at?: string \| null`。 |
| Backend | `GET /api/v1/admin/tile-skus` 列表项增加 `published_at`；未改分页、summary、鉴权、错误响应；`POST /publish` 每次成功刷新 `tiles.published_at`。 |
| Web Admin | SKU 表格在“更新时间”前新增“发布时间”；复用 `formatSkuDateTime`，空值/非法值显示 `—`。 |
| Layout | SKU 表格仍使用 `.table-card` 横向滚动、`min-width: 760px` 与 `.admin-sticky-action-cell` sticky 操作列；新增列不影响搜索、筛选、分页、toast 或操作列 DOM。 |
| Cross-cutting | 保持 `.page-summary` + `.page-right` 分页 DOM；未引入 `window.confirm`；未改危险状态操作的确认弹窗路径。 |

## Validation Evidence

| 命令 | 结果 |
|---|---|
| `uv run pytest src/backend/tests/test_admin_tile_skus.py` | Pass：24 passed。 |
| `pnpm --dir src/web test -- TileSkuManagementPage.test.tsx` | Pass：Vitest run 完成，56 files / 297 tests passed。 |
| `openspec validate update-admin-sku-list-published-at --strict` | Pass。 |

## Impact Conclusion

- API：有兼容新增字段 `published_at`，已同步 OpenAPI 与 Orval。
- DB：新增 `tiles.published_at`，已同步 SQLite/MySQL schema、SQLite/MySQL 兼容迁移与数据库文档。
- Web/Admin：仅管理端 SKU 列表展示变更。
- 小程序/存储/Docker：无影响，本次未触发 Docker Compose 验证。
- 残余风险：既有已上架历史数据迁移时以 `updated_at` 回填初始 `published_at`；后续每次上架/恢复上架会刷新为真实发布操作时间。
