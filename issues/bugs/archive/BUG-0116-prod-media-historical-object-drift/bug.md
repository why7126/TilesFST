---
bug_id: BUG-0116-prod-media-historical-object-drift
title: 生产历史媒体对象与缩略图存在规范漂移
severity: high
status: done
owner:
discovered_at: 2026-08-04 10:25:13
environment: production-media
related_requirement: REQ-0012-object-storage-key-layout
related_change: fix-prod-media-historical-object-drift
created_at: 2026-08-04 10:39:56
updated_at: 2026-08-04 22:59:22
---

# 生产历史媒体对象与缩略图存在规范漂移

## 现象

生产环境存在一批历史图片类媒体记录未完全符合当前单 Bucket、标准前缀和同目录缩略图规则，影响范围包括 SKU 商品图片、品牌 Logo 和品牌证书图片三类对象。

具体表现：

- SKU 商品图片绑定商品并进入公开展示后，仍可能引用 `images/default/tiles/staging/` 暂存目录，而不是归入 `images/default/tiles/{tile_id}/` 或等价商品目录。
- SKU 商品图片可能缺少同目录 `.thumb` 缩略图，或缩略图仍是旧规则生成结果，尺寸、体积或 bytes 与当前轻量缩略图规则不一致。
- 品牌 Logo 可能缺少同目录 `.thumb` 缩略图，导致品牌列表、品牌详情和 Banner 选图等端侧场景无法稳定使用轻量资源。
- 品牌证书中的 JPG、PNG、WebP 图片仍可能存放在 `files/default/brand-certificates/`，未迁移到 `images/default/brand-certificates/`。
- 品牌证书图片可能缺少同目录 `.thumb` 缩略图，或缩略图不是通过当前后端 resize/compress 逻辑生成的真实轻量资源。
- PDF 等文档类证书应继续保留在 `files/default/brand-certificates/`，不得被图片迁移逻辑误迁移。

## 复现要点

在生产等价环境中以 dry-run 方式审计历史媒体数据：

1. 查询公开 SKU 主图，统计 `tile_images.object_key` 仍以 `images/default/tiles/staging/` 开头的记录。
2. 对 SKU 主图计算同目录 `.thumb` key，检查原图 object、缩略图 object 是否存在，并识别缩略图与原图同 size 或同 bytes 的记录。
3. 查询 `brands.logo_object_key`，检查品牌 Logo 原图与同目录 `.thumb` 缩略图是否存在，并识别缩略图不符合当前生成规则的记录。
4. 查询 `brand_certificates.file_key` 和 `brand_certificate_images.file_key`，统计 JPG、PNG、WebP 图片仍位于 `files/default/brand-certificates/` 的记录，并确认 PDF 或其他文档类证书不进入图片迁移范围。
5. 对证书图片计算同目录 `.thumb` key，检查原图 object、缩略图 object 是否存在，并识别缩略图与原图同 size 或同 bytes 的记录。
6. 通过后端受控 `/media/{object_key}` 或等价 URL 验证原图和缩略图读取，不使用未授权对象存储直连地址作为通过依据。

本地探索中已确认：现有脚本可作为排查基础，但生产执行必须先配置正确数据库和对象存储环境，并以 dry-run 摘要作为修复输入。

## 期望结果

- SKU 图片绑定商品或进入公开展示后，不再长期引用 `images/default/tiles/staging/`。
- SKU 图片、品牌 Logo 和证书图片都具备同目录 `.thumb` 缩略图。
- 缩略图由当前后端图片处理逻辑生成，体积和尺寸符合轻量展示目的，不是原图 bytes 复制品。
- 图片类证书归入 `images/default/brand-certificates/`；PDF 和其他文档类证书继续保留在 `files/default/brand-certificates/`。
- 业务记录中的 key、对象存储 object、后端受控 URL 和端侧渲染结果一致。
- 批处理支持 dry-run、apply、二次审计和幂等执行，并且输出不包含生产密钥、真实客户数据、Authorization header、Cookie、`.env` 内容或本机绝对路径。

## 实际结果

生产历史媒体数据可能同时存在以下漂移：

- 公开 SKU 主图仍在 暂存目录。
- SKU、品牌 Logo 或证书图片缺少同目录缩略图。
- 旧缩略图与原图大小或 bytes 一致，不符合当前轻量缩略图规则。
- 图片类证书仍被归类在 `files/` 前缀。
- 端侧虽然可能通过 `/media/{object_key}` 回退读取原图，但性能、治理和发布验收无法满足当前对象存储规范。

## 影响范围

- Web 管理端：SKU 图片管理、品牌 Logo、品牌证书列表和详情展示。
- 店主 Web / 小程序：SKU 商品卡片、商品详情、品牌列表、品牌详情、证书列表和证书详情。
- 媒体对象存储：单 Bucket 标准前缀、同目录缩略图、历史对象迁移和幂等回填。
- 发布验收：媒体 BUG 四联验收中的 `key`、`object`、`URL`、`render` 四个维度。
- 运维执行：生产数据库、对象存储备份、dry-run/apply 证据和失败重试摘要。

## 严重等级说明

严重等级为 `high`。该问题影响生产历史数据治理和多端媒体展示性能，且同时覆盖 SKU、品牌 Logo 和证书图片三类核心媒体对象。虽然不一定导致所有页面立即不可用，但会造成公开图片继续引用暂存目录、缩略图缺失或无效、对象 key 分类错误，以及发布前媒体验收无法闭环，因此需要按高优先级进入后续缺陷补齐、评审和受控修复流程。
