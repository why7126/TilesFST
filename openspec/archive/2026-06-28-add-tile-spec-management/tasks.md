## 1. 数据库与后端基础

- [x] 1.1 在 `schema.sql` / migration 新增 `tile_specs` 表（UNIQUE width/length/unit、status、sku_count）
- [x] 1.2 migration 为 `tiles` 新增 `spec_id` FK（可 NULL）
- [x] 1.3 实现 `app/models/tile_spec.py` ORM 与 CheckConstraint
- [x] 1.4 实现 `TileSpecRepository`：分页、keyword/status 筛选、summary、CRUD
- [x] 1.5 实现 `TileSpecAdminService`：display_name 生成、唯一性、删除规则、启停、sku_count

## 2. Admin Tile Specs API

- [x] 2.1 实现 `GET/POST /api/v1/admin/tile-specs` 与 Pydantic schemas
- [x] 2.2 实现 `GET/PUT /api/v1/admin/tile-specs/{id}`
- [x] 2.3 实现 `POST .../enable` 与 `POST .../disable`
- [x] 2.4 实现 `DELETE .../{id}` 与错误码 `TILE_SPEC_*`
- [x] 2.5 注册路由（`require_admin_access`）；登记 `docs/standards/error-codes.md`
- [x] 2.6 更新 OpenAPI

## 3. SKU 联动与迁移

- [x] 3.1 扩展 SKU create/update schemas 与 service：`spec_id`、size 同步、ENABLED 校验
- [x] 3.2 publish 校验 `spec_id` 非空
- [x] 3.3 维护 `tile_specs.sku_count`（create/update/delete SKU）
- [x] 3.4 实现 migration 脚本：匹配 `tiles.size` → `spec_id`（dry-run + apply）
- [x] 3.5 更新 `docs/04-database-design.md`

## 4. 后端测试

- [x] 4.1 pytest：spec CRUD、启停、重复、删除矩阵、summary、RBAC
- [x] 4.2 pytest：SKU spec_id 联动、publish、sku_count、迁移匹配
- [x] 4.3 运行 `cd src/backend && uv run pytest tests/ -k tile_spec`

## 5. 前端 API 与路由

- [x] 5.1 运行 `./scripts/generate-openapi-client.sh`（Orval）
- [x] 5.2 `admin-nav.ts` 新增「瓷砖规格」`path: '/admin/tile-specs'`
- [x] 5.3 注册 `/admin/tile-specs` 路由与 `TileSpecManagementPage`
- [x] 5.4 实现 `features/admin/api/tile-specs-api.ts`

## 6. CSS Port 与规格页

- [x] 6.1 创建 `features/admin/styles/tile-spec-management.css`（自 HTML port）
- [x] 6.2 实现 `TileSpecManagementPage`：指标卡、状态筛选、表格、分页
- [x] 6.3 实现 `TileSpecFormModal`（720px、实时 display_name、重复校验）
- [x] 6.4 实现启停二次确认（对齐 `BrandManagementPage`）
- [x] 6.5 实现删除确认与置灰/tooltip 逻辑

## 7. SKU 表单改造

- [x] 7.1 `TileSkuFormModal`：规格 `<select>` 加载 ENABLED 规格
- [x] 7.2 提交 `spec_id`；迁移失败 SKU 提示选手动规格
- [x] 7.3 vitest：规格必选校验（create 模式）

## 8. 前端测试与构建

- [x] 8.1 vitest：规格删除按钮 disabled 矩阵
- [x] 8.2 `cd src/web && npm run build`
- [x] 8.3 `./scripts/smoke-tile-spec-docker.sh` 验证 `/admin/tile-specs` 与 SKU 下拉

## 9. 视觉验收（HTML gate；PNG 待导出）

- [x] 9.1 1440×1024 并排 `/admin/tile-specs` 与 `tile-size-management.html`（HTML gate vitest #1–6）
- [x] 9.2 并排新增/编辑弹窗与 `tile-size-management-modal.html`（HTML gate vitest #7–9）
- [x] 9.3 导出 `tile-size-management.png` / `modal.png` Golden Reference（prototype/web 已存在；vitest #12）
- [x] 9.4 填写 `openspec/changes/add-tile-spec-management/trace.md` checklist

## 10. 文档与追溯

- [x] 10.1 更新 `docs/03-api-index.md`
- [x] 10.2 更新 REQ-0009 `trace.md`（status: applied）
- [x] 10.3 migration dry-run 步骤写入 release note
- [x] 10.4 完成后 `/opsx-archive add-tile-spec-management`
