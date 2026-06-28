---
bug_id: BUG-0032-banner-modal-upload-button-label
status: pending_review
created_at: 2026-06-28 16:17:02
updated_at: 2026-06-28 16:17:02
---

# 临时规避方案

## 1. 可用性规避

该缺陷不阻断 Banner 图片上传与保存，当前可继续使用：

1. 点击「自定义上传 浏览…」按钮（或 label 可点击区域）仍可打开系统文件选择器。
2. 选择 JPG / PNG / WebP 后，`handleCustomUpload` 正常调用 `uploadBannerImage`，预览与 `imageKey` 会更新。
3. Banner 新增、编辑、各 `jump_type` 下的保存、上下线等流程均不受影响。

## 2. 验收规避

在正式修复前，验收 REQ-0016 弹窗时应明确标注：

- Banner 图片自定义上传按钮文案与品牌 Logo 上传不一致，**暂不作为管理端 UI 一致性通过项**。
- 按钮出现「浏览…」字样为已知 UI 缺陷，**不影响 AC-032 / AC-045 功能验收**（上传链路与 MinIO 存储仍须单独验证）。

## 3. 运营规避

内部管理员可忽略按钮文案混乱，按现有路径操作：

1. 进入 Banner 管理 → 新增/编辑 Banner。
2. 在「Banner 图片」区点击上传按钮选择运营图。
3. 等待预览更新后保存 Banner。

## 4. 风险说明

该规避方案只能保证功能可用，不能消除：

- 管理端上传控件视觉与文案不一致，影响 REQ-0016 弹窗并排验收体验。
- 上传中无按钮禁用反馈，用户可能重复点击触发并发上传（后端仍应正确处理，但 UX 较差）。

因此仍建议进入 `/bug-review`，评审通过后通过 `fix-*` OpenSpec Change 修复。
