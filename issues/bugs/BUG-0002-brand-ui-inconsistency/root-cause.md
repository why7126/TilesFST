---
bug_id: BUG-0002-brand-ui-inconsistency
status: approved
updated_at: 2026-06-25
root_cause_type: design
---

# 根因分析

## 1. 直接原因

### 1.1 品牌分页结构与用户分页结构未复用

用户管理页使用统一分页结构：

```text
pagination
├── page-summary
└── page-right
    ├── page-buttons
    └── page-size-wrap
```

品牌管理页使用了另一套页面局部结构：

```text
pagination
├── page-left
└── brand-pagination-right
    ├── jump-input
    └── page-size
```

虽然两者都依赖 `user-management.css` 中的 `.pagination`、`.page-btn`、`.page-size` 基础样式，但品牌页额外引入 `brand-pagination-right`、`jump-input` 和不同的摘要文案布局，导致视觉和交互结构与用户管理页不一致。

### 1.2 Logo 上传控件使用页面专属大面积上传框

品牌弹窗中「品牌Logo」使用 `BrandFormModal.tsx` 的隐藏 file input + `button.brand-upload`，样式来自 `brand-management.css`：

- 高度 138px。
- 虚线金色边框。
- 大面积金色淡底。
- 居中图标和文案。

用户管理弹窗中「头像」上传则使用 `avatar-upload` 行内结构：

- 左侧头像预览和说明。
- 右侧 `btn` 触发文件选择。
- 与表单行、按钮和输入框视觉层级一致。

两者同属管理端弹窗内的图片选择/上传控件，但品牌 Logo 未沿用用户头像上传的控件表达或统一抽象，因此产生风格割裂。

## 2. 根本原因

### 2.1 管理端分页缺少共享组件或强制复用约束

当前管理端分页由各页面手写 DOM 组合完成，而不是统一使用一个管理端分页组件。页面实现时容易在局部新增结构和样式，造成同类页面底部分页视觉不一致。

### 2.2 图片上传/文件选择控件缺少统一设计约束

用户头像上传、品牌 Logo 上传、SKU 图片/视频上传分别采用页面局部实现。品牌 Logo 场景选择了更接近拖拽上传区的大框样式，但新增品牌弹窗整体是紧凑管理端表单，大面积上传框的视觉权重与弹窗内其他表单控件不匹配。

### 2.3 品牌页继承用户管理样式又叠加局部样式

`BrandManagementPage.tsx` 同时引入：

```text
src/web/src/features/admin/styles/user-management.css
src/web/src/features/admin/styles/brand-management.css
```

这使品牌页部分复用用户管理基础样式，部分使用品牌页专属样式。若专属样式没有严格对齐用户管理页结构，就容易出现“看起来相似但细节不一致”的 UI 偏差。

## 3. 触发条件

满足以下条件时可复现：

1. 访问 Web 管理端「瓷砖品牌」页面。
2. 品牌列表渲染底部分页区域。
3. 与「用户管理」页面分页区域对比。
4. 打开新增或编辑品牌弹窗。
5. 观察「品牌Logo」选择文件控件。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否媒体上传安全缺陷 | 否，当前记录仅指 UI 呈现不一致 |
| 主要修复面 | Web 管理端分页结构与品牌 Logo 上传控件样式 |

## 5. 后续修复建议

1. 将品牌列表分页结构对齐用户管理页分页结构，或抽取管理端列表分页组件统一使用。
2. 将品牌 Logo 上传控件改为与用户头像上传一致的行内上传模式，或抽取统一的管理端图片上传控件。
3. 若保留「跳至」能力，应在统一分页组件中作为可选能力设计，并保证默认视觉不偏离用户管理页。
4. 修复时补充品牌管理页相关单元测试或视觉验收说明。
