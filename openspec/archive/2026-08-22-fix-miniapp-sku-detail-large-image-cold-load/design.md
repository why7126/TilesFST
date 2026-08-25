## 根因与证据

`BUG-0132` 当前根因状态为 `probable`。用户提供的微信小程序开发者工具 Network 截图显示，商品详情页冷加载阶段存在超大图片资源请求，且耗时主要集中在 `Content Download` 或大资源传输阶段。已观察到的样本包括 `3.6 MB` PNG 约 `11.10 s`、`1.5 MB` PNG 约 `5.24 s`、`1.1 MB` JPEG 约 `6.04 s` 和 `826 kB` JPEG 约 `5.68 s`。

因此本修复假设的直接原因是：详情页普通展示链路仍可能绑定原图、大 PNG 或未压缩展示图 URL，导致冷加载阶段下载不必要的大资源。最终实现阶段需要通过代码定位、接口响应样本和小程序 Network 复测把根因升级为 `confirmed`，或在证据不成立时更新 BUG 根因状态与修复方案。

## 修复策略

详情页图片链路分成普通展示和高清预览两类：

- 普通展示：页面 `<image>` 默认绑定详情展示图、压缩图或等价安全展示 URL，不默认绑定 `>1 MB` 原图。
- 高清预览：用户点击图片后才使用原图、高清图或等价预览 URL。
- 首屏关键图：优先保证可读纹理和快速显示，目标体积 `100-300 kB`。
- 普通详情图：目标体积 `150-500 kB`，超过 `1 MB` 时不得作为默认冷加载展示图。
- PNG 大图：需要展示版替代；非透明 PNG 可转换为 JPG 或 WebP，透明 PNG 需保留透明语义并生成受控展示版。
- 首屏外图片：启用 `lazy-load` 或等价延迟加载，避免非关键图片阻塞首屏体验。

## API 与数据边界

优先复用或补齐媒体响应中的展示 URL 与预览 URL 字段。若 `REQ-0115` 的 `thumbnail_url`、`display_url`、`original_url` 已落地，本修复直接使用这些字段；若通用能力尚未完整落地，本修复也必须提供最小等价字段或后端安全选择逻辑，以避免 BUG 修复被通用能力阻塞。

API 响应不得暴露原始 object key、bucket、endpoint、未授权对象存储路径或内部文件系统路径。后端返回 `display_url`、`thumbnail_url` 前必须确认对应派生对象存在且可读；若 `.display.*` 或 `.thumb.*` 派生对象缺失、不可读或未补生成，接口应返回空展示字段，让端侧使用轻量占位图，不得返回一个会 404 的派生 URL，也不得把 `original_url`、`preview_url` 或 `media[].url` 原图放回默认冷加载链路。

## 与 REQ-0115 的关系

`REQ-0115` 建设上传后生成 `thumbnail / display / original` 的通用媒体多规格能力，覆盖管理端、后端、对象存储、存量批处理和多端选择。本 Change 只修复 `BUG-0132` 的商品详情页冷加载问题：

- 可以依赖 `REQ-0115` 已提供的字段或派生图。
- 不要求完成全部存量媒体批处理和 CDN 正式接入后才能修复详情页冷加载。
- 若两者同 Sprint 并行，实现时需要以同一字段语义收敛，避免小程序详情页出现两套 URL 选择规则。

## UI Contract

| 项 | 内容 |
|---|---|
| 事实源优先级 | `issues/requirements/archive/REQ-0044-miniapp-sku-detail-page/prototype/miniapp/sku-detail.html`、原型 PNG、`prototype-context.md`、`interaction.md`、本 Change acceptance、既有小程序详情页实现。 |
| 页面与入口 | 微信小程序 `pages/tile-detail/index`，通过 `skuId` 进入商品详情页；本修复不改变导航、品牌入口、收藏、分享或推荐跳转。 |
| 信息架构 | 保持顶部媒体轮播、摘要、品牌卡、参数、备注、推荐和底部操作栏结构不变。 |
| 视觉 token | 不改变现有深色品牌视觉、尺寸、卡片、底部栏和媒体区布局；仅调整图片 URL 选择与加载策略。 |
| 交互状态 | 普通展示加载展示图；点击图片进入预览并使用高清 URL；首屏外图片继续 lazy-load；图片失败沿用现有 fallback。 |
| Mock/API 边界 | 使用真实 `GET /api/v1/miniapp/skus/{sku_id}` 响应字段；若 `display_url` 或 `thumbnail_url` 对应派生对象不存在或不可读，后端返回空展示字段，普通展示不得 fallback 到原图 URL。 |
| 权限规则 | 不新增鉴权或管理端能力；小程序仍只消费公开 SKU 数据和受控 `/media` URL。 |
| 一致性参照 | 与 `REQ-0044` 媒体区“大图/视频呈现、点击图片全屏预览”一致，同时满足 `BUG-0132` 冷加载大图限制。 |

## 验证方案

- 后端测试覆盖 SKU 详情接口图片媒体字段语义：展示 URL 与预览 URL 可区分，展示 URL 不默认指向超大原图。
- 小程序静态或单元测试覆盖详情页 `<image>` 绑定展示 URL、点击预览使用高清 URL、首屏外图片开启 lazy-load。
- 媒体处理或 fixture 测试覆盖 PNG 大图展示版替代、非透明 PNG 转 JPG/WebP 或等价展示格式。
- 验收补充小程序 DevTools、体验版或真机 Network evidence，记录首屏关键图、普通详情图、预览原图的 Size、Time、Waterfall 和缓存状态。
- 媒体四点 evidence 覆盖 key、object、URL、render；如缺少真机证据，不得把验收结论写为通过。
