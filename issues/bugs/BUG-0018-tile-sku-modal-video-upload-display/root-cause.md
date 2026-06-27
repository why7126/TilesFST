---
bug_id: BUG-0018-tile-sku-modal-video-upload-display
status: pending_review
created_at: 2026-06-27 13:47:16
updated_at: 2026-06-27 13:47:16
root_cause_type: code
---

# 根因分析

## 1. 分类

| 项 | 值 |
|---|---|
| 缺陷类型 | **code**（前端 SKU 弹窗视频上传 UX / 反馈链路未闭环） |
| 引入阶段 | `add-tile-sku-management` apply（2026-06-27 前后） |
| 责任模块 | `TileSkuFormModal.tsx`、`tile-sku-management.css`、`tile-skus-api.ts` |
| 关联存储 | 上传 API 与 MinIO 链路 **预期正常**（与 SKU 图片同源模式）；本 BUG 聚焦**弹窗内即时可见反馈** |

## 2. 直接原因

### 2.1 视频上传缺少 AC-035 要求的「上传状态」与区域级反馈

`TileSkuFormModal` 虽在 `handleVideoUpload` 成功回调中调用 `setVideos`，但视频区 **未实现** 与 REQ-0006 AC-035、`BrandFormModal` Logo 上传对齐的状态机：

| 能力 | BrandFormModal（Logo） | TileSkuFormModal（视频） |
|---|---|---|
| 上传状态 | `idle / uploading / uploaded / failed` | **无** |
| 进度反馈 | 进度条 + 百分比 | **无** |
| 成功提示 | 「Logo 已更新」等区域文案 | **无** |
| 上传中禁用 | 上传中禁止重复选择与保存 | **无** |
| 即时可见回显 | `<img>` + 文案 | 仅依赖 `.sku-video-card` 列表追加 |

大体积 MP4 上传期间，`.sku-video-list` 保持空白、「上传视频」按钮无变化，用户 **无法感知上传进行中**，极易判定为「上传后未显示 / 功能未生效」。

### 2.2 错误提示位于弹窗顶部，视频区用户不可见

失败时 `setError(...)` 渲染于 `.modal-body` **顶部** `.admin-notice`：

```tsx
{error ? <p className="admin-notice">{error}</p> : null}
```

用户按复现步骤已滚动至底部「商品视频」区块操作。上传失败（非 MP4、超限、502 等）时，错误信息出现在视口外顶部，**表现为静默失败 + 列表仍为空**，与「未回显」现象一致。

### 2.3 成功回显依赖低显著性列表追加，无成功锚点

图片上传成功后立即在 `sku-upload-grid` 插入 **可见缩略图**；视频成功仅向 `.sku-video-list` 追加文字卡片（MP4 图标 + 文件名），且：

- 空列表无占位/引导，成功前后视觉对比弱；
- 无 `scrollIntoView` 或区域级成功态；
- 未清空 `videoInputRef`，同文件重复选择时 `onChange` 可能不触发（次要）。

### 2.4 测试未覆盖视频上传回显

`TileSkuFormModal.test.tsx` 仅覆盖弹窗滚动布局、字段规则与副标题，**无** mock `uploadTileVideo` 后断言 `.sku-video-card` 出现或上传状态切换，缺陷进入产品验收才暴露。

## 3. 根本原因

1. **`add-tile-sku-management` 交付缺口**：实现「能调上传 API + 写入 `videos` state」的最小路径，未落实 AC-035 的 **上传状态** 与可感知即时回显，属于需求验收条款遗漏而非新能力缺失。
2. **品牌 Logo 修复未横向同步**：`fix-brand-logo-upload-progress`（BUG-0004）已在 `BrandFormModal` 建立上传状态机模板，SKU 视频区未复用，形成模块间体验不一致。
3. **长表单 + 分区操作未设计分区反馈**：SKU 弹窗内容区可滚动（BUG-0011 已修），但错误/成功反馈仍沿用单点顶部 notice，未按「商品视频」分区就近展示。
4. **原 capture 误记品牌弹窗**：导致早期排查方向偏差；实际组件为 `TileSkuFormModal`，需求归属 REQ-0006。

## 4. 触发条件

满足以下条件可稳定复现「上传后看不到视频 / 无法确认成功」：

1. admin 登录 Web 管理端，访问 `/admin/tile-skus`。
2. 打开「新增 SKU」或「编辑 SKU」弹窗，滚动至 **「商品视频」** 区块。
3. 选择 MP4 触发上传，且满足以下任一：
   - **大文件或慢网络**：上传耗时数秒～数十秒，期间 UI 无进度（**最常见感知路径**）；
   - **上传失败**：非 MP4、存储不可用等，错误出现在弹窗顶部，用户未回滚至顶部查看；
   - **成功但无成功态**：列表追加卡片但用户未注意到文件名行（对比图片缩略图显著性不足）。

## 5. 非根因（排除）

| 假设 | 结论 |
|---|---|
| 品牌弹窗缺视频能力 | 否；scope 已修正为 SKU 弹窗 |
| MinIO 写入失败（系统性） | 否；与 SKU 图片同链路，图片区可正常回显 |
| 后端缺 `object_key` | 否；`upload_tile_video` 返回 `UploadResult(object_key, url)`，与图片一致 |
| 保存后 DB 未持久化视频 | **不在本 BUG scope**；capture 聚焦即时回显 |
| BUG-0011 弹窗无法滚动 | 已修复；可能加剧历史报告，非当前唯一根因 |

## 6. 修复方向

建议 Change：`fix-tile-sku-modal-video-upload-display`（`fix-*`，关联 REQ-0006）。

1. **前端**：为视频上传引入 `idle → uploading → uploaded / failed` 状态机；上传中展示进度或明确「上传中」文案；成功后在 **视频区内** 展示文件卡片 + 成功提示；失败时在 **视频区内** 展示错误；成功后 `scrollIntoView`（可选）；上传中禁用重复选择与保存（对齐 Logo）。
2. **API 封装（可选）**：`uploadTileVideo` 增加 `onUploadProgress`（对齐 `uploadBrandLogo`）。
3. **测试**：Vitest mock 上传成功/失败，断言 `.sku-video-card` 与状态文案。
4. **范围**：仅即时回显 + 上传状态；保存后重开、列表计数不在本 Change 必选项（除非修复时发现连带缺陷）。
