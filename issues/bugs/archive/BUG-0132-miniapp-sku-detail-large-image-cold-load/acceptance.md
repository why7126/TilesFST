---
bug_id: BUG-0132-miniapp-sku-detail-large-image-cold-load
acceptance_status: passed
created_at: 2026-08-22 10:59:53
updated_at: 2026-08-25 14:51:36
template_ref: docs/standards/media-bug-four-point-acceptance-template.md
---

# Acceptance

## 回归验收清单

| AC | 验收项 | 状态 |
|---|---|---|
| AC-001 | 商品详情页冷加载默认不请求大于 1MB 的原图作为普通展示图 | passed |
| AC-002 | 首屏关键图片优先控制在 100-300KB，普通详情展示图控制在 150-500KB | passed |
| AC-003 | PNG 大图有展示版替代；非透明 PNG 可转为 JPG 或 WebP 展示图 | passed |
| AC-004 | 高清原图只在点击预览或明确查看高清时加载 | passed |
| AC-005 | 首屏外详情图片启用 lazy-load，不在进入详情页时全部请求 | passed |
| AC-006 | 微信小程序开发者工具 Network 记录修复前后 Size、Time、Waterfall、URL 和缓存状态 | passed |
| AC-007 | 媒体类 BUG 四联验收覆盖 key、object、URL、render 四个维度 | passed |

## 媒体类 BUG 四联验收

模板引用：`docs/standards/media-bug-four-point-acceptance-template.md`

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0132-miniapp-sku-detail-large-image-cold-load |
| 标题 | 小程序商品详情页冷加载存在大图资源导致图片加载耗时过长 |
| 严重等级 | high |
| 影响范围 | 小程序 / 后端接口 / 对象存储 / 媒体 URL |
| 复现入口 | 微信小程序商品详情页 |
| 受影响端 | miniapp / backend / storage |
| 环境 | miniapp-devtools |
| 媒体类型 | image / thumbnail / original |
| 业务资源 | 脱敏商品详情页图片资源 |
| 修复前实际结果 | 商品详情页冷加载存在 1MB 以上 JPEG、1.5MB PNG、3.6MB PNG 等大图请求，下载耗时约 5s-11s |
| 修复后期望结果 | 商品详情页普通展示使用小程序适配图片资源，高清原图仅在预览时加载，首屏外详情图 lazy-load |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | passed | SKU 362 使用脱敏 key `83d26016...jpg`，接口隐藏缺失 `.display` 并返回 `.thumb.jpg`；SKU 377 使用脱敏 key `90cd8fa8...png`，冷加载请求 `.display.png` | 无 |
| object | passed | SKU 362 `.thumb.jpg` HTTP 200，`content-length: 15263`，`content-type: image/jpeg`，`x-media-fallback: 0`；SKU 377 `.display.png` 可渲染，原图 `90cd8fa8...png` 约 1.13MB 未出现在干净冷加载列表 | 存量 display/thumb 批量补生成 dry-run/apply 继续由媒体治理后续承接，不阻塞本 BUG |
| URL | passed | SKU 362 `display_url=null`、`media[].url=.thumb.jpg`、`original_url=.jpg`；SKU 377 干净 Network 仅见 `.display.png` 与其他 `.thumb.jpg`，未见原图 `.png` | 无 |
| render | passed | 用户补充微信小程序 DevTools 截图确认 SKU 362、SKU 377 页面正常展示；SKU 377 干净 Network 过滤后不再出现原图请求 | 无 |

### 媒体上传横切检查

