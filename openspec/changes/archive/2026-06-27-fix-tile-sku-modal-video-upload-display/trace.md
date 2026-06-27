---
created_at: 2026-06-27 13:55:06
updated_at: 2026-06-27 13:58:57
title: fix-tile-sku-modal-video-upload-display Trace
purpose: BUG-0018 → OpenSpec 修复追溯
---

# fix-tile-sku-modal-video-upload-display — Trace

## 变更摘要

- **BUG**: `BUG-0018-tile-sku-modal-video-upload-display`
- **REQ**: `REQ-0006-tile-sku-management`（AC-035）
- **Type**: fix
- **Depends**: `add-tile-sku-management`；参考 `fix-brand-logo-upload-progress`
- **Related BUG**: `BUG-0011-tile-sku-modal-content-overflow`（MUST 不回退）
- **Iteration**: `sprint-002`
- **Status**: applied

## 代码变更

| 文件 | 变更 |
|---|---|
| `src/web/src/features/admin/components/TileSkuFormModal.tsx` | 视频上传状态机、区域进度/成功/错误、上传中禁用保存、scrollIntoView |
| `src/web/src/features/admin/api/tile-skus-api.ts` | `uploadTileVideo` 增加 `onUploadProgress` 回调 |
| `src/web/src/features/admin/styles/tile-sku-management.css` | `.sku-video-*` 上传进度/成功/错误样式 |
| `src/web/src/features/admin/components/TileSkuFormModal.test.tsx` | 新增视频上传成功/失败 Vitest |

## 即时回显验收 Checklist

| # | 检查项 | 结果 | 备注 |
|---|--------|------|------|
| 1 | 选择 MP4 后立即触发上传 | pass | mock 验证 + 实现即时调用 |
| 2 | 上传中展示可感知状态 | pass | 进度条 + 「上传中 N%」 |
| 3 | 成功后即时出现 `.sku-video-card` | pass | Vitest 断言 demo.mp4 |
| 4 | 失败时视频区错误可见 | pass | `role="alert"` 区域错误 |
| 5 | 多视频追加与移除 | pass | 既有 remove 逻辑保留 |
| 6 | BUG-0011 弹窗滚动仍可用 | pass | 未改 modal-body flex 布局；4 项回归 pass |
| 7 | SKU 图片上传无回归 | pass | 未改 handleImageUpload |

## REQ-0006 / BUG 验收对齐

| 条款 | 结果 |
|---|---|
| REQ-0006 AC-035（上传状态 + 即时回显） | pass |
| BUG AC-001～AC-008 | pass |

## 测试

- `npx vitest run src/features/admin/components/TileSkuFormModal.test.tsx` — 6 passed
- `npm run build` — success

## 知识沉淀

- 不需要 `docs/knowledge-base/incidents/`（交付缺口，无 incidents 沉淀）

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 13:55:06 | `/bug-opsx` | 创建 change；status → proposed |
| 2026-06-27 13:58:57 | `/opsx-apply` | 视频上传状态机 + Vitest；status → applied |
