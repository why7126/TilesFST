## 背景

Banner 媒体链路已经具备两侧证据：新上传接口会请求生成同目录 `thumbnail` / `display` 派生图；历史批量维护任务却没有扫描 `banners.image_object_key`。生产中 `.thumb.webp` URL 返回 200 但带 `x-media-fallback: 1`，说明派生图缺失被原图 fallback 掩盖。

## 目标

- 历史 Banner 自定义上传图能被批量媒体维护命令发现。
- `backfill-image-variants` 能补齐 Banner `.thumb.webp` 与 `.display.webp`。
- 缩略图专项任务与 `media-drift-reconcile` 能补齐 Banner `.thumb.webp`。
- dry-run/apply/幂等输出可用于生产验收，且保持脱敏。
- 不改变 Banner 上传接口、Banner 表结构、原图格式和客户端字段契约。

## 非目标

- 不新增 Banner 管理页面或小程序页面。
- 不新增 API、OpenAPI 字段、Orval 生成物或 DB migration。
- 不删除历史原图，不把原图转码为 WebP。
- 不改变 `/media` fallback 机制；本 Change 只让缺失派生图被批量生成后直接命中。
- 不处理 SVG、PDF、GIF、HEIC、TIFF、BMP 等非首期支持格式的自动转码扩展。

## 根因与修复方案

根因：`_thumbnail_source_rows()` 未包含 `banners.image_object_key`，而 `run_thumbnail_backfill()`、`run_image_variant_backfill()` 和 `media-drift-reconcile` 都依赖该候选来源。

修复方案：

1. 在 `_thumbnail_source_rows()` 中追加 Banner 来源：
   - `source_type`: `banner_image`
   - `source_id`: `banners.id`
   - `object_key`: `banners.image_object_key`
   - `mime_type`: `NULL`，由 object key 或对象信息推断
2. 过滤范围优先限定为 Banner 自定义上传图：
   - `image_source = 'custom_upload'`，或
   - `image_object_key LIKE 'images/default/banners/%'`
3. 保持现有去重逻辑：同一个 `object_key` 多次出现在不同业务来源时只处理一次。
4. 保持现有派生命名规则：
   - 原图：`images/default/banners/<uuid>.<ext>`
   - 缩略图：`images/default/banners/<uuid>.thumb.webp`
   - 展示图：`images/default/banners/<uuid>.display.webp`
5. 保持历史删除策略：不删除原图；不删除已有合格派生图；仅在 apply 中写入缺失或不合格的 WebP 派生对象。

## 输出与验收口径

dry-run：

- 不写数据库。
- 不写对象存储。
- 不删除对象。
- 输出中应能看到 `banner_image` 候选和缺失派生图统计。
- 若 `failed = 0` 且对象存储维度不是 `blocked`，可根据 `estimated_writes`、`thumbnail_missing`、`display_missing` 判断是否进入 apply。

apply：

- 必须显式传入 `--apply --confirm-backup`。
- 写入 Banner `.thumb.webp` 与 `.display.webp` 派生对象。
- 不改写 `banners.image_object_key`。
- 输出成功、失败、跳过、重试候选和失败原因统计。
- apply 后执行同命令 dry-run，应不再报告同一 Banner 派生图缺失。

URL / render：

- apply 后 `/media/...thumb.webp` 与 `/media/...display.webp` 应返回 `Content-Type: image/webp`。
- 响应不应再出现 `x-media-fallback: 1`。
- Web 管理端或小程序 Banner 页面需补充 Network/render evidence，证明普通展示不再加载原始大图。

## 产品数据采集与链路观测

本设计部分适用 `docs/standards/product-data-collection-observability.md`。

```yaml
product_data_collection_observability:
  status: partial
  affected_layers:
    - backend
    - storage
  reason: 本设计只调整后端媒体维护命令候选来源和对象存储派生图写入范围，不新增业务 API、DB schema、请求日志、行为事件、Task Trace、Web 请求封装、小程序请求封装或 App 请求封装。
  validation: 实现后以单元测试、OpenSpec 校验、维护任务 dry-run/apply/幂等 JSON、URL 响应头和 Web 或小程序 render evidence 验证。
```

- affected_layers: `backend`、`storage`
- 不适用项：不新增业务 API、DB schema、请求日志、行为事件、Task Trace、Web 请求封装、小程序请求封装或 App 请求封装。
- 验证：通过维护任务 JSON summary、acceptance_summary、生产 dry-run/apply/幂等摘要和端侧 evidence 证明闭环。

## 测试策略

- 单元测试 `_thumbnail_source_rows()` 包含 Banner 自定义上传图。
- 单元测试 Banner 来源只覆盖 `custom_upload` 或 `images/default/banners/`，避免重复扫描引用 SKU/品牌来源的 Banner。
- 单元测试 `backfill-image-variants` 对 `banner_image` 输出 thumbnail/display 缺失和 estimated writes。
- 聚合测试确认 `media-drift-reconcile` 汇总能包含 Banner 缩略图候选。
- 脱敏测试确认输出不包含真实 object key、bucket、endpoint、密钥、连接串或 `.env` 内容。
- 文档/Runbook 测试确认生产命令和 Banner 覆盖说明存在。

## 风险与缓解

- 风险：Banner 引用 SKU/品牌已有图片时重复处理。缓解：优先过滤 `custom_upload` 或 Banner 标准目录，并保留 object key 去重。
- 风险：HTTP 200 被误读为派生图存在。缓解：验收必须检查 `Content-Type` 和 `x-media-fallback`。
- 风险：生产 apply 写入大量派生对象。缓解：要求先 dry-run、分批 `--limit`、备份确认和幂等复核。
- 风险：输出泄露对象定位信息。缓解：继续复用 `_safe_object_ref()` 等脱敏摘要，新增测试覆盖。
