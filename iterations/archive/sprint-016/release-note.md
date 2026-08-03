---
sprint_id: sprint-016
title: Sprint 016 Release Note
status: published
created_at: 2026-08-01 07:31:37
updated_at: 2026-08-01 08:28:07
---

# Sprint 016 Release Note

## 计划交付

- 优化管理端 SKU 列表默认排序：未上架 SKU 优先展示。
- 未上架 SKU 组内按创建时间倒序展示，帮助运营优先处理最新录入但未上架的 SKU。
- 已上架 SKU 组内按发布时间倒序展示，保持已发布商品的时间顺序可预期。
- SKU 下架后仍展示最近一次发布时间，便于运营复核历史发布记录。
- 保持管理端 SKU 列表既有筛选、分页、搜索、上下架、素材列和操作列行为不回归。
- 修复公开商品主图对象 key 长期停留在 `images/default/tiles/pending/...` 的问题，绑定 SKU 后归入商品目录。
- 补齐主图缩略图真实缩小策略，并让原图与缩略图随历史 pending 迁移进入同一商品目录。
- 修复 `media_type=tile-sku` 缩略图与原图大小一致的问题，确保新生成 `.thumb.*` 对象真实缩小并可被公开接口和小程序继续使用。
- 支持历史同尺寸或字节一致 `.thumb` 对象的审计与幂等再生成计划。

发布状态：已发布。Sprint 016 范围内 3 个 Change 均已实现并归档，关联 REQ/BUG 已完成闭环。

## 影响范围

- 影响：管理端 Web SKU 列表展示顺序、后端 SKU 列表默认排序、SKU 图片对象 key、缩略图生成、历史 pending 主图迁移、历史同尺寸 `.thumb` 审计/再生成、审计脚本。
- 可能影响：管理端 SKU 列表 API/OpenAPI/Orval，取决于实现是否调整或显式化排序契约；公开 SKU 图片响应契约，取决于是否暴露新的图片字段。
- 不影响：数据库表结构、店主端 Web、Docker Compose。

## 发布风险

- 中等风险。排序项主要风险为分组优先级、未上架 `created_at` 降序、已上架 `published_at` 降序之间的组合顺序实现偏差，以及前端列表展示与后端排序出现二次排序冲突。媒体项主要风险为历史 pending 对象迁移遗漏、URL 不可访问、小程序图片渲染失败或缩略图仍无带宽收益。需通过后端排序测试、前端展示顺序测试、对象存储存在性验证、小程序图片渲染验证和 admin/media 横切验收确认。

## 关联范围

| 类型 | 编号 | Change | 状态 |
|---|---|---|---|
| REQ | REQ-0087-admin-sku-list-sort-optimization | update-admin-sku-list-sort-optimization | archived |
| BUG | BUG-0099-public-sku-main-image-key-pending-path | fix-public-sku-main-image-pending-path | archived |
| BUG | BUG-0100-thumbnail-size-equals-original | fix-media-thumbnail-generation | archived |
