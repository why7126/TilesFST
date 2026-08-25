## 背景

`BUG-0134-miniapp-certificate-detail-display-url` 已确认小程序证书详情页顶部展示缺少 `display_url`，在缩略图缺失或展示图字段缺口时可能直接回退证书原图，造成详情加载性能退化和原图访问流量增加。

该问题发生在 `REQ-0115-media-multi-variant-images` 已归档后，说明媒体多规格契约尚未覆盖品牌证书详情链路，需要以 fix Change 补齐 API、端侧展示和验收约束。

## 变更内容

- 修复小程序证书详情接口媒体项缺少 `display_url` / `original_url` 或等价字段的问题。
- 调整小程序证书详情顶部图片展示策略：普通展示优先使用 `display_url`，缩略图仅作为轻量 fallback，原图仅用于图片预览或保真场景。
- 明确图片证书使用 `images/default/brand-certificates/`，PDF/文档证书使用 `files/default/brand-certificates/`；涉及历史对象时必须记录 dry-run、apply 和幂等摘要。
- 补齐媒体四联验收、接口测试、小程序静态/Network evidence、OpenAPI / Orval / API 文档同步任务。

## 能力影响

### 新增能力

- 无。

### 修改能力

- `media-multi-variant-images`：补齐证书详情媒体项的 `thumbnail_url`、`display_url`、`original_url` 语义和 fallback 规则。
- `object-storage`：补齐品牌证书图片 / PDF 对象前缀、派生图对象和媒体四联验收约束。

## 影响范围

- 后端：`MiniappCertificateMediaItem`、证书详情服务组装、证书媒体 URL 派生策略。
- 小程序：证书详情页顶部展示、图片预览、PDF/文档证书打开或占位。
- API：证书详情响应字段语义变化，需要同步 OpenAPI、Orval 和 API 文档。
- 对象存储：图片证书 `images/default/brand-certificates/`、PDF/文档证书 `files/default/brand-certificates/`，以及 display/thumbnail 派生对象可读性。
- 测试与验收：后端接口测试、小程序静态测试、媒体四联验收和小程序 Network evidence。

## 回滚计划

- 若修复导致证书详情图片不可展示，回滚后端证书详情响应字段组装和小程序详情页展示优先级，恢复到原 `thumbnail_url || url` 行为。
- 回滚不得删除或覆盖已生成的原图、缩略图或 display 对象；若历史对象维护任务已执行，保留 dry-run/apply/幂等摘要并按对象存储 runbook 单独处理。
- 回滚后必须记录普通展示可能回退原图的已知风险，并在后续 Change 重新修复。
