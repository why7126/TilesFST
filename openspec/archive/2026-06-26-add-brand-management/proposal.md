## Why

REQ-0005-brand-management 要求 TILESFST 管理后台提供瓷砖品牌主数据管理能力（列表、筛选、新增/编辑、启停、条件删除、Logo 上传）。品牌是 SKU、前台展示与搜索筛选的基础主数据；当前 Sidebar「瓷砖品牌」无路由、无 `brands` 表与 Admin Brands API。在 `add-admin-home` Shell 与 `add-user-management` 列表/弹窗模式就绪后，MUST 补齐品牌管理能力，否则运营无法维护品牌主数据。

## What Changes

- 新增 `brands` 表：名称唯一、排序、简称、英文名、Logo object_key、介绍、状态（ENABLED/DISABLED）、`sku_count`（本期 SKU 未实现时默认 0）、时间戳。
- 新增 Admin Brands REST API：`GET/POST /api/v1/admin/brands`、`GET/PUT /api/v1/admin/brands/{id}`、`POST .../enable`、`POST .../disable`、`DELETE .../{id}`；`admin` 与 `employee` 可调用（运营主数据维护）。
- 业务规则：创建默认 ENABLED；删除仅允许 `sku_count=0` 且 `DISABLED`；名称唯一；排序为正整数。
- 前端 `/admin/brands`：指标卡、筛选、表格、分页（含每页 20/50/100）、新增/编辑弹窗（720px）；无导出、无批量操作。
- CSS Port 自 `brand-management.html` / `brand-management-modal.html`；复用 `AdminLayout` + admin Shell 样式。
- Logo 上传走后端授权（MinIO `brands/` 前缀）。
- Sidebar「瓷砖品牌」导航至 `/admin/brands`；Dashboard「新增品牌」快捷操作跳转品牌页。
- OpenAPI 更新 + Orval；pytest + vitest；HTML/PNG 视觉验收 gate。

## Capabilities

### New Capabilities

- `brand-management`：品牌数据模型、Admin Brands API、删除/启停规则、Logo 存储、列表 summary、错误码。

### Modified Capabilities

- `admin-dashboard`：Sidebar「瓷砖品牌」active 态与真实路由；「新增品牌」快捷操作不再占位 toast。
- `web-client`：新增「管理端瓷砖品牌管理页」requirement（路由、列表、弹窗、删除规则、CSS Port）。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 新 `admin/brands` 路由、model、repository、service |
| 前端 Web 管理端 | `BrandManagementPage`、`BrandFormModal`、`brand-management.css`、路由、Sidebar path |
| 数据库 | 新 `brands` 表；更新 `schema.sql` 与 `docs/04-database-design.md` |
| API / Orval | **MUST** 重新生成 |
| MinIO | 品牌 Logo object_key；单桶前缀 |
| Design System | `/design-system` 可选品牌管理预览 |
| 测试 | pytest 集成 + vitest 组件 |
| Docker | backend + web 镜像重建 |
| 迭代 | sprint-002；依赖 `add-admin-home` Admin Shell |
