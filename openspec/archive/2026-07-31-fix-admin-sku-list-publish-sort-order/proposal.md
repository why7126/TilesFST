## Why

Web 管理端 SKU 列表默认排序未按业务时间展示，已记录为 [BUG-0090](../../../issues/bugs/archive/BUG-0090-admin-sku-list-publish-sort-order/bug.md)。当前正式规格仍要求列表默认按 `updated_at` 降序，后端仓储层也按 `t.updated_at DESC` 返回结果。这会导致已发布 SKU 因后续编辑覆盖发布时间顺序，未发布草稿也可能因最近编辑覆盖创建顺序，影响后台运营查找最近发布和最近创建的 SKU。

## What Changes

- 修改管理端 SKU 列表默认排序契约：默认结果按发布状态分组，已发布 SKU 优先；已发布 SKU 按 `published_at DESC`，未发布 SKU 按 `created_at DESC`。
- 为主排序时间为空或重复的情况补充稳定兜底排序，避免刷新、筛选和分页后顺序跳动。
- 保持现有筛选、分页、鉴权、响应结构、错误码、加载态、空态和行操作行为不变。
- 补充后端列表排序测试和 Web 管理端列表回归测试，覆盖已发布、未发布、混排、时间相同、发布时间为空、搜索筛选和分页。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `tile-sku-management`: 修改管理端 SKU 列表与筛选 API 的默认排序契约，移除“默认按 `updated_at` 降序”的旧要求，补充发布时间、创建时间和稳定兜底排序场景。

## Impact

- `backend`: 影响 `GET /api/v1/admin/tile-skus` 列表查询排序，重点是 `tile_sku_repository.list_skus()`。
- `web`: 影响 Web 管理端 `/admin/tile-skus` 列表默认展示顺序；不计划新增前端排序控件。
- `admin`: 影响后台运营浏览 SKU 的默认顺序，不改变新增、编辑、上架、下架、删除权限和交互。
- `api`: 若仅调整默认排序，响应结构和请求参数不变，不需要 Orval；若实现阶段新增排序参数，必须同步 OpenAPI、Orval、接口文档和测试。
- `database`: 不计划新增表或字段；依赖现有 `published_at`、`created_at`、`id`。
- `tests`: 需要补充后端排序测试和 Web 管理端列表顺序回归测试。

## Rollback Plan

实现阶段应将排序调整集中在后端列表查询中，便于回滚为旧的 `updated_at DESC` 查询。若新排序造成分页或运营验收异常，可临时回退查询排序，同时保留测试样本和 BUG 记录用于重新确认混排规则。回滚不得改变 `published_at` 写入逻辑、SKU 响应结构、鉴权、筛选、分页或已有列表列展示。
