---
bug_id: BUG-0116-prod-media-historical-object-drift
status: done
created_at: 2026-08-04 10:25:13
updated_at: 2026-08-04 22:59:43
severity_hint: high
environment: production-media
related_requirement: REQ-0012-object-storage-key-layout
related_bug: BUG-0099-public-sku-main-image-key-staging-path
lifecycle_stage: plan
captured_via: capture
classification_rationale: SKU 图片 staging 路径、缩略图缺失或尺寸不符合当前规则、品牌 Logo/证书图片缩略图缺失、证书图片仍在 files 前缀，均偏离已交付的对象存储 key 布局和媒体缩略图规则，属于生产历史数据与既有规范不一致，因此归类为媒体类 BUG。
---

# 缺陷捕获

## 标题

生产历史媒体对象与缩略图存在规范漂移

## 现象

生产环境中仍存在一批历史媒体数据没有完全符合当前对象存储与缩略图规则：

1. SKU 商品图片未按商品/图片归属目录存储，仍存在 `images/default/tiles/staging/` 目录中。
2. SKU 商品缩略图未按当前尺寸限制重新生成。
3. SKU 商品图片可能缺少同目录 `.thumb` 缩略图。
4. 品牌 Logo 图片可能缺少同目录 `.thumb` 缩略图。
5. 证书图片仍存放在 `files/default/brand-certificates/`，未归入 `images/default/brand-certificates/`。
6. 证书图片可能缺少同目录 `.thumb` 缩略图。

## 期望 vs 实际

- 期望：图片类媒体 key 按当前单 Bucket 与标准前缀策略归位；SKU 图片绑定商品后不再公开引用 staging；品牌 Logo、SKU 图片和证书图片具备真实轻量缩略图；PDF/文档证书继续留在 `files/`。
- 实际：生产历史对象仍存在 staging、files 图片证书、缺缩略图或缩略图不符合当前生成规则的情况，需要批量审计和修复。

## 影响范围

- 生产对象存储 key 规范与对象生命周期。
- SKU 列表、商品卡片、详情页、小程序商品展示的图片加载性能。
- 品牌列表、品牌详情、证书列表和证书详情的图片展示。
- 媒体验收、发布检查和后续对象存储治理。

## 初步线索

- 当前对象存储规则要求 SKU 图片绑定商品后归入 `images/default/tiles/{tile_id}/` 或等价目录，公开主图不应继续引用 staging。
- 当前证书规则要求 JPG、PNG、WebP 图片证书使用 `images/default/brand-certificates/`，PDF 等文档继续使用 `files/default/brand-certificates/`。
- 当前缩略图规则使用同目录 `.thumb` key，并通过后端 resize/compress 生成真实轻量资源，不能只是原图 bytes 复制品。
- 已有脚本可作为基础，但生产外部 MySQL 和 Docker Compose 执行方式需要单独治理。

## 建议验收或复现要点

- [ ] dry-run 统计生产中 staging SKU 图片数量、缺失原图数量、缺失缩略图数量和同 bytes 缩略图数量。
- [ ] dry-run 统计证书图片中仍位于 `files/default/brand-certificates/` 的 JPG/PNG/WebP 数量，确认 PDF 不迁移。
- [ ] apply 后二次审计确认 SKU 公开图片不再引用 暂存目录。
- [ ] apply 后二次审计确认证书图片 key 归入 `images/default/brand-certificates/`。
- [ ] apply 后二次审计确认 SKU、品牌 Logo、证书图片缩略图 object 存在，且不是原图 bytes 复制品。
- [ ] 端侧通过后端受控 `/media/{object_key}` 或等价 URL 展示，不直连未授权对象存储。
- [ ] 批处理过程记录 dry-run/apply/幂等统计摘要，不输出生产密钥、真实客户数据或本机绝对路径。

## 附件

- 暂无。
