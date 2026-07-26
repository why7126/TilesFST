## 1. 准备与门禁

- [x] 1.1 阅读 `BUG-0018-tile-sku-modal-video-upload-display` 的 bug.md、root-cause.md、acceptance.md、review.md
- [x] 1.2 确认 BUG 状态为 `in_sprint` 或 `approved`
- [x] 1.3 对照 `BrandFormModal` Logo 上传状态机（`fix-brand-logo-upload-progress`）
- [x] 1.4 确认本 change 默认不新增数据库字段、不改变 SKU CRUD API schema

## 2. TileSkuFormModal 视频上传状态机

- [x] 2.1 为「商品视频」区块增加 `idle / uploading / uploaded / failed` 状态与 progress state
- [x] 2.2 选择 MP4 后立即触发 `uploadTileVideo`，不依赖保存 SKU
- [x] 2.3 上传中在视频区内展示进度条、百分比或「上传中」文案
- [x] 2.4 上传中禁用「上传视频」重复触发；上传中禁止 footer 保存（对齐 Logo）
- [x] 2.5 上传成功后立即 append `.sku-video-card`（文件名、大小）+ 区域成功提示
- [x] 2.6 上传失败时在视频区内展示错误，不得仅依赖顶部 `.admin-notice`
- [x] 2.7 重置 video file input value，允许重选同一文件
- [x] 2.8 可选：成功后 `scrollIntoView` 至新卡片（不破坏 BUG-0011 滚动）

## 3. API 封装与样式

- [x] 3.1 评估 `uploadTileVideo` 是否增加 `onUploadProgress`（对齐 `uploadBrandLogo`）
- [x] 3.2 更新 `tile-sku-management.css` 视频上传状态/进度/错误样式（semantic token）
- [x] 3.3 确认品牌 Logo、用户头像、SKU 图片上传入口不回退

## 4. 测试

- [x] 4.1 Vitest：mock `uploadTileVideo` 成功 → 断言 uploading 态 + `.sku-video-card` 出现
- [x] 4.2 Vitest：mock 上传失败 → 断言视频区内错误文案
- [x] 4.3 回归 `TileSkuFormModal` 既有滚动布局、字段规则、副标题测试
- [x] 4.4 运行 `cd src/web && npx vitest run src/features/admin/components/TileSkuFormModal`
- [x] 4.5 运行 `cd src/web && npm run build`

## 5. 验收与追溯

- [x] 5.1 手工验证：新增/编辑弹窗 → 上传 MP4 → 见进度 → 即时文件卡片 → 可移除 → 可继续添加
- [x] 5.2 手工验证：上传失败时视频区错误可见且可重试
- [x] 5.3 对照 BUG acceptance AC-001～AC-008 与 REQ-0006 AC-035，记录于本 change `trace.md`
- [x] 5.4 更新 `BUG-0018-tile-sku-modal-video-upload-display/trace.md` 中 change 状态
- [x] 5.5 评估是否更新 `docs/knowledge-base/incidents/`（交付缺口，通常不需要）
