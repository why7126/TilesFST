## 背景

`REQ-0120-webp-derived-image-variants` 已确认：系统已具备 `thumbnail / display / original` 三规格模型，但当前派生图格式仍跟随原图 MIME，JPEG 生成 JPEG、PNG 生成 PNG，图片密集页面仍可能加载较重的展示资源。

本变更将新上传图片和历史补生成任务中的 `thumbnail` 与 `display` 统一收敛为 WebP 派生图，同时保留原图上传格式，用更小的展示资源改善 Web、管理端与微信小程序的加载性能。

## 变更内容

- 新上传 JPEG、PNG、WebP 图片后保留原图格式，并生成 WebP `thumbnail` 与 WebP `display`。
- 统一 WebP 派生 key 与 MIME 规则，避免 `.thumb.jpg` / `.display.png` 返回 `image/webp` 的不一致状态。
- SVG、PDF 首期不生成 WebP 派生图；GIF、HEIC、TIFF、BMP 首期暂不转码，并记录跳过、拒绝或 fallback 策略。
- Web 管理端、店主 Web 与小程序继续通过 `thumbnail_url`、`display_url`、`original_url` 或等价字段消费媒体，不新增端侧直连对象存储逻辑。
- 历史图片补生成维护任务支持 WebP 派生图 dry-run / apply、幂等执行、备份前置条件、脱敏摘要和二次审计。
- 验收覆盖 key、object、URL、render、benefit 五联，以及小程序 key/object/URL/render 四联证据。

## 能力影响

### 新增能力

- 无。

### 修改能力

- `media-multi-variant-images`：三规格图片能力新增 WebP 派生格式策略、特殊格式跳过策略和端侧消费约束。
- `object-storage`：对象 key、MIME、受控 URL 和派生对象读取规则新增 WebP key / content 一致性要求。
- `prod-media-maintenance-jobs`：历史图片多规格维护任务新增 WebP 派生补生成、dry-run/apply 和二次审计要求。

## 影响范围

- 后端：媒体上传、图片派生生成、MIME 判断、派生 key 推导、fallback 候选、媒体维护任务。
- API：优先复用既有 `thumbnail_url`、`display_url`、`original_url` 字段；如响应结构、Schema 或示例变化，需要同步 OpenAPI、Orval、API 文档和测试。
- 对象存储：同 Bucket、同业务目录下新增或改用 `.thumb.webp` / `.display.webp` 或等价 WebP 派生对象。
- Web 管理端：头像、品牌 Logo、Banner、SKU 图片、证书图片上传回显和列表/表单展示优先消费 WebP 派生 URL。
- 店主 Web：商品、品牌、Banner 和证书展示优先消费 WebP 派生 URL；高清查看保留原图。
- 微信小程序：列表/卡片优先 `thumbnail_url`，详情普通展示优先 `display_url`，预览使用 `original_url`。
- 数据库：默认不新增业务表字段；若实现选择持久化派生对象状态、尺寸、MIME 或体积，必须同步 SQLite/MySQL schema、迁移、数据库文档和测试。
- 测试与验收：后端派生图、API 字段、Web/小程序消费、维护任务、媒体五联、小程序四联、语言校验和 OpenSpec 校验。
