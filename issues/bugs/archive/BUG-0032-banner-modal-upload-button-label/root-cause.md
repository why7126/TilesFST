---
bug_id: BUG-0032-banner-modal-upload-button-label
status: pending_review
created_at: 2026-06-28 16:17:02
updated_at: 2026-06-28 16:17:02
root_cause_type: code
---

# 根因分析

## 1. 直接原因

### 1.1 上传按钮文案硬编码为「自定义上传」

`BannerFormModal.tsx` 中自定义上传控件使用固定文案：

```tsx
<label className="btn">
  自定义上传
  <input type="file" ... />
</label>
```

未根据 `imageUrl` / `imageKey` 是否存在切换「选择」与「更换」，也未在 `imageUploadState === 'uploading'` 时展示「上传中」并禁用按钮。管理端已验收的 `BrandFormModal` 使用三元表达式：`logoUrl ? '更换 Logo' : '选择 Logo'`。

### 1.2 file input 使用 `sr-only` 导致原生「浏览…」泄漏

Banner 弹窗对 `<input type="file">` 使用 Tailwind `sr-only`（屏幕阅读器可见、视觉裁剪）。在 Chrome 等浏览器中，label 内的 file input 仍会渲染原生「浏览…」按钮，与 label 文案并列，呈现为「自定义上传 浏览…」。

`BrandFormModal` 对同类控件使用 HTML `hidden` 属性（`display: none`），原生按钮完全不渲染。

### 1.3 上传状态未绑定到按钮 UI

`imageUploadState`（`idle | uploading | uploaded | failed`）已在组件内维护，且 `handleSubmit` 会在 uploading 时阻止保存，但上传按钮未读取该状态，缺少 disabled / 「上传中」文案，与 BUG-0004 修复后的品牌 Logo 模式不一致。

## 2. 根本原因

### 2.1 `add-banner-management` 实现时未复用管理端上传控件模式

REQ-0016 弹窗采用 CSS Port + 单组件 `BannerFormModal` 按 `jump_type` 分支。图片上传区从原型 HTML 移植了「自定义上传」按钮文案，但未参照 Sprint-002 已修复的 `BrandFormModal` 上传交互（动态文案、`hidden` input、上传中禁用、input value 重置）。

### 2.2 管理端 file upload 模式缺少共享组件约束

品牌 Logo、用户头像、Banner 图片等上传控件各自在 feature modal 内手写 `<label>` + `<input type="file">`，无统一 `FileUploadButton` 组件或 lint 规则，新增页面易重复 invent 非标准实现（`sr-only` vs `hidden`、静态文案 vs 动态文案）。

### 2.3 原型与一致性基准存在文案差异未在实现前裁定

REQ-0016 原型 HTML 在已上传态使用「重新上传」，SKU 详情态使用独立按钮「自定义上传」；管理端黄金参考（品牌 Logo）使用「选择 Logo」/「更换 Logo」。`add-banner-management` 直接采用原型 SKU 详情按钮文案，未在 trace/acceptance 中明确以哪条基准为准，导致 UI 分裂。

## 3. 触发条件

满足以下条件时可稳定复现：

1. 以 admin 或 employee 登录 Web 管理端（local `5173` 或 Docker `3000`）。
2. 进入 `/admin/banners`，点击「+ 新增 Banner」或编辑已有 Banner。
3. 在「Banner 图片」模块观察自定义上传 `<label className="btn">` 按钮。
4. 使用 Chrome / Edge 等 Chromium 内核浏览器（原生 file input 按钮最易可见）。

任意 `jump_type` 均会渲染该上传控件；`SKU_DETAIL` 模式下除「使用 SKU 主图」外仍保留自定义上传按钮。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 主要修复面 | `BannerFormModal.tsx` 上传按钮文案、input 隐藏方式、上传中状态 |
| 关联需求 AC | REQ-0016 AC-032（自定义上传能力）、AC-045（上传链路）；UI 一致性为 BUG 级补充 |

## 5. 后续修复建议

1. 对齐 `BrandFormModal`：`imageUploadState === 'uploading' ? '上传中' : imageUrl ? '更换' : '选择'`（或「选择图片」/「更换图片」，与 acceptance 一致）。
2. 将 `<input type="file">` 的 `className="sr-only"` 改为 `hidden`，并在上传中 `disabled`。
3. `onChange` 后重置 `input.value = ''`，支持重复选择同一文件（参考 `BrandFormModal`）。
4. 建议 Change：`fix-banner-modal-upload-button-label`，或与 BUG-0031/0033–0036 合并为 `fix-banner-modal-ui`。
5. 补充 `BannerFormModal.test.tsx`：断言无「浏览…」、文案随状态切换（参考 `BrandFormModal.test.tsx`）。
