---
created_at: 2026-08-03 13:35:00
updated_at: 2026-08-03 13:35:00
---

# Trace - fix-miniapp-card-banner-thumbnail-usage

## 关联对象

- Issue: BUG-0110-miniapp-card-banner-thumbnail-usage
- Sprint: sprint-018
- Change: fix-miniapp-card-banner-thumbnail-usage
- 归档路径: openspec/archive/2026-08-03-fix-miniapp-card-banner-thumbnail-usage
- 归档时间: 2026-08-03 13:35:00

## 实现摘要

- 小程序首页、品牌列表、品牌卡片、证书列表、分类商品列表等卡片场景优先使用缩略图或轻量展示图。
- Banner 上传链路补齐缩略图生成，避免列表或首页 Banner 因缺少缩略图对象回退原图。
- 品牌列表接口瘦身，不再在列表 item 下发原图 Logo URL；详情接口保留高清原图能力。
- 小程序品牌列表移除本地 `logo_display_url` 派生字段，避免重复 URL 进入页面 data。
- 证书列表接口瘦身，不再在列表 item 下发 `file_url`；详情接口保留原文件 URL 用于预览和下载。
- 分类商品列表经测试确认返回 `.thumb.webp`，并补充回归断言。

## 验证命令与验证结果

- `uv run pytest src/backend/tests/test_admin_banners.py::test_banner_image_upload tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel tests/test_miniapp_home.py::test_miniapp_home_returns_public_data_and_hides_internal_fields` 通过。
- `uv run pytest tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel tests/test_miniapp_home.py::test_miniapp_brand_home_endpoints_return_public_detail_and_certificates tests/test_miniapp_static.py::test_miniapp_home_detail_search_smoke_contracts` 通过。
- `uv run pytest tests/test_miniapp_static.py::test_miniapp_home_detail_search_smoke_contracts tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel tests/test_miniapp_home.py::test_miniapp_brand_home_endpoints_return_public_detail_and_certificates` 通过。
- `uv run pytest tests/test_miniapp_home.py::test_miniapp_certificate_list_filters_public_data_and_supports_facets tests/test_miniapp_home.py::test_miniapp_certificate_detail_returns_public_data_and_filters_private_records tests/test_miniapp_static.py::test_miniapp_certificate_list_page_replaces_placeholder_with_public_list` 通过。
- `uv run pytest tests/test_miniapp_home.py::test_miniapp_product_list_category_and_keyword_default_sort_uses_public_order tests/test_miniapp_home.py::test_miniapp_product_list_supports_context_filters_sort_and_facets` 通过。
- `openspec validate fix-miniapp-card-banner-thumbnail-usage --strict` 通过。
- `python scripts/validate-openspec-language.py` 通过。

## 验收结论

- BUG-0110 的代码修复、接口瘦身和回归测试已完成。
- 本次 `/opsx-archive BUG-0110` 由用户发起，作为归档授权继续执行。
- 风险提示：微信开发者工具或体验版中的网络面板手工验证未在当前终端环境执行；归档记录保留该警告。

## 归档证据

- OpenSpec CLI 已将 Change 合并到正式规格并归档到 `openspec/archive/2026-08-03-fix-miniapp-card-banner-thumbnail-usage`。
- 相关 issue 与 sprint 状态将在归档后通过 workflow sync 和 promote 脚本继续同步。
