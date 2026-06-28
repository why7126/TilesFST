---
bug_id: BUG-0018-tile-sku-modal-video-upload-display
status: captured
created_at: 2026-06-27 12:03:34
updated_at: 2026-06-27 13:45:04
severity_hint: high
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_bug: BUG-0011-tile-sku-modal-content-overflow
captured_via: capture
classification_rationale: 经 /bug-explore 确认实际场景为瓷砖 SKU 新增/编辑弹窗（/admin/tile-skus），非品牌弹窗；商品视频上传后弹窗内无即时文件卡片回显，属 REQ-0006 多视频管理实现/体验缺口，非新需求。
scope_note: 原 /capture 误记为品牌弹窗；组件为 TileSkuFormModal，需求归属 REQ-0006。
---

# 现象

瓷砖 SKU 新增/编辑弹窗（`/admin/tile-skus`）中，「商品视频」区域选择 MP4 并上传后，弹窗内未出现已上传视频的文件卡片列表项，用户无法确认上传是否成功。

# 复现步骤

1. 以 admin 登录 Web 管理端。
2. 进入 **瓷砖 SKU** 列表页（`/admin/tile-skus`），点击「＋ 新增 SKU」或某行「编辑」，打开 SKU 弹窗。
3. 向下滚动至弹窗内 **「商品视频」** 区块。
4. 点击「上传视频」，选择合法 **MP4** 文件并触发上传。
5. 等待上传完成（或观察 Network：`POST /api/v1/admin/uploads/tile-videos` 返回 200）。
6. 检查弹窗内 **同一弹窗会话** 是否立即出现视频文件卡片（文件名、大小/上传状态）。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 视频上传成功后，弹窗内 **MUST 立即回显** 已上传视频，以 **文件卡片** 展示（文件名、大小/时长、上传状态），支持继续添加与移除；**不要求** 视频缩略图或 inline 播放器（与 REQ-0006 原型 `tile-sku-create-modal` 一致）。 |
| **实际** | 上传后弹窗中未出现视频文件卡片，功能未生效或即时回显失败。 |

# 验收范围

| 范围 | 是否纳入本 BUG |
|---|---|
| **即时回显** | **是** — 上传完成当次弹窗内 MUST 出现视频文件卡片 |
| 保存后重开回填 | 否（可单独跟踪；本 capture 聚焦即时回显） |
| 列表页视频计数 | 否 |

# 探索备注（/bug-explore）

- 品牌弹窗（`BrandFormModal`）无视频上传能力；本缺陷 scope 已修正为 SKU 弹窗（`TileSkuFormModal`）。
- 可能叠加因素：弹窗需滚动至底部视频区（曾关联 BUG-0011）；缺少上传进度/成功状态反馈（可参考 BUG-0004 品牌 Logo 模式）。

# 附件

- 暂无截图。
