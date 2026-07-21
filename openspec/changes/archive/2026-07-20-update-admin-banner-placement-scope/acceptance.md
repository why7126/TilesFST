---
change_id: update-admin-banner-placement-scope
status: applied
created_at: 2026-07-20 18:55:00
updated_at: 2026-07-20 22:51:30
---

# Acceptance

本文件引用 `issues/requirements/archive/REQ-0062-admin-banner-placement-scope/acceptance.md`。实现阶段必须逐项核对：

- 功能 AC：AC-001 至 AC-020
- API / DB / Orval AC：AC-API-001 至 AC-TEST-004
- UI / UE AC：AC-UI-001 至 AC-UI-005
- 横切 AC：AC-XCUT-001 至 AC-XCUT-010

## Change 级验收摘要

- [x] Banner 管理展示端仅为“小程序”，展示位置仅为“首页轮播”和“品牌列表页轮播”。
- [x] 旧 Banner 数据按策略删除，列表、summary、分页不再包含旧数据。
- [x] 小程序首页和品牌列表页轮播查询完全隔离。
- [x] Banner 跳转类型支持“品牌详情”，管理端选择品牌后可按品牌 Logo 取图，小程序可跳转品牌详情页。
- [x] API、DB、OpenAPI、Orval、docs 和测试同步完成。
- [x] 管理端列表、弹窗和上传横切 AC 通过。

## Evidence

- `openspec/changes/archive/2026-07-20-update-admin-banner-placement-scope/implementation.md`
- `uv run pytest src/backend/tests/test_admin_banners.py tests/test_miniapp_home.py`
- `pnpm --dir src/web exec vitest run src/features/admin/components/BannerFormModal.test.tsx`
- `pnpm --dir src/web exec vitest run src/features/admin/lib/banner-display.test.ts src/pages/admin/BannerManagementPage.test.tsx`
- `bash -n scripts/smoke-banner-docker.sh`
- `./scripts/generate-openapi-client.sh`
