## 1. 后端接口与媒体字段

- [x] 1.1 为小程序证书详情媒体项补齐 `display_url`、`original_url` 或等价字段，并保留必要兼容字段。
- [x] 1.2 调整证书详情媒体组装逻辑，使图片证书普通展示 URL 使用 display 规格，图片预览 URL 使用原图或高清 URL。
- [x] 1.3 明确 PDF/文档证书不生成图片 `display_url`，继续走文件打开、占位或失败态策略。
- [x] 1.4 如发现历史图片证书 key 或派生图缺失，接入既有媒体维护 dry-run/apply 流程并记录幂等摘要。

## 2. 小程序展示与交互

- [x] 2.1 调整证书详情页类型与数据归一化，保留 `display_url`、`thumbnail_url`、`original_url` / `preview_url`。
- [x] 2.2 调整顶部图片展示优先级为 `display_url -> thumbnail_url -> 占位 / 失败态`，不得默认回退原图。
- [x] 2.3 调整图片预览入口，使点击预览时才使用 `original_url`、`preview_url` 或等价高清 URL。
- [x] 2.4 复核 PDF/文档证书打开、占位和失败态，不依赖图片组件展示文档资源。

## 3. API、文档与生成物

- [x] 3.1 同步 FastAPI OpenAPI，确保证书详情响应字段语义可见。
- [x] 3.2 运行 `./scripts/generate-openapi-client.sh` 并同步 Orval 生成物。
- [x] 3.3 更新 `docs/03-api-index.md` 和相关媒体 / 对象存储文档，说明证书详情 `display_url`、`thumbnail_url`、`original_url` fallback 边界。

## 4. 测试与验收

- [x] 4.1 补充后端接口测试，覆盖图片证书 `display_url`、`thumbnail_url`、`original_url` 字段和 PDF/文档证书字段分流。
- [x] 4.2 补充小程序静态测试，覆盖顶部图片 `display_url` 优先展示、预览原图和无 display 时占位/缩略图 fallback。
- [x] 4.3 补充媒体四联验收记录，覆盖 key、object、URL、render 以及图片/PDF 证书前缀分流。
- [x] 4.4 补充小程序 DevTools、真机或体验版 Network evidence，记录 URL 类型、HTTP 状态、资源大小、耗时、Waterfall 和缓存状态。
- [x] 4.5 运行根因证据校验，必要时将 `BUG-0134` 根因状态从 `probable` 更新为 `confirmed` 并回填证据。

## 5. 收尾

- [x] 5.1 运行相关后端 pytest、小程序静态测试、OpenSpec 校验和语言校验。
- [x] 5.2 回填 `BUG-0134` acceptance 验收结果、失败项或 blocked 项。
- [x] 5.3 评估是否需要沉淀 `docs/knowledge-base/incidents/`；若无复用价值，在验收记录中说明不沉淀。

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-08-23 08:30:02 | `bug-0116-media-drift` dry-run 在检查 `.thumb/.display` 变体时报告 `object_storage_unreachable`；只读诊断显示 COS 原图 HEAD 成功，但缺失 `.thumb.webp` 返回 `NoSuchResource` | 将对象存储适配层缺失对象识别统一为 `NoSuchKey` / `NoSuchObject` / `NoSuchResource`，并兼容 SDK `get_error_code()`，避免腾讯 COS 缺失派生图被误判为存储不可达 | 聚焦 pytest 13 项通过；使用当前源码加载 `sqlite-tencent-cos.env` dry-run 后 `failed=0`、`retry_candidates=99`、`thumbnail_candidates=99`、`non_standard_keys_after_audit=0` |
| 2026-08-24 13:08:11 | 用户反馈小程序首页商品卡仍显示“暂无图片”；接口样本显示同一批商品回填前 `original_url` 有值但 `cover_image`、`thumbnail_url`、`display_url` 均为 `null` | 确认前序 `backfill-image-variants --limit 100/500` 未覆盖全量候选，改为全量 dry-run/apply/幂等复跑并记录证据；本次不改业务源码 | 全量 dry-run 初始 `total=684`、`thumbnail_missing=186`、`display_missing=186`、`estimated_writes=372`；全量 apply 成功 370 个写入；幂等 dry-run `skipped=682`、`thumbnail_missing=1`、`display_missing=1`；刷新后 `/products` 为 `product_id=377/361/362/...` 返回 `.thumb.webp` / `.display.webp`，截图 `codex-clipboard-77f20599-cb4c-4c6c-b85e-c070c03d10b0.png` 显示首页商品卡图片恢复 |
| 2026-08-24 14:30:46 | 用户反馈证书详情 `media[]` 仍为旧 `files/default/brand-certificates` URL 且 `display_url/thumbnail_url=null`，轮播显示占位 | 详情接口查询 `brand_certificate_images.file_key`，服务层优先使用 canonical `images/default/brand-certificates/` key 派生 display/thumb/original；主证书查询同步把 canonical key 转为受控 `/media/images/...` URL | SQLite 显示 `media_id=40` 的 `file_key` 已迁移但 `file_url` 仍旧；`migrate-certificate-image-keys` dry-run `image_candidates=0`、`document_skipped=5`；`tests/test_miniapp_home.py` 44 项通过；运行时 `/api/v1/miniapp/certificates/4` 返回非空 canonical `.display/.thumb`，两者 HEAD 均 `200 OK`、`content-type=image/webp`、`x-media-fallback=0` |
