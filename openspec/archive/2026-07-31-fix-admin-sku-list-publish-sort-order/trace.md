---
change_id: fix-admin-sku-list-publish-sort-order
source_bug: BUG-0090-admin-sku-list-publish-sort-order
change_type: fix
status: archived
created_at: 2026-07-30 23:28:00
updated_at: 2026-07-31 00:18:00
owner: product
iteration: sprint-014
---

# Change Trace

## 来源

- BUG: `issues/bugs/archive/BUG-0090-admin-sku-list-publish-sort-order/`
- 相关需求：`REQ-0006-tile-sku-management`
- 相关历史需求：`REQ-0079-admin-sku-list-published-at`
- 相关能力：`tile-sku-management`
- 预期 Change：`fix-admin-sku-list-publish-sort-order`

## 影响分析

```yaml
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - tile-sku-management
change_type: fix
readiness: Ready
```

## 规格依据

- `openspec/specs/tile-sku-management/spec.md` 当前要求管理端 SKU 列表默认按 `updated_at` 降序。
- `BUG-0090` 要求已发布 SKU 按 `published_at` 降序、未发布 SKU 按 `created_at` 降序。
- `REQ-0079` 已沉淀 `published_at` 字段来源和发布时间列展示，本 Change 只修改默认排序契约。

## 验收证据要求

```text
BUG-0090 acceptance.md > root-cause.md > openspec/specs/tile-sku-management/spec.md
```

Evidence checklist：

- [x] 后端列表排序测试覆盖已发布、未发布、混排、空发布时间、同时间和分页稳定。
- [x] Web 管理端列表测试或验收截图覆盖发布时间列、更新时间列和默认顺序。
- [x] API 请求/响应结构未变更；如变更则提供 OpenAPI、Orval、docs 和测试同步证据。
- [x] BUG trace、Change trace、Sprint 验收材料记录实现与回滚策略。

## 实现记录

- 后端 `TileSkuRepository.list_skus()` 默认排序改为：已发布优先；已发布按 `published_at DESC`；非 `PUBLISHED` 按 `created_at DESC`；空发布时间、重复业务时间使用 `t.id DESC` 稳定兜底。
- Web 管理端未新增排序参数，`TileSkuManagementPage` 继续按后端分页返回顺序渲染。
- API 请求参数、响应 envelope、错误码、Pydantic Schema、OpenAPI / Orval、数据库表结构均未变更。
- 回滚策略：若上线后默认顺序不符合运营验收，可集中回退 `src/backend/app/repositories/tile_sku_repository.py` 的排序表达式为旧排序；回滚不涉及数据迁移。
- 后续事项：本次未发现实际历史 `PUBLISHED` 且 `published_at` 为空的数据治理证据，未自动创建 follow-up Issue。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-30 23:28:00 | `/bug-opsx` | 从 BUG-0090 创建 OpenSpec Change，生成 proposal、design、delta spec、tasks 与 trace |
| 2026-07-30 23:38:50 | `/sprint-propose sprint-014` | 纳入 sprint-014 正式范围 |
| 2026-07-31 00:18:00 | `/opsx-apply` | 完成后端默认排序修复、Web 顺序回归测试、OpenSpec 与目录校验 |
| 2026-07-31 00:18:00 | `/opsx-archive` | 合并 delta spec 至正式规格并归档到 `openspec/archive/2026-07-31-fix-admin-sku-list-publish-sort-order/` |
