## 1. 排序契约确认

- [x] 1.1 确认 `GET /api/v1/admin/tile-skus` 默认排序采用已发布优先、已发布按 `published_at DESC`、未发布按 `created_at DESC`。
- [x] 1.2 明确非 `PUBLISHED` 状态均归入未发布分组，包括 `DRAFT`、`NEEDS_COMPLETION`、`DISABLED`。
- [x] 1.3 明确 `published_at` 为空、主排序时间重复时的稳定兜底字段，优先使用 `id DESC` 或等价唯一递减字段。

## 2. 后端实现

- [x] 2.1 修改 SKU 仓储层列表查询排序，替换当前 `updated_at DESC` 默认排序。
- [x] 2.2 保持分页、关键词、品牌、类目、状态、素材完整度筛选和 summary 查询不变。
- [x] 2.3 保持管理端鉴权、响应 envelope、错误码和 `TileSkuAdminItem` 响应字段不变。
- [x] 2.4 若实现阶段新增排序参数或响应字段，同步 Pydantic Schema、OpenAPI、Orval、接口文档和测试夹具。

## 3. Web 管理端回归

- [x] 3.1 确认 Web 管理端 `/admin/tile-skus` 不做当前页本地排序，默认顺序来自后端分页结果。
- [x] 3.2 回归发布时间列、更新时间列、筛选、分页、加载态、空态、失败态和行操作不受排序调整影响。
- [x] 3.3 覆盖上架、下架、编辑后刷新列表时的默认顺序符合业务时间排序。

## 4. 测试与校验

- [x] 4.1 补充后端测试：已发布 SKU `updated_at` 晚但 `published_at` 旧时，不应排在发布时间更新的 SKU 前面。
- [x] 4.2 补充后端测试：未发布 SKU `updated_at` 晚但 `created_at` 旧时，不应排在创建时间更新的 SKU 前面。
- [x] 4.3 补充后端测试：混排、发布时间为空、主排序时间相同和分页边界顺序稳定。
- [x] 4.4 补充或更新 Web 管理端测试，覆盖列表加载后展示顺序和发布时间/更新时间列不回归。
- [x] 4.5 运行相关 pytest、Vitest、OpenSpec 校验和目录结构校验。

## 5. 验收与追溯

- [x] 5.1 在 BUG trace、Change trace 和 Sprint 验收材料中记录实现、测试、环境、剩余风险和回滚策略。
- [x] 5.2 若修复过程中发现历史 `PUBLISHED` 且 `published_at` 为空的数据需要治理，按标准 capture 文案提出后续 Issue，未授权时不自动创建。
- [x] 5.3 若该排序问题沉淀出可复用的管理端列表默认排序经验，补充 `docs/knowledge-base/best-practices/` 或相关 incident 文档。

说明：本次未发现实际历史数据治理证据，因此未自动创建 follow-up Issue；管理端列表页经验复用既有 `docs/knowledge-base/best-practices/admin-list-page-consistency.md` 与 Sprint 014 横切清单，未新增长期知识库文档。
