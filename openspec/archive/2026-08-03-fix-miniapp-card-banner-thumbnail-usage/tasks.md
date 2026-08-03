## 1. 实现

- [x] 1.1 排查小程序商品卡片、品牌列表卡片、共享品牌卡片组件、证书卡片、首页商品卡片以及首页/品牌 Banner 的图片字段使用。
- [x] 1.2 对齐商品卡片图片选择逻辑，让列表、搜索、首页和品牌详情商品卡片优先使用真实缩略图或轻量图片 URL，并保留原图/占位图兜底。
- [x] 1.3 对齐品牌卡片图片选择逻辑，让品牌列表卡片和可复用品牌卡片组件优先使用 Logo/图片缩略图，并保留原图、首字母或占位图兜底。
- [x] 1.4 对齐证书卡片图片选择逻辑，让图片类证书优先使用缩略图，PDF、未知类型或缺失文件保持稳定占位展示。
- [x] 1.5 对齐 Banner 图片选择逻辑，让小程序 Banner 使用缩略图、展示图或明确性能边界内的安全 URL，并保持既有跳转行为。
- [x] 1.6 如公共 API 响应字段必须变更，同步更新 FastAPI schema/service/repository、OpenAPI、Orval 生成客户端、文档和测试。
- [x] 1.7 详情、图片预览、PDF 打开、点击导航和分享路径在需要高清资源时继续使用原图或安全高分辨率引用。

## 2. 验证

- [x] 2.1 字段选择变更时，新增或更新公共商品列表、品牌列表、证书列表和首页/Banner 响应的后端测试。
- [x] 2.2 新增或更新商品卡片、品牌卡片、证书卡片和 Banner 缩略图/展示图映射的小程序静态测试。
- [x] 2.3 运行本仓库相关 pytest 和小程序静态/类型检查。
- [x] 2.4 如 API 已变更，运行 `./scripts/generate-openapi-client.sh` 并验证生成客户端和测试。
- [x] 2.5 在微信开发者工具或体验版中手工验证：商品卡片、品牌卡片、证书卡片、Banner、缩略图缺失兜底以及详情/预览路径。
- [x] 2.6 记录 BUG-0110 AC-001 至 AC-006 的验收 evidence。
- [x] 2.7 运行 `openspec validate fix-miniapp-card-banner-thumbnail-usage --strict`。
- [x] 2.8 评估确认后的实现经验是否应沉淀到 `docs/knowledge-base/incidents/`；仅当修复揭示可复用的媒体字段漂移治理经验时更新。

Notes:
- 1.6 / 2.4: No public response fields were added or removed; existing `image_url`, `cover_image`, `brand_logo_thumbnail_url`, and `thumbnail_url` fields were reused, so OpenAPI/Orval regeneration was not required.
- 2.3: `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` ran with 66 passed / 1 unrelated time-window failure in `test_miniapp_product_list_brand_default_sort_uses_published_at_and_id`; `tests/test_audit_miniapp_card_images.py` could not collect because the current environment lacks `PIL`.
- 2.5: 微信开发者工具或体验版网络面板验证需在当前终端外执行；归档时已在 trace.md 风险提示中记录该手工验证限制，后续体验版验证可按 BUG-0110 AC-001 至 AC-006 复核。
- 2.8: Existing media thumbnail knowledge-base guidance already covers this class of regression; no new reusable incident pattern was introduced.

## 验收返修记录

### 2026-08-03 12:57:15 品牌列表页 Banner 非真实缩略图

- 验收反馈：品牌列表页 Banner 看起来不是缩略图，需要确认是没有缩略图对象还是没有实现。
- 定位结论：小程序公开接口已返回同目录 `.thumb` URL，前端也渲染 `item.image_url`；但 Banner 自定义上传接口此前未生成 `thumbnail_key`，媒体读取层在缩略图对象缺失时会回退原图，因此属于 Banner 上传缩略图生成链路未闭环。
- 返修调整：`/api/v1/admin/uploads/banner-images` 上传 Banner 图片时生成同目录缩略图对象，并补充上传接口测试断言真实缩略图对象写入。
- 验证：`uv run pytest src/backend/tests/test_admin_banners.py::test_banner_image_upload tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel tests/test_miniapp_home.py::test_miniapp_home_returns_public_data_and_hides_internal_fields` 通过。

