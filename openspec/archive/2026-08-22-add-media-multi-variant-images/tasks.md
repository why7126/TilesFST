## 1. 后端媒体模型与生成策略

- [x] 1.1 设计并实现 `thumbnail / display / original` 三规格资源模型，明确 DB 字段或可派生 key 规则。
- [x] 1.2 实现新上传图片生成 `thumbnail` 与 `display`，保留 `original`，并覆盖失败降级和可观测日志。
- [x] 1.3 明确并实现 `display` 规格的目标宽高、质量、格式和体积上限。
- [x] 1.4 明确透明 PNG、非透明 PNG、JPG、WebP 的保留或转换策略。
- [x] 1.5 保证生成逻辑不使用用户原始文件名作为对象 key，不暴露内部路径或存储凭据。

## 2. API、OpenAPI 与 Orval

- [x] 2.1 扩展商品、SKU 或媒体相关响应，提供 `thumbnail_url`、`display_url`、`original_url` 或等价统一媒体字段。
- [x] 2.2 明确旧客户端兼容和目标规格缺失时的 fallback 顺序。
- [x] 2.3 同步 OpenAPI、Orval、API 文档和聚焦接口测试。
- [x] 2.4 若最终不改 API 字段，记录统一媒体服务适配方案和不改字段原因。

## 3. 对象存储直出与安全

- [x] 3.1 实现对象存储直出 URL 生成或适配层，明确签名、过期、缓存、公开范围和后端代理 fallback。
- [x] 3.2 验证前端和小程序不得直连未授权对象存储，不暴露 endpoint、bucket、access key 或 secret key。
- [x] 3.3 保持后续 CDN 替换能力，字段语义不绑定唯一 URL 形态。
- [x] 3.4 更新对象存储、媒体和部署相关文档，说明直出边界与安全限制。

## 4. 存量图片批量生成

- [x] 4.1 实现存量图片多规格生成 dry-run，输出待处理数量、缺失规格、跳过原因、失败分类和预计写入对象。
- [x] 4.2 实现显式 apply，要求备份或风险确认，输出成功、失败、跳过、重试建议和幂等摘要。
- [x] 4.3 实现二次审计，覆盖 key、object、URL、render 和规格收益。
- [x] 4.4 确保所有输出脱敏，不包含真实密钥、真实 `.env`、连接串、本机绝对路径、Authorization header、Cookie 或真实客户数据。

## 5. Web 管理端与小程序

- [x] 5.1 管理端上传或媒体回显入口复用上传状态机，覆盖 `idle -> uploading -> done / failed` 和同会话即时回显。
- [x] 5.2 管理端列表、详情、编辑或预览按场景选择对应规格，并在失败时稳定 fallback。
- [x] 5.3 小程序列表使用 `thumbnail_url`，SKU 详情普通展示使用 `display_url`，图片预览使用 `original_url`。
- [x] 5.4 小程序详情首屏外图片启用 lazy-load 或等价策略。
- [x] 5.6 验收返修：小程序 SKU 详情图片预览基于 media 下标统一使用 `original_url || preview_url || url` 生成 `current` 和 `urls`。
- [x] 5.5 若新增或调整 UI，补齐 1440px Web 截图、小程序截图或等价证据，并记录 UI Contract 一致性。

## 6. 测试与验收

- [x] 6.1 后端测试覆盖三规格生成、失败降级、URL 字段、fallback 和对象存储直出。
- [x] 6.2 存量批量生成测试覆盖 dry-run、apply、幂等、失败统计和脱敏输出。
- [x] 6.3 小程序静态测试覆盖列表、详情、预览 URL 绑定和 lazy-load。
- [x] 6.4 验收记录补齐媒体 key/object/URL/render 四联、`thumbnail/display` 收益和小程序 Network evidence。
- [x] 6.5 运行 `python scripts/validate-openspec-language.py`。
- [x] 6.6 运行 `openspec validate add-media-multi-variant-images --strict`。
- [x] 6.7 运行 Workflow Sync，确认 `REQ-0115`、Change 和 `sprint-025` scope 已同步。
- [x] 6.8 验收返修静态测试覆盖小程序预览 original 优先级、media 下标匹配和 `wx.previewImage({ urls, current })`。

## 验收返修记录

| 时间 | 来源 | 调整 | 结果 |
|---|---|---|---|
| 2026-08-22 17:21:41 | `/opsx-modify REQ-0115` | 小程序 SKU 详情图片预览从事件 `data-url` 当前图改为 media 下标匹配，并用同一 resolver 生成 `current` 与 `urls`，优先级为 `original_url || preview_url || url`。 | 静态测试已补并通过；真实 DevTools/体验版 `original_url` Network 请求待复验。 |
| 2026-08-22 17:28:36 | `/opsx-modify REQ-0115` | 基于复验证据继续返修：`wx.previewImage` 前使用 `wx.getImageInfo({ src: current })` 显式获取当前 original URL，完成后仍以 original URL 的 `current` 和 `urls` 调用预览。 | 静态测试已补；待重新观察 DevTools Network 是否出现原图 `.png` 请求。 |
| 2026-08-22 17:33:29 | `/opsx-modify REQ-0115` | 回填二次复验证据。 | DevTools Network 已出现同一对象的原图 `.png` 请求，AC-MINIAPP-003 可按 DevTools evidence 记为通过。 |
