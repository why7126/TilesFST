## Context

`BUG-0004-brand-logo-upload-progress-missing` 描述了编辑品牌弹窗内的 Logo 更换体验缺陷：选择图片后没有明显上传反馈，预览不更新，也没有进度条让用户感知等待时间。

相关上下文：

| 项目 | 内容 |
|---|---|
| 父需求 | `REQ-0005-brand-management` |
| 相关 BUG | `BUG-0003-brand-image-display-layout-shift` |
| 目标页面 | `/admin/brands` |
| 目标组件 | `BrandFormModal` |
| 上传 API | 既有品牌 Logo 上传接口 |
| 主要风险 | 上传状态不可见、预览状态未同步、失败重试不明确 |

## Root Cause Summary

### RC-001：上传交互缺少状态机

Logo 控件缺少 `idle → uploading → uploaded / failed` 的明确状态管理。选择文件后，即使底层请求发起，用户也无法看到进度、等待态或禁用态。

### RC-002：预览更新与上传结果耦合不完整

上传成功后必须同时更新：

- 表单中的 `logo_object_key`。
- 弹窗内展示用 `logoUrl`。
- 上传按钮和帮助文案状态。

若任一状态未同步，就会出现“已选择文件但预览不变”的体验。

### RC-003：上传进度未进入验收闭环

`BUG-0003` 重点修复 URL 可访问和列表/弹窗展示，未把“选择文件后必须有上传进度反馈”作为验收项。因此本 change 需要补齐上传体验闭环。

## Decisions

### D1：上传状态机

`BrandFormModal` MUST 为 Logo 上传维护独立状态：

```text
idle | uploading | uploaded | failed
```

上传中 MUST 禁止重复提交同一上传动作，或明确忽略重复选择。

### D2：进度反馈策略

优先使用真实上传进度：

- 若当前 API 封装可传入 `onUploadProgress`，接入真实百分比。
- 若当前封装不支持，修复阶段可扩展前端上传调用函数，但不得改变后端响应 schema。

若测试环境无法稳定触发真实 progress event，前端仍 MUST 展示确定性的上传中状态，并在成功/失败后完成状态切换。

### D3：预览更新策略

上传成功后 MUST 使用上传响应中的可访问 URL 更新预览，并使用返回的 `object_key` 更新保存 payload。若 URL 可能被浏览器缓存，MAY 使用 cache-busting 或本地临时预览，但最终保存 MUST 以服务端返回 `object_key` 为准。

### D4：失败与重试

上传失败时：

- MUST 展示明确错误文案。
- MUST 保留重新选择文件入口。
- MUST 不得把旧 Logo 替换成无效预览。
- SHOULD 重置 file input value，允许选择同一文件重试。

### D5：Design System

进度条、错误文案、按钮禁用态和预览态 MUST 复用现有管理端样式变量、语义 Token 或共享 UI 模式，不新增裸 Hex。

## Test Strategy

| 层级 | 验证 |
|---|---|
| Frontend Vitest | 选择文件后进入上传中状态；展示进度反馈；上传成功更新预览；失败展示错误；同文件可重试 |
| Regression Vitest | 品牌创建/编辑 payload 仍携带最新 `logo_object_key`；既有品牌弹窗测试不回退 |
| Backend pytest | 如未改后端，仅回归现有品牌 Logo 上传可访问测试；若改上传接口则补充对应测试 |
| Build | Web build 通过 |
| Manual | 编辑品牌 → 更换 Logo → 看到进度 → 预览更新 → 保存 → 重新打开回显 |

## Risks

| 风险 | 影响 | 缓解 |
|---|---|---|
| 测试环境无法模拟真实 progress | Vitest 不稳定 | 抽象上传回调；测试上传中状态与成功/失败切换 |
| API 封装变更影响其他上传入口 | 用户头像、SKU 图片/视频上传回归 | 限定变更面；补充上传函数单测或调用方回归 |
| 上传失败保留旧预览导致误解 | 用户不知是否已替换 | 错误文案明确说明失败，保存 payload 不更新为失败对象 |
| 进度 UI 破坏弹窗布局 | UI 回归 | 固定高度/紧凑布局，复用 DS 变量 |

## Out of Scope

- 不新增后端上传端点。
- 不改变 `UploadResult` / 品牌响应 schema，除非实现阶段发现必须调整并按 API 规则同步 OpenAPI 与 Orval。
- 不处理用户头像、SKU 图片、SKU 视频上传进度，除非前端上传封装调整带来必要回归。
