---
bug_id: BUG-0116-prod-media-historical-object-drift
title: 生产历史媒体对象与缩略图存在规范漂移根因分析
severity: high
created_at: 2026-08-04 10:43:35
updated_at: 2026-08-04 10:43:35
---

# 生产历史媒体对象与缩略图存在规范漂移根因分析

## 直接原因

当前对象存储和缩略图规则已经要求图片类媒体使用标准图片前缀、同目录 `.thumb` 缩略图和后端受控 `/media/{object_key}` 读取，但生产环境仍保留了规则演进前产生的历史对象引用。历史引用没有在规则交付后完成统一审计、迁移、缩略图回填和二次校验，导致 SKU 商品图片、品牌 Logo 和品牌证书图片三类对象出现漂移。

具体直接原因包括：

- SKU 图片新建前允许使用 `images/default/tiles/staging/` 暂存目录，但部分历史公开主图未在绑定商品或公开展示后正式化到 `images/default/tiles/{tile_id}/`。
- SKU 图片、品牌 Logo 和证书图片在历史上传或历史迁移阶段未统一生成同目录 `.thumb` 缩略图，或旧缩略图可能只是原图复制品，不符合当前 resize/compress 轻量缩略图规则。
- 品牌证书功能演进后，图片类证书应迁移到 `images/default/brand-certificates/`，但历史 JPG、PNG、WebP 证书图片仍可能保留在 `files/default/brand-certificates/`。
- PDF 等文档类证书仍应保留在 `files/default/brand-certificates/`，因此迁移逻辑必须按 MIME/扩展名分流，不能用简单前缀替换一次性处理全部证书。

## 根本原因

根本原因是媒体对象 key 布局和缩略图策略在多次能力迭代中逐步收敛，但缺少覆盖生产历史数据的统一治理闭环。新上传链路和历史兼容读取各自解决了局部问题，但没有形成一套面向生产外部数据库和对象存储的完整维护流程。

治理缺口包括：

- 缺少一次性覆盖 SKU、品牌 Logo、证书图片三类对象的生产 dry-run 汇总和风险分级。
- 缺少“key 迁移、object 存在性、缩略图回填、受控 URL、端侧渲染”的四联闭环验收记录。
- 现有脚本各自覆盖部分场景，命名和职责不够直观，容易把品牌 Logo 缩略图、证书图片迁移或 SKU 暂存 正式化遗漏在不同脚本之间。
- 生产外部 MySQL 和对象存储执行方式需要独立治理；如果没有备份、dry-run、apply、幂等和二次审计证据，不能安全执行批量修复。

## 触发条件

- 历史 SKU 主图在公开状态下仍引用 `images/default/tiles/staging/`。
- 历史 SKU 图片、品牌 Logo 或证书图片没有同目录 `.thumb` object。
- 历史缩略图与原图 size 或 bytes 一致，无法体现当前缩略图收益。
- 历史品牌证书图片仍使用 `files/default/brand-certificates/`。
- 端侧列表或详情页优先使用缩略图 URL 时，缺失缩略图会触发原图回退、加载变慢、占位或失败态。

## 分类

- 类型：历史数据治理 / object-storage / media / migration
- 影响层：数据库引用、对象存储 object、媒体代理 URL、Web 管理端、店主 Web、小程序
- 是否回归：不是单一代码回归，更接近规则演进后的生产历史数据漂移。
- 关联需求：`REQ-0012-object-storage-key-layout`
- 关联缺陷：`BUG-0099-public-sku-main-image-key-staging-path`

## 排查线索

- `scripts/migrate-staging-tile-images.py` 可作为公开 SKU 暂存主图正式化的基础。
- `scripts/audit-miniapp-card-images.py` 可作为公开 SKU 主图、缩略图存在性和缩略图同 bytes 审计的基础。
- `scripts/backfill-brand-certificate-thumbnails.py` 当前会扫描 `brands.logo_object_key`、`brand_certificates.file_key` 和 `brand_certificate_images.file_key`，可作为品牌 Logo 与证书图片缩略图回填基础。
- `scripts/migrate_object_keys.py` 与 `src/backend/app/modules/media/key_migration.py` 可作为历史 `files/default/brand-certificates/*.{jpg,jpeg,png,webp}` 迁移到 `images/default/brand-certificates/` 的基础；PDF 不应迁移。
