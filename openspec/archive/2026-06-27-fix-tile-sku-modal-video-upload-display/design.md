## Context

- **BUG**: `BUG-0018-tile-sku-modal-video-upload-display`
- **Severity**: high
- **Root cause type**: code / frontend-ui
- **Related REQ**: `REQ-0006-tile-sku-management`（AC-035）
- **Related BUG**: `BUG-0011-tile-sku-modal-content-overflow`（已归档，滚动 MUST 不回退）
- **Reference pattern**: `fix-brand-logo-upload-progress` / `BrandFormModal` Logo 上传状态机
- **Parent change**: `add-tile-sku-management`（in-progress）
- **Target**: `TileSkuFormModal.tsx`、`tile-sku-management.css`、`tile-skus-api.ts`

## Bug Analysis Report

### 现象

SKU 弹窗「商品视频」区块选择 MP4 上传后，用户无法在同一弹窗会话内确认上传是否成功；大文件上传期间 UI 无变化；失败时错误出现在弹窗顶部，底部操作区用户不可见。

### 复现路径

1. admin 登录，访问 `/admin/tile-skus`。
2. 打开「新增SKU」或「编辑SKU」弹窗，滚动至「商品视频」。
3. 点击「上传视频」，选择合法 MP4。
4. 观察：上传中无进度；成功后 `.sku-video-list` 可能追加卡片但无成功态；失败时顶部 notice 不可见。

### 影响

- **阻塞** REQ-0006 AC-035 即时回显与上传状态验收。
- 不影响 SQLite schema、SKU CRUD API、MinIO 写入链路（预期正常）。
- 不影响小程序 / 店主端。

## Root Cause

### RC-001：视频上传缺少 AC-035 状态机

`TileSkuFormModal` 调用 `uploadTileVideo` 并在成功时 `setVideos`，但未实现 `idle / uploading / uploaded / failed` 状态与区域级反馈，与 `BrandFormModal` Logo 不对齐。

### RC-002：错误反馈位于弹窗顶部

`setError(...)` 渲染于 `.modal-body` 顶部；用户在底部「商品视频」操作时失败表现为静默。

### RC-003：成功回显显著性不足

视频成功仅追加文字卡片，无进度/成功锚点；对比图片缩略图即时可见性弱。

### RC-004：测试缺口

`TileSkuFormModal.test.tsx` 未 mock 视频上传回显与状态切换。

## Design Decisions

### D1：复用 BrandFormModal 上传状态机模式

```text
videoUploadState: idle | uploading | uploaded | failed
videoUploadProgress: 0–100（可选）
videoUploadError: string | null（区域内展示）
videos[]: 成功后 append { object_key, file_name, file_size_bytes, ... }
```

MUST NOT 要求先保存 SKU 再上传。

### D2：分区就近反馈

- 上传中/失败/成功文案与进度 MUST 位于「商品视频」区块内（`.sku-video-section` 或等价）。
- 顶部 `.admin-notice` MAY 保留通用错误，但 MUST NOT 作为视频上传唯一反馈通道。

### D3：即时回显 scope

- 本 change MUST 保证同一弹窗会话内 `.sku-video-card` 即时出现。
- 保存后重开回填、列表页视频计数 **不在** 本 change 必验范围（除非 apply 时发现连带缺陷并另开任务）。

### D4：不扩大行为面

本 change 不修改：

- SKU API 契约、校验规则、`save_mode` 逻辑。
- 数据库 schema、Orval 生成接口（除非 progress 封装纯前端）。
- BUG-0011 已修复的 `.modal-body` 滚动布局。
- SKU 图片上传与主图逻辑。

### D5：可选 progress 回调

若实现真实进度，`uploadTileVideo(file, onProgress?)` 对齐 `uploadBrandLogo`；MUST 确认品牌/用户/图片上传入口不回退。

## Test Strategy

- Vitest + RTL：mock `uploadTileVideo` 成功 → 断言 uploading 态文案 + `.sku-video-card` 出现。
- Vitest：mock 失败 → 断言视频区内错误文案，非仅顶部 notice。
- 回归：现有弹窗滚动、字段规则、图片上传测试 MUST pass。
- 构建：`cd src/web && npx vitest run …`；`npm run build`。

## Risks

| 风险 | 缓解 |
|---|---|
| 上传中禁用保存影响草稿流程 | 与 Logo 一致：uploading 时 disable footer 保存按钮 |
| 多视频并发上传 | 首版可串行；上传中禁用「上传视频」 |
| 回归 BUG-0011 滚动 | 不改变 modal-body flex 布局；仅改视频区块 DOM |
| 回归 SKU 图片 | 不修改 `handleImageUpload` 路径 |
