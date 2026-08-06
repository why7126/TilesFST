---
requirement_id: REQ-0098-admin-media-list-thumbnails
acceptance_status: passed
created_at: 2026-08-05 09:20:54
updated_at: 2026-08-06 08:23:35
---

# 验收标准

## 功能 AC

- [x] AC-001 SKU 列表接口对存在主图的列表项返回 `main_image_thumbnail_url`，且保留 `main_image_url` 原有语义。
- [x] AC-002 SKU 列表页图片展示优先级为 `main_image_thumbnail_url` → `main_image_url` → 既有无图占位。
- [x] AC-003 Banner 列表接口对存在图片的列表项返回 `image_thumbnail_url`，且保留 `image_url` 原有语义。
- [x] AC-004 Banner 列表页图片展示优先级为 `image_thumbnail_url` → `image_url` → 既有无图占位。
- [x] AC-005 Banner 图片来源为 SKU 主图、SKU 图集、品牌 Logo、专题封面或自定义上传时，`image_thumbnail_url` 与最终 `image_object_key` 指向的资源一致。
- [x] AC-006 品牌列表复核通过：优先使用缩略图字段，缺失时回退原图或首字母占位。
- [x] AC-007 证书列表复核通过：图片证书优先使用缩略图字段，缺失时回退原文件或文件类型占位。
- [x] AC-008 缩略图 URL 为空、404 或加载失败时，列表不得显示浏览器默认破图，不得阻塞行操作。
- [x] AC-009 详情、编辑、上传预览、放大预览和原文件查看仍使用原图或原文件，不因列表缩略图优化降低清晰度。
- [x] AC-010 新增响应字段同步 OpenAPI 与 Orval，前端不得手写与后端重复的接口类型。
- [x] AC-011 后端测试覆盖 SKU/Banner 新字段返回、空图字段和原图字段兼容性。
- [x] AC-012 前端测试覆盖 SKU/Banner 列表缩略图优先级、fallback 和无图态。
- [x] AC-013 验收记录包含至少一组 URL/render 证据，能说明列表加载的是缩略图，详情或预览仍可访问原图。

## 非功能 AC

- [x] AC-NF-001 不新增或修改 SQLite/MySQL 表结构。
- [x] AC-NF-002 不改变媒体上传鉴权、MinIO 单桶策略和后端受控 `/media/{object_key}` 访问边界。
- [x] AC-NF-003 列表图片容器尺寸稳定，缩略图、原图或占位切换不造成表格行高和列宽抖动。
- [x] AC-NF-004 管理端样式继续使用 Design System semantic token，不新增裸 Hex 或临时视觉体系。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 复发类缺陷

- [x] AC-XCUT-001 分页 DOM 若被本需求触碰，必须保持左侧 `page-summary` 与右侧 `page-right` 结构，并与用户管理基准一致；若未触碰分页，验收记录标注 `N/A — 本需求不修改分页结构`。
- [x] AC-XCUT-002 摘要指标卡若被本需求触碰，DOM 必须继续使用 `.metric-label` / `.metric-value` / `.metric-desc`；若未触碰指标卡，验收记录标注 `N/A — 本需求不修改指标卡`。
- [x] AC-XCUT-003 筛选下拉若被本需求触碰，必须复用既有 shared admin filter select 或给出等价 shared wrapper 理由；若未触碰筛选区，验收记录标注 `N/A — 本需求不修改筛选下拉`。
- [x] AC-XCUT-004 本需求引入的成功/失败反馈若使用 toast，必须为 fixed toast，不得通过文档流 notice 推挤 hero 或表格布局。
- [x] AC-XCUT-005 若本需求新增或触发状态变更类操作，必须使用 Design System confirm modal；本需求不新增状态操作时，验收记录标注 `N/A — 本需求不新增状态变更操作`。
- [x] AC-XCUT-006 代码与测试中不得新增 `window.confirm`。
- [x] AC-XCUT-007 管理端列表图片加载失败、fallback 与占位展示不得改变 sticky action column、表格滚动容器或操作列布局。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-06 08:23:35
accepted_by: workflow-sync
source_change: optimize-admin-media-list-thumbnails
source_sprint: sprint-020
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

