---
change_id: fix-miniapp-sku-detail-media-thumbnails
status: applied
created_at: 2026-08-07 22:55:00
updated_at: 2026-08-07 23:24:00
---

# 任务清单

- [x] 1. 后端修复 SKU 详情媒体 URL 语义
  - [x] 1.1 图片媒体首屏展示 URL 优先使用同目录 `.thumb`
  - [x] 1.2 图片预览 URL 保留原图
  - [x] 1.3 视频 `cover_url` 优先使用主图缩略图，视频 `url` 保持原视频
  - [x] 1.4 分享图与兜底主图不暴露 object key 或未授权对象存储路径
- [x] 2. 小程序详情页修复首屏媒体渲染
  - [x] 2.1 首屏图片使用展示 URL
  - [x] 2.2 图片预览继续使用原图 URL
  - [x] 2.3 视频封面使用 `cover_url || product.cover_image || imageFallback`
- [x] 3. 测试同步
  - [x] 3.1 更新 `tests/test_miniapp_home.py` SKU 详情媒体断言
  - [x] 3.2 更新 `tests/test_miniapp_static.py` 详情页媒体字段绑定断言
  - [x] 3.3 覆盖现有首页、商品列表、搜索结果、Banner 和推荐卡片缩略图不回退
- [x] 4. 文档与验收同步
  - [x] 4.1 更新 `docs/03-api-index.md` SKU 详情媒体字段语义
  - [x] 4.2 回填 BUG-0125 acceptance 的媒体四联 evidence
  - [x] 4.3 必要时补充 `docs/knowledge-base/incidents/` 经验，不复制完整 BUG 文档
- [x] 5. 校验
  - [x] 5.1 运行相关 pytest 和小程序静态测试
  - [x] 5.2 运行 `python scripts/validate-openspec-language.py`
  - [x] 5.3 运行 OpenSpec 校验

## 校验记录

- 2026-08-07：`uv run pytest tests/test_miniapp_home.py::test_miniapp_sku_detail_returns_public_media_recommendations_and_share tests/test_miniapp_static.py::test_miniapp_sku_detail_page_covers_media_favorite_share_and_empty_states` 通过。
- 2026-08-07：`uv run pytest tests/test_miniapp_home.py tests/test_miniapp_static.py` 中 BUG-0125 相关断言通过；存在既有非本 Change 失败 `test_miniapp_product_list_brand_default_sort_uses_published_at_and_id`，该失败与 SKU 详情媒体 URL 语义无关。
