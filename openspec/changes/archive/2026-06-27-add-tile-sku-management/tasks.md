## 1. 数据库与后端基础

- [x] 1.1 扩展 `schema.sql`：`tiles` 新增 sku_code、brand_id、surface_finish、reference_price、remark 等；创建 `tile_videos`
- [x] 1.2 数据迁移：`model` → `sku_code`（若需）；更新 `app/models/tile.py` 与 Brand/Category FK
- [x] 1.3 实现 SKU 校验（编码唯一、必填项、save_mode draft/create）
- [x] 1.4 实现 `TileSkuRepository`：分页、多维筛选、summary、material_completeness 计算
- [x] 1.5 实现 `TileSkuAdminService`：publish/unpublish、删除规则、主图唯一性

## 2. Admin Tile SKU API

- [x] 2.1 实现 `GET/POST /api/v1/admin/tile-skus` 与 Pydantic schemas（含 save_mode）
- [x] 2.2 实现 `GET/PUT /api/v1/admin/tile-skus/{id}`（含图片/视频）
- [x] 2.3 实现 `POST .../publish` 与 `POST .../unpublish`
- [x] 2.4 实现 `DELETE .../{id}` 与错误码 `TILE_SKU_CODE_DUPLICATED`、`TILE_SKU_DELETE_FORBIDDEN`、`TILE_SKU_PUBLISH_FORBIDDEN`
- [x] 2.5 注册路由（`require_admin_user`）；更新 OpenAPI
- [x] 2.6 扩展图片/视频上传（`tiles/{id}/images/`、`tiles/{id}/videos/` 前缀）

## 3. 后端测试

- [x] 3.1 pytest：CRUD、筛选 summary、save_mode、publish 矩阵、删除矩阵、编码重复、employee 可访问
- [x] 3.2 运行 `cd src/backend && uv run pytest tests/ -k tile_sku`

## 4. 前端 API 与路由

- [x] 4.1 运行 `./scripts/generate-openapi-client.sh`（Orval）
- [x] 4.2 `admin-nav.ts` 为「瓷砖SKU」添加 `path: '/admin/tile-skus'`
- [x] 4.3 注册 `/admin/tile-skus` 路由与 `TileSkuManagementPage`
- [x] 4.4 实现 `features/admin/api/tile-skus-api.ts`
- [x] 4.5 `DashboardQuickActions`「新增 SKU」导航至 `/admin/tile-skus?action=create`

## 5. CSS Port 与页面

- [x] 5.1 创建 `features/admin/styles/tile-sku-management.css`（自 v4 HTML port）
- [x] 5.2 实现 `TileSkuManagementPage`：header、4 指标卡、五维筛选、表格、分页
- [x] 5.3 实现 `TileSkuFormModal`（880px、字段顺序、多图主图、多视频、save_mode 双按钮）
- [x] 5.4 实现上下架、删除确认、Toast、列表刷新与空态/skeleton
- [x] 5.5 参考价格格式化 `¥ xx.xx`；素材列 badge（主图已设/缺主图、N图/M视频）

## 6. 前端测试

- [x] 6.1 vitest：主图切换、必填校验、save_mode 行为、删除禁用逻辑、价格格式化
- [x] 6.2 运行 `cd src/web && npx vitest run src/features/admin src/pages/admin`

## 7. 构建与部署

- [x] 7.1 `cd src/web && npm run build`
- [x] 7.2 `./scripts/docker-up.sh` 验证 `/admin/tile-skus`

## 8. 视觉验收（HTML 原型 gate；PNG 可选）

- [x] 8.1 1440×1024 并排 `/admin/tile-skus` 与 `tile-sku-management-list.html`
- [x] 8.2 打开新增/编辑弹窗并排 `tile-sku-create-modal.html`
- [x] 8.3 填写 `openspec/changes/add-tile-sku-management/trace.md` checklist
- [x] 8.4（可选）导出 PNG 至 `prototype/images/` 供 golden reference

## 9. 文档与追溯

- [x] 9.1 更新 `docs/03-api-index.md`、`docs/04-database-design.md`
- [x] 9.2 更新 `issues/requirements/REQ-0006-tile-sku-management/trace.md`（openspec 关联）
- [x] 9.3 建议导出 `prototype/images/*.png`（**可选**）
- [x] 9.4 完成后 `/opsx-archive add-tile-sku-management`
