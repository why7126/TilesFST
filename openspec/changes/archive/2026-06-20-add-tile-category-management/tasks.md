## 1. 数据库与后端基础

- [x] 1.1 扩展 `schema.sql` 中 `tile_categories`（parent_id、code UNIQUE、sort_order、level、description、status、sku_count、path、时间戳）
- [x] 1.2 实现迁移脚本（`migrations.py` 或等价）兼容现有桩数据
- [x] 1.3 实现 `app/models/tile_category.py` ORM 与约束
- [x] 1.4 实现类目校验（名称长度、编码唯一、排序正整数、最大三级）
- [x] 1.5 实现 `TileCategoryRepository`：树构建、分页列表、keyword/status/level/parent_id 筛选、summary、CRUD
- [x] 1.6 实现 `TileCategoryAdminService`：path/level 计算、删除规则、启停

## 2. Admin Tile Categories API

- [x] 2.1 实现 `GET /api/v1/admin/tile-categories/tree`
- [x] 2.2 实现 `GET/POST /api/v1/admin/tile-categories` 与 Pydantic schemas
- [x] 2.3 实现 `GET/PUT /api/v1/admin/tile-categories/{id}`
- [x] 2.4 实现 `POST .../enable` 与 `POST .../disable`
- [x] 2.5 实现 `DELETE .../{id}` 与错误码 `CATEGORY_*`
- [x] 2.6 注册路由（`require_admin_user`）；更新 OpenAPI

## 3. 后端测试

- [x] 3.1 pytest：CRUD、tree、筛选 summary、编码重复、删除矩阵、三级深度、enable/disable
- [x] 3.2 运行 `cd src/backend && uv run pytest tests/ -k tile_categor`

## 4. 前端 API 与路由

- [x] 4.1 运行 `./scripts/generate-openapi-client.sh`（Orval）
- [x] 4.2 `admin-nav.ts` 为「瓷砖类目」添加 `path: '/admin/tile-categories'`
- [x] 4.3 注册 `/admin/tile-categories` 路由与 `TileCategoryManagementPage`
- [x] 4.4 实现 `features/admin/api/tile-categories-api.ts`
- [x] 4.5 `DashboardQuickActions`「新增类目」导航至 `/admin/tile-categories`

## 5. CSS Port 与页面

- [x] 5.1 创建 `features/admin/styles/tile-category-management.css`（自 HTML V2 port）
- [x] 5.2 实现 `TileCategoryManagementPage`：header、指标卡、检索、work-grid
- [x] 5.3 实现 `CategoryTree`（280px、level 缩进、active、sku_count）
- [x] 5.4 实现列表表格、工具栏仅「调整排序」、分页（10/20/50）
- [x] 5.5 实现 `CategoryFormModal`（560px、单列六字段、Switch 状态）
- [x] 5.6 实现删除确认与删除入口条件展示逻辑
- [x] 5.7 实现启用/停用、Toast、「调整排序」占位 Toast

## 6. Design System 预览（可选）

- [ ] 6.1 `/design-system` 增加类目管理树+列表/弹窗预览片段（可选）

## 7. 前端测试

- [x] 7.1 vitest：删除入口矩阵、三级深度 parent 选项（`tile-categories-api.test.ts`）
- [x] 7.2 运行 `cd src/web && npx vitest run src/features/admin src/pages/admin`

## 8. 构建与部署

- [x] 8.1 `cd src/web && npm run build`
- [x] 8.2 `./scripts/docker-up.sh` 冒烟 `/admin/tile-categories`（Web 路由 200；登录后 UI 人工确认）

## 9. 视觉验收

- [x] 9.1 1280×1024 并排 `tile-category-management.html`：填写 `trace.md` 列表 checklist（≥15 项）
- [x] 9.2 并排 `tile-category-management-add.html`：填写弹窗 checklist（≥5 项）
- [ ] 9.3 PNG 补齐后升级 golden reference 并复验

## 10. 文档

- [x] 10.1 更新 `docs/03-api-index.md`、`docs/04-database-design.md`
- [x] 10.2 更新 `issues/requirements/archive/REQ-0005-tile-category-management/trace.md` change 状态
- [ ] 10.3 sprint acceptance-report（若纳入迭代）
