---
bug_id: BUG-0146-batch-media-maintenance-banner-variants
root_cause_status: confirmed
category: code
created_at: 2026-08-29 19:10:08
updated_at: 2026-08-29 19:10:08
---

# Root Cause

## 根因状态

`confirmed`

生产响应头和代码定位已能闭环解释该问题：Banner 派生图 URL 可访问并不代表 `.thumb.webp` 对象存在；当前 `/media` 会在同目录派生图缺失时 fallback 到原图。同时，批量媒体维护任务的候选来源没有扫描 `banners.image_object_key`，因此无法为历史 Banner 自定义上传图补齐 `.thumb.webp` 与 `.display.webp`。

## 直接原因

批量媒体维护任务复用 `app.modules.media.maintenance._thumbnail_source_rows()` 作为历史图片候选来源，但该 SQL 只查询了以下表和字段：

- `tile_images.object_key`
- `brands.logo_object_key`
- `brand_certificates.file_key`
- `brand_certificate_images.file_key`

该候选集合未包含 `banners.image_object_key`。因此 `backfill-brand-certificate-thumbnails`、`backfill-image-variants` 以及调用缩略图回填子任务的 `media-drift-reconcile` 都不会处理 Banner 自定义上传图。

## 根本原因

媒体多规格能力在上传链路和历史批处理链路之间覆盖范围不一致。Banner 上传接口已按同目录策略生成并传入 `thumbnail_key` 与 `display_key`，但后续历史数据补齐和漂移治理任务没有把 Banner 业务表纳入统一媒体来源矩阵，导致历史 Banner 对象缺少派生图时无法被批处理发现。

## 触发条件

1. 生产环境存在历史 Banner 自定义上传图，业务记录保存在 `banners.image_object_key`。
2. 对应原图位于 `images/default/banners/` 或等价 Banner 图片前缀。
3. 同目录 `.thumb.webp` 或 `.display.webp` 对象不存在。
4. 运行现有批量媒体维护 dry-run 或 apply。
5. 维护任务候选来源未包含 Banner，无法生成缺失派生图。
6. 客户端或管理端请求 `/media/...thumb.webp` / `/media/...display.webp` 时，后端媒体代理 fallback 到原图。

## 证据链

| 证据入口 | 类型 | 摘要 | 结论 |
|---|---|---|---|
| `用户提供的生产 curl -I 响应头` | 生产复现 | `/media/images/default/banners/<uuid>.thumb.webp` 返回 `HTTP/1.1 200 OK`、`Content-Type: image/png`、`Content-Length: 6191144`、`x-media-fallback: 1` | 缩略图 URL 实际 fallback 到 PNG 原图，并非真实 WebP 缩略图 |
| `src/backend/app/modules/media/maintenance.py` | 代码定位 | `_thumbnail_source_rows()` 查询 SKU 图片、品牌 Logo、证书文件和证书图片，没有 `banners.image_object_key` | 批量维护候选来源漏 Banner |
| `src/backend/app/modules/media/maintenance.py` | 代码定位 | `run_thumbnail_backfill()` 与 `run_image_variant_backfill()` 都遍历 `_thumbnail_source_rows()` | 缩略图专项和 WebP 派生任务都会漏 Banner |
| `src/backend/app/modules/media/maintenance.py` | 代码定位 | `run_bug_0116_media_drift()` 调用 `run_thumbnail_backfill()` 作为聚合任务子步骤 | `media-drift-reconcile` 也会间接漏 Banner |
| `src/backend/app/api/v1/uploads.py` | 代码定位 | `upload_banner_image()` 为 Banner 上传传入 `same_directory_thumbnail_object_key(object_key)` 与 `same_directory_display_object_key(object_key)` | 新上传 Banner 具备生成派生图意图，偏差集中在历史批处理 |
| `src/backend/app/modules/media/storage.py` | 代码定位 | `_same_directory_variant_origin_candidates()` 和 `_resolve_candidate_keys()` 会为 `.thumb.webp` / `.display.webp` 请求追加原图候选 | 派生图缺失时 `/media` 可能 200 返回原图，掩盖对象缺失 |
| `src/backend/app/db/schema.mysql.sql` | 数据模型定位 | `banners` 表含 `image_object_key`、`image_source`、`status` 等字段 | Banner 历史图片具备可扫描的数据来源 |
| `src/backend/tests/test_media_maintenance.py` | 测试定位 | 现有 `_thumbnail_source_rows()` 单测只断言 SKU、品牌、证书来源 | 测试未覆盖 Banner 来源，导致漏扫未被回归测试捕获 |

## 人工补证步骤

1. 在生产或预发布环境导出脱敏 Banner 样本：记录 `banners.id`、`image_source`、脱敏后的 `image_object_key` 前缀和扩展名。
2. 对样本分别检查原图、`.thumb.webp`、`.display.webp` 的 COS 存在性、MIME 与大小。
3. 对同一样本执行 `/media/...thumb.webp` 与 `/media/...display.webp` 的 `curl -I`，记录 `Content-Type`、`Content-Length`、`x-media-fallback`。
4. 修复后先运行 `backfill-image-variants` dry-run，确认输出中出现 `source_type: banner_image` 且 `estimated_writes` 与缺失派生图数量一致。
5. apply 后再次检查 COS 和 `curl -I`，期望返回 `Content-Type: image/webp`，不再出现 `x-media-fallback: 1`。
6. 在小程序 DevTools、真机或体验版补充首页/品牌列表 Banner Network 与 render evidence。

## 验证方式

- 修复前：维护任务 dry-run 输出无 `banner_image` 来源；生产 Banner `.thumb.webp` 请求返回 `x-media-fallback: 1` 且 `Content-Type` 为原图类型。
- 修复后：维护任务 dry-run 输出包含 Banner 候选；apply 生成 Banner `.thumb.webp` 与 `.display.webp`；幂等 dry-run 不再报告同一 Banner 缺失派生图；端侧普通展示不再加载原始大图。
