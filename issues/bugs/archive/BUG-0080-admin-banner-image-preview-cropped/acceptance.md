---
bug_id: BUG-0080-admin-banner-image-preview-cropped
title: 管理端 Banner 列表和弹窗中 Banner 图片显示不全
status: done
severity: medium
created_at: 2026-07-22 09:00:41
updated_at: 2026-07-22 09:35:50
related_requirement: REQ-0016-banner-management
related_change: fix-admin-banner-image-preview-cropped
---

# Acceptance - BUG-0080 管理端 Banner 列表和弹窗中 Banner 图片显示不全

## 回归验收标准

- [ ] AC-BUG-001 Banner 列表中的图片缩略图 MUST 能完整呈现图片主体，不裁掉关键文字、Logo 或主体内容。
- [ ] AC-BUG-002 Banner 弹窗中的图片预览 MUST 能完整呈现当前图片，上传后预览和编辑回显表现一致。
- [ ] AC-BUG-003 横幅图、方图、竖图和超宽图 MUST 使用一致且可预期的适配策略，不得出现明显拉伸、压扁或比例失真。
- [ ] AC-BUG-004 列表缩略图修复后 MUST 不破坏表格行高、列宽、分页、筛选和操作按钮布局。
- [ ] AC-BUG-005 弹窗预览修复后 MUST 不破坏上传控件、表单字段、弹窗滚动和底部保存按钮布局。
- [ ] AC-BUG-006 自定义上传图、品牌 Logo、SKU 主图等 Banner 图片来源 MUST 均按同一预览规则正确显示。
- [ ] AC-BUG-007 修复 MUST 不影响 Banner 新建、编辑、保存、上线/下线、排序和跳转类型配置。
- [ ] AC-BUG-008 如采用 `object-contain` 或等价完整展示策略，空白背景、边框和占位状态 MUST 符合管理端 Design System semantic token。

## 验收证据

| 证据 | 要求 |
|---|---|
| 列表截图 | 至少包含一张问题前后对比或修复后完整缩略图截图 |
| 弹窗截图 | 至少包含新建或编辑弹窗中完整图片预览截图 |
| 多比例素材 | 覆盖横幅图、方图、竖图和超宽图 |
| 回归说明 | 说明 Banner 保存、编辑回显和上线/下线未受影响 |
| 自动化或人工验证 | UI 变更若难以自动断言，至少提供人工验收记录；可补充前端组件测试或截图测试 |

## 非目标

- 本 BUG 不要求新增 Banner 类型、展示位置或跳转类型。
- 本 BUG 不要求修改 Banner API、数据库表结构或对象存储策略。
- 本 BUG 不要求改变展示端真实投放图片的裁切策略，除非修复阶段发现展示端也存在同源缺陷并另行记录。
