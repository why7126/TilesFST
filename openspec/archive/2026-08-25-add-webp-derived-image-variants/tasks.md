## 1. 后端派生生成

- [x] 1.1 定位所有图片上传入口，确认头像、品牌 Logo、Banner、SKU 图片和品牌证书图片是否生成 `thumbnail` / `display`。
- [x] 1.2 调整图片派生生成逻辑，使 JPEG、PNG、WebP 输入统一输出 WebP `thumbnail` 与 WebP `display`。
- [x] 1.3 保留 `original` 上传格式、原始 MIME、对象 key 和高清预览 URL 语义。
- [x] 1.4 为 SVG、PDF、GIF、HEIC、TIFF、BMP 等首期不转码格式补齐跳过、拒绝或 fallback 记录。
- [x] 1.5 确保派生失败不阻断原图上传，并记录 warning、失败原因或可观测 span。

## 2. 对象存储、URL 与 API

- [x] 2.1 调整 WebP 派生 key 推导，使用 `.thumb.webp` / `.display.webp` 或等价稳定 WebP key。
- [x] 2.2 写入对象时设置 `image/webp` Content-Type，并验证读取响应 MIME 与扩展名一致。
- [x] 2.3 保留历史 `.thumb.jpg`、`.thumb.png`、`.display.jpg`、`.display.png` 等旧派生 key 的读取 fallback 候选。
- [x] 2.4 复用 `thumbnail_url`、`display_url`、`original_url` 或等价字段；若响应结构、Schema 或示例变化，同步 OpenAPI、Orval、API 文档和测试。
- [x] 2.5 确认不新增数据库字段；若实现确需记录派生状态、MIME、尺寸或 bytes，同步 SQLite/MySQL schema、迁移、数据库文档和测试。

## 3. 多端消费与 UI 边界

- [x] 3.1 管理端上传回显、列表和表单展示优先使用 WebP `thumbnail_url` 或 `display_url`，高清预览继续使用原图。
- [x] 3.2 店主 Web 商品、品牌、Banner 和证书展示按列表/卡片优先 thumbnail、详情普通展示优先 display、预览优先 original 的规则消费。
- [x] 3.3 微信小程序列表/卡片优先 `thumbnail_url`，详情普通展示优先 `display_url`，图片预览使用 `original_url`。
- [x] 3.4 端侧加载失败时提供受控 fallback 或占位，避免图片空白、无限重试或默认请求原图作为性能通过证据。
- [x] 3.5 如改动 Web UI，使用 Design System semantic token、既有上传状态机、fixed toast 和 inline error，不新增裸 Hex。

## 4. 历史补生成维护任务

- [x] 4.1 更新存量图片多规格维护任务，使 dry-run 能识别待生成 WebP 派生、已存在 WebP 派生、不支持格式、原图缺失和对象存储不可达。
- [x] 4.2 确保 dry-run 不写数据库、不写对象存储，并输出待处理数量、已存在数量、跳过原因、失败分类和预计写入数量。
- [x] 4.3 确保 apply 必须显式触发，并在生产执行前要求数据库和对象存储 bucket/prefix 备份确认。
- [x] 4.4 确保 apply 幂等，重复运行不重复写入无变化对象，也不破坏已有引用。
- [x] 4.5 补齐维护任务脱敏输出，禁止真实 `.env`、密钥、Authorization header、Cookie、数据库连接串、本机绝对路径和未脱敏 object key 全量值。

## 5. 测试与验收

- [x] 5.1 补充后端测试，覆盖 JPEG、PNG、WebP 输入生成 WebP thumbnail/display，且 original 保留上传格式。
- [x] 5.2 补充 key/MIME 测试，覆盖 `.thumb.webp` / `.display.webp` 或等价 key 与 `image/webp` 一致。
- [x] 5.3 补充特殊格式测试，覆盖 SVG/PDF 跳过，以及 GIF/HEIC/TIFF/BMP 暂不转码的策略记录。
- [x] 5.4 补充 API 和端侧测试，覆盖 Web、管理端和小程序按场景优先消费派生 URL 与 fallback。
- [x] 5.5 补充维护任务测试，覆盖 dry-run、apply、幂等、对象存储不可达、原图缺失、失败分类和脱敏摘要。
- [x] 5.6 记录媒体五联 evidence：key、object、URL、render、benefit。
- [x] 5.7 记录小程序媒体四联 evidence：key、object、URL、render 和 Network evidence。
- [x] 5.8 运行相关 pytest、Web/Vitest 或小程序静态校验、OpenAPI/Orval 校验、`openspec validate add-webp-derived-image-variants --strict` 和 `python scripts/validate-openspec-language.py`。

## 6. 文档与收尾

- [x] 6.1 更新 `rules/media.md`、`rules/object-storage.md`、长期媒体/对象存储文档和维护任务说明，记录 WebP 派生格式策略。
- [x] 6.2 回填 REQ-0120 acceptance、trace 和 Change trace 的实现证据、验收结果、测试命令和已知风险。
- [x] 6.3 评估是否需要把“WebP 派生图 key/MIME 一致性”沉淀为媒体最佳实践；无明确新增复用价值时记录不沉淀。

## 验收返修记录

- [x] 2026-08-25 `/opsx-modify`：补充 Docker Web `http://localhost:3000` SKU 图片上传与 `display.webp` 展示边界证据；确认上传接口 `200 OK` / `code=0`、原图保留 PNG、派生 URL 为 `.thumb.webp` / `.display.webp`、SKU 编辑弹窗即时回显且 `display.webp` GET `200`。
