## 1. Implementation

- [x] 1.1 定义并实现商品图片缩略图 key helper：同目录、文件名差异化、支持 JPG/PNG/WebP，覆盖 `images/default/tiles/pending/` 与已绑定 tile_id 路径。
- [x] 1.2 调整 SKU 图片上传或主图保存链路，在原图写入成功后生成列表缩略图；生成失败需可观测且不破坏原图上传。
- [x] 1.3 调整小程序首页和商品列表 `cover_image` 解析逻辑，优先返回可访问同路径缩略图，缺失时回退原主图或占位，不返回已知不可访问的缩略图 URL。
- [x] 1.4 实现历史缩略图回填脚本，支持 dry-run、分批、可重入和执行摘要，覆盖公开 SKU 主图与 pending 主图。
- [x] 1.5 实现商品卡片图片审计脚本或命令，输出公开 SKU、无主图、pending 主图、原图缺失、缩略图缺失等统计与可定位 SKU 清单。
- [x] 1.6 确认 `thumbnails/` 前缀仅作为历史兼容或迁移来源，不作为 pending 主图列表缩略图最终写入策略。

## 2. Tests

- [x] 2.1 补充后端单元测试，覆盖缩略图 key helper 对 pending 原图和 tile-id 原图的派生规则。
- [x] 2.2 补充后端服务测试，覆盖原图存在但缩略图缺失时的 `cover_image` 回退，以及缩略图存在时返回同路径缩略图 URL。
- [x] 2.3 补充回填测试或等价集成验证，覆盖成功、原图缺失、对象存储写入失败、重复执行幂等。
- [x] 2.4 补充小程序静态测试，覆盖商品卡片 `lazy-load` 保留、图片失败兜底和复用入口图片字段一致。
- [x] 2.5 回归 `BUG-0092-miniapp-card-images-slow-load` 核心验收，确认恢复图片展示不导致首屏外图片初始化全量请求。

## 3. Documentation And Validation

- [x] 3.1 如 OpenAPI 描述或接口文档包含 `cover_image` URL 语义，更新 API 文档并按需运行 Orval。
- [x] 3.2 更新对象存储或媒体文档中商品缩略图命名规则，保持单 Bucket + 标准前缀策略。
- [x] 3.3 运行 `openspec validate fix-miniapp-product-card-thumbnails --strict`。
- [x] 3.4 运行相关后端 pytest、小程序静态测试和回填 dry-run 验证。
- [x] 3.5 视情况沉淀到 `docs/knowledge-base/incidents/`，记录“性能优化不能返回不可访问媒体 URL”的经验。
