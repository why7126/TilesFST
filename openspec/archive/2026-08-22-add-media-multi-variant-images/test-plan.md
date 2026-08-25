---
change_id: add-media-multi-variant-images
status: applied
created_at: 2026-08-22 14:33:52
updated_at: 2026-08-22 17:33:29
source_requirement: REQ-0115-media-multi-variant-images
source_sprint: sprint-025
---

# 测试记录

## 已通过

| 命令 | 结果 |
|---|---|
| `uv run --project src/backend python -m pytest tests/test_media_storage.py tests/test_deploy_media_maintenance_script.py` | 31 passed |
| `uv run --project src/backend python -m pytest tests/test_miniapp_home.py::test_miniapp_sku_detail_returns_public_media_recommendations_and_share tests/test_miniapp_static.py::test_miniapp_product_card_component_contract_and_reuse tests/test_miniapp_static.py::test_miniapp_sku_detail_page_covers_media_favorite_share_and_empty_states` | 3 passed |
| `pnpm --dir src/web --pm-on-fail=ignore test -- --run src/features/admin/components/TileSkuFormModal.test.tsx` | 62 files / 359 tests passed |
| `python -m py_compile src/backend/app/core/config.py src/backend/app/modules/media/storage.py src/backend/app/modules/media/tile_images.py src/backend/app/modules/media/maintenance.py src/backend/app/api/v1/uploads.py src/backend/app/services/tile_sku_admin_service.py src/backend/app/services/miniapp_home_service.py src/backend/app/schemas/media.py src/backend/app/schemas/tile_sku_admin.py src/backend/app/schemas/miniapp_home.py` | pass |
| `./scripts/generate-openapi-client.sh` | pass，已更新 `src/web/openapi.json` 和 `src/web/src/shared/api/generated.ts` |
| `uv run --project src/backend python -m pytest tests/test_miniapp_static.py::test_miniapp_sku_detail_page_covers_media_favorite_share_and_empty_states` | 1 passed；覆盖验收返修后的 media 下标预览与 `original_url || preview_url || url` 优先级静态断言 |

## 已知阻塞

`pnpm --dir src/web --pm-on-fail=ignore exec tsc --noEmit --ignoreDeprecations 6.0` 被既有/旁支类型问题阻塞：

- `src/features/admin/components/BrandCertificateComponents.test.tsx` 的证书 mock 字段与当前生成类型不一致。
- `src/features/auth/store/auth-store.ts` 将普通字符串赋给 `UserProfileThemeMode` 枚举类型。

这些错误不在本 Change 的 SKU 图片多规格改动面内；本 Change 通过 Web 测试集和后端聚焦测试覆盖主要行为。

`uv run python -m app.modules.media.maintenance backfill-image-variants --limit 5` 在本机 dry-run 时被对象存储环境阻塞：Docker 默认 endpoint `tilesfst-minio:9000` 在当前宿主机不可解析。该命令未写数据库或对象存储，真实 dry-run/apply 需在 Docker self-hosted-storage 或生产等价对象存储可达环境补证。

## 验收返修测试

- 小程序 SKU 详情 `previewImage` 静态测试已锁定：点击节点提供 `data-media-index="{{index}}"`；TS/JS 均存在 `previewUrlForMedia`；`current` 与 `urls` 均从同一 media-index 映射链路生成；预览 URL 优先级固定为 `original_url || preview_url || url`。
- 复验证据显示 DevTools Network 仍只出现 `.thumb.png` 与 `.display.png`；第二次返修新增 `wx.getImageInfo({ src: current })`，用于在调用 `wx.previewImage` 前显式请求当前 original URL，提升端侧 Network evidence 可观测性。
- 端侧 Network 二次复验：用户提供的微信 DevTools 截图显示 SKU 377 点击图片预览后，同一对象名下已出现 `.thumb.png`、`.display.png` 和原图 `.png` 请求；`AC-MINIAPP-003` 的 DevTools evidence 已满足。
