---
sprint_id: sprint-015
title: Sprint 015 Release Note
status: published
created_at: 2026-07-31 15:17:00
updated_at: 2026-07-31 23:07:14
---

# Sprint 015 Release Note

## 计划交付

- 修复管理后台瓷砖 SKU 列表素材列展示冗余：素材列只显示图片数量与视频数量，不再显示主图状态标签。
- 修复管理后台瓷砖 SKU 页类目筛选只能选择一级类目的问题：改为级联选择控件，并支持父类目包含所有子孙类目 SKU。
- 删除管理后台瓷砖 SKU 列表素材完整度条件筛选，保留图片/视频数量识别能力。
- 修复管理端类目树右侧计数口径：节点显示下一层级类目数量，“全部类目”显示顶层类目数量。
- 统一管理端筛选条件下拉框位置和 UI 样式：以瓷砖类目页为基准，覆盖品牌、类目、规格、品牌证书、Banner、用户、系统设置、日志审计、接口文档和界面主题等页面。
- 优化微信小程序品牌列表页 UI 与交互体验：新版品牌 Hero、品牌矩阵、单品牌卡片和类目胶囊独立点击，去除品牌矩阵与类目区说明性冗余文案，并将类目胶囊字号调整为比品牌名称小 2rpx。
- 修复微信小程序商品列表图片加载优化后的无图回归：补齐同路径缩略图生成、历史回填、审计和列表 `cover_image` 可访问性。

发布状态：已发布到 Sprint 归档记录。2026-07-31 23:07:14 关闭 Sprint 时，6/6 Change 已归档，范围内 REQ/BUG 均为 done。

## 影响范围

- 影响：管理端 Web SKU 列表筛选与展示、管理端筛选下拉 UI 一致性、管理端类目树展示、微信小程序品牌列表页、微信小程序商品卡片图片展示、后端公开列表 `cover_image`、对象存储缩略图生成与历史回填。
- 可能影响：管理端 SKU 列表 API/OpenAPI/Orval、管理端类目树 API/OpenAPI/Orval、品牌列表公开接口/OpenAPI/Orval、公开 SKU 列表接口文档，取决于 SKU 类目筛选参数语义、直接子类目数量字段、品牌类目 `categoryId` 和 `cover_image` URL 语义是否已暴露。
- 不影响：数据库表结构、Docker Compose。

## 发布风险

- 中风险。主要风险为 SKU 父类目筛选子树范围不完整、级联控件布局回归、管理端筛选下拉横向统一时弹层裁切或样式分化、素材列提示误删、类目树计数字段误绑、小程序品牌/类目点击边界误触、商品卡片缩略图回填失败、列表继续返回不可访问媒体 URL 或小程序图片性能回归，需通过前后端测试、小程序静态测试、对象存储回填 dry-run、必要接口测试和视检确认。

## 关联范围

| 类型 | 编号 | Change | 状态 |
|---|---|---|---|
| REQ | REQ-0086-miniapp-brand-list-ui-interaction-optimization | update-miniapp-brand-list-ui-interaction-optimization | done，已归档 |
| BUG | BUG-0096-admin-sku-category-filter-only-top-level | fix-admin-sku-category-cascade-filter | done，已归档 |
| BUG | BUG-0097-admin-sku-material-main-image-tag-redundant | fix-admin-sku-material-main-image-tag | done，已归档 |
| BUG | BUG-0095-admin-category-tree-count-shows-product-count | fix-admin-category-tree-count | done，已归档 |
| BUG | BUG-0094-miniapp-list-images-not-loading-after-speed-fix | fix-miniapp-product-card-thumbnails | done，已归档 |
| BUG | BUG-0098-admin-filter-dropdown-ui-consistency | fix-admin-filter-dropdown-ui-consistency | done，已归档 |
