---
bug_id: BUG-0032-banner-modal-upload-button-label
status: pending_review
created_at: 2026-06-28 16:17:02
updated_at: 2026-06-28 16:17:02
related_requirement: REQ-0016-banner-management
related_bug: BUG-0031-banner-modal-image-section-label
---

# 回归验收标准

> 修复本缺陷 MUST 使 Banner 弹窗自定义上传按钮对齐管理端上传控件模式（品牌 Logo 基准），且 MUST NOT 回归 REQ-0016 **AC-032**（自定义上传能力）与 **AC-045**（MinIO 上传链路）。

**文案裁定**：按钮使用「选择」/「更换」/「上传中」（非 REQ-0016 原型「重新上传」/「自定义上传」）；与原型冲突以本 BUG acceptance 为准，fix change delta spec 中 MODIFIED 消化。

## AC-001 未选图时按钮 MUST 显示「选择」

**Given** 管理员已打开 Banner 新增弹窗，且 `imageUrl` 为空  
**When** 观察「Banner 图片」模块自定义上传按钮  
**Then** 按钮文案 MUST 为「选择」（MAY 为「选择图片」，实现与测试须一致）  
**And** MUST NOT 显示「自定义上传」或浏览器原生「浏览…」

- [ ] AC-001

## AC-002 已有图片时按钮 MUST 显示「更换」

**Given** Banner 弹窗已配置 Banner 图片（自定义上传或编辑态回显）  
**When** 观察自定义上传按钮  
**Then** 按钮文案 MUST 为「更换」（MAY 为「更换图片」）  
**And** MUST NOT 显示「自定义上传」或「浏览…」

- [ ] AC-002

## AC-003 上传中按钮 MUST 显示「上传中」且不可重复触发

**Given** 用户已选择待上传图片，上传请求进行中（`imageUploadState === 'uploading'`）  
**When** 观察自定义上传按钮  
**Then** 按钮文案 MUST 为「上传中」  
**And** `<input type="file">` MUST 为 `disabled` 或 label MUST 含 `disabled` / `aria-disabled` 等价态  
**And** 保存 Banner MUST 仍提示「图片上传中，请稍后保存」（既有逻辑无回归）

- [ ] AC-003

## AC-004 file input MUST 完全隐藏原生控件

**Given** Banner 弹窗已渲染  
**When** 检查自定义上传 `<input type="file">`  
**Then** MUST 使用 `hidden` 属性（或等效 `display: none`）  
**And** MUST NOT 使用仅 `sr-only` 导致 Chromium 渲染「浏览…」  
**And** 按钮可见区域 MUST 仅含 AC-001~003 规定文案

- [ ] AC-004

## AC-005 上传功能 MUST 无回归（REQ-0016 AC-032 / AC-045）

**Given** 用户点击「选择」并选择合法 JPG / PNG / WebP  
**When** 上传完成  
**Then** 预览 MUST 更新，`imageKey` / `imageSource=custom_upload` MUST 正确设置  
**And** 保存 Banner MUST 成功，对象 MUST 写入 MinIO（AC-045）  
**And** 各 `jump_type`（含 `SKU_DETAIL` 下自定义上传）MUST 均可用

- [ ] AC-005

## AC-006 重复选择同一文件 SHOULD 可再次触发上传

**Given** 用户已成功上传一张图片  
**When** 再次通过「更换」选择同一文件  
**Then** SHOULD 再次触发上传（`input.value` 重置，对齐 `BrandFormModal`）  
**And** MUST NOT 因 input 未清空导致 silently 无响应

- [ ] AC-006

## AC-007 与品牌 Logo 上传模式 MUST 结构一致

**Given** 分别打开 Banner 弹窗与品牌编辑弹窗  
**When** 对比自定义上传 / Logo 上传控件  
**Then** DOM 模式 MUST 一致：`<label className="btn">` + 动态文案 + `hidden` file input  
**And** 上传中禁用策略 MUST 与 `BrandFormModal` 同等

- [ ] AC-007

## AC-008 修复范围 MUST 为纯前端 UI

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API 路径、请求/响应、SQLite schema、Orval、Docker  
**And** MUST NOT 影响小程序或店主端

- [ ] AC-008

## AC-009 单元测试 SHOULD 覆盖按钮文案与隐藏方式

**Given** 进入 `fix-banner-modal-upload-button-label`（或等价 fix-* / 合并 change）  
**When** 完成 `/opsx-apply`  
**Then** SHOULD 新增 `BannerFormModal.test.tsx`（或扩展现有测试）断言：  
**And** 无图态含「选择」、有图态含「更换」、上传中态含「上传中」  
**And** file input MUST 含 `hidden` 属性  
**And** MUST NOT 在 document 中出现「浏览…」文本（file input 原生按钮）

- [ ] AC-009

## AC-010 视觉验收（SHOULD）

**Given** 修复完成  
**When** 在 Chrome 1440×1024 打开 Banner 新增弹窗「Banner 图片」模块  
**Then** 上传按钮 MUST 仅显示「选择」或「更换」或「上传中」  
**And** Change `trace.md` SHOULD 记录与品牌 Logo 上传并排对比结论  
**And** 截图 MAY 更新 `screenshots/`（替换 capture 待补充项）

- [ ] AC-010
