## Context

`BUG-0090-admin-sku-list-publish-sort-order` 指向 Web 管理端 SKU 列表默认排序不符合业务预期。当前代码证据显示：

- `src/backend/app/repositories/tile_sku_repository.py` 的 `list_skus()` 使用 `ORDER BY t.updated_at DESC LIMIT :limit OFFSET :offset`。
- `src/web/src/pages/admin/TileSkuManagementPage.tsx` 的 `loadSkus()` 调用 `fetchTileSkus()` 时只传分页和筛选参数，没有传排序参数。
- 正式规格 `openspec/specs/tile-sku-management/spec.md` 仍写明“列表 MUST 默认按 `updated_at` 降序”，与本 BUG 的期望相冲突。

关联需求 `REQ-0079-admin-sku-list-published-at` 已要求管理端 SKU 列表展示“发布时间”列并明确 `published_at` 字段来源，但该需求当时要求“不改变默认排序”。本修复专门修改默认排序契约。

## Goals / Non-Goals

**Goals:**

- 默认列表中已发布 SKU 按最近发布时间展示。
- 未发布 SKU 按最近创建时间展示。
- 已发布与未发布混排时规则明确、稳定、可分页。
- 搜索、筛选、状态筛选、素材完整度筛选和分页继续遵守同一排序契约。
- 响应结构、鉴权、错误码、加载态、空态和行操作不回归。

**Non-Goals:**

- 不新增 SKU 数据字段或数据库迁移。
- 不新增用户可配置排序控件。
- 不改变 `published_at` 的写入语义、上架/下架接口响应结构或发布时间列展示格式。
- 不调整 SKU 新增、编辑、上架、下架、删除的业务校验。

## Decisions

### D1. 默认排序由后端统一执行

排序必须在后端查询层完成，避免前端只排序当前页导致跨页结果不稳定。Web 端继续使用现有 `fetchTileSkus()` 请求参数；除非实现阶段明确新增排序参数，否则不需要同步 Orval。

### D2. 混排规则采用已发布优先

默认列表应先展示已发布 SKU，再展示未发布 SKU。已发布分组按 `published_at DESC`；未发布分组按 `created_at DESC`。该规则贴合管理端优先查看最近发布商品，其次查看待处理草稿和下架记录的运营场景。

### D3. 稳定兜底排序必须覆盖空值和重复值

已发布 SKU 的 `published_at` 理论上由发布动作写入，但历史数据或异常数据可能为空。实现阶段应选择稳定表达式处理空值，并以 `id DESC` 或等价唯一递减字段作为末级兜底。未发布 SKU 使用 `created_at DESC` 后也必须追加稳定兜底，确保分页不会因相同时间值抖动。

### D4. 状态筛选不改变排序口径

当用户按 `PUBLISHED` 筛选时，结果仍按 `published_at DESC`；当用户按 `DRAFT`、`NEEDS_COMPLETION` 或 `DISABLED` 筛选时，结果仍按 `created_at DESC`。混合状态列表按 D2 分组排序。

### D5. 测试以构造差异时间样本为核心

回归测试必须构造 `updated_at` 与 `published_at` / `created_at` 不一致的数据，避免测试样本碰巧同序。分页测试应覆盖排序边界跨页稳定，不只断言第一页。

## Risks / Trade-offs

- [Risk] 历史已发布 SKU `published_at` 为空导致排序不直观。Mitigation: 明确空值兜底并补充测试；必要时在实现阶段记录历史数据兼容策略。
- [Risk] 默认排序改变可能影响习惯按最近编辑查找记录的运营人员。Mitigation: 本 BUG 已明确业务期望；后续若需要“最近编辑”入口，应单独提出排序控件需求。
- [Risk] SQL 在 SQLite/MySQL 对 NULL 排序表达式兼容性不同。Mitigation: 使用跨数据库可控的 CASE 表达式和稳定字段排序，并用 SQLite 测试覆盖本地路径。

## Migration Plan

1. 更新后端 SKU 列表查询排序表达式，使用状态分组、业务时间和稳定兜底字段。
2. 保持 API 请求/响应结构不变；若实现阶段新增参数，则同步 OpenAPI、Orval、docs 和测试夹具。
3. 补充后端测试，覆盖已发布、未发布、混排、空发布时间、同时间和分页。
4. 补充 Web 管理端测试或现有页面测试断言列表顺序、发布时间列和更新时间列不回归。
5. 运行相关 pytest、前端测试、OpenSpec 校验和目录结构校验。

## Open Questions

- 下架 SKU 是否应归入“未发布”分组并按 `created_at DESC` 排序；本 Change 默认将非 `PUBLISHED` 均视为未发布分组。
- 历史 `PUBLISHED` 但 `published_at` 为空的 SKU 是否需要数据修复；本 Change 默认先通过排序兜底处理，不要求迁移。
