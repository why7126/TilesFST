---
note: workflow-sync — 3/3 Change 已 archive；0 applied；待人工 sign-off
sprint_id: sprint-016
title: Sprint 016 Acceptance Report
status: accepted
created_at: 2026-08-01 07:31:37
updated_at: 2026-08-01 08:30:46
---

# Sprint 016 Acceptance Report

## 验收状态

最终结论：通过。Sprint 016 正式范围内 1 个 REQ、2 个 BUG 与 3 个 OpenSpec Change 均已完成实现、验证和归档；关联 Issue 已进入 archive 阶段。

## 正式范围

| 类型 | 编号 | Change | 状态 | 验收 |
|---|---|---|---|---|
| REQ | REQ-0087-admin-sku-list-sort-optimization | update-admin-sku-list-sort-optimization | done，已归档（`update-admin-sku-list-sort-optimization` archived 2026-08-01 08:05:03） | 通过 |
| BUG | BUG-0099-public-sku-main-image-key-pending-path | fix-public-sku-main-image-pending-path | done，已归档（`fix-public-sku-main-image-pending-path` archived 2026-08-01 07:43:29） | 通过 |
| BUG | BUG-0100-thumbnail-size-equals-original | fix-media-thumbnail-generation | done，已归档（`fix-media-thumbnail-generation` archived 2026-08-01 08:28:07） | 通过 |

## 验收清单

- [x] 管理端 SKU 列表默认排序先展示未上架 SKU，再展示已上架 SKU。
- [x] 未上架 SKU 组内按创建时间降序展示。
- [x] 已上架 SKU 组内按发布时间降序展示。
- [x] 混合上架状态、同组多条记录和发布时间为空边界排序稳定。
- [x] 搜索、品牌筛选、类目筛选、状态筛选与分页组合后仍保持排序规则。
- [x] 上下架操作后列表刷新顺序符合新规则。
- [x] SKU 下架后，管理端列表、详情与下架响应仍展示最近一次发布时间。
- [x] SKU 列表不新增排序控件，不改变既有筛选区、表格卡片、分页、素材列、状态列和操作列结构。
- [x] SKU 列表筛选区参照其他管理端列表页铺满 filter-card 可用宽度，右侧无多余空列。
- [x] fixed toast、DS confirm/window.confirm 与列表页横切行为不回归。
- [x] 如 API 排序契约发生变化，OpenAPI、Orval、API 文档和相关测试已同步。
- [x] 公开商品主图对象 key 不再保留在 `images/default/tiles/pending/...` 暂存路径。
- [x] 新建 SKU、编辑 SKU 图片、发布 SKU 或等价绑定流程均将主图归入商品目录。
- [x] 原图与缩略图位于同一商品目录，且缩略图尺寸真实小于原图。
- [x] 新上传 `media_type=tile-sku` 主图后，`.thumb.*` 对象不是原图字节复制，像素尺寸小于原图且对象大小合理下降。
- [x] 缩略图生成覆盖 JPEG、PNG、WebP、小图、透明 PNG 与异常图片边界。
- [x] 历史同尺寸或字节一致 `.thumb` 对象可被审计并支持 dry-run、apply、幂等再生成与失败回滚窗口说明。
- [x] 历史 pending 主图迁移支持 dry-run、apply、幂等与失败回滚窗口说明。
- [x] 后端媒体 URL 可访问，对象存储对象存在，小程序卡片图片可渲染。
- [x] `scripts/audit-miniapp-card-images.py` 不再对已公开主图报告 `pending_main_image`。
- [x] 小程序图片仍优先使用可用缩略图 URL，加载失败时具备既有降级行为且不回归卡片布局。

## 验证记录

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-08-01 08:05:03 | `/opsx-archive update-admin-sku-list-sort-optimization` | 已归档并完成 REQ-0087 archive promote |
| 2026-08-01 07:58:44 | `/opsx-apply fix-public-sku-main-image-pending-path` | 已执行，49 个相关 pytest 通过；迁移 dry-run total=0；OpenSpec strict 通过 |
| 2026-08-01 08:06:04 | `/opsx-archive fix-public-sku-main-image-pending-path` | 已归档并完成 BUG-0099 archive promote |
| 2026-08-01 08:10:23 | `/opsx-apply fix-media-thumbnail-generation` | 已执行，14 个直接相关 pytest 通过；审计 dry-run 输出安全；后端 Docker build 与容器内 Pillow 导入验证通过；OpenSpec strict 通过 |
| 2026-08-01 08:28:07 | `/sprint-archive sprint-016` | readiness 通过；3/3 Change archived；issue promote gate 通过；AI usage 使用 estimated_fallback/stale 警告 |