| Gate | 状态 | 说明 |
|---|---|---|
| 上传状态机 | n/a | 本 BUG 聚焦商品详情页展示侧冷加载，不直接修改上传入口；若修复涉及重新生成展示图，则在实现阶段补充生成任务证据 |
| 同会话即时回显 | n/a | 本 BUG 不涉及 Web 管理端上传或编辑即时回显 |
| Docker Web 边界 | n/a | 本 BUG 不涉及 Nginx、Docker Web 上传大小或边界文件 |
| 媒体代理一致性 | passed | SKU 362 `.thumb.jpg` 通过受控 `/media` URL 返回 200，`x-media-fallback: 0`，缓存策略正确 |
| 历史对象与审计 | follow_up | 本 BUG 已通过接口过滤与端侧展示策略阻断冷加载原图；存量 display/thumb 批量补生成 dry-run/apply evidence 由媒体多规格治理继续承接 |
| 小程序 evidence | passed | 用户补充 DevTools Network 截图确认 SKU 362 和 SKU 377 冷加载阶段不请求原图，页面正常展示 |

## 验收数据建议

- 至少选择 2 个修复前存在慢图的商品详情页样本。
- 每个样本记录普通展示图片的最大 Size、最大 Time、请求数量、总资源量和是否命中缓存。
- 若存在 PNG 大图，记录转换或展示版生成前后的 MIME、大小和端侧 URL。
- 若使用 lazy-load，记录进入详情页首屏时首屏外图片未立即请求，滚动到可视区域后再请求。

## 实现阶段证据

| 证据 | 结论 |
|---|---|
| 用户补充的小程序 WXML / AppData 截图 | 根因已确认：普通展示在 `display_url` 缺失时 fallback 到与 `preview_url` 相同的原图 URL |
| `src/miniapp/pages/tile-detail/index.wxml` | 普通展示改为 `display_url || thumbnail_url || imageFallback`；预览仍使用高清 URL |
| `src/miniapp/pages/tile-detail/index.ts` 与 `index.js` | 归一化阶段不再把 `item.url` 写回普通展示 URL，避免原图进入展示兜底 |
| `tests/test_miniapp_static.py` | 静态测试覆盖展示 URL、预览 URL 和 lazy-load 绑定 |
| `tests/test_miniapp_home.py::test_miniapp_sku_detail_returns_public_media_recommendations_and_share` | 后端 SKU 详情接口返回 `display_url`、`thumbnail_url`、`original_url`，且不暴露原始对象路径 |
| 用户补充的失败 URL `...83d26016-aa94-43cb-a18c-536e37c61cd3.display.jpg` | 返修确认：后端推导的 `display_url` 可能对应不存在或不可读对象，必须在响应前过滤 |
| `tests/test_miniapp_home.py::test_miniapp_sku_detail_hides_missing_display_variants_and_avoids_original_cold_load` | 派生展示图 / 缩略图缺失时，SKU 详情接口不返回坏的 `display_url` / `thumbnail_url`，普通展示 `url` 不回退原图 |
| `src/miniapp/pages/tile-detail/index.ts` 与 `index.js` | 详情页占位图改为现有资源 `/assets/logos/product-logo.png`，确保后端展示字段为空时端侧兜底资源可加载 |

用户已补充微信小程序 DevTools 复测证据，SKU 362 与 SKU 377 均满足冷加载不请求原图、展示资源可用和页面正常渲染；本 BUG 验收可闭合为 `passed`。

## 归档验收证据

| 样本 | 证据 | 结论 |
|---|---|---|
| SKU 362 | 接口返回 `display_url=null`、`media[].url=.thumb.jpg`；`.thumb.jpg` HTTP 200，`content-length: 15263`，`x-media-fallback: 0` | 缺失 display 时后端不返回坏 URL，端侧冷加载使用可用缩略图 |
| SKU 377 | 干净 DevTools Network 过滤后仅见 `90cd8fa8...display.png` 和其他 `.thumb.jpg`，未见 `90cd8fa8...png` 原图 | display 存在时冷加载使用展示图，1.13MB 原图未进入普通展示冷加载 |
| 静态与接口测试 | `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` 通过，`78 passed` | 回归覆盖小程序绑定、接口字段、安全字段和缺失派生图 fallback |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-22 19:56:51
accepted_by: user
source_change: fix-miniapp-sku-detail-large-image-cold-load
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

