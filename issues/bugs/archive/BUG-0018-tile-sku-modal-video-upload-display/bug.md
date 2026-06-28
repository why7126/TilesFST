---
bug_id: BUG-0018-tile-sku-modal-video-upload-display
title: SKU弹窗商品视频上传后未即时回显文件卡片
severity: high
status: approved
owner: product
discovered_at: 2026-06-27 12:03:34
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_change: null
---

# 缺陷说明

瓷砖 SKU 新增/编辑弹窗（`TileSkuFormModal`，`/admin/tile-skus`）中，「商品视频」区域选择 MP4 并完成上传后，**同一弹窗会话内**未出现已上传视频的文件卡片列表项。用户无法确认上传是否成功，与 REQ-0006 多视频管理（AC-035：文件卡片 + 上传状态）及原型 `tile-sku-create-modal` 不一致。

> **Scope 说明**：原 `/capture` 误记为品牌弹窗；经 `/bug-explore` 确认实际场景为 SKU 弹窗。本 BUG **聚焦即时回显**，不包含保存后重开回填或列表页视频计数。

# 复现步骤

1. 以 admin 用户登录 Web 管理端（local 或 Docker 均可）。
2. 进入「瓷砖 SKU」列表页（`/admin/tile-skus`）。
3. 点击「＋ 新增 SKU」或某行「编辑」，打开 SKU 弹窗。
4. 向下滚动至弹窗内 **「商品视频」** 区块。
5. 点击「上传视频」，选择合法 **MP4** 文件并触发上传。
6. 等待上传完成（或观察 Network：`POST /api/v1/admin/uploads/tile-videos` 返回 200）。
7. 检查弹窗内 **同一弹窗会话** 是否立即出现视频文件卡片（文件名、大小/上传状态）。

# 期望结果

- 视频上传成功后，弹窗内 **MUST 立即回显** 已上传视频。
- 展示形式为 **文件卡片**（文件名、大小/时长、上传状态），支持继续添加与移除。
- **不要求** 视频缩略图或 inline 播放器（与 REQ-0006 原型一致）。
- 上传过程 SHOULD 提供可感知的状态反馈（上传中 / 成功 / 失败），对齐 AC-035 与品牌 Logo 上传体验（可参考 BUG-0004 修复模式）。

# 实际结果

- 上传后弹窗中未出现视频文件卡片，功能未生效或即时回显失败。
- 用户无法在上传当次会话内确认视频是否已加入待保存列表。
- 可能叠加体验问题：视频区位于弹窗底部需滚动可见（曾关联 BUG-0011）；缺少上传进度/成功提示时，大文件上传期间 UI 无变化，易被误判为「未生效」。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / SKU 新增弹窗 | 无法确认视频是否上传成功，影响素材维护信心 |
| Web 管理端 / SKU 编辑弹窗 | 同上 |
| REQ-0006 验收 | 阻塞 AC-035（多视频文件卡片 + 上传状态）即时回显验收 |
| 后端 / API | 待 `/bug-complete` 根因确认；上传接口 `POST /api/v1/admin/uploads/tile-videos` 可能正常 |
| 数据库 | 无直接影响（即时回显为前端状态/UI 问题为主） |
| 小程序 / 店主端 | 无直接影响 |

**本 BUG 验收范围**

| 范围 | 是否纳入 |
|---|---|
| 即时回显（当次弹窗会话） | **是** |
| 保存后重开回填 | 否 |
| 列表页视频计数 | 否 |

# 严重等级说明

严重程度为 `high`。

理由：

- **阻塞 SKU 视频素材维护的可确认性**：运营无法在上传后立即看到文件卡片，影响 REQ-0006 核心 FR-005（多视频上传与管理）。
- 影响 Web 管理端 SKU 新增/编辑弹窗，可稳定复现（按 capture 步骤）。
- 不涉及数据丢失或安全边界，但优先级应高于纯视觉 medium 类缺陷。
- 修复面预计集中在前端 `TileSkuFormModal` 视频上传状态与列表回显；是否涉及 API 响应需在 `/bug-complete` 阶段确认。

# 代码线索

| 线索 | 路径 |
|---|---|
| SKU 弹窗组件 | `src/web/src/features/admin/components/TileSkuFormModal.tsx`（`handleVideoUpload`、`videos` state、`.sku-video-list`） |
| 视频上传 API 封装 | `src/web/src/features/admin/api/tile-skus-api.ts`（`uploadTileVideo`） |
| 后端上传端点 | `src/backend/app/api/v1/uploads.py`（`upload_tile_video`） |
| 弹窗样式 | `src/web/src/features/admin/styles/tile-sku-management.css`（`.sku-video-*`） |
| 列表页入口 | `src/web/src/pages/admin/TileSkuManagementPage.tsx` |
| 参照（Logo 上传状态机） | `src/web/src/features/admin/components/BrandFormModal.tsx` |
| 弹窗原型 | `issues/requirements/archive/REQ-0006-tile-sku-management/prototype/web/tile-sku-create-modal.html` |
| 关联缺陷 | BUG-0011（弹窗滚动）、BUG-0004（上传进度模式） |

# 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（REQ-0006 已实现视频区，即时回显/上传状态未达标） |
| 根因类型 | 待 `/bug-complete` 确认（预计 frontend-ui / 上传反馈链路） |
| 建议修复 | 对齐 AC-035：上传状态 + 成功后文件卡片即时展示；必要时 `scrollIntoView` 至视频区 |
