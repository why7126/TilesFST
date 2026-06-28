---
bug_id: BUG-0032-banner-modal-upload-button-label
title: Banner弹窗图片上传按钮文案应为选择或更换
severity: low
status: draft
owner: product
discovered_at: 2026-06-28 16:04:18
environment: local|docker
related_requirement: REQ-0016-banner-management
related_change: add-banner-management
---

# 缺陷说明

Web 管理端 Banner 新增/编辑弹窗（`BannerFormModal`）「Banner 图片」模块中，自定义上传控件的按钮文案为「自定义上传 浏览…」，与管理端已验收的上传控件模式（如品牌 Logo「选择 Logo」/「更换 Logo」）不一致。

根因类型为 **frontend-ui**：

1. 上传按钮文案硬编码为「自定义上传」，未按是否已有图片动态切换。
2. `<input type="file">` 使用 `sr-only` 隐藏，部分浏览器仍会渲染原生「浏览…」按钮，与 label 文案拼接显示；品牌弹窗使用 `hidden` 属性可完全隐藏原生控件。

上传功能本身正常（`handleCustomUpload` → `uploadBannerImage`），属纯 UI/文案缺陷，非功能阻断。

# 复现步骤

1. 以 admin 或 employee 登录 Web 管理端（local `5173` 或 Docker `3000`）。
2. 进入「Banner 管理」列表页（`/admin/banners`）。
3. 点击「+ 新增 Banner」打开弹窗；在「Banner 图片」模块观察自定义上传按钮文案。
4. 可选：编辑已有 Banner 或上传一张图片后再次观察按钮文案。
5. 对比「瓷砖品牌」新增/编辑弹窗 Logo 上传按钮（「选择 Logo」/「更换 Logo」）。

# 期望结果

- 未选图时，上传按钮文案为 **「选择」**（或与管理端一致的「选择图片」，以 `/bug-complete` acceptance 为准）。
- 已有图片时，按钮文案为 **「更换」**（对齐品牌 Logo 模式）。
- 图片上传中时，按钮文案为 **「上传中」** 且不可再次触发（对齐 `BrandFormModal`）。
- 按钮 **仅** 显示上述文案，**不得** 出现浏览器原生「浏览…」字样。
- `<input type="file">` MUST 使用 `hidden`（或等效 `display: none`），与 `BrandFormModal` 一致。

# 实际结果

- `BannerFormModal.tsx` 中上传 `<label className="btn">` 固定显示「自定义上传」。
- 内嵌 `<input type="file" className="sr-only">` 在 Chrome 等浏览器中仍渲染「浏览…」，与 label 文案并列显示为「自定义上传 浏览…」。
- 上传中无按钮 disabled / 「上传中」文案反馈（`imageUploadState` 已存在但未绑定到按钮 UI）。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / Banner 弹窗 | 新增与编辑模式下，各 `jump_type` 的自定义上传按钮文案与交互反馈不一致 |
| 管理端上传控件一致性 | 未对齐 `BrandFormModal` 已验收模式（BUG-0004 修复后） |
| 关联需求 | REQ-0016-banner-management（`add-banner-management` 弹窗实现） |
| 关联缺陷 | BUG-0031（同上传区首行标题冗余，可同 change 修复） |

不影响 API、数据库、MinIO 上传链路、权限边界、小程序或店主端。

# 严重等级说明

严重程度为 `low`。

理由：

- 不阻断 Banner 创建/编辑或图片上传保存。
- 主要为可见文案混乱与管理端 UI 一致性问题。
- 应在 `add-banner-management` 收尾或独立 `fix-banner-modal-upload-button-label`（建议与 BUG-0031/0033–0036 合并为 `fix-banner-modal-ui`）中修复。

# 代码线索

| 线索 | 路径 |
|---|---|
| Banner 弹窗上传按钮（问题点） | `src/web/src/features/admin/components/BannerFormModal.tsx` |
| 品牌 Logo 上传基准 | `src/web/src/features/admin/components/BrandFormModal.tsx` |
| 品牌上传 Vitest 参考 | `src/web/src/features/admin/components/BrandFormModal.test.tsx` |
| 父 Change | `openspec/changes/add-banner-management` |
| REQ-0016 原型（SKU 详情态按钮为「自定义上传」；无跳转已上传态为「重新上传」） | `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-modal-*.html` |

**文案裁定说明**：本 BUG 验收以管理端上传控件一致性（选择/更换/上传中）为准；若与 REQ-0016 原型「重新上传」冲突，在 `/bug-complete` acceptance 或 fix change delta spec 中 MODIFIED 消化（同 BUG-0030 列表分页模式）。
