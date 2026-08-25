---
bug_id: BUG-0134-miniapp-certificate-detail-display-url
root_cause_status: confirmed
category: design
created_at: 2026-08-22 21:08:06
updated_at: 2026-08-24 14:30:46
---

# Root Cause

## 根因状态

`confirmed`

已有代码定位显示，证书详情接口的媒体项 Schema 未提供 `display_url` 字段，后端证书媒体组装逻辑把图片媒体的 `url` 与 `preview_url` 都设置为 `file_url`，小程序证书详情页顶部图片展示使用 `thumbnail_url || url`。这说明详情页缺少“普通展示使用 display 规格、预览才使用原图”的契约贯通，导致缺展示图字段时容易退回证书原图。

后续验收返修已补齐小程序 DevTools Network、维护任务 dry-run/apply/幂等摘要、接口响应字段和小程序 render 截图。证据链能够解释三类表现：证书详情缺少 display 字段会导致展示规格语义混淆；历史图片派生对象未全量回填时，商品卡接口会返回 `thumbnail_url/display_url/cover_image = null` 并显示“暂无图片”；历史证书图片完成 `file_key` 迁移后，如果详情接口仍使用旧 `file_url` 派生变体，`media[]` 会继续返回空 `display_url/thumbnail_url` 并显示轮播占位。因此根因状态升级为 `confirmed`。

## 直接原因

证书详情媒体项没有稳定返回 `display_url`。后端 `_certificate_media_items()` 当前为证书图片媒体写入 `url=image.file_url`、`preview_url=image.file_url`，只额外派生 `thumbnail_url`；小程序证书详情页顶部展示绑定 `item.thumbnail_url || item.url`，当缩略图不可用或字段缺失时会直接使用 `url`，也就是证书原图 URL。

验收返修追加确认一类半迁移状态：本地 `media_id=40` 的 `brand_certificate_images.file_key` 已是 `images/default/brand-certificates/...jpg`，但 `file_url` 仍保留 `/media/files/default/brand-certificates/...jpg`。详情接口此前只查询 `file_url`，导致服务层按旧 `files/default` 路径检查 `.display/.thumb`，即使 canonical key 的派生对象已经存在，响应仍可能返回 `display_url=null`、`thumbnail_url=null`。

## 根本原因

媒体多规格图片策略已经要求相关 API 提供 `thumbnail_url`、`display_url`、`original_url` 或等价字段，但证书详情链路仍停留在 `file_url` / `thumbnail_url` 双字段模型，没有把“详情普通展示 display、图片预览 original”的语义纳入后端 Schema、服务组装和小程序渲染契约。

## 触发条件

1. 品牌证书为 JPG、PNG 或 WebP 图片证书。
2. 用户打开微信小程序证书详情页。
3. 证书详情接口返回的媒体项缺少 `display_url`，或小程序端未消费该字段。
4. 详情顶部图片展示优先级为 `thumbnail_url || url`。
5. `thumbnail_url` 缺失、不可用，或展示策略需要比缩略图更清晰的 display 规格时，页面使用 `url` 回退到证书原图。

## 证据链

