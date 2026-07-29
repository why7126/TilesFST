## Context

来源需求：`REQ-0079-admin-sku-list-published-at`，已评审通过，父需求为 `REQ-0006-tile-sku-management`。

当前正式能力 `tile-sku-management` 已定义管理端 SKU 列表与筛选 API：`GET /api/v1/admin/tile-skus` 支持分页、关键词、品牌、类目、状态、素材完整度筛选，响应包含 `items`、`pagination`、`summary`，列表默认按 `updated_at` 降序。现有 spec 已要求管理端列表以商品名称作为主标题，SKU 编码为弱化内部辅助信息。

本 Change 增强管理端 SKU 列表展示：新增“发布时间”列并放在“更新时间”列前。实现确认当前模型缺少语义明确的发布时间字段，因此新增 `tiles.published_at` 作为最终字段来源；每次 `publish` 成功写入当前时间，恢复上架视为重新发布，`unpublish` 不清空数据库历史值，但非 `PUBLISHED` 状态响应返回 `published_at: null`。

## Goals / Non-Goals

**Goals:**

- 管理端 SKU 列表展示“发布时间”列，并保持与“更新时间”一致的时间格式和视觉样式。
- 明确发布时间字段语义，使用 `tiles.published_at`，不以 `updated_at` 或 `created_at` 冒充发布时间。
- 保持现有列表筛选、分页、默认排序、空态、加载态、错误态和行操作行为不变。
- 同步后端响应、Pydantic Schema、OpenAPI、Orval、API 文档和测试。
- 将 `admin-list` knowledge-base gate 纳入实现验收。

**Non-Goals:**

- 不新增按发布时间筛选。
- 不新增按发布时间排序或改变默认排序。
- 不调整批量导出字段。
- 不新增 SKU 发布审批、定时发布或撤回流程；仅在现有 `publish` 成功时维护 `published_at`。
- 不调整店主 Web、小程序商品列表或详情展示。
- 不做额外历史数据治理；兼容迁移仅对历史已上架 SKU 用 `updated_at` 回填 `published_at`。

## Decisions

### D1. UI Strategy: DS / Existing Admin List

采用现有管理端 SKU 列表结构与 Design System 语义 token，不做 CSS Port。

理由：本需求是已有列表页的列级增强，HTML prototype 只用于确认列顺序、格式和空值展示，不要求重设页面外观。实现应优先复用现有 SKU 列表 DOM、时间格式化 helper、表格横向滚动策略和 admin-list best-practice。

备选：CSS Port HTML 原型。未采用，因为这会扩大视觉迁移范围，且本需求不要求重做页面。

### D2. 发布时间字段使用 `tiles.published_at`

实现确认管理端 SKU 列表响应和后端数据模型没有语义明确的发布时间字段，因此新增 `tiles.published_at`。`POST /api/v1/admin/tile-skus/{id}/publish` 每次成功都会刷新该字段；从 `DISABLED` 恢复上架视为重新发布。`POST /api/v1/admin/tile-skus/{id}/unpublish` 不清空数据库历史值，但列表和响应在非 `PUBLISHED` 状态下返回 `published_at: null`。

理由：发布时间与更新时间是不同业务语义。真实字段可以表达“最近一次发布成功时间”，避免把后续编辑时间误认为发布行为。

历史兼容：已有 `PUBLISHED` SKU 在迁移时使用 `updated_at` 回填 `published_at`，作为上线前存量数据的最佳可得时间；非已上架历史 SKU 保持空值。

### D3. 列表行为保持

新增列不得改变 `GET /api/v1/admin/tile-skus` 的分页、搜索、筛选、默认排序和错误响应结构。列表仍默认按 `updated_at` 降序。

理由：需求目标是可见性增强，不是列表查询模型调整；保持行为稳定可以降低回归风险。

### D4. Prototype Conflict Resolution

原型优先级为 HTML > PNG > context > acceptance > `rules/ui-design.md` > `openspec/specs`。

Conflict Report:

| 项 | 结论 |
|---|---|
| HTML prototype | 明确列顺序为“状态 → 发布时间 → 更新时间 → 操作”，示例含合法时间和 `-` 空值。 |
| PNG | 暂无，非阻塞。 |
| prototype context | 与 HTML 一致，强调复用现有列表和 DS token。 |
| acceptance | 与 HTML/context 一致，要求列顺序、格式、空值和横切 AC。 |
| ui-design | 支持管理端列表复用模板与 semantic token。 |
| existing spec | 已有列表 API 和视觉 gate，需 MODIFIED 扩展。 |

处理：按 HTML 和 context 落地列顺序；按 acceptance 落地测试与横切 AC；不因无 PNG 阻塞。

### D5. Knowledge-base Gate

后续实现必须引用：

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/retrospectives/sprint-012-retrospective.md`

需要验收：

- 分页 DOM 对齐用户管理基准。
- fixed toast 不造成布局位移。
- 本需求无危险状态变更；如实现触及危险操作，必须使用 DS confirm modal。
- 不调用 `window.confirm`。
- 宽表与长时间文本不得遮挡核心字段和操作列。

## Risks / Trade-offs

- [Risk] 现有系统没有发布时间字段 → Mitigation: 先确认模型和发布流程；若缺字段，在实现任务中同步 DB/API/Orval/docs/tests，并为历史数据定义空值占位。
- [Risk] 直接以 `updated_at` 或 `created_at` 代替发布时间导致业务语义错误 → Mitigation: spec 和任务明确禁止未经确认的替代；测试覆盖字段映射。
- [Risk] 新增时间列导致宽表挤压操作列 → Mitigation: 沿用现有横向滚动/列宽策略，并在 1440x1024 与窄屏视口验收。
- [Risk] API 字段新增后 Orval 或前端类型未同步 → Mitigation: 将 OpenAPI/Orval 生成、类型检查和测试列为条件任务。
- [Risk] 列表页横切一致性回归 → Mitigation: acceptance 中保留 5 条 `AC-XCUT` 并在 trace 中记录验收 evidence。

## Migration Plan

1. 新增 `tiles.published_at` 字段、SQLite/MySQL schema 与兼容迁移。
2. 管理端列表、详情与发布响应补充 `published_at`，并在非 `PUBLISHED` 状态下返回 `null`。
3. `publish` 成功刷新 `published_at`；`unpublish` 保留数据库历史值。
4. 同步 Pydantic Schema、OpenAPI、Orval、API 文档、数据库文档和测试。
5. 部署后通过管理端列表回归测试确认列顺序、格式、空值和分页/筛选行为。

Rollback：如果后端字段新增引发问题，可先回退前端列展示并保留后端兼容字段；若仅前端列展示异常，回退列配置不影响已有 API。

## Resolved Questions

- `GET /api/v1/admin/tile-skus` 原先不返回语义明确的发布时间字段，本 Change 新增 `published_at`。
- 发布时间最终语义为最近一次发布成功时间；恢复上架视为重新发布。
- 历史已发布但缺发布时间的 SKU 由兼容迁移使用 `updated_at` 回填；未发布或下架 SKU 在列表响应中返回 `null`。
