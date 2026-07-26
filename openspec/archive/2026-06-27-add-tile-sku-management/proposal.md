## Why

REQ-0006-tile-sku-management 要求 TILESFST 管理后台提供瓷砖 SKU 商品主数据管理能力（列表、多维筛选、新增/编辑、多图主图、多视频、参考价格、上下架、条件删除）。SKU 是平台最核心的商品实体；当前 Sidebar「瓷砖SKU」无路由、现有 `tiles` 表字段不足以支撑 v4 原型（缺品牌、SKU 编码、工艺、价格、视频等），且无 Admin Tile SKU API。在 `add-admin-home` Shell、`add-brand-management` 与 `add-tile-category-management` 主数据就绪后，MUST 补齐 SKU 管理能力，否则运营无法维护商品资料与素材。

## What Changes

- 扩展 `tiles` 表（或等价 SKU 表）：`sku_code` UNIQUE、`brand_id`、`category_id`、`surface_finish`、`color_family`、`reference_price`、`remark`、`status`（PUBLISHED/DRAFT/NEEDS_COMPLETION/DISABLED）等；保留并扩展 `tile_images.is_main`。
- 新增 `tile_videos` 表（或 media 关联）：多视频元数据（object_key、文件名、大小、时长等）。
- 新增 Admin Tile SKU REST API：`GET/POST /api/v1/admin/tile-skus`、`GET/PUT .../{id}`、`POST .../publish`、`POST .../unpublish`、`DELETE .../{id}`；列表含 summary（总数/已上架/待完善/草稿）与素材完整度筛选。
- 业务规则：创建默认 DRAFT；弹窗无状态字段；「保存草稿」与「创建SKU」校验级别不同（见 design D8）；删除仅允许非 PUBLISHED 且无业务引用；已上架不可删。
- 图片/视频上传走后端授权 MinIO（`tiles/{id}/images/`、`tiles/{id}/videos/` 前缀，见 `rules/media.md`）。
- 前端 `/admin/tile-skus`：指标卡、五维筛选、表格、分页（10/20/50/100，默认 20）、新增/编辑弹窗（880px）；CSS Port 自 v4 HTML 原型。
- Sidebar「瓷砖SKU」与 Dashboard「新增 SKU」导航至真实路由。
- OpenAPI 更新 + Orval；pytest + vitest；HTML 原型视觉验收 gate（PNG 可选）。

## Capabilities

### New Capabilities

- `tile-sku-management`：SKU 数据模型扩展、Admin Tile SKU API、多图主图、多视频、publish/unpublish、条件删除、素材完整度、错误码。

### Modified Capabilities

- `admin-dashboard`：Sidebar「瓷砖SKU」active 态与 `/admin/tile-skus` 路由；Dashboard「新增 SKU」快捷操作不再占位 toast。
- `web-client`：新增「管理端瓷砖 SKU 管理页」requirement（列表、880px 弹窗、多图主图、多视频、CSS Port）。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 新/扩展 `admin/tile-skus` 路由、model、repository、service、media 上传 |
| 前端 Web 管理端 | `TileSkuManagementPage`、`TileSkuFormModal`、`tile-sku-management.css`、路由、Sidebar |
| 数据库 | 扩展 `tiles`；新 `tile_videos`；更新 `schema.sql` 与 `docs/04-database-design.md` |
| API / Orval | **MUST** 重新生成 |
| MinIO | SKU 图片/视频 object_key；单桶前缀 |
| 依赖 | `add-brand-management`（brand 下拉）、`add-tile-category-management`（category 下拉） |
| 测试 | pytest 集成 + vitest 组件 |
| Docker | backend + web 镜像重建 |
