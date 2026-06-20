## Why

REQ-0005-tile-category-management 要求 TILESFST 管理后台提供瓷砖类目主数据管理能力（最多三级类目树、列表联动、检索、新增/编辑、启停、条件删除）。类目是 SKU 归属、前台目录与筛选导航的基础主数据；当前 Sidebar「瓷砖类目」无路由、`tile_categories` 表仅为桩结构、无 Admin Tile Categories API。在 `add-admin-home` Shell 与用户/品牌管理列表模式就绪后，MUST 补齐类目管理能力，否则运营无法维护类目树与 SKU 绑定关系。

## What Changes

- 扩展 `tile_categories` 表：`parent_id` 自引用、`code` UNIQUE、`sort_order`、`level`（1–3）、`description`、`status`（ENABLED/DISABLED）、`sku_count`（本期默认 0）、`path`、`created_at`、`updated_at`。
- 新增 Admin Tile Categories REST API：`GET/POST /api/v1/admin/tile-categories`、`GET/PUT .../{id}`、`GET .../tree`、`POST .../enable`、`POST .../disable`、`DELETE .../{id}`；`admin` 与 `employee` 可调用。
- 业务规则：最多三级类目；删除仅允许 `sku_count=0` 且 `DISABLED`；编码唯一；排序为正整数；三级类目不可再挂子级。
- 前端 `/admin/tile-categories`：四指标卡、检索（名称/编码/状态/层级）、左侧类目树（280px）+ 右侧列表联动、工具栏仅「调整排序」、分页（10/20/50）；无导出。
- 新增/编辑弹窗 560px 单列六字段；CSS Port 自 `tile-category-management.html` / `tile-category-management-add.html`。
- Sidebar「瓷砖类目」导航至 `/admin/tile-categories`；Dashboard「新增类目」快捷操作跳转类目页。
- OpenAPI 更新 + Orval；pytest + vitest；HTML/PNG 视觉验收 gate。

## Capabilities

### New Capabilities

- `tile-category-management`：类目数据模型（树形）、Admin Tile Categories API、tree 端点、删除/深度/启停规则、列表 summary、错误码。

### Modified Capabilities

- `admin-dashboard`：Sidebar「瓷砖类目」active 态与真实路由；「新增类目」快捷操作不再占位 toast。
- `web-client`：新增「管理端瓷砖类目管理页」requirement（路由、类目树+列表、弹窗、删除规则、CSS Port）。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 新 `admin/tile-categories` 路由、model、repository、service、tree 构建 |
| 前端 Web 管理端 | `TileCategoryManagementPage`、`CategoryFormModal`、`CategoryTree`、`tile-category-management.css`、路由、Sidebar path |
| 数据库 | 扩展 `tile_categories` 表；更新 `schema.sql` 与 `docs/04-database-design.md` |
| API / Orval | **MUST** 重新生成 |
| MinIO | 不涉及（本期无图片上传） |
| Design System | `/design-system` 可选类目管理预览 |
| 测试 | pytest 集成 + vitest 组件 |
| Docker | backend + web 镜像重建 |
| 迭代 | backlog / sprint-003；依赖 `add-admin-home`；可与 `add-brand-management` 并行或顺序 |
