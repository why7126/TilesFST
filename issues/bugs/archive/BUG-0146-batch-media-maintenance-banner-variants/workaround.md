---
bug_id: BUG-0146-batch-media-maintenance-banner-variants
created_at: 2026-08-29 19:10:08
updated_at: 2026-08-29 19:10:08
---

# Workaround

## 临时规避方案

正式修复前，可先通过运维和运营手段降低生产影响：

1. 对首页、品牌列表等高曝光 Banner，优先替换为体积较小的 WebP/JPG 原图，降低 fallback 到原图时的首屏和流量压力。
2. 对已确认缺少 `.thumb.webp` / `.display.webp` 的 Banner，可人工按同目录命名规则补上传派生对象：
   - 原图：`images/default/banners/<uuid>.png`
   - 缩略图：`images/default/banners/<uuid>.thumb.webp`
   - 展示图：`images/default/banners/<uuid>.display.webp`
3. 补传后用 `curl -I` 验证 `/media/...thumb.webp` 与 `/media/...display.webp` 返回 `Content-Type: image/webp`，且没有 `x-media-fallback: 1`。
4. 在生产执行批量维护 apply 前，避免只依赖 HTTP 200 判断派生图存在，应同时检查 `Content-Type`、`Content-Length` 和 `x-media-fallback`。

## 不足与风险

- 人工补传只能覆盖已知 Banner，无法保证后续历史补齐任务自动发现所有遗漏。
- 压缩或替换原图可能影响 Banner 高清预览质量。
- 如果只看 HTTP 200，仍可能误判 fallback 原图为派生图正常。
- 手工处理缺少批量幂等统计，不适合作为长期治理手段。

## 正式修复方向

- 将 `banners.image_object_key` 纳入批量媒体维护候选来源。
- 优先覆盖 `image_source = 'custom_upload'` 或 `image_object_key` 位于 `images/default/banners/` 的 Banner 自定义上传图，避免重复处理引用 SKU/品牌 Logo 的同一对象。
- 让 `backfill-image-variants` 对 Banner 生成 `.thumb.webp` 与 `.display.webp`。
- 让缩略图专项任务或聚合任务覆盖 Banner `.thumb.webp` 补齐，并在命令描述和 runbook 中明确覆盖范围。
- 增加回归测试，确保 Banner 来源不会再次从维护任务候选矩阵中遗漏。
