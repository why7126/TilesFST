## Why

REQ-0009-tile-spec-management 要求 TILESFST 管理后台提供瓷砖规格主数据管理能力，并将 SKU 表单「规格尺寸」从自由文本改为下拉选择已启用规格。规格是 SKU 建档与列表展示的基础主数据；当前 `TileSkuFormModal` 手写 `size` 易产生重复与不一致，且无 `/admin/tile-specs` 路由、`tile_specs` 表与 Admin Tile Specs API。在 `add-brand-management` 与 `add-tile-sku-management` 基线就绪后，MUST 补齐规格主数据与 SKU `spec_id` 联动，否则运营无法统一维护标准规格。

## What Changes

- 新增 `tile_specs` 表：`(width_mm, length_mm, unit)` 唯一、`display_name` 系统生成、厚度/排序/备注、启停、`sku_count`。
- 扩展 `tiles` 表：新增 `spec_id` FK；创建/更新 SKU 时同步 `size = display_name`。
- 新增 Admin Tile Specs REST API：CRUD + enable/disable + 条件删除；`admin` 与 `employee` 可调用。
- 历史 SKU 迁移：按 `size` 文本匹配回填 `spec_id`；失败项须运营手动选择。
- 前端 `/admin/tile-specs`：指标卡、状态筛选、启停二次确认、条件删除、720px 弹窗；对齐品牌页模式。
- **MODIFIED** `TileSkuFormModal`：规格字段改为 `<select>`（仅 `ENABLED` 规格）。
- Sidebar OPERATIONS 新增「瓷砖规格」（类目与 Banner 之间）；`admin-nav.ts` path `/admin/tile-specs`。
- OpenAPI 更新 + Orval；pytest + vitest；HTML 视觉验收 gate（PNG 待导出）。

## Capabilities

### New Capabilities

- `tile-spec-management`：规格数据模型、Admin Tile Specs API、启停/删除规则、sku_count 维护、迁移脚本、错误码、PNG/HTML 验收 gate。

### Modified Capabilities

- `tile-sku-management`：SKU 数据模型增加 `spec_id`；create/update/publish 校验规格主数据；sku_count 联动。
- `web-client`：新增「管理端瓷砖规格管理页」；SKU 弹窗规格下拉 MODIFIED。
- `admin-dashboard`：Sidebar 新增「瓷砖规格」导航与 active 态。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 新 `admin/tile-specs` 路由、model、repository、service；migration；SKU service 变更 |
| 前端 Web 管理端 | `TileSpecManagementPage`、`TileSpecFormModal`、`tile-spec-management.css`、SKU modal、路由、Sidebar |
| 数据库 | 新 `tile_specs`；`tiles.spec_id`；迁移脚本 |
| API / Orval | **MUST** 重新生成；SKU payload 含 `spec_id` |
| 测试 | pytest specs + SKU linkage + migration；vitest 删除/启停逻辑 |
| Docker | backend + web 镜像重建 |
| 迭代 | sprint-003；依赖 brand/category/SKU 基线 |
