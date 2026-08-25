## 上下文

当前媒体能力已建立 `thumbnail / display / original` 三规格语义，且 `REQ-0118` 已沉淀 Web 与小程序消费矩阵，`REQ-0119` 已补齐 display 图体积目标配置。REQ-0120 在此基础上只收敛派生图编码策略：原图保留上传格式，展示和缩略派生统一 WebP。

现有上传链路写入原图后会调用图片处理生成派生图，派生 key 目前可能沿用原图扩展名。若直接把内容改成 WebP 但 key 仍为 `.jpg` 或 `.png`，会造成缓存、Content-Type、调试和后续维护任务混乱。因此本变更必须同时调整编码、key、MIME、URL、历史补生成和端侧消费验收。

## 目标 / 非目标

**目标：**

- 支持 JPEG、PNG、WebP 输入生成 WebP `thumbnail` 与 WebP `display`。
- 保留 `original` 上传格式、对象 key、MIME 和高清预览语义。
- 保证 WebP 派生对象 key 扩展名、Content-Type 和实际 bytes 一致。
- 复用既有多规格 URL 字段，端侧按场景优先使用 WebP 派生 URL。
- 历史图片通过受控维护任务补生成 WebP 派生图，支持 dry-run、apply、幂等和脱敏二次审计。

**非目标：**

- 不把原图强制转为 WebP。
- 不引入 AVIF、`picture` 多源协商或浏览器能力协商。
- 不覆盖视频转码、多清晰度视频或封面策略。
- 不新增前端直传对象存储能力。
- 不在系统设置保存时自动扫描或重建历史对象。
- 默认不新增数据库字段；若实现阶段确需持久化派生状态，必须同步 DB schema 和迁移。

## 设计决策

### D1 WebP 派生策略

JPEG、PNG、WebP 输入属于首期支持范围，统一通过后端图片处理生成 WebP `thumbnail` 与 `display`。PNG 透明图需要在实现和验收记录中明确透明度保留或背景处理结果。派生失败不得阻断原图上传，但必须记录 warning、失败原因或任务 span。

替代方案：全部原图也转 WebP。该方案会破坏素材保真、审计、下载和高清预览语义，本期不采用。

### D2 key 与 MIME 一致

新生成 WebP 派生图使用 `.thumb.webp` 与 `.display.webp` 或等价稳定 WebP key。对象写入时 Content-Type 必须为 `image/webp`，读取响应也必须保持一致。读取层可以保留历史 `.thumb.jpg`、`.display.png` 等 fallback 候选，但新生成对象不得出现扩展名与内容不一致。

替代方案：保留旧扩展名但改写 Content-Type。该方案不利于缓存、排障和外部工具识别，本期不采用。

### D3 特殊格式边界

SVG、PDF 首期不生成 WebP 派生图。GIF、HEIC、TIFF、BMP 首期暂不转码，按现有上传策略拒绝、跳过或仅返回原图 fallback，但必须在上传响应、维护任务摘要或验收记录中可诊断。

替代方案：引入 HEIC/TIFF/BMP/GIF 转码依赖。该方案会扩大依赖、兼容性和动画语义风险，本期延后。

### D4 端侧消费边界

Web 管理端、店主 Web 和小程序继续使用接口返回的规格 URL 字段，不拼接对象 key。列表和卡片优先 `thumbnail_url`，详情普通展示优先 `display_url`，预览、下载和保真查看使用 `original_url`。若目标规格缺失，端侧可使用受控 fallback 或占位，但验收不得把原图 fallback 计为性能通过。

### D5 历史补生成

历史对象补生成继续纳入媒体维护任务：默认 dry-run，apply 必须显式触发，并要求生产执行前确认数据库与对象存储 bucket/prefix 备份。任务输出只保留计数、资源类型、key hash、标准前缀、失败原因和二次审计摘要。

## 原型与验收冲突处理

