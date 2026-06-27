## Why

[BUG-0018-tile-sku-modal-video-upload-display](issues/bugs/BUG-0018-tile-sku-modal-video-upload-display/) 已评审通过并纳入 `sprint-002`。瓷砖 SKU 新增/编辑弹窗（`TileSkuFormModal`，`/admin/tile-skus`）中，用户在「商品视频」区块选择 MP4 并完成上传后，**同一弹窗会话内**无法感知上传进度、成功或失败，且文件卡片回显缺乏可感知锚点，表现为「上传后未显示 / 功能未生效」。

根因已确认为前端 UX/反馈链路未闭环（非 MinIO 或上传 API 缺失）。`add-tile-sku-management` 实现了最小上传路径，但未落实 REQ-0006 **AC-035** 的「上传状态 + 文件卡片即时回显」；`fix-brand-logo-upload-progress`（BUG-0004）已在 `BrandFormModal` 建立状态机模板，SKU 视频区未横向同步。根据项目规则，已评审缺陷 MUST 使用新的 `fix-*` change 修复。

## What Changes

- 为 `TileSkuFormModal`「商品视频」区块引入 `idle → uploading → uploaded / failed` 上传状态机，对齐 `BrandFormModal` Logo 模式。
- 上传中展示进度条、百分比或等价「上传中」文案；上传中禁用重复选择与保存。
- 上传成功后 **立即** 在视频区内追加 `.sku-video-card`（文件名、大小），并展示区域级成功提示。
- 上传失败时在 **视频区内** 展示明确错误（不得仅依赖弹窗顶部 `.admin-notice`）。
- 可选：`uploadTileVideo` 增加 `onUploadProgress` 回调（对齐 `uploadBrandLogo`）。
- 补充 Vitest：mock `uploadTileVideo` 成功/失败，断言卡片与状态文案；回归 BUG-0011 弹窗滚动与 SKU 图片上传。
- **Scope**：仅即时回显 + 上传状态；保存后重开回填、列表页视频计数不在本 change 必选项。

## Capabilities

### New Capabilities

（无 — 本 change 修复既有 SKU 管理能力，不引入新 capability 域。）

### Modified Capabilities

- `web-client`：新增 SKU 弹窗商品视频上传状态与即时回显修复 requirement。
- `tile-sku-management`：新增 AC-035 对齐的 SKU 弹窗视频上传 UX requirement（视觉验收 gate 补充）。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `/admin/tile-skus` 新增/编辑弹窗「商品视频」区块交互 |
| REQ-0006 | 满足 AC-035 即时回显与上传状态；不修改 AC-031～034 图片能力 |
| 后端 API | 默认不变更 schema；可选前端封装增加 progress 回调 |
| 数据库 | 不变 |
| Orval | 默认不需要 |
| MinIO | 复用既有 `tile-videos` 前缀与授权上传 |
| 小程序 / 店主端 | 不涉及 |
| 测试 | Vitest 补充 `TileSkuFormModal` 视频上传用例 |
| Design System | 进度条、错误态、成功文案 MUST 使用 semantic token，禁止裸 Hex |

## Rollback Plan

若修复引起 SKU 弹窗视频上传异常，可回滚本 change 涉及的前端改动：

1. 恢复 `TileSkuFormModal.tsx` 视频上传状态机与区域反馈至修复前。
2. 恢复 `tile-sku-management.css` 中新增的视频上传状态样式（若有）。
3. 恢复 `tile-skus-api.ts` 中 `uploadTileVideo` 封装（若增加 progress 回调）。
4. 保留既有 `POST /api/v1/admin/uploads/tile-videos` 与 MinIO 链路，不回滚 BUG-0011 弹窗滚动修复。
5. 回滚后重新标记 `BUG-0018` 未修复，并保留验收失败记录。
