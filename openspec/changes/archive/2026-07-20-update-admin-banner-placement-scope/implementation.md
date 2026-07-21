---
change_id: update-admin-banner-placement-scope
status: applied
created_at: 2026-07-20 19:30:00
updated_at: 2026-07-20 22:51:30
---

# Implementation Notes

## Enum Decision

展示端继续使用兼容存储值 `MINIAPP_HOME`，管理端统一显示为“小程序”。展示位置仅保留：

- `MINIAPP_HOME_CAROUSEL`：首页轮播
- `MINIAPP_BRAND_LIST_CAROUSEL`：品牌列表页轮播

后端保存校验、管理端选项、SQLite/MySQL schema、OpenAPI/Orval 生成类型和小程序公开查询均按该范围收敛。

## Jump Type Extension

补充支持 `BRAND_DETAIL` 跳转类型。`banners.brand_id` 保存品牌详情目标，后端校验品牌必须存在且 `status=ENABLED`，且不能同时携带 `sku_id`、`topic_id` 或 `external_url`。图片来源新增 `brand_logo`，语义与 `sku_main_image` 对齐：当使用品牌 Logo 时，`image_object_key` 必须等于品牌 `logo_object_key`；也允许运营自定义上传 Banner 图。

小程序公开响应将 `BRAND_DETAIL` 映射为 `jump_type=brand` 与 `target_id=brand_id`。首页和品牌列表页轮播点击 `brand` 时进入 `pages/brand-detail/index?brandId=...`。

## Legacy Cleanup

SQLite 迁移清理函数：`src/backend/app/db/migrations.py::_cleanup_legacy_banner_scope`

删除条件：

```sql
display_client != 'MINIAPP_HOME'
OR position NOT IN ('MINIAPP_HOME_CAROUSEL', 'MINIAPP_BRAND_LIST_CAROUSEL')
```

删除数量由函数返回值和应用日志记录；测试覆盖旧库中 2 条旧范围 Banner 被删除、1 条有效小程序 Banner 被保留。

## Media Boundary

清理逻辑只执行 `DELETE FROM banners`，不访问 MinIO、不删除 `/media` 对象，也不修改其他业务表中的媒体引用。旧 Banner 业务记录如需恢复，依赖生产执行前数据库备份或导出恢复。

## Validation Evidence

- `uv run pytest src/backend/tests/test_admin_banners.py tests/test_miniapp_home.py`：45 passed
- `pnpm --dir src/web exec vitest run src/features/admin/components/BannerFormModal.test.tsx`：1 file / 6 tests passed
- `pnpm --dir src/web exec vitest run src/features/admin/lib/banner-display.test.ts src/pages/admin/BannerManagementPage.test.tsx`：2 files / 8 tests passed
- `bash -n scripts/smoke-banner-docker.sh`：passed
- `./scripts/generate-openapi-client.sh`：OpenAPI 与 Orval 已重新生成

Docker Web `:3000` 上传边界已补入 `scripts/smoke-banner-docker.sh`，需在容器环境运行该脚本取得人工/环境 evidence。