| 证据入口 | 类型 | 摘要 | 结论 |
|---|---|---|---|
| `src/backend/app/schemas/miniapp_home.py` | 代码定位 | `MiniappCertificateMediaItem` 仅声明 `url`、`preview_url`、`thumbnail_url`，未声明 `display_url` 或 `original_url` | 证书详情媒体项缺少多规格展示字段 |
| `src/backend/app/services/miniapp_home_service.py` | 代码定位 | `_certificate_media_items()` 对证书图片写入 `url=image.file_url`、`preview_url=image.file_url`、`thumbnail_url=...` | 后端把普通展示入口和原图预览入口绑定到同一个原图 URL |
| `src/miniapp/pages/certificate-detail/index.wxml` | 代码定位 | 顶部图片 `src` 绑定为 `item.thumbnail_url || item.url` | 缺缩略图时端侧会退回 `url` |
| `src/miniapp/pages/certificate-detail/index.ts` | 代码定位 | 图片预览使用 `preview_url || url` | 当前预览和普通展示都可能落到原图字段 |
| `openspec/specs/media-multi-variant-images/spec.md` | 规格定位 | 媒体相关 API MUST 提供 `thumbnail_url`、`display_url`、`original_url` 或等价语义字段 | 证书详情链路与媒体多规格 API 契约存在偏差 |
| 用户补充的 DevTools Network 截图 | 小程序证据 | `.thumb.jpg` 受控 `/media` URL 返回 `200 OK`，包含 `content-type=image/jpeg`、资源大小与 `x-media-fallback: 0` 证据 | 修复后小程序端可通过后端受控媒体 URL 渲染，不直连对象存储 |
| `backfill-image-variants` 全量维护任务摘要 | 运维证据 | 初始全量 dry-run 为 `total=684`、`thumbnail_missing=186`、`display_missing=186`；全量 apply 后幂等 dry-run 为 `skipped=682`、`thumbnail_missing=1`、`display_missing=1` | 之前 `--limit 100/500` 覆盖不足是首页商品卡继续空图的直接原因 |
| 用户补充的 `/products` 响应字段 | 接口证据 | 回填前同一批商品仅 `original_url` 有值；回填后 `product_id=377/361/362/...` 均返回 `.thumb.webp` 与 `.display.webp` | 派生对象补齐后后端商品卡字段恢复 |
| `codex-clipboard-77f20599-cb4c-4c6c-b85e-c070c03d10b0.png` | 小程序 render 证据 | 首页新品推荐与热销推荐商品卡图片正常渲染 | 小程序空图现象已恢复 |
| 本地 SQLite `brand_certificate_images` 查询 | 数据证据 | `media_id=40` 显示 `file_key=images/default/brand-certificates/...jpg`，但 `file_url=/media/files/default/brand-certificates/...jpg`；历史图片 key 计数为 0，canonical 证书图片 key 计数为 26 | 证书图片 key 已迁移，但旧 `file_url` 仍可让详情接口误用历史路径 |
| `migrate-certificate-image-keys` dry-run | 运维证据 | 本地 `sqlite-tencent-cos` 返回 `image_candidates=0`、`document_skipped=5`、`failed=0` | `brand_certificate_images` 无剩余待迁移图片 key；剩余 `files/default/brand-certificates` 均为文档类边界 |
| `/api/v1/miniapp/certificates/4` 运行时响应 | 接口证据 | `media_id=40` 返回 `display_url=/media/images/default/brand-certificates/...display.webp`、`thumbnail_url=/media/images/default/brand-certificates/...thumb.webp`、`original_url=/media/images/default/brand-certificates/...jpg` | 详情接口已优先使用 canonical image key 派生轮播图片 URL |
| `.display/.thumb` URL HEAD | 对象证据 | `.display.webp` 返回 `200 OK`、`content-type=image/webp`、`content-length=106654`、`x-media-fallback=0`；`.thumb.webp` 返回 `200 OK`、`content-type=image/webp`、`content-length=9698`、`x-media-fallback=0` | 证书详情轮播依赖的 display/thumb 对象存在、可读且未走 fallback |

## 人工补证步骤

已补齐本 BUG 必需证据。后续若要追平剩余 2 个 `backfill-image-variants` retry candidate，可单独补充对应脱敏对象摘要、失败原因和重试结果，不阻塞 BUG-0134 归档。

## 验证方式

- 修复前：证书详情接口媒体项缺少 `display_url`，小程序详情顶部图片在缩略图缺失或不可用时请求证书原图 URL。
- 修复后：图片证书详情接口返回 `display_url`，顶部普通展示优先使用 `display_url`；图片预览才使用 `original_url`、`preview_url` 或等价高清 URL；PDF/文档证书仍按文件打开或占位展示，不走图片 display 规格。