事实源优先级：`prototype.html` > PNG/截图 > `prototype/web/context.md` > `acceptance.md` > `rules/ui-design.md` > 既有 OpenSpec specs。

本 REQ 仅提供 `prototype/web/context.md`，未提供 HTML 或 PNG，且明确不新增独立页面。结论：本 Change 不要求新增高保真 UI 原型，也不新增独立媒体处理页；后续实现若触达既有上传控件、维护任务结果或媒体展示组件，必须遵守既有 Design System、上传状态机、即时回显、错误态和小程序 Network evidence 验收。

## UI Contract

| 项 | 契约 |
|---|---|
| 事实源优先级 | 无 HTML/PNG；以 `prototype/web/context.md`、`acceptance.md`、`rules/ui-design.md` 和既有页面规范为准。 |
| 页面与入口 | 管理端复用头像、品牌 Logo、Banner、SKU 图片、品牌证书图片等既有上传入口；店主 Web 和小程序复用既有图片展示入口；不新增独立页面。 |
| 信息架构 | 上传控件保留原有字段、预览、错误态和保存关系；维护任务如展示结果，仅展示统计摘要、状态和失败分类。 |
| 视觉 token | Web UI 如有改动必须使用 semantic token、`cn()` 和既有 DS 组件；不得新增裸 Hex。 |
| 交互状态 | 上传入口必须覆盖 `idle -> uploading -> done / failed`；图片加载失败需有占位或受控失败态。 |
| 图标与文案 | 用户可见文案表达“展示图/缩略图/原图”语义，不展示内部 object key、异常堆栈或存储配置。 |
| Mock/API 边界 | 本 Change 以真实上传 API、媒体 URL 字段和维护任务为准；Mock 仅可用于 UI 单测，不代表后端已生成 WebP。 |
| 权限规则 | 上传仍走后端鉴权；管理端和店主端权限边界不变；小程序不得直连未授权对象存储。 |
| 一致性参照 | `admin-media-upload-chain`、`miniapp-media-four-part-acceptance-practice`、三规格消费矩阵和 REQ-0120 acceptance。 |

## 风险 / 取舍

- WebP 生成失败或体积收益不明显 → 保留原图上传成功，记录 warning，并在验收中区分 fail、blocked、fallback 和 no-benefit。
- 历史旧派生 key 与新 WebP key 并存 → 读取层保留兼容候选，维护任务通过 dry-run 分类并逐步补生成。
- 小程序或旧浏览器 WebP 兼容性差异 → 小程序和现代 Web 默认支持 WebP；端侧仍保留受控 fallback 或占位。
- 历史补生成写对象存储有风险 → apply 需要显式授权、备份确认、幂等处理和二次审计。
- 容量缓冲偏低 → sprint-025 纳入后剩余 fix 缓冲仅 3.5 人天，后续不宜继续追加非阻断范围。

## 迁移计划

1. 调整新上传派生生成：支持 JPEG/PNG/WebP 输入，输出 WebP thumbnail/display。
2. 调整 key、MIME、URL 与 fallback 候选，确保新对象使用 WebP key 和 `image/webp`。
3. 更新历史多规格维护任务 dry-run/apply，支持 WebP 派生补生成和脱敏二次审计。
4. 更新多端消费测试和验收，证明列表/卡片/详情普通展示优先使用 WebP 派生 URL。
5. 若接口 Schema 或示例变化，同步 OpenAPI、Orval、API 文档和测试。
6. 发布前先 dry-run 历史补生成；生产 apply 需人工确认备份和执行窗口。

## 未决问题

- 是否需要为透明 PNG 统一保留 alpha，还是按具体业务图类型允许白底合成，由实现阶段结合现有图片处理库能力确认并写入验收记录。
- 是否需要持久化派生对象 MIME、尺寸和 bytes；默认不新增 DB 字段，除非实现阶段证明仅 key 推导不足以支撑验收或维护任务。
