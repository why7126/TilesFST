## 1. 数据库与后端基础

- [ ] 1.1 在 `schema.sql` 新增 `brands` 表（name UNIQUE、sort_order、status、sku_count 等）
- [ ] 1.2 实现 `app/models/brand.py` ORM 与 CheckConstraint
- [ ] 1.3 实现品牌校验（名称长度、排序正整数、名称唯一）
- [ ] 1.4 实现 `BrandRepository`：分页列表、keyword/status 筛选、summary、CRUD
- [ ] 1.5 实现 `BrandAdminService`：删除规则（sku_count=0 且 DISABLED）、启停

## 2. Admin Brands API

- [ ] 2.1 实现 `GET/POST /api/v1/admin/brands` 与 Pydantic schemas
- [ ] 2.2 实现 `GET/PUT /api/v1/admin/brands/{id}`
- [ ] 2.3 实现 `POST .../enable` 与 `POST .../disable`
- [ ] 2.4 实现 `DELETE .../{id}` 与错误码 `BRAND_DELETE_FORBIDDEN`、`BRAND_NAME_DUPLICATED`
- [ ] 2.5 注册路由（`require_admin_user`）；更新 OpenAPI
- [ ] 2.6 扩展 Logo 上传（`brands/logos` 前缀 + MIME 校验）

## 3. 后端测试

- [ ] 3.1 pytest：CRUD、筛选 summary、名称重复、删除矩阵、enable/disable、employee 可访问、store_owner 403
- [ ] 3.2 运行 `cd src/backend && uv run pytest tests/ -k brand`

## 4. 前端 API 与路由

- [ ] 4.1 运行 `./scripts/generate-openapi-client.sh`（Orval）
- [ ] 4.2 `admin-nav.ts` 为「瓷砖品牌」添加 `path: '/admin/brands'`
- [ ] 4.3 注册 `/admin/brands` 路由与 `BrandManagementPage`
- [ ] 4.4 实现 `features/admin/api/brands-api.ts`
- [ ] 4.5 `DashboardQuickActions`「新增品牌」导航至 `/admin/brands`

## 5. CSS Port 与页面

- [ ] 5.1 创建 `features/admin/styles/brand-management.css`（自 HTML V7 port）
- [ ] 5.2 实现 `BrandManagementPage`：header、指标卡、筛选、表格、分页（含 page_size）
- [ ] 5.3 实现 `BrandFormModal`（720px、字段顺序、校验、Logo 上传）
- [ ] 5.4 实现删除确认弹窗与删除按钮禁用/tooltip 逻辑
- [ ] 5.5 实现启用/停用、Toast 反馈、列表刷新

## 6. Design System 预览（可选）

- [ ] 6.1 `/design-system` 增加品牌管理列表/弹窗预览片段（可选）

## 7. 前端测试

- [ ] 7.1 vitest：删除按钮四态矩阵、弹窗字段顺序、page_size 重置页码
- [ ] 7.2 运行 `cd src/web && npx vitest run src/features/admin src/pages/admin`

## 8. 构建与部署

- [ ] 8.1 `cd src/web && npm run build`
- [ ] 8.2 `./scripts/docker-up.sh` 验证 `/admin/brands`（admin/employee 登录）

## 9. 视觉验收（HTML / PNG Golden Reference Gate）

- [ ] 9.1 1280×1024 并排 `/admin/brands` 与 `brand-management.html`（PNG 补齐后升级为 PNG gate）
- [ ] 9.2 打开新增/编辑弹窗并排 `brand-management-modal.html`
- [ ] 9.3 填写 `openspec/changes/add-brand-management/trace.md` checklist

## 10. 文档与追溯

- [ ] 10.1 更新 `docs/03-api-index.md`、`docs/04-database-design.md`
- [ ] 10.2 更新 `issues/requirements/REQ-0005-brand-management/trace.md`（status: applied）
- [ ] 10.3 建议导出 `prototype/web/brand-management.png` 与 `brand-management-modal.png`
- [ ] 10.4 完成后 `/opsx-archive add-brand-management`
