## 任务清单

- [x] 1. 根因补证与现状定位
  - [x] 定位商品详情页图片媒体字段来源、页面 `<image>` 绑定字段和点击预览 URL 来源。
  - [x] 记录当前接口响应样本与页面 Network 样本，确认是否默认加载原图、大 PNG 或 `>1 MB` 展示图。
  - [x] 将 `BUG-0132` 根因状态从 `probable` 更新为 `confirmed`，或记录证据不足原因。
- [x] 2. 后端详情媒体 URL 选择修复
  - [x] 确保 SKU 详情接口返回可区分的展示 URL 与预览 URL，或返回等价统一媒体字段。
  - [x] 普通展示 URL 不得默认指向 `>1 MB` 原图；展示图缺失时必须有可观测 fallback。
  - [x] 确保响应不暴露 object key、bucket、endpoint、未授权对象存储路径或内部文件系统路径。
- [x] 3. 小程序详情页展示与预览修复
  - [x] 详情页普通 `<image>` 绑定展示 URL。
  - [x] 点击预览时使用原图、高清图或等价预览 URL。
  - [x] 首屏外图片启用 `lazy-load` 或等价延迟加载。
  - [x] 保持视频、占位图、失败态和现有媒体顺序兼容。
- [x] 4. PNG 大图与展示版兜底
  - [x] 大 PNG 必须有展示版替代。
  - [x] 非透明 PNG 可转换为 JPG/WebP 或等价压缩展示格式。
  - [x] 透明 PNG 保留透明语义并生成受控展示版。
- [x] 5. 回归测试
  - [x] 补充或更新后端测试，覆盖详情接口展示 URL、预览 URL 和安全字段边界。
  - [x] 补充或更新小程序测试，覆盖展示 URL 绑定、预览 URL 使用和 lazy-load。
  - [x] 补充或更新媒体 fixture 测试，覆盖 `>1 MB` 原图不会进入默认冷加载展示链路。
- [x] 6. API、文档与客户端同步
  - [x] 若 API 字段发生变化，同步 OpenAPI、Orval、API 文档和错误码说明。
  - [x] 若 DB 或对象存储规则发生变化，同步 schema、数据库文档、对象存储文档和测试。
  - [x] 与 `REQ-0115` 的通用媒体多规格字段保持语义一致。
- [x] 7. 验收与证据回填
  - [x] 使用小程序 DevTools、体验版或真机 Network 复测商品详情页冷加载。
  - [x] 记录首屏关键图、普通详情图、预览原图的 Size、Time、Waterfall 和缓存状态。
  - [x] 回填 `BUG-0132` acceptance、root-cause、trace；如沉淀为复用经验，补充 `docs/knowledge-base`。

## 验收返修记录

### 2026-08-22 16:54:48

- 反馈：进入商品详情页后提示“图片加载失败，可稍候重试”，失败 URL 为 `...83d26016-aa94-43cb-a18c-536e37c61cd3.display.jpg`；确认 `.display` 派生展示对象不存在或不可读。
- 范围判断：属于本 Change 的详情页冷加载展示图可用性与 fallback 边界，不新增业务范围。
- 调整：后端 SKU 详情聚合返回 `display_url` / `thumbnail_url` 前校验派生对象存在性；对象缺失时返回空展示字段，普通展示 `url` 不再回退原图；小程序详情页占位图改为现有 `/assets/logos/product-logo.png`。
- 测试：新增 `tests/test_miniapp_home.py::test_miniapp_sku_detail_hides_missing_display_variants_and_avoids_original_cold_load`，覆盖缺失派生对象时不返回坏 URL 且不回退原图冷加载。
- 未完成：仍需小程序 DevTools、体验版或真机 Network 复测，并补充存量图片 display/thumb 批量生成的 dry-run/apply evidence。

### 2026-08-22 19:56:51

- 验收证据：SKU 362 接口返回 `display_url=null`、普通展示 `media[].url=.thumb.jpg`，`.thumb.jpg` HTTP 200、`content-length: 15263`、`x-media-fallback: 0`；SKU 377 干净 DevTools Network 仅见 `.display.png` 与 `.thumb.jpg`，未见 1.13MB 原图 `.png` 冷加载。
- 结论：BUG-0132 页面冷加载修复通过；存量 display/thumb 批量补生成 dry-run/apply evidence 作为 `REQ-0115` 媒体多规格治理后续，不阻塞本 BUG 归档。
