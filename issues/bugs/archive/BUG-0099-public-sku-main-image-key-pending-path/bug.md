---
bug_id: BUG-0099-public-sku-main-image-key-pending-path
title: 公开商品主图对象 key 仍停留在 pending 暂存路径
severity: high
status: done
owner: null
discovered_at: 2026-08-01 07:12:45
environment: backend-media
related_requirement: null
related_change: null
created_at: 2026-08-01 07:22:02
updated_at: 2026-08-01 08:06:26
---

# 现象

公开商品主图已经完成商品绑定，并会进入店主 Web 展示端与微信小程序公开商品列表/详情页，但大量主图对象 key 仍位于 `images/default/tiles/pending/...`。

`pending` 在当前上传链路中用于无 `tile_id` 的 SKU 图片上传暂存路径。上传阶段出现该前缀是合理的，但商品保存、设为主图或发布后仍长期保留该路径，会让公开商品素材看起来仍处于未绑定暂存状态。

# 复现步骤

1. 在管理端新建 SKU，先上传 SKU 主图。
2. 保存 SKU，并确保该图片被标记为主图。
3. 将 SKU 发布为公开商品。
4. 查看数据库 `tile_images.object_key`、管理端详情或公开端返回的商品主图 URL。
5. 观察该公开商品主图是否仍为 `images/default/tiles/pending/...` 或 `/media/images/default/tiles/pending/...`。

# 期望 vs 实际

- 期望：SKU 图片在完成商品绑定、主图设置或发布后，应迁移到商品自身稳定目录，或至少进入明确的已绑定商品图片目录；`pending` 仅保留未绑定、未发布、可过期清理的临时对象。
- 实际：当前创建/保存 SKU 时，后端把上传返回的 `object_key` 原样写入 `tile_images`；发布 SKU 时只更新商品状态和发布时间，不会迁移对象或重写 key，导致公开主图继续停留在 `pending` 路径。

# 影响范围

- 后端媒体上传接口：`/api/v1/admin/uploads/tile-images`。
- 管理端 SKU 创建、编辑、主图保存、发布流程。
- 数据库 `tile_images.object_key` 与公开商品主图引用。
- 微信小程序商品卡片和商品列表：公开接口会基于主图 key 生成同目录 `.thumb` 缩略图 URL，pending 主图会继续派生 pending 缩略图 URL。
- 对象存储生命周期与清理策略：若后续按 `pending` 语义清理临时对象，可能误删公开商品图片。
- 存量公开商品图片迁移或兼容策略。

# 严重等级说明

严重等级为 `high`。

理由：

- 影响公开商品主图的对象生命周期语义，不只是后台路径展示问题。
- 公开端会继续访问 pending 路径及其同目录缩略图。
- 一旦引入 pending 清理任务或对象生命周期策略，存在公开商品主图丢失风险。
- 修复可能涉及对象复制/迁移、数据库引用更新、缩略图同步和存量数据迁移，需要谨慎设计和回归测试。

# 初步定位

- 上传 SKU 图片时，如果没有 `tile_id`，后端会生成 `tiles/pending` 资源路径。
- SKU 创建时，业务保存阶段调用图片替换逻辑，但当前逻辑直接保存上传返回的 `object_key`。
- SKU 发布时只更新发布状态，不处理媒体对象路径。
- 现有审计脚本已把公开商品主图位于 `images/default/tiles/pending/` 识别为 `pending_main_image` 指标。

# 建议后续分析

- 明确商品图片绑定后的目标 key 形态，例如 `images/default/tiles/{tile_id}/<uuid>.<ext>`。
- 评估新建 SKU、编辑已有 SKU、新增图片、删除图片、主图切换、发布/下架各阶段是否需要迁移。
- 设计对象迁移的失败回滚策略，避免数据库引用已更新但对象复制失败。
- 设计存量 pending 主图迁移脚本，要求 dry-run、可重入、输出统计摘要。
- 同步处理同目录缩略图 key，避免公开端缩略图访问回退到原图或 404。
