---
change_id: add-miniapp-sku-detail-page
created_at: 2026-07-18 19:54:32
updated_at: 2026-07-18 19:54:32
---

# 实现与验收证据

## 数据盘点

- 复用 `tiles`、`brands`、`tile_categories`、`tile_specs`、`tile_images`、`tile_videos` 支撑 SKU 主体、品牌、类目、规格、图片和视频。
- 新增 `miniapp_sku_favorites` 存储 SKU 粒度收藏状态；不新增公开状态字段，公开性继续以 `tiles.status = PUBLISHED` 判定。
- 后台 `tiles.remark` 当前按内部备注处理，SKU 详情接口不直接公开该字段，避免泄露内部维护信息。

## API / DB / Orval

- 新增 `GET /api/v1/miniapp/skus/{sku_id}` 返回 SKU 主体、媒体、品牌、收藏状态、同系列推荐、同品牌推荐和分享数据。
- 新增 `PUT /api/v1/miniapp/skus/{sku_id}/favorite`，通过 `(client_id, sku_id)` 唯一约束实现幂等收藏/取消收藏。
- 同步 `src/backend/app/db/schema.sql`、`src/backend/app/db/schema.mysql.sql`、`src/backend/app/db/migrations.py`、`docs/03-api-index.md`、`docs/04-database-design.md`、`src/web/openapi.json` 和 `src/web/src/shared/api/generated.ts`。

## 小程序验收

- `src/miniapp/pages/tile-detail/` 覆盖骨架屏、错误态、图片/视频混合轮播、图片预览、视频主动播放与隐藏暂停、品牌卡、参数、备注空态、同系列/同品牌推荐、收藏回滚、分享和底部安全区操作栏。
- 页面样式延续首页 v6 深色企业轻奢风，核心点击目标使用 `min-height: 88rpx`，底部栏使用 `env(safe-area-inset-bottom)`。
- 320 到 430px 逻辑宽度验收依据：`tests/test_miniapp_static.py::test_miniapp_sku_detail_page_covers_media_favorite_share_and_empty_states` 与 `test_miniapp_styles_keep_primary_tappable_targets_at_least_44pt` 覆盖结构、底部安全区、44x44px 等效点击目标和范围外能力未出现；原型 PNG 仍位于 `issues/requirements/archive/REQ-0044-miniapp-sku-detail-page/prototype/miniapp/`。

## 测试结果

- `openspec validate add-miniapp-sku-detail-page --strict`：PASS。
- `uv run pytest tests/test_miniapp_home.py tests/test_miniapp_static.py`：22 passed，3 warnings（Pydantic class config 与 FastAPI startup on_event 既有弃用警告）。
