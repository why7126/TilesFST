## 上下文

`BUG-0134` 的根因状态为 `probable`：代码定位显示 `MiniappCertificateMediaItem` 只有 `url`、`preview_url`、`thumbnail_url`，后端证书图片媒体组装将 `url` 和 `preview_url` 都设置为 `file_url`，小程序证书详情顶部图片展示绑定 `thumbnail_url || url`。这使普通详情展示与原图预览语义混在一起。

`REQ-0115` 已要求媒体相关 API 提供 `thumbnail_url`、`display_url`、`original_url` 或等价字段；对象存储规范也已要求品牌证书图片使用 `images/default/brand-certificates/`，PDF/文档证书使用 `files/default/brand-certificates/`。本 Change 只修复证书详情链路的契约缺口，不新增通用多规格媒体平台能力。

## 目标与非目标

**目标：**

- 证书详情接口对图片媒体返回 `display_url` 和 `original_url` 或等价语义字段。
- 小程序证书详情顶部普通展示优先使用 `display_url`，图片预览使用 `original_url` / `preview_url`。
- 图片证书、PDF/文档证书的 key 前缀和展示行为清晰分流。
- API、OpenAPI、Orval、测试、媒体四联和小程序 Network evidence 同步闭环。

**非目标：**

- 不建设新的媒体规格生成平台。
- 不引入生产 CDN 正式接入。
- 不自动执行生产历史对象写入维护任务。
- 不改变品牌证书上传入口的权限边界或 MinIO 单桶策略。

## 设计决策

### 决策 1：证书图片媒体项补齐多规格字段

证书详情媒体项应对图片返回：

- `thumbnail_url`：卡片、列表或轻量 fallback。
- `display_url`：详情顶部普通展示。
- `original_url` 或等价高清 URL：图片预览、保真查看。

`url` 可保留兼容语义，但小程序普通展示不得把 `url` 当作默认原图 fallback。这样可以兼容已有客户端，同时给新端侧逻辑明确规格选择。

### 决策 2：小程序展示优先级从原图兜底改为受控兜底

证书详情顶部图片展示优先级为 `display_url -> thumbnail_url -> 占位 / 失败态`。图片预览入口使用 `original_url -> preview_url -> 受控高清 URL`。当 `display_url` 缺失时，普通展示不得直接使用原图字段作为性能通过证据。

### 决策 3：图片与文档证书按对象前缀和端侧行为分流

JPG、JPEG、PNG、WebP 证书图片使用 `images/default/brand-certificates/` 或等价图片前缀，并可具备同目录 thumbnail/display 派生对象。PDF 或其他文档证书使用 `files/default/brand-certificates/`，小程序通过文件打开或占位展示，不生成图片 `display_url`。

### 决策 4：历史对象维护只作为受控任务

若发现历史图片证书仍在 `files/` 前缀，或缺少 thumbnail/display 派生对象，修复实现应通过既有媒体维护能力或明确任务执行 dry-run、apply、幂等验证。Change 本身不得默认自动写生产对象存储。

## 风险与取舍

- 派生图缺失时普通展示可能出现占位或较低清晰度缩略图：通过验收记录 fallback 事件、Network evidence 和失败态，避免静默加载原图。
- 老客户端可能仍读取 `url`：保留兼容字段，但新小程序详情页必须使用 `display_url` / `original_url` 语义字段。
- 根因尚未通过真实 Network 证据升级为 confirmed：实现前后都必须补接口响应摘要和小程序 DevTools、真机或体验版 evidence。
- API 字段变化会影响生成物：实现阶段必须同步 OpenAPI、Orval 和 API 文档，避免前端类型漂移。

## 迁移与回滚

- 先补后端 schema/service 和测试，再补小程序端类型、绑定和静态测试。
- 如涉及历史对象，先 dry-run 输出脱敏统计，再由人工确认 apply；apply 后记录幂等摘要。
- 回滚时保留对象存储数据，不删除历史对象；仅回退接口字段组装和端侧展示优先级，并记录原图 fallback 风险。
