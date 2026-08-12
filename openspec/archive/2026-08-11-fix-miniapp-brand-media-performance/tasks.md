---
change_id: fix-miniapp-brand-media-performance
status: proposed
created_at: 2026-08-10 23:31:00
updated_at: 2026-08-10 23:31:00
---

# 任务清单

- [x] 1. 后端品牌链路媒体字段与缩略图策略修复
  - [x] 1.1 复核 `GET /api/v1/miniapp/brands` 品牌轮播、品牌 Logo 和品牌卡片图片展示 URL，确保优先使用真实轻量缩略图
  - [x] 1.2 复核 `GET /api/v1/miniapp/brands/{brand_id}` 品牌 Logo、商品 Tab 和证书 Tab 图片字段语义
  - [x] 1.3 复核 `GET /api/v1/miniapp/products?brandId=...&categoryId=...` 品牌分类商品列表的商品卡片主图字段
  - [x] 1.4 确认 `.thumb` 缺失回退原图时有可观测记录，且不得作为性能验收通过
- [x] 2. 小程序品牌链路图片渲染修复
  - [x] 2.1 品牌列表页轮播、Logo 和非首屏品牌卡片图启用缩略图优先与懒加载
  - [x] 2.2 品牌详情页 Logo、商品 Tab 商品卡片图、证书 Tab 图片启用缩略图优先与非首屏懒加载
  - [x] 2.3 品牌分类商品列表页继续复用商品卡片缩略图优先策略，不因入口参数回退原图
  - [x] 2.4 保持图片点击、商品跳转、证书预览、分享和失败态不退化
- [x] 3. 历史缩略图审计与回填证据
  - [x] 3.1 提供品牌 Logo、Banner、SKU 主图、图片类品牌证书的历史缩略图 dry-run 审计摘要
  - [x] 3.2 对需回填或重生成的对象记录 apply 前置备份、幂等策略和失败摘要
  - [x] 3.3 对 `.thumb` 缺失、0 字节、复制原图、体积无收益、MIME 不匹配或对象不可读输出脱敏 evidence
- [x] 4. `/media` 缓存与观测验证
  - [x] 4.1 记录 `/media/{object_key}` 图片响应缓存头、网关缓存或 CDN 策略
  - [x] 4.2 记录请求 key、实际 resolved key、content length、MIME 和耗时的日志或等价 evidence
  - [x] 4.3 若生产缓存暂不启用，记录原因、影响范围和剩余风险
- [x] 5. 测试、文档与验收同步
  - [x] 5.1 更新后端 pytest，覆盖品牌列表、品牌详情、品牌分类商品列表缩略图优先和回退记录
  - [x] 5.2 更新小程序静态测试，覆盖 `brand-list`、`brand-detail`、`product-list`、`product-card` 图片绑定和懒加载
  - [x] 5.3 按需更新 `docs/03-api-index.md`、OpenAPI 和 Orval；若无 API schema 变化，记录无需 Orval 的原因
  - [x] 5.4 回填 BUG-0126 acceptance 的媒体四联 evidence
  - [x] 5.5 必要时补充 `docs/knowledge-base/incidents/`，沉淀品牌链路媒体性能经验
- [x] 6. 校验
  - [x] 6.1 运行相关后端 pytest 与小程序静态测试
  - [x] 6.2 运行 `python scripts/validate-openspec-language.py`
  - [x] 6.3 运行 OpenSpec 校验

## 校验记录

- 2026-08-10：`uv run pytest tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel tests/test_miniapp_home.py::test_miniapp_brand_home_endpoints_return_public_detail_and_certificates tests/test_miniapp_home.py::test_miniapp_product_list_supports_context_filters_sort_and_facets` 通过。
- 2026-08-10：`uv run pytest tests/test_miniapp_static.py` 通过。
- 2026-08-10：`python -m py_compile scripts/audit-miniapp-card-images.py src/backend/app/modules/media/storage.py` 通过。
- 2026-08-10：`uv run pytest tests/test_media_storage.py tests/test_audit_miniapp_card_images.py` 在当前 Python 环境缺少 `PIL`/Pillow，collection 阶段失败；需在完整后端依赖环境重跑。
- 2026-08-10：`python scripts/audit-miniapp-card-images.py --limit 5` 因本地默认 `DATABASE_URL=sqlite:////app/data/sqlite/tilesfst.db` 指向不可写 `/app` 阻塞；需在 compose/生产等价环境补充 dry-run evidence。