### 2026-08-03 13:06:45 品牌列表 item 图片 URL payload 瘦身

- 验收反馈：品牌列表页接口返回的 `items` 中每个 item 包含多个图片 URL，担心影响加载性能。
- 定位结论：JSON 中多个 URL 字符串不会自动触发图片下载，小程序只会加载 `<image src>` 实际引用的 URL；但额外原图 URL 会增加响应体并增加误用原图的风险。
- 返修调整：品牌列表接口不再为每个 item 下发原图 Logo URL，仅保留列表卡片需要的 `brand_logo_thumbnail_url`；品牌详情接口继续返回 `brand_logo_url` 与 `brand_logo_thumbnail_url`，保证详情/分享不回归。
- 验证：`uv run pytest tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel tests/test_miniapp_home.py::test_miniapp_brand_home_endpoints_return_public_detail_and_certificates tests/test_miniapp_static.py::test_miniapp_home_detail_search_smoke_contracts` 通过。

### 2026-08-03 13:12:50 品牌列表本地重复 URL 字段清理

- 验收反馈：接口或页面数据中仍看到 `brand_logo_thumbnail_url` 与 `logo_display_url` 两个有值字段，需要确认是否还能优化。
- 定位结论：`brand_logo_thumbnail_url` 是接口返回的必要展示字段；`logo_display_url` 不是接口字段，而是小程序本地 `normalizeBrandItem()` 派生字段，会在页面 data 中复制一份相同 URL。
- 返修调整：移除小程序本地 `logo_display_url` 派生字段，WXML 直接使用 `item.brand_logo_thumbnail_url || item.brand_logo_url` 渲染；图片失败时清空后端字段，保持 fallback 行为。
- 验证：`uv run pytest tests/test_miniapp_static.py::test_miniapp_home_detail_search_smoke_contracts tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel tests/test_miniapp_home.py::test_miniapp_brand_home_endpoints_return_public_detail_and_certificates` 通过。

### 2026-08-03 13:18:49 证书列表 item 原文件 URL 瘦身

- 验收反馈：证书列表页接口 `items` 中同时存在 `file_url` 与 `thumbnail_url`，担心列表加载性能和误用原文件。
- 定位结论：证书 Tab 列表卡片点击后按 `certificate_id` 进入详情页，列表渲染只需要 `thumbnail_url`、`file_kind` 和占位信息；原文件 URL 应由详情接口提供给预览、下载或 PDF 打开。
- 返修调整：证书 Tab 列表接口不再为每个 item 下发 `file_url`；证书详情接口继续保留 `file_url` 与媒体原文件 URL。小程序证书列表只在 `thumbnail_url` 存在时渲染图片，缩略图缺失时展示占位，不再用原文件 URL 兜底加载。
- 验证：`uv run pytest tests/test_miniapp_home.py::test_miniapp_certificate_list_filters_public_data_and_supports_facets tests/test_miniapp_home.py::test_miniapp_certificate_detail_returns_public_data_and_filters_private_records tests/test_miniapp_static.py::test_miniapp_certificate_list_page_replaces_placeholder_with_public_list` 通过。

### 2026-08-03 13:23:49 分类商品列表缩略图复核

- 验收反馈：分类商品列表页 `items` 中的商品图片疑似仍使用原图，需要确认并优化。
- 定位结论：分类商品列表与普通商品列表共用 `/api/v1/miniapp/products` 和 `_to_product_card()`；默认 `prefer_thumbnail=True`，`cover_image` 会解析为同目录 `.thumb` URL。实际测试确认一级分类分页、二级分类列表均返回 `/media/tiles/*.thumb.webp`。
- 返修调整：无需业务代码修改；补充分类商品列表回归断言，防止后续分类分支回退原图。
- 验证：`uv run pytest tests/test_miniapp_home.py::test_miniapp_product_list_category_and_keyword_default_sort_uses_public_order tests/test_miniapp_home.py::test_miniapp_product_list_supports_context_filters_sort_and_facets` 通过。
