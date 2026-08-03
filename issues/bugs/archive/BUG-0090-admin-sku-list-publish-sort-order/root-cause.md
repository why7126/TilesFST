---
bug_id: BUG-0090-admin-sku-list-publish-sort-order
status: done
created_at: 2026-07-30 23:11:20
updated_at: 2026-07-31 00:18:16
---

# 直接原因

管理端 SKU 列表的后端查询当前按 `t.updated_at DESC` 返回列表。Web 端 `TileSkuManagementPage` 请求 SKU 列表时只传分页、关键词、品牌、类目、状态和素材完整度筛选条件，没有传入排序参数，也没有在前端对返回结果进行业务排序。因此默认列表顺序完全依赖后端仓储层的 `updated_at` 排序。

代码证据：

- `src/backend/app/repositories/tile_sku_repository.py` 的 `list_skus()` 使用 `ORDER BY t.updated_at DESC LIMIT :limit OFFSET :offset`。
- `src/web/src/pages/admin/TileSkuManagementPage.tsx` 的 `loadSkus()` 调用 `fetchTileSkus()` 时未传排序字段。
- 列表表格展示了 `published_at` 与 `updated_at`，但当前排序依据仍是更新时间。

# 根本原因

SKU 管理列表缺少明确的默认排序契约：

- 关联需求 `REQ-0006-tile-sku-management` 已覆盖 SKU 管理能力，但未把“已发布按发布时间、未发布按创建时间”的排序规则沉淀为接口和验收契约。
- 后端列表查询使用通用的“最近更新优先”排序，适合管理最近变更，但不符合 SKU 发布运营场景中“最近发布”和“最近创建草稿”的浏览目标。
- API 请求参数中没有排序字段，前端也没有显式声明默认排序策略，导致排序行为难以从页面调用侧看出业务意图。
- 当前列表在已发布和未发布混排、发布时间为空、主排序时间重复时缺少稳定兜底规则，分页场景存在顺序跳动风险。

# 触发条件

1. 管理端存在多条 SKU。
2. 至少一条已发布 SKU 的 `updated_at` 晚于其他已发布 SKU，但 `published_at` 并非最新。
3. 或至少一条未发布 SKU 被编辑过，导致 `updated_at` 晚于其他更晚创建的未发布 SKU。
4. 运营人员进入 `/admin/tile-skus`，或使用搜索、筛选、分页查看 SKU 列表。

# 分类

- 类型：code / contract
- 层级：后端管理端 SKU 列表查询、Web 管理端列表展示
- 数据风险：低，不涉及数据写入或历史数据迁移
- API 风险：中，若调整默认排序不新增参数，响应结构不变但列表顺序契约改变；若新增排序参数，需要同步 OpenAPI / Orval
- 回归风险：中，需要覆盖默认列表、状态筛选、搜索、分页和发布时间为空的稳定排序

# 待修复阶段确认

后续修复应优先在后端统一排序，保证分页稳定。建议排序契约在 `/bug-opsx` 或实现阶段明确：

- 已发布 SKU 使用 `published_at DESC`。
- 未发布 SKU 使用 `created_at DESC`。
- 若已发布与未发布在同一列表混排，需要明确分组先后规则。
- 主排序时间相同或为空时，使用稳定兜底字段，例如 `id DESC` 或等价创建顺序字段。
