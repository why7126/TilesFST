---
bug_id: BUG-0146-batch-media-maintenance-banner-variants
title: 批量媒体维护命令未覆盖 Banner 自定义上传图
severity: high
status: done
owner:
discovered_at: 2026-08-29 19:02:43
environment: prod
related_requirement: REQ-0115-media-multi-variant-images
related_change:
fix-media-maintenance-banner-variants
updated_at: 2026-08-30 08:36:05
created_at: 2026-08-29 19:33:31
---

# 现象

生产环境 Banner 自定义上传图缺少同目录 `.thumb.webp` 与 `.display.webp` 派生对象。请求 Banner 缩略图 URL 时 HTTP 状态码可能仍为 200，但实际由媒体代理 fallback 到原图，而不是真实返回 WebP 缩略图。

已观察到的生产响应头：

```text
HTTP/1.1 200 OK
Content-Type: image/png
Content-Length: 6191144
x-media-fallback: 1
```

这表示 `/media/images/default/banners/...thumb.webp` 请求最终返回的是 PNG 原图，页面可以显示，但会加载约 6MB 的大图。

# 复现步骤

1. 在生产环境选择一张通过 Banner 管理上传的自定义 Banner 图片。
2. 检查 COS 的 `images/default/banners/` 目录，确认该 Banner 原图存在，但缺少同名 `.thumb.webp` 与 `.display.webp`。
3. 执行：

```bash
curl -I 'https://tilesfst.wjoyhappy.site/media/images/default/banners/673dd7ed-5264-4cd1-a6a3-4faee8befb69.thumb.webp'
```

4. 观察响应头是否出现 `x-media-fallback: 1`，以及 `Content-Type` 是否不是 `image/webp`。
5. 运行现有批量媒体维护 dry-run，检查输出候选来源是否未包含 `banner_image` 或 `banners.image_object_key`。

# 期望 vs 实际

期望：

- 批量媒体维护命令覆盖历史 Banner 自定义上传图。
- `backfill-image-variants` 能为 Banner 原图生成同目录 `.thumb.webp` 与 `.display.webp`。
- 缩略图专项任务或聚合任务能补齐 Banner `.thumb.webp`。
- apply 后 `/media/...thumb.webp` 与 `/media/...display.webp` 直接命中 WebP 派生对象，不再 fallback 到原图。

实际：

- 批量维护候选来源未扫描 `banners.image_object_key`。
- 历史 Banner 缺失 `.thumb.webp` 与 `.display.webp` 时不会被现有维护命令补齐。
- `/media` fallback 让缺失派生图看起来仍可访问，但实际返回原图，掩盖了对象缺失问题。

# 影响范围

- 生产环境历史 Banner 自定义上传图。
- 小程序首页轮播、品牌列表轮播等 Banner 展示位。
- Web 管理端中依赖 Banner 缩略图预览的展示链路。
- 批量维护命令：
  - `media-drift-reconcile`
  - `backfill-brand-certificate-thumbnails`
  - `backfill-image-variants`
- 首屏加载性能、弱网体验、对象存储回源流量和媒体维护验收准确性。

# 严重等级说明

严重等级：high。

该问题发生在生产环境媒体链路，虽然不一定造成页面不可用，但会让 Banner 普通展示加载原始大图，并通过 fallback 掩盖 `.thumb.webp` / `.display.webp` 真实缺失状态。Banner 属于首页或列表页高曝光资源，影响移动端首屏性能、流量成本和多规格媒体治理验收，因此按 high 处理。
openspec_changes:
  - change_id: fix-media-maintenance-banner-variants
    type: fix
    status: archived
