## 1. 后端接口与字段语义

- [x] 1.1 复核小程序品牌证书摘要接口，明确 `file_url` 仅用于详情、预览或打开动作，不作为卡片图片兜底。
- [x] 1.2 如现有字段不足以表达卡片展示资源，补充 `card_image_url`、`thumbnail_url` 或等价轻量字段，并保留必要兼容字段。
- [x] 1.3 明确图片证书使用 `images/default/brand-certificates/`，PDF/文档证书使用 `files/default/brand-certificates/`；不为 PDF/文档证书生成图片卡片 URL。
- [x] 1.4 如发现历史图片证书 key、缩略图或对象漂移，接入既有媒体维护 dry-run/apply 流程并记录幂等摘要。

## 2. 小程序证书卡展示

- [x] 2.1 调整品牌详情页证书 Tab 卡片图片绑定，使用 `thumbnail_url`、卡片专用小图或占位，不使用 `file_url` 作为图片 `src` fallback。
- [x] 2.2 为证书卡补齐图片加载失败状态，缩略图加载失败后展示统一占位，不二次请求原文件。
- [x] 2.3 复核证书列表页、品牌证书摘要和商品详情关联证书入口，确保卡片展示策略一致。
- [x] 2.4 保持证书详情页、图片预览和 PDF/文档打开入口可通过受控 URL 访问原文件，不被卡片策略误降级。

## 3. API、文档与生成物

- [x] 3.1 如后端响应字段发生变化，同步 FastAPI OpenAPI。
- [x] 3.2 如 OpenAPI 变化，运行 `./scripts/generate-openapi-client.sh` 并同步 Orval 生成物。
- [x] 3.3 更新 `docs/03-api-index.md` 和相关媒体 / 对象存储文档，说明证书卡 `thumbnail_url`、`file_url` 和占位 fallback 边界。

## 4. 测试与验收

- [x] 4.1 补充后端接口测试，覆盖图片证书有缩略图、缺缩略图、PDF/文档证书字段分流。
- [x] 4.2 补充小程序静态测试，断言证书卡图片 `src` 不包含 `file_url` fallback，并覆盖图片加载失败占位。
- [x] 4.3 补充媒体四联验收记录，覆盖 key、object、URL、render 以及图片/PDF 证书前缀分流。
- [x] 4.4 补充微信小程序 DevTools、真机或体验版 Network evidence，记录 URL 类型、HTTP 状态、资源大小、耗时、Waterfall、缓存状态和 render 结果。
- [x] 4.5 运行根因证据校验，必要时将 `BUG-0135` 根因状态从 `probable` 更新为 `confirmed` 并回填证据。

## 5. 收尾

- [x] 5.1 运行相关后端 pytest、小程序静态测试、OpenSpec 校验和语言校验。
- [x] 5.2 回填 `BUG-0135` acceptance 验收结果、失败项或 blocked 项。
- [x] 5.3 评估是否需要沉淀 `docs/knowledge-base/incidents/`；若无复用价值，在验收记录中说明不沉淀。
