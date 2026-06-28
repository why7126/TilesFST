## Why

REQ-0016-banner-management 要求 TILESFST 管理后台提供 Banner 运营配置能力。`REQ-0004-admin-home` 已在 Sidebar 预留「Banner 管理」、Dashboard 含「新增 Banner」快捷操作，但当前无 `/admin/banners` 路由、无 `banners` 表与 Admin Banner API。运营需维护各展示端 Banner 素材、排序、跳转目标与有效期，并在列表控制上线/下线。在 `add-tile-sku-management`（SKU 图库）与 `add-brand-management`（列表/启停模式）基线就绪后，MUST 补齐 Banner CRUD 与四种跳转类型弹窗，否则 Dashboard 占位无法闭环。

## What Changes

- 新增 `banners` 表：展示端、展示位置、跳转类型、SKU/外链/专题目标、`image_source`、排序、有效期、状态（`DRAFT`/`ONLINE`/`OFFLINE`/`EXPIRED`）。
- 新增最小 `topics` 种子表 + `GET /api/v1/admin/topics`（只读，供专题跳转下拉）。
- 新增 Admin Banners REST API：CRUD + online/offline + 条件删除 + Banner 图上传（MinIO `images/` 前缀，与 `update-object-storage-key-layout` 对齐）。
- 前端 `/admin/banners`：列表（筛选、指标卡、分页、上线下线确认）；640px 弹窗按 `jump_type` 分化（SKU 详情 / 外部链接 / 专题页 / 无跳转）；弹窗 **不含** 状态字段。
- SKU 详情跳转：关联 SKU、默认主图、可切换 `tile_images` 或自定义上传。
- **MODIFIED** `admin-nav.ts`：「Banner 管理」`path: '/admin/banners'`。
- **MODIFIED** Dashboard「新增 Banner」：导航至 `/admin/banners?action=create`（非占位 toast）。
- OpenAPI 更新 + Orval；pytest + vitest；列表 + 四套弹窗 HTML/PNG 视觉验收 gate。

## Capabilities

### New Capabilities

- `banner-management`：Banner 与 topics 种子数据模型、Admin Banners/Topics API、跳转类型校验、online/offline 规则、MinIO Banner 上传、错误码、PNG/HTML 验收 gate。

### Modified Capabilities

- `admin-dashboard`：Sidebar Banner 可导航与 active 态；Dashboard「新增 Banner」快捷操作落地。
- `web-client`：新增「管理端 Banner 管理页」与 `BannerFormModal`（jump_type 条件字段）。
- `object-storage`：Banner 运营图上传 object_key 形态（`images/default/banners/...`）。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 新 `admin/banners`、`admin/topics` 路由、model、repository、service；migration；upload 端点 |
| 前端 Web 管理端 | `BannerManagementPage`、`BannerFormModal`、`banner-management.css`、路由、Sidebar、Dashboard |
| 数据库 | 新 `banners`、`topics`（种子） |
| 存储 | MinIO Banner 图；SKU 图库引用不重复上传 |
| API / Orval | **MUST** 重新生成 |
| 测试 | pytest banners CRUD/online/offline/validation；vitest jump_type 切换与删除 disabled |
| Docker | backend + web 镜像重建 |
| 迭代 | sprint-003；依赖 admin-home、tile-sku、brand-management |
| Out of Scope | 店主端/小程序 Banner 消费展示、类目页跳转、专题 CRUD、外链白名单引擎 |
