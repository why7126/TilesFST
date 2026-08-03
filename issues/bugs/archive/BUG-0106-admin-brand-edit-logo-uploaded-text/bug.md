---
bug_id: BUG-0106-admin-brand-edit-logo-uploaded-text
title: 管理后台品牌编辑弹窗 Logo 旁显示冗余已上传文案
severity: low
status: done
owner:
discovered_at: 2026-08-03 08:13:39
environment: admin-brand-edit-dialog
related_requirement: null
related_change: fix-admin-brand-edit-logo-uploaded-text
created_at: 2026-08-03 08:19:09
updated_at: 2026-08-03 12:50:44
---

# 管理后台品牌编辑弹窗 Logo 旁显示冗余已上传文案

## 现象

管理后台品牌编辑弹窗中，品牌 Logo 区域旁显示了不需要的 `已上传Logo` 文案。该文案与当前界面预期不一致，会在已有图片预览和上传控件之外增加额外视觉噪音。

## 复现步骤

1. 登录管理后台。
2. 进入品牌列表。
3. 打开任一已上传 Logo 的品牌编辑弹窗。
4. 查看品牌 Logo 区域旁的提示文案。

## 期望结果

品牌 Logo 旁不显示 `已上传Logo` 文案，仅保留必要的图片预览、上传或替换控件。上传失败、格式不支持等错误提示仍应按原有规则展示。

## 实际结果

Logo 旁显示冗余的 `已上传Logo` 文案，造成品牌编辑弹窗界面噪音。

## 影响范围

- 管理后台品牌编辑弹窗。
- 品牌 Logo 上传、预览与替换区域。

## 严重等级说明

严重等级为 `low`。该问题属于管理后台品牌编辑弹窗的 UI 展示偏差，不阻断品牌 Logo 预览、替换或上传流程，但会影响界面清晰度与产品观感。
