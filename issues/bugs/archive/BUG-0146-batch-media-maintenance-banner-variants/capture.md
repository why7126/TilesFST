---
bug_id: BUG-0146-batch-media-maintenance-banner-variants
status: done
created_at: 2026-08-29 19:02:43
updated_at: 2026-08-30 08:36:14
severity_hint: high
environment: prod
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0137-miniapp-lightweight-image-variant-consumption
lifecycle_stage: plan
---

# 现象

生产环境 Banner 自定义上传图未被批量媒体维护命令覆盖，导致 COS 的 Banner 目录下缺少 `.thumb.webp` 与 `.display.webp` 派生图。线上请求 `/media/images/default/banners/673dd7ed-5264-4cd1-a6a3-4faee8befb69.thumb.webp` 虽返回 200，但响应头显示 `Content-Type: image/png`、`Content-Length: 6191144`、`x-media-fallback: 1`，说明后端媒体代理 fallback 到原始 PNG，而非真实命中 WebP 缩略图。

# 复现步骤

1. 在生产环境选择一张通过 Banner 管理上传的 Banner 图片。
2. 检查 COS 中 `images/default/banners/` 目录，确认该 Banner 原图存在但缺少同名 `.thumb.webp` 与 `.display.webp`。
3. 请求 Banner 缩略图 URL：
   `curl -I 'https://tilesfst.wjoyhappy.site/media/images/default/banners/673dd7ed-5264-4cd1-a6a3-4faee8befb69.thumb.webp'`
4. 观察响应头是否出现 `x-media-fallback: 1`，以及 `Content-Type` 是否不是 `image/webp`。
5. 运行现有批量媒体维护 dry-run 命令，观察候选来源是否未包含 `banners.image_object_key`。

# 期望 vs 实际

- 期望：批量媒体维护命令覆盖 Banner 自定义上传图，能为历史 Banner 原图生成同目录 `.thumb.webp` 与 `.display.webp`，后续 `/media/...thumb.webp`、`/media/...display.webp` 直接命中 WebP 派生对象。
- 实际：维护命令仅覆盖商品图、品牌 Logo、证书文件/图片等来源，未扫描 `banners.image_object_key`；生产 Banner 派生图缺失时仍由 `/media` fallback 返回原图，页面能显示但加载大图。

# 影响范围

- 生产环境历史 Banner 图片。
- 首页 Banner 与其他消费 Banner 图片的 Web / 小程序展示链路。
- 批量维护命令：`media-drift-reconcile`、`backfill-brand-certificate-thumbnails`、`backfill-image-variants`。
- 首屏加载性能、弱网体验、对象存储回源流量与媒体维护验收口径。

# 初步线索

- `app.modules.media.maintenance` 的批量候选查询未包含 `banners.image_object_key`。
- Banner 上传入口已按同目录策略传入 `thumbnail_key` 与 `display_key`，说明新增上传具备生成派生图的设计意图。
- Banner 管理服务会暴露同目录缩略图 URL，消费侧存在读取 `.thumb.webp` 的路径。
- `/media` 代理对 `.thumb.webp` / `.display.webp` 请求存在 fallback 原图逻辑，因此缺失派生对象时不会 404，而是返回 `x-media-fallback: 1`。

# 建议验收或复现要点

- [ ] `backfill-image-variants` dry-run 能识别历史 Banner 候选，并报告将生成 `.thumb.webp` 与 `.display.webp`。
- [ ] `backfill-brand-certificate-thumbnails` 或对应缩略图专项任务能覆盖 Banner 缩略图补齐，或明确拆分/改名为通用缩略图任务。
- [ ] `media-drift-reconcile` 聚合任务能通过内部子任务覆盖 Banner 派生图候选。
- [ ] apply 后 COS 中 Banner 原图旁存在 `.thumb.webp` 与 `.display.webp`。
- [ ] apply 后 `curl -I` Banner `.thumb.webp` 返回 `Content-Type: image/webp`，不再出现 `x-media-fallback: 1`，且 `Content-Length` 明显小于原 PNG。
- [ ] 更新生产媒体维护 runbook，明确 Banner 覆盖范围、生成格式、删除策略、dry-run 进入 apply 条件与 JSON 输出文件解析。

# 来源

- 来源命令：`/bug-capture`
- 来源描述：批量媒体维护命令未覆盖 Banner 自定义上传图，导致生产 Banner 缺少 `thumb.webp` / `display.webp` 并 fallback 到原图。
- 生产证据：用户提供的 `curl -I` 响应头显示 `HTTP/1.1 200 OK`、`Content-Type: image/png`、`Content-Length: 6191144`、`x-media-fallback: 1`。

# 拆分说明

本次不拆分。三个维护命令属于同一批量媒体候选来源矩阵遗漏 `banners.image_object_key` 所导致的同一问题，可由一次修复统一补齐候选来源、命令行为和 runbook 说明。

# 附件

- 暂无。
