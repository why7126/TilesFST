---
bug_id: BUG-0018-tile-sku-modal-video-upload-display
status: pending_review
created_at: 2026-06-27 13:47:16
updated_at: 2026-06-27 13:47:16
related_requirement: REQ-0006-tile-sku-management
---

# 回归验收标准

> 修复本缺陷 MUST 满足 REQ-0006 **AC-035** 中与 **即时回显、上传状态** 相关条款，且 **不得回归** BUG-0011 弹窗滚动与 AC-031～AC-034 图片能力。  
> **Scope**：仅验收 **同一弹窗会话内即时回显**；保存后重开回填、列表页视频计数 **不在本 BUG 必验范围**。

## AC-001 选择 MP4 后 MUST 触发授权上传

**Given** admin 已打开 SKU 新增或编辑弹窗，并位于「商品视频」区块  
**When** 点击「上传视频」并选择合法 MP4  
**Then** 系统 MUST 立即触发 `POST /api/v1/admin/uploads/tile-videos`  
**And** 不得要求先保存 SKU 后才开始上传

## AC-002 上传过程中 MUST 展示可感知状态（对齐 AC-035）

**Given** 用户已选择 MP4 文件  
**When** 上传正在进行  
**Then** 「商品视频」区块 MUST 展示 **上传中** 状态（进度条、百分比或等价文案）  
**And** 状态 MUST 经过 `idle → uploading → uploaded / failed`  
**And** 上传中 SHOULD 禁用重复点击「上传视频」或进入 uploading 态  
**And** 上传中 MUST 禁止提交保存（与 `BrandFormModal` Logo 行为一致）

## AC-003 上传成功后 MUST 即时回显文件卡片（本 BUG 核心）

**Given** 上传接口返回 200 且含有效 `object_key`  
**When** 上传完成（**同一弹窗会话，未关闭弹窗**）  
**Then** 「商品视频」区块 MUST **立即** 出现文件卡片（`.sku-video-card` 或等价）  
**And** 卡片 MUST 展示 **文件名** 与 **大小**（或占位「—」）  
**And** **不要求** 视频缩略图或 inline 播放器（与原型 `tile-sku-create-modal` 一致）  
**And** 卡片 MUST 提供「移除」入口  
**And** 区域 SHOULD 展示简短成功提示（如「视频已添加」）

## AC-004 上传失败 MUST 在视频区内展示错误

**Given** 上传失败、网络异常或非 MP4 文件  
**When** 上传流程结束  
**Then** 「商品视频」区块 MUST 进入 `failed` 状态并展示 **明确错误信息**（不得仅依赖弹窗顶部 notice）  
**And** 用户 MUST 可重新选择文件重试  
**And** 失败时列表 MUST NOT 静默保持为空且无说明

## AC-005 支持继续添加多个视频

**Given** 已有一个视频文件卡片  
**When** 再次点击「上传视频」并选择另一个 MP4  
**Then** 新卡片 MUST 追加到列表  
**And** 先前卡片 MUST 保留

## AC-006 修复范围与回归

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 SQLite schema 或 SKU CRUD API 契约（除非发现独立缺陷并另开 Change）  
**And** BUG-0011 弹窗 `.modal-body` 滚动 MUST 仍可用  
**And** SKU 图片上传与主图逻辑 MUST 无回归

## AC-007 测试与记录

**Given** 进入 `fix-tile-sku-modal-video-upload-display`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** MUST 补充 `TileSkuFormModal` Vitest：mock `uploadTileVideo` 成功后断言 `.sku-video-card` 与上传状态文案  
**And** SHOULD 覆盖上传失败时的区域错误展示  
**And** MUST 在 Change `trace.md` 记录即时回显手工验收结论

## AC-008 REQ-0006 AC-035 对齐确认

**Given** BUG-0018 修复完成  
**When** 对照 `issues/requirements/REQ-0006-tile-sku-management/acceptance.md` AC-035  
**Then** 「支持上传多个视频；以文件卡片展示名称、大小/时长、**上传状态**」中与 **即时回显 + 上传状态** 相关的 MUST 条款 MUST 全部满足
