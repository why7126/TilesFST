---
bug_id: BUG-0132-miniapp-sku-detail-large-image-cold-load
root_cause_status: confirmed
category: design
created_at: 2026-08-22 10:59:53
updated_at: 2026-08-22 16:54:48
---

# Root Cause

## 根因状态

`confirmed`

用户提供的多组微信小程序开发者工具 Network 截图已经能确认商品详情页冷加载存在大图资源，且慢点集中在图片下载阶段。后续补证截图进一步确认，小程序商品详情页普通 `<image>` 展示链路优先读取 `display_url`，但接口媒体数据中缺少 `display_url` 时会 fallback 到 `item.url`；该样本中 `item.url` 与 `preview_url` 指向同一原图 URL。验收返修反馈进一步确认，后端可能返回推导出的 `.display.jpg` URL，但对应派生对象不存在或不可读，进入商品详情页后出现“图片加载失败，可稍候重试”。因此根因可确认：普通展示链路既存在原图 fallback 过宽，也存在后端返回未验证派生展示 URL 的问题，导致冷加载要么请求原图，要么请求不可用展示图。

## 直接原因

小程序商品详情页普通图片展示链路在 `display_url` 缺失时 fallback 到 `item.url`，而 `item.url` 与 `preview_url` 指向同一原图 URL，导致详情页冷加载阶段请求不适合普通展示的大图资源，包括 1MB 以上 JPEG、1.5MB PNG、3.6MB PNG 等，图片下载耗时达到 5s-11s。

## 根本原因

实现层根因是商品详情页展示 URL fallback 过宽且后端展示图可用性校验不足：端侧普通展示虽然优先 `display_url`，但曾允许在 `display_url` 缺失时回退到 `item.url`；接口样本中 `item.url` 仍是原图语义，且与预览 URL 相同。返修反馈中的 `.display.jpg` URL 说明后端还会基于原图 key 推导展示图 URL，而没有在响应前确认对应对象存在和可读。两者都会绕过“普通展示只加载可用轻量资源”的策略。

历史对象或生产环境中若 `display_url` 派生图缺失，后端需返回可区分的展示 URL 与预览 URL，端侧也不得将原图字段作为普通展示兜底。

## 触发条件

1. 商品详情页包含大图素材或 PNG 长图。
2. 用户首次进入详情页，或开发者工具禁用缓存后进行冷加载。
3. 详情接口媒体项缺少可用 `display_url`，或端侧未使用展示图字段。
4. 页面普通 `<image>` 绑定展示 URL 时 fallback 到原图字段。
5. 端侧请求一个或多个原图资源，导致大图下载阶段明显拖慢页面可见体验。

## 证据链

| 证据入口 | 类型 | 摘要 | 结论 |
|---|---|---|---|
| 用户补充的微信小程序开发者工具 Network 截图 | 截图 / 复现证据 | 1.1MB JPEG 用时约 6.04s；1.5MB PNG 用时约 5.24s；3.6MB PNG 用时约 11.10s；826KB JPEG 用时约 5.68s | 大图冷加载耗时过长已复现 |
| 用户补充的多页详情请求数据 | 截图 / 对比证据 | 部分详情页请求数量达到 24-54 个，总资源量达到 3.9MB-4.7MB | 详情页冷加载媒体资源压力较大 |
| 用户补充的小图样本 | 对比证据 | 13KB-46KB 等小图通常在 150ms-800ms 范围 | 问题集中在大图资源和加载策略，不是全部媒体请求不可用 |
| 用户补充的小程序详情页 AppData / WXML 截图 | 截图 / 代码定位 / 接口字段证据 | WXML 普通展示绑定 `src="{{item.display_url || item.url || imageFallback}}"`；预览绑定 `data-url="{{item.original_url || item.preview_url || item.url}}"`；AppData 样本中 `url` 与 `preview_url` 指向同一原图 URL，未看到 `display_url` | 展示图缺失时普通展示会 fallback 到原图，根因闭环 |
| 用户补充的失败 URL | 验收返修证据 | `http://127.0.0.1:8000/media/images/default/tiles/362/83d26016-aa94-43cb-a18c-536e37c61cd3.display.jpg` 进入详情页后加载失败 | 派生展示图 URL 不能只靠 key 推导，后端需确认对象存在和可读后才返回 |
| `issues/bugs/archive/BUG-0132-miniapp-sku-detail-large-image-cold-load/bug.md` | 缺陷描述 | 已记录复现步骤、期望结果、实际结果和影响范围 | 可作为后续修复与验收基线 |

## 已确认结论

- 直接原因：小程序商品详情页普通图片展示链路在 `display_url` 缺失时使用原图字段。
- 触发条件：进入商品详情页后，图片媒体列表渲染普通 `<image>`，展示 URL fallback 到 `item.url`。
- 影响范围：小程序详情页图片普通展示、后端 SKU 详情媒体字段、历史图片展示版或 PNG 大图治理。
- 修复方向：后端只返回存在且可读的 `display_url`、`thumbnail_url`；普通展示只使用 `display_url`、`thumbnail_url` 或可用占位图；点击预览才使用 `original_url`、`preview_url` 或原图字段。

## 仍需验收补证

1. 对同一商品执行修复前后 Network 对比，记录 Size、Time、Waterfall 和缓存状态。
2. 抽取至少 2 个慢请求样本的脱敏媒体 URL 类型、MIME、大小、扩展名和展示版存在性。
3. 若涉及历史对象治理，补充 dry-run、apply、幂等性和失败统计摘要。

## 验证方式

- 修复前：在微信小程序开发者工具中禁用缓存进入商品详情页，确认存在大于 1MB 的普通展示图请求，且下载耗时达到秒级。
- 修复后：同一商品冷加载时，普通展示图不再请求大于 1MB 的原图；首屏关键图片控制在 100-300KB；普通详情展示图控制在 150-500KB；高清原图仅在点击预览时请求。
