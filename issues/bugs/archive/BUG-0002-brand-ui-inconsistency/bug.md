---
bug_id: BUG-0002-brand-ui-inconsistency
title: 品牌管理分页与Logo选择文件控件UI不一致
severity: medium
status: in_sprint
owner: product
discovered_at: 2026-06-25
environment: local|docker
related_requirement: null
related_change: fix-brand-ui-consistency
iteration: sprint-002
---

# 缺陷说明

瓷砖品牌管理界面存在两处视觉一致性缺陷：

1. 品牌列表底部分页 UI 与用户管理页底部分页 UI 不一致。
2. 新增/编辑品牌弹窗中的「品牌Logo」选择文件控件与管理端整体表单和上传控件风格不一致。

# 复现步骤

1. 以 admin 用户登录 Web 管理端。
2. 进入「瓷砖品牌」页面，查看列表底部的分页区域。
3. 进入「用户管理」页面，查看列表底部分页区域。
4. 对比两个页面分页区域的布局、文案、每页显示控件、跳页输入、按钮尺寸和视觉层级。
5. 返回「瓷砖品牌」页面，点击「新增品牌」。
6. 查看弹窗中的「品牌Logo」上传/选择文件区域，并与用户管理弹窗「头像」上传区域及其他表单控件对比。

# 期望结果

- 品牌列表底部分页应与用户管理页分页保持一致的结构和视觉语言：
  - 统一高度、内边距、边框、字号、按钮尺寸和激活态。
  - 统一「总数摘要 + 翻页按钮 + 每页显示」布局。
  - 如需跳页能力，应以统一组件或统一样式扩展，不能破坏页面间一致性。
- 品牌 Logo 选择文件控件应符合管理端 Design System：
  - 与输入框、按钮、用户头像上传区域保持一致的边框、圆角、背景、字号和操作按钮样式。
  - 文件选择入口应使用明确按钮或可访问标签，不暴露浏览器默认文件控件皮相。
  - 预览态、空态、帮助文案与错误态应在弹窗内保持统一层级。

# 实际结果

- 品牌列表分页使用 `page-left` + `brand-pagination-right`，并包含「跳至」输入，与用户管理页的 `page-summary` + `page-right` + `page-buttons` + `page-size-wrap` 结构不一致。
- 品牌 Logo 上传区域使用大面积虚线框 `brand-upload`，视觉重量、布局和交互表达与用户管理弹窗的 `avatar-upload` 行内上传样式不一致。
- 该差异导致品牌管理页在管理端整体 UI 中显得割裂，影响页面一致性与视觉验收。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / 瓷砖品牌列表 | 分页样式与用户管理页不一致 |
| Web 管理端 / 新增品牌弹窗 | Logo 选择文件控件不符合整体表单风格 |
| Design System 验收 | 管理端复合控件复用和一致性不达标 |

# 严重等级说明

严重程度建议为 `medium`。

理由：

- 不阻断品牌管理功能使用。
- 不影响 API、数据库或权限边界。
- 但属于可见管理端 UI 缺陷，会影响视觉一致性、验收质量和长期组件复用。

# 代码线索

| 线索 | 路径 |
|---|---|
| 品牌页分页 DOM | `src/web/src/pages/admin/BrandManagementPage.tsx` |
| 用户页分页 DOM | `src/web/src/pages/admin/UserManagementPage.tsx` |
| 品牌 Logo 上传 DOM | `src/web/src/features/admin/components/BrandFormModal.tsx` |
| 用户头像上传参考 | `src/web/src/features/admin/components/UserFormModal.tsx` |
| 通用分页样式 | `src/web/src/features/admin/styles/user-management.css` |
| 品牌页补充样式 | `src/web/src/features/admin/styles/brand-management.css` |
