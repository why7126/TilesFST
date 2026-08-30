## ADDED Requirements

### Requirement: 生产媒体维护作业必须覆盖 Banner 自定义上传图

生产媒体维护作业 MUST 将 Banner 自定义上传图纳入历史图片派生图维护范围。对于 `banners.image_object_key` 指向 `images/default/banners/` 或等价 Banner 自定义上传目录的 JPEG、PNG、WebP 原图，系统 MUST 能通过 dry-run 报告缺失或不合格的 `thumbnail` 与 `display` 派生图，并能在 apply 中生成同目录 WebP `.thumb.webp` 与 `.display.webp`。当 Banner 原图已迁入 `images/default/banners/{banner_id}/` 目录时，作业 MUST 同步维护历史无 id URL 的同名 WebP alias，避免旧 `/media/images/default/banners/<filename>.thumb.webp` 或 `.display.webp` fallback 到原图。维护作业 MUST 保留原图格式和访问语义，MUST NOT 删除原图或已有合格派生图。

#### Scenario: Banner 派生图 dry-run

- **WHEN** 运维执行 `backfill-image-variants` dry-run
- **AND** 数据库存在 `banners.image_object_key` 指向 `images/default/banners/` 的历史自定义上传图片
- **AND** 对应 `.thumb.webp` 或 `.display.webp` 对象缺失或不合格
- **THEN** 作业 MUST 在候选或摘要中包含 Banner 来源，来源类型 SHOULD 为 `banner_image`
- **AND** 作业 MUST 报告缺失规格、预计写入对象数量、跳过原因和失败分类
- **AND** 对已迁入 `images/default/banners/{banner_id}/` 的 Banner，作业 MUST 报告旧无 id 路径 alias 是否缺失或不合格
- **AND** dry-run MUST NOT 写数据库
- **AND** dry-run MUST NOT 写对象存储
- **AND** dry-run MUST NOT 删除对象
- **AND** 输出 MUST 保持脱敏。

#### Scenario: Banner 派生图 apply

- **GIVEN** Banner 派生图 dry-run 已通过
- **AND** MySQL 快照与对象存储 bucket / prefix 快照已完成
- **WHEN** 运维显式执行 `backfill-image-variants --apply --confirm-backup`
- **THEN** 作业 MUST 为支持格式的 Banner 原图生成同目录 WebP `.thumb.webp` 与 `.display.webp`
- **AND** 对已迁入 `images/default/banners/{banner_id}/` 的 Banner，作业 MUST 为旧无 id 路径生成或覆盖同名 WebP alias
- **AND** 作业 MUST NOT 改写 `banners.image_object_key`
- **AND** 作业 MUST NOT 改写原图对象格式或原图访问语义
- **AND** 输出 MUST 包含成功、失败、跳过、重试候选和失败原因统计
- **AND** 重复执行 MUST 保持幂等。

#### Scenario: 聚合维护任务包含 Banner 缩略图候选

- **WHEN** 运维执行 `media-drift-reconcile` dry-run 或 apply
- **THEN** 聚合任务 MUST 通过缩略图回填或等价子任务覆盖 Banner `.thumb.webp` 缺失候选
- **AND** 顶层摘要或子任务摘要 MUST 不把 Banner 缺失缩略图遗漏为 0
- **AND** 仍 MUST 保持对象存储不可达 blocked 传播、失败分类、脱敏输出和 `--apply --confirm-backup` 写入门禁。

#### Scenario: Banner 派生图 URL 二次审计

- **WHEN** Banner 派生图 apply 完成
- **THEN** 运维 MUST 能用 `/media/...thumb.webp` 与 `/media/...display.webp` 验证派生图 URL
- **AND** 历史无 id Banner 派生图 URL 若仍被访问，也 MUST 直接命中 WebP alias
- **AND** 成功响应 MUST 返回 `Content-Type: image/webp`
- **AND** 成功响应 MUST NOT 出现 `x-media-fallback: 1`
- **AND** 验收记录 SHOULD 包含 Content-Length 对比、对象 MIME、幂等 dry-run 摘要和端侧 render evidence。
