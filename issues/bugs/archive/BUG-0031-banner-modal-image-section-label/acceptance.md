---
bug_id: BUG-0031-banner-modal-image-section-label
status: pending_review
created_at: 2026-06-28 16:20:00
updated_at: 2026-06-28 16:46:00
related_requirement: REQ-0016-banner-management
related_change: fix-banner-admin-ui
related_bug: BUG-0032-banner-modal-upload-button-label
---

# 回归验收标准

> 修复本缺陷 MUST 移除 Banner 弹窗图片模块冗余首行来源标题，且 MUST NOT 回归 REQ-0016 **AC-032**（自定义上传）与 **AC-045**（MinIO 上传链路）。与 BUG-0032 同 change 修复时，按钮文案验收以 BUG-0032 acceptance 为准。

**文案裁定**：本 BUG 不要求以 REQ-0016 原型 `upload-title`（「已上传：filename」/「SKU图库：…」）替换当前实现；验收标准为 **移除** 来源类型首行，对齐 `BrandFormModal` 信息层级。

## AC-001 新增弹窗 MUST NOT 展示来源首行标题

**Given** 管理员已打开 Banner **新增**弹窗（默认 `jump_type = NO_JUMP`）  
**When** 观察「Banner 图片」模块 upload box  
**Then** MUST NOT 存在 `.banner-upload-title` 或 DOM 等效首行  
**And** MUST NOT 显示「自定义上传」「SKU 主图」「SKU 图库」等来源类型标签  
**And** 字段 Label「Banner 图片*」之下 MUST 直接为预览区 + 帮助说明（若保留）+ 操作按钮

- [ ] AC-001

## AC-002 SKU 详情跳转类型 MUST NOT 展示来源首行标题

**Given** Banner 新增/编辑弹窗已打开  
**When** 将「跳转类型」切换为 **SKU 详情**  
**Then** MUST NOT 显示「SKU 主图」或「自定义上传」等 `.banner-upload-title` 首行  
**And** 「使用 SKU 主图」按钮（及 BUG-0032 上传按钮）MUST 仍可见且可操作

- [ ] AC-002

## AC-003 编辑态各 image_source MUST NOT 展示来源首行标题

**Given** 编辑已有 Banner，且 `image_source` 分别为 `custom_upload` / `sku_main_image` / `sku_gallery_image`  
**When** 打开编辑弹窗并观察「Banner 图片」模块  
**Then** 三种来源下 MUST NOT 渲染来源类型首行标题  
**And** 图片预览 MUST 正确回显

- [ ] AC-003

## AC-004 与品牌 Logo 上传区 MUST 信息层级一致

**Given** 分别打开 Banner 弹窗与品牌编辑弹窗  
**When** 对比「Banner 图片」与 Logo 上传区 DOM 结构  
**Then** Banner 区 MUST NOT 多出独立的来源类型 title 行（品牌区无此类行）  
**And** 字段 Label 之下 MUST 为 preview + 说明/按钮层级

- [ ] AC-004

## AC-005 图片上传与 SKU 主图操作 MUST 无回归

**Given** fix 已 apply  
**When** 执行自定义上传、切换 SKU 详情后点击「使用 SKU 主图」、保存 Banner  
**Then** 功能 MUST 与 fix 前一致（`imageKey` / `imageSource` / MinIO 链路正确）  
**And** MUST NOT 因移除 title 导致 upload box 布局 collapse 或按钮不可见

- [ ] AC-005

## AC-006 修复范围 MUST 为纯前端 UI

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API 路径、请求/响应、SQLite schema、Orval、Docker  
**And** MUST NOT 影响小程序或店主端

- [ ] AC-006

## AC-007 单元测试 SHOULD 断言无 banner-upload-title

**Given** `fix-banner-admin-ui`（或等价 fix-*）已 apply  
**When** 运行 `BannerFormModal` 相关 Vitest  
**Then** SHOULD 断言 render 结果 MUST NOT 含 `.banner-upload-title` 或「自定义上传」作为 upload box 首行 title  
**And** MAY 与 BUG-0032 测试同文件维护

- [ ] AC-007

## AC-008 视觉验收（SHOULD）

**Given** 修复完成  
**When** 在 Chrome 1440×1024 打开 Banner 新增弹窗与各 `jump_type` 分支  
**Then** 「Banner 图片」模块 MUST 无冗余首行来源标题  
**And** `openspec/changes/fix-banner-admin-ui/trace.md` SHOULD 记录与品牌 Logo 上传区并排对比结论  
**And** 截图 MAY 更新 `screenshots/`（替换 capture 待补充项）

- [ ] AC-008
