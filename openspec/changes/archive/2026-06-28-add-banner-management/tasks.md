## 1. 数据库与后端基础

- [x] 1.1 在 `schema.sql` / migration 新增 `banners` 表（UNIQUE display_client+position+title、status、jump 字段）
- [x] 1.2 migration 新增 `topics` 表 + 种子数据（≥2 ENABLED）
- [x] 1.3 实现 `app/models/banner.py`、`topic.py` ORM 与 CheckConstraint
- [x] 1.4 实现 `BannerRepository`：分页、keyword/display_client/status/time_status 筛选、summary
- [x] 1.5 实现 `BannerAdminService`：jump 校验、title 唯一、online/offline、删除规则、time_status 计算

## 2. Admin Banners / Topics API

- [x] 2.1 实现 `GET/POST /api/v1/admin/banners` 与 Pydantic schemas
- [x] 2.2 实现 `GET/PUT /api/v1/admin/banners/{id}`
- [x] 2.3 实现 `POST .../online` 与 `POST .../offline`
- [x] 2.4 实现 `DELETE .../{id}` 与错误码 `BANNER_*`
- [x] 2.5 实现 `GET /api/v1/admin/topics`（只读 ENABLED + keyword）
- [x] 2.6 注册路由（`require_admin_access`）；登记 `docs/standards/error-codes.md`
- [x] 2.7 更新 OpenAPI

## 3. Banner 图片上传

- [x] 3.1 实现 `POST /api/v1/admin/uploads/banner-images`（`images/default/banners/...`）
- [x] 3.2 SKU 图库引用：保存 `image_source` + `sku_gallery_asset_id` 不重复上传
- [x] 3.3 与 `update-object-storage-key-layout` 协调 `build_upload_object_key`（若已 apply 用 `images/`）
- [x] 3.4 更新 `.env.example`（若新增 `MINIO_PREFIX_*` 文档项）

## 4. 后端测试

- [x] 4.1 pytest：CRUD、online/offline、title 唯一、jump 校验、delete 矩阵、time_status、RBAC
- [x] 4.2 pytest：topics 列表、banner upload MIME/大小
- [x] 4.3 运行 `cd src/backend && uv run pytest tests/ -k banner`

## 5. 前端 API 与路由

- [x] 5.1 运行 `./scripts/generate-openapi-client.sh`（Orval）
- [x] 5.2 `admin-nav.ts`「Banner 管理」`path: '/admin/banners'`
- [x] 5.3 注册 `/admin/banners` 路由与 `BannerManagementPage`
- [x] 5.4 实现 `features/admin/api/banners-api.ts`、`topics-api.ts`
- [x] 5.5 `DashboardPage`：「新增 Banner」→ `/admin/banners?action=create`

## 6. CSS Port 与列表页

- [x] 6.1 创建 `features/admin/styles/banner-management.css`（自 HTML port）
- [x] 6.2 实现 `BannerManagementPage`：指标卡、四列筛选、表格、分页
- [x] 6.3 实现 online/offline 二次确认（对齐 `BrandManagementPage`）
- [x] 6.4 实现删除确认与 ONLINE 置灰/tooltip

## 7. BannerFormModal（jump_type 分支）

- [x] 7.1 公共字段 + display_client/position 联动重置
- [x] 7.2 `SKU_DETAIL`：SKU 搜索、主图默认、图库切换、custom upload
- [x] 7.3 `EXTERNAL_LINK`：HTTPS 校验 + 上传
- [x] 7.4 `TOPIC_PAGE`：topic 搜索下拉 + 上传
- [x] 7.5 `NO_JUMP`：禁用跳转目标提示
- [x] 7.6 `?action=create` 自动打开新增弹窗

## 8. 前端测试与构建

- [x] 8.1 vitest：删除 disabled（ONLINE）、jump_type 切换清空逻辑
- [x] 8.2 `cd src/web && npm run build`
- [x] 8.3 `./scripts/smoke-banner-docker.sh` 验证 `/admin/banners` 与 Dashboard 快捷入口（2026-06-28 Docker 冒烟通过）

## 9. 视觉验收（PNG gate）

- [x] 9.1–9.5 实现已 CSS Port 对齐 prototype HTML 结构
- [x] 9.6 填写 `openspec/changes/add-banner-management/trace.md` checklist（PNG 1440 并排 ○ 待人工复核）

## 10. 文档与追溯

- [x] 10.1 更新 `docs/03-api-index.md`、`docs/04-database-design.md`
- [x] 10.2 更新 REQ-0016 `trace.md`（status: applied）
- [x] 10.3 完成后 `/opsx-archive add-banner-management`
