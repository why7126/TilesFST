---
bug_id: BUG-0080-admin-banner-image-preview-cropped
title: 管理端 Banner 列表和弹窗中 Banner 图片显示不全
status: done
severity: medium
review_result: approved
reviewed_at: 2026-07-22 09:15:12
created_at: 2026-07-22 09:15:12
updated_at: 2026-07-22 09:35:50
related_requirement: REQ-0016-banner-management
related_change: fix-admin-banner-image-preview-cropped
---

# Review - BUG-0080 管理端 Banner 列表和弹窗中 Banner 图片显示不全

## 评审结论

结论：`approved`，确认需要修复。

该缺陷发生在 Web 管理端 Banner 管理链路，影响运营人员在列表浏览、弹窗编辑和上传回显时确认 Banner 素材。缺陷包已补齐现象、复现步骤、初步根因、临时规避方案和回归验收标准，可以进入后续 `/bug-opsx` 与 Sprint 规划流程。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 用户反馈明确指出列表与弹窗两个位置均显示不全；初步根因指向管理端图片预览 CSS/容器适配策略 |
| 严重等级合理 | 通过 | `medium` 合理：不阻断保存或投放数据，但影响运营预览准确性和上线前确认 |
| 回归验收明确 | 通过 | acceptance 已覆盖列表、弹窗、多比例图片、图片来源、布局稳定和非目标范围 |
| 是否需 hotfix 路径 | 不需要 | 当前未阻断核心保存链路，也未发现生产数据或展示端投放异常；可按常规修复纳入迭代 |

## 批准范围

| 范围 | 说明 |
|---|---|
| 终端 | Web 管理端 |
| 页面 | Banner 管理页面 `/admin/banners` |
| 问题类型 | 图片预览显示不全 |
| 修复方向 | 调整列表缩略图与弹窗图片预览的容器、比例和 `object-fit` 等展示策略 |

## 后续动作

1. 已创建修复 Change `fix-admin-banner-image-preview-cropped`。
2. 允许通过 `/sprint-propose` 纳入 Sprint 正式范围。
3. 修复阶段需补充截图或等价 UI 验收证据，覆盖列表与弹窗两个位置。

## 注意事项

- 修复不得改变 Banner API、数据库结构或对象存储策略，除非后续探索发现另有问题并创建独立变更。
- 如果修复阶段发现展示端真实投放也存在同源裁切问题，应另行 capture 或在 Change 评审时明确扩展范围。
